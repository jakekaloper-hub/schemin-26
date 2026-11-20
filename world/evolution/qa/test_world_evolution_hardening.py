#!/usr/bin/env python3
"""Adversarial coverage for conservative World Evolution transaction guards."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "world" / "evolution"))
from engine.world_evolution import apply_to_payloads, validate_request, world_payloads


def request(week=4):
    return {
        "schema_version": "1.0",
        "transaction_id": "TXN-HARDEN-W4-001",
        "week": week,
        "season": 2026,
        "source_release": "TEST_ONLY_RELEASE",
        "release_verified": True,
        "operations": [{
            "op": "APPEND_WORLD_STATE_EVENT",
            "event": {
                "id": "EVT-HARDEN-W4-001", "week": week,
                "location_id": "LOC-COUNTRY-CLUB-JACKSON",
                "event_type": "test", "classification": "TEST_ONLY",
                "source_provenance": ["TEST_ONLY"],
                "entering_state": ["pretest"],
                "continuity_out": ["test only"]
            }
        }],
        "approvals": {"umpire": True, "closer": True, "commissioner": False}
    }


class WorldEvolutionHardening(unittest.TestCase):
    def setUp(self):
        self.data = world_payloads()

    def fatal_codes(self, r):
        p = validate_request(r, self.data)
        self.assertEqual(p["status"], "FATAL")
        self.assertFalse(p["state_apply_allowed"])
        return {f["code"] for f in p["findings"]}

    def test_original_week4_transaction_remains_eligible(self):
        p = validate_request(request(), self.data)
        self.assertTrue(p["state_apply_allowed"])

    def test_earlier_week_cannot_rewind_live_world_clock(self):
        self.assertIn("STATE_CHRONOLOGY_REGRESSION", self.fatal_codes(request(2)))

    def test_same_week_addendum_may_be_applied(self):
        r = request(3)
        after, plan = apply_to_payloads(r, self.data)
        self.assertTrue(plan["state_apply_allowed"])
        self.assertEqual(after["state"]["as_of"], "end_of_week_3_2026")
        self.assertEqual(self.data["state"]["as_of"], "end_of_week_3_2026")

    def test_missing_schema_version_rejected(self):
        r = request()
        del r["schema_version"]
        self.assertIn("MISSING_FIELD", self.fatal_codes(r))

    def test_invalid_schema_version_rejected(self):
        r = request()
        r["schema_version"] = "1.1"
        self.assertIn("SCHEMA_VERSION_INVALID", self.fatal_codes(r))

    def test_boolean_week_rejected(self):
        r = request()
        r["week"] = True
        self.assertIn("WEEK_INVALID", self.fatal_codes(r))

    def test_invalid_season_rejected(self):
        r = request()
        r["season"] = "2026"
        self.assertIn("SEASON_INVALID", self.fatal_codes(r))

    def test_string_approval_does_not_count_as_signature(self):
        r = request()
        r["approvals"]["umpire"] = "yes"
        self.assertIn("APPROVALS_NOT_EXPLICIT_BOOLEAN", self.fatal_codes(r))

    def test_release_verified_string_does_not_count(self):
        r = request()
        r["release_verified"] = "true"
        self.assertIn("RELEASE_VERIFIED_NOT_BOOLEAN", self.fatal_codes(r))

    def test_repeated_event_within_transaction_rejected(self):
        r = request()
        r["operations"].append(copy.deepcopy(r["operations"][0]))
        self.assertIn("DUPLICATE_EVENT_ID", self.fatal_codes(r))

    def test_event_week_must_match_transaction(self):
        r = request()
        r["operations"][0]["event"]["week"] = 3
        self.assertIn("EVENT_WEEK_MISMATCH", self.fatal_codes(r))

    def test_unknown_world_clock_fails_closed(self):
        p = copy.deepcopy(self.data)
        p["state"]["as_of"] = "unknown"
        result = validate_request(request(), p)
        self.assertIn("CURRENT_STATE_CLOCK_INVALID", {f["code"] for f in result["findings"]})
        self.assertFalse(result["state_apply_allowed"])

    def test_candidate_only_request_keeps_approval_boundary(self):
        r = request()
        r["operations"] = [{
            "op": "REQUEST_CANDIDATE_PROMOTION",
            "candidate_id": "CAND-CHAMP-LAST-FIELD",
            "event_class": "CHAMPIONSHIP",
            "route_resolution": "RESOLVED",
            "championship_verified": True,
            "finalists_verified": True,
            "proposed_location": {"id": "LOC-HARDEN-TEST", "physical_zone_id": "REG-CENTRAL-BASIN"}
        }]
        r["approvals"]["commissioner"] = False
        p = validate_request(r, self.data)
        self.assertFalse(p["candidate_promotion_plans"][0]["ready_for_separate_location_transaction"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
