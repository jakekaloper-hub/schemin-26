#!/usr/bin/env python3
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"world"/"location-control-plane"/"compiler"))
from location_control_plane import compile_world_packet, resolve_environment_reference

GEN=ROOT/"world"/"environment-references"/"render_structural_plates.py"
spec=importlib.util.spec_from_file_location("render_structural_plates",GEN)
renderer=importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(renderer)

class EnvironmentReferencePhase3Tests(unittest.TestCase):
    def load(self,path):
        return json.loads((ROOT/path).read_text())

    def test_all_23_have_structural_reference(self):
        reg=self.load("world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json")
        self.assertEqual(len(reg["locations"]),23)
        self.assertTrue(all(x.get("structural_reference_status")=="APPROVED_STRUCTURAL_REFERENCE" for x in reg["locations"]))
        self.assertTrue(all(len(x.get("approved_structural_reference_uris",[]))==1 for x in reg["locations"]))

    def test_all_structural_reference_files_exist(self):
        reg=self.load("world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json")
        for row in reg["locations"]:
            for uri in row["approved_structural_reference_uris"]:
                self.assertTrue((ROOT/uri).is_file(),uri)

    def test_no_false_cinematic_approval(self):
        reg=self.load("world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json")
        self.assertTrue(all(x.get("cinematic_reference_status")=="MISSING_APPROVED_CINEMATIC_REFERENCE" for x in reg["locations"]))
        self.assertTrue(all(x.get("approved_cinematic_reference_uris",[])==[] for x in reg["locations"]))

    def test_structural_packet_blocks_without_renderer_injection_proof(self):
        p=compile_world_packet("LOC-COUNTRY-CLUB-JACKSON",["CHAR-ZACH-WILSON"],"VISUAL",reference_requirement="STRUCTURAL")
        self.assertEqual(p["status"],"HUMAN_REVIEW_REQUIRED")
        self.assertIn("RENDERER_INJECTION_UNPROVEN",p["review_blockers"])

    def test_cinematic_packet_blocks(self):
        p=compile_world_packet("LOC-COUNTRY-CLUB-JACKSON",["CHAR-ZACH-WILSON"],"VISUAL",reference_requirement="CINEMATIC")
        self.assertEqual(p["status"],"HUMAN_REVIEW_REQUIRED")
        self.assertIn("MISSING_APPROVED_CINEMATIC_REFERENCE",p["review_blockers"])

    def test_backward_visual_required_means_cinematic(self):
        p=compile_world_packet("LOC-COUNTRY-CLUB-JACKSON",["CHAR-ZACH-WILSON"],"VISUAL",require_visual_reference=True)
        self.assertEqual(p["status"],"HUMAN_REVIEW_REQUIRED")
        self.assertIn("MISSING_APPROVED_CINEMATIC_REFERENCE",p["review_blockers"])

    def test_reference_resolver(self):
        r=resolve_environment_reference("LOC-MUD-DOGS-SWAMP")
        self.assertEqual(r["status"],"CURRENT_ENVIRONMENT_REFERENCE_RESOLVED")
        self.assertEqual(r["reference"]["structural_reference_status"],"APPROVED_STRUCTURAL_REFERENCE")
        self.assertEqual(r["reference"]["repo_byte_status"],"VERIFIED_REPO_PATH")
        self.assertEqual(r["reference"]["renderer_injection_status"],"UNPROVEN")
        self.assertFalse(r["reference"]["renderer_ready"])

    def test_structural_plates_are_deterministic(self):
        locs=self.load("world/data/locations.json")["locations"]
        zones={x["id"]:x for x in self.load("world/data/physical_zones.json")["regions"]}
        state=self.load("world/data/current_world_state.json")
        for loc in locs:
            expected=renderer.render(loc,zones[loc["physical_zone_id"]],state)
            actual=(ROOT/f"world/environment-references/plates/{loc['id']}/STRUCTURAL_PLATE.svg").read_text()
            self.assertEqual(actual,expected,loc["id"])

    def test_candidate_store_unchanged(self):
        c=self.load("world/data/atlas_location_candidates.json")
        self.assertEqual(len(c["candidates"]),48)

if __name__=="__main__":
    unittest.main(verbosity=2)
