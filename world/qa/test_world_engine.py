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

    def test_current_wilson_morphology_requires_integrated_four_legged_hybrid(self):
        p = self.payloads()
        bad = copy.deepcopy(p)
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-WILSON-LOOK":
                d["canon_guard"] = ["ARSENAL_GORILLA_CENTAUR_WARRIOR"]
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("four-legged Arsenal gorilla-centaur identity" in e for e in errs))

    def test_old_no_centaur_guard_fails_closed_not_migrated_to_current_canon(self):
        bad = copy.deepcopy(self.payloads())
        for d in bad[3]["domains"]:
            if d["character_id"] == "CHAR-WILSON-LOOK":
                d["canon_guard"].append("NO_CENTAUR_ANATOMY")
        errs = mod.validate_payloads(*bad)
        self.assertTrue(any("stale bipedal/no-centaur guard" in e for e in errs))

    def test_world_active_wilson_guard_matches_character_primary_authority(self):
        p = self.payloads()
        d = next(x for x in p[3]["domains"] if x["character_id"] == "CHAR-WILSON-LOOK")
        self.assertEqual(set(d["canon_guard"]), {
            "ARSENAL_GORILLA_CENTAUR_WARRIOR",
            "ONE_BODY_GORILLA_UPPER_FOUR_LEGGED_EQUINE_LOWER",
            "ARSENAL_IDENTITY_REQUIRED",
        })
        canonical=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        self.assertIn("FOUR-LEGGED CENTAUR LOWER BODY",canonical)
        self.assertIn("ONE BODY",canonical)

    def test_current_wilson_world_surfaces_cannot_disagree(self):
        root=ROOT
        owners=mod.load_json("owner_domains.json")
        domain=next(d for d in owners["domains"] if d["character_id"]=="CHAR-WILSON-LOOK")
        profiles=json.loads((root/"world/data/domain_profiles.json").read_text())
        profile=next(d for d in profiles["domains"] if d["owner_character_id"]=="CHAR-WILSON-LOOK")
        homeland=json.loads((root/"world/location-control-plane/homelands/CHAR-WILSON-LOOK/CARD.json").read_text())
        expected={
            "ARSENAL_GORILLA_CENTAUR_WARRIOR",
            "ONE_BODY_GORILLA_UPPER_FOUR_LEGGED_EQUINE_LOWER",
            "ARSENAL_IDENTITY_REQUIRED",
        }
        self.assertEqual(set(domain["canon_guard"]),expected)
        self.assertTrue(expected.issubset(set(profile["forbidden_drift"])))
        self.assertEqual(set(homeland["canon_guard"]),expected)
        for guards in (domain["canon_guard"],profile["forbidden_drift"],homeland["canon_guard"]):
            self.assertNotIn("NO_CENTAUR_ANATOMY",guards)
            self.assertNotIn("ARSENAL_GORILLA_WARRIOR",guards)
        self.assertIn("Arsenal Gorilla Centaur Warrior",str(profile["current_state"]))
        self.assertIn("Arsenal Gorilla Centaur Warrior",str(homeland["current_world_state"]))

    def test_all_twelve_active_owner_world_guard_sets_match_homelands_and_profiles(self):
        import re
        owners=mod.load_json("owner_domains.json")["domains"]
        profiles=json.loads((ROOT/"world/data/domain_profiles.json").read_text())["domains"]
        owner_ids={x["character_id"] for x in owners}
        profile_by_id={x["owner_character_id"]:x for x in profiles}
        canon=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        canon_ids=set(re.findall(r"\bid:\s*(CHAR-[A-Z-]+)",canon))
        self.assertEqual(len(owners),12)
        self.assertEqual(len(profiles),12)
        self.assertEqual(owner_ids,set(profile_by_id))
        self.assertEqual(owner_ids,canon_ids)
        for owner in owners:
            cid=owner["character_id"]
            homeland=json.loads(
                (ROOT/f"world/location-control-plane/homelands/{cid}/CARD.json").read_text()
            )
            guards=owner.get("canon_guard",[])
            self.assertTrue(guards,cid)
            self.assertEqual(len(guards),len(set(guards)),cid)
            self.assertEqual(set(guards),set(homeland["canon_guard"]),cid)
            self.assertTrue(set(guards).issubset(
                set(profile_by_id[cid]["forbidden_drift"])
            ),cid)
            self.assertNotIn("NO_CENTAUR_ANATOMY",guards,cid)
            self.assertEqual(homeland["character_id"],cid)

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
