import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "data-gateway" / "refresh_espn_snapshot.py"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "espn-cold-standby.yml"
HEALTH_PATH = ROOT / "data-gateway" / "check_snapshot_health.py"


def load_gateway():
    spec = importlib.util.spec_from_file_location("refresh_espn_snapshot", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_health():
    module_dir = str(HEALTH_PATH.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    spec = importlib.util.spec_from_file_location("check_snapshot_health", HEALTH_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def league_fixture(roster_counts=None):
    counts = roster_counts or [17, 19, 18, 19, 18, 19, 17, 18, 17, 17, 18, 19]
    teams = []
    for team_id, count in enumerate(counts, start=1):
        teams.append(
            {
                "id": team_id,
                "roster": {"entries": [{"playerId": f"{team_id}-{i}"} for i in range(count)]},
            }
        )
    return {
        "id": 1417621,
        "teams": teams,
        "schedule": [{"matchupPeriodId": 1}],
        "settings": {
            "rosterSettings": {
                "lineupSlotCounts": {
                    "0": 1,
                    "2": 2,
                    "4": 2,
                    "5": 1,
                    "6": 1,
                    "16": 1,
                    "17": 1,
                    "20": 7,
                    "21": 2,
                    "23": 1,
                }
            }
        },
        "status": {},
    }


class DataGatewaySnapshotContractTests(unittest.TestCase):
    def test_live_roster_validation_allows_reserve_variance(self):
        gateway = load_gateway()
        summary = gateway.validate(league_fixture())
        self.assertEqual(summary["team_count"], 12)
        self.assertEqual(summary["configured_roster_capacity"], 19)
        self.assertEqual(min(summary["roster_entry_counts"]), 17)
        self.assertEqual(max(summary["roster_entry_counts"]), 19)

    def test_roster_validation_rejects_capacity_overflow(self):
        gateway = load_gateway()
        fixture = league_fixture([20] + [17] * 11)
        with self.assertRaisesRegex(ValueError, "exceeds configured capacity"):
            gateway.validate(fixture)

    def test_validation_rejects_empty_schedule(self):
        gateway = load_gateway()
        fixture = league_fixture()
        fixture["schedule"] = []
        with self.assertRaisesRegex(ValueError, "schedule missing or empty"):
            gateway.validate(fixture)

    def test_validation_rejects_duplicate_team_ids(self):
        gateway = load_gateway()
        fixture = league_fixture()
        fixture["teams"][1]["id"] = fixture["teams"][0]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate team ids"):
            gateway.validate(fixture)

    def test_validation_rejects_empty_team_roster(self):
        gateway = load_gateway()
        fixture = league_fixture()
        fixture["teams"][0]["roster"]["entries"] = []
        with self.assertRaisesRegex(ValueError, "roster empty"):
            gateway.validate(fixture)

    def test_snapshot_meta_contains_required_freshness_fields(self):
        gateway = load_gateway()
        data = league_fixture()
        validation = gateway.validate(data)
        envelope = gateway.build_envelope(
            data,
            "2026-09-28T00:00:00+00:00",
            validation=validation,
        )
        required = {
            "stale",
            "fetched_at",
            "snapshot_age_seconds",
            "failure_reason",
        }
        self.assertTrue(required.issubset(envelope["meta"]))
        self.assertEqual(envelope["meta"]["snapshot_age_seconds"], 0)
        self.assertFalse(envelope["meta"]["stale"])
        self.assertEqual(envelope["meta"]["validation"]["configured_roster_capacity"], 19)

    def test_freshness_is_recomputed_at_read_time(self):
        gateway = load_gateway()
        envelope = gateway.build_envelope(
            league_fixture(),
            "2026-09-28T00:00:00+00:00",
        )
        fresh = gateway.refresh_freshness_for_read(
            envelope,
            now="2026-09-28T00:10:00+00:00",
            max_stale_seconds=900,
        )
        self.assertEqual(fresh["meta"]["snapshot_age_seconds"], 600)
        self.assertFalse(fresh["meta"]["stale"])

        stale = gateway.refresh_freshness_for_read(
            envelope,
            now="2026-09-28T00:16:00+00:00",
            max_stale_seconds=900,
        )
        self.assertEqual(stale["meta"]["snapshot_age_seconds"], 960)
        self.assertTrue(stale["meta"]["stale"])
        self.assertEqual(stale["meta"]["failure_reason"], "SNAPSHOT_AGE_EXCEEDED_SLO")

    def test_failed_refresh_marks_last_good_stale_without_replacing_data(self):
        gateway = load_gateway()
        envelope = gateway.build_envelope(
            {"id": int(gateway.LEAGUE_ID), "payload": "last-good"},
            "2026-09-28T00:00:00+00:00",
        )
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = pathlib.Path(tmp) / gateway.LEAGUE_ID
            gateway.write_snapshot(envelope, out_dir)
            marked = gateway.mark_last_good_stale(
                out_dir,
                "network failure",
                now="2026-09-28T00:05:00+00:00",
            )
            self.assertTrue(marked)
            persisted = json.loads((out_dir / "latest.json").read_text())
            self.assertEqual(persisted["data"]["payload"], "last-good")
            self.assertTrue(persisted["meta"]["stale"])
            self.assertEqual(persisted["meta"]["snapshot_age_seconds"], 300)
            self.assertEqual(persisted["meta"]["failure_reason"], "network failure")

    def test_repository_native_health_check_applies_slo(self):
        gateway = load_gateway()
        health = load_health()
        envelope = gateway.build_envelope(
            {"id": int(gateway.LEAGUE_ID), "payload": "last-good"},
            "2026-09-28T00:00:00+00:00",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "latest.json"
            path.write_text(json.dumps(envelope))

            green, green_code = health.evaluate_snapshot(
                path=path,
                max_stale_seconds=900,
                now="2026-09-28T00:10:00+00:00",
            )
            self.assertEqual(green_code, 0)
            self.assertEqual(green["state"], "GREEN_LIVE")

            stale, stale_code = health.evaluate_snapshot(
                path=path,
                max_stale_seconds=900,
                now="2026-09-28T00:16:00+00:00",
            )
            self.assertEqual(stale_code, 1)
            self.assertEqual(stale["state"], "YELLOW_DEGRADED")
            self.assertEqual(stale["meta"]["snapshot_age_seconds"], 960)

    def test_snapshot_write_is_atomic_and_complete(self):
        gateway = load_gateway()
        envelope = gateway.build_envelope(
            {"id": int(gateway.LEAGUE_ID)},
            "2026-09-28T00:00:00+00:00",
        )
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = pathlib.Path(tmp) / gateway.LEAGUE_ID
            gateway.write_snapshot(envelope, out_dir)
            self.assertTrue((out_dir / "latest.json").exists())
            self.assertTrue((out_dir / "manifest.json").exists())
            self.assertFalse((out_dir / "latest.json.tmp").exists())
            self.assertFalse((out_dir / "manifest.json.tmp").exists())

    def test_workflow_hydrates_lkg_before_refresh_and_persists_failure_state(self):
        text = WORKFLOW_PATH.read_text()
        self.assertIn("Hydrate last-known-good snapshot", text)
        self.assertIn("git fetch origin refs/heads/data/live:refs/heads/data/live", text)
        self.assertIn('git show "data/live:$SNAPSHOT_PATH/latest.json"', text)
        self.assertIn("continue-on-error: true", text)
        self.assertIn("if: always()", text)
        self.assertIn("if: steps.refresh.outcome != 'success'", text)
        self.assertIn("git worktree add /tmp/schemin-data-live data/live", text)
        self.assertIn("git push origin HEAD:data/live", text)
        self.assertNotIn("git push origin HEAD:main", text)
        hydrate_pos = text.index("Hydrate last-known-good snapshot")
        refresh_pos = text.index("Fetch and validate ESPN snapshot")
        self.assertLess(hydrate_pos, refresh_pos)
        add_pos = text.index("git add data/snapshots/1417621")
        diff_pos = text.index("git diff --cached --quiet -- data/snapshots/1417621")
        self.assertLess(add_pos, diff_pos)


if __name__ == "__main__":
    unittest.main()
