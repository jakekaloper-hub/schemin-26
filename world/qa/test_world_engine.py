#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "world" / "engine" / "validate_world.py"

spec = importlib.util.spec_from_file_location("validate_world", VALIDATOR_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class WorldEngineTests(unittest.TestCase):
    def payloads(self):
        return [
            mod.load_json("physical_zones.json"),
            mod.load_json("divisions.json"),
            mod.load_json("locations.json"),
            mod.load_json("owner_domains.json"),
            mod.load_json("routes.json"),
            mod.load_json("world_state_events.json"),
            mod.load_json("current_world_state.json"),
        ]

    def test_repository_payloads_pass(self):
        self.assertEqual(mod.validate_repo(), [])

    def test_wings_semantic_lock_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        for d in bad[1]["divisions"]:
            if d["id"] == "DIV-WINGS":
                d["food_referent"] = "bird_wings"
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("Wings semantic lock" in e for e in errs))

    def test_duplicate_division_member_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        bad[1]["divisions"][0]["member_team_ids_2026"][0] = 1
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("cover team ids 1..12 exactly once" in e for e in errs))

    def test_location_outside_zone_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        bad[2]["locations"][0]["abstract_position"] = [-999, -999]
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("outside assigned physical zone" in e for e in errs))

    def test_broken_route_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        bad[4]["routes"][0]["to"] = "LOC-NOT-REAL"
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("missing endpoint" in e for e in errs))

    def test_missing_world_state_location_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        bad[5]["events"][0]["location_id"] = "LOC-MISSING"
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("references missing location" in e for e in errs))

    def test_character_negative_lock_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-WILSON-LOOK":
                d["canon_guard"] = ["ARSENAL_GORILLA_WARRIOR"]
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("retired-centaur negative lock" in e for e in errs))

    def test_tds_three_head_lock_fails_bad_fixture(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-PHILLIP-PITTS":
                d["canon_guard"] = []
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("three-head body lock" in e for e in errs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
