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
        bad[1]["divisions"][0]["member_team_ids_2026"][0] = bad[1]["divisions"][0]["member_team_ids_2026"][1]
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

    def test_missing_gorilla_centaur_anatomy_fails_bad_fixture(self):
        bad = copy.deepcopy(self.payloads())
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-WILSON-LOOK":
                d["canon_guard"] = ["ARSENAL_GORILLA_CENTAUR_WARRIOR"]
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("FOUR_LEGGED_CENTAUR_LOWER_BODY" in e for e in errs))
        self.assertTrue(any("ONE_INTEGRATED_GORILLA_EQUINE_BODY" in e for e in errs))

    def test_superseded_no_centaur_guard_is_rejected(self):
        bad = copy.deepcopy(self.payloads())
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-WILSON-LOOK":
                d["canon_guard"].append("NO_CENTAUR_ANATOMY")
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("obsolete no-centaur" in e for e in errs))

    def test_wilson_active_location_and_visual_context_match_character_canon(self):
        domain = next(d for d in mod.load_json("owner_domains.json")["domains"] if d["character_id"] == "CHAR-WILSON-LOOK")
        profile = next(d for d in mod.load_json("domain_profiles.json")["domains"] if d["owner_character_id"] == "CHAR-WILSON-LOOK")
        homeland = mod.load_repo_json("world/location-control-plane/homelands/CHAR-WILSON-LOOK/CARD.json")
        location = next(d for d in mod.load_json("locations.json")["locations"] if d["id"] == "LOC-DK-HIGHLAND-STRONGHOLD")
        location_card = mod.load_repo_json("world/location-control-plane/locations/LOC-DK-HIGHLAND-STRONGHOLD/CARD.json")
        ontology = mod.load_json("inhabitant_ontology.json")["people_notes"]["CHAR-WILSON-LOOK"]
        required = {"ARSENAL_GORILLA_CENTAUR_WARRIOR", "ONE_INTEGRATED_GORILLA_EQUINE_BODY", "FOUR_LEGGED_CENTAUR_LOWER_BODY"}
        self.assertTrue(required.issubset(set(domain["canon_guard"])))
        self.assertTrue(required.issubset(set(homeland["canon_guard"])))
        self.assertTrue(all(lock not in profile["forbidden_drift"] for lock in required))
        self.assertTrue({"NO_GENERIC_BIPEDAL_GORILLA", "NO_HORSE_HEADED_CENTAUR",
                         "NO_RIDER_MOUNT_SUBSTITUTE", "NO_TWO_CREATURE_SUBSTITUTE",
                         "NO_ARSENAL_IDENTITY_OMISSION"}.issubset(set(profile["forbidden_drift"])))
        self.assertNotIn("NO_CENTAUR_ANATOMY", domain["canon_guard"])
        self.assertNotIn("NO_CENTAUR_ANATOMY", profile["forbidden_drift"])
        self.assertNotIn("NO_CENTAUR_ANATOMY", homeland["canon_guard"])
        self.assertIn("Gorilla Centaur Warrior", location["current_state"][0])
        self.assertIn("Gorilla Centaur Warrior", location_card["base_location_state"][0])
        self.assertIn("Gorilla Centaur Warrior", ontology)

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
