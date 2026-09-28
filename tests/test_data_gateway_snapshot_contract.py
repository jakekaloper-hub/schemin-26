import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "data-gateway" / "refresh_espn_snapshot.py"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "espn-cold-standby.yml"


def load_gateway():
    spec = importlib.util.spec_from_file_location("refresh_espn_snapshot", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataGatewaySnapshotContractTests(unittest.TestCase):
    def test_snapshot_meta_contains_required_freshness_fields(self):
        gateway = load_gateway()
        data = {
            "id": int(gateway.LEAGUE_ID),
            "teams": [{} for _ in range(12)],
            "schedule": [],
            "settings": {},
            "status": {},
        }
        gateway.validate(data)
        envelope = gateway.build_envelope(data, "2026-09-28T00:00:00+00:00")
        required = {
            "stale",
            "fetched_at",
            "snapshot_age_seconds",
            "failure_reason",
        }
        self.assertTrue(required.issubset(envelope["meta"]))
        self.assertEqual(envelope["meta"]["snapshot_age_seconds"], 0)
        self.assertFalse(envelope["meta"]["stale"])

    def test_snapshot_write_is_atomic_and_complete(self):
        gateway = load_gateway()
        envelope = gateway.build_envelope({"id": int(gateway.LEAGUE_ID)}, "2026-09-28T00:00:00+00:00")
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = pathlib.Path(tmp) / gateway.LEAGUE_ID
            gateway.write_snapshot(envelope, out_dir)
            self.assertTrue((out_dir / "latest.json").exists())
            self.assertTrue((out_dir / "manifest.json").exists())
            self.assertFalse((out_dir / "latest.json.tmp").exists())

    def test_workflow_stages_untracked_snapshot_before_diff_gate(self):
        text = WORKFLOW_PATH.read_text()
        add_pos = text.index("git add data/snapshots/1417621")
        diff_pos = text.index("git diff --cached --quiet -- data/snapshots/1417621")
        self.assertLess(add_pos, diff_pos)


if __name__ == "__main__":
    unittest.main()
