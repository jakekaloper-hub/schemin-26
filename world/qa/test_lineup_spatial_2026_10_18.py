"""Lineup atmosphere cannot rewrite existing World Engine geography."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REFERENCE=ROOT/"world/location-control-plane/evidence/APPROVED_LINEUP_SPATIAL_RECONCILIATION_2026_10_18.json"

class LineupSpatialContinuityTests(unittest.TestCase):
    def test_spatial_anchors_preserve_twelve_real_homelands(self):
        artifact=json.loads(REFERENCE.read_text())
        self.assertTrue(artifact["existing_world_canon_unchanged"])
        self.assertEqual(artifact["metric_geometry_state"],"HOLD_UNTIL_MEASURED")
        worlds=json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]
        known={x["character_id"]:x for x in worlds}
        self.assertEqual(len(artifact["subjects"]),12)
        self.assertEqual(set(known),{x["character_id"] for x in artifact["subjects"]})
        for subject in artifact["subjects"]:
            key=subject["character_id"]
            self.assertEqual(subject["primary_location_id"],known[key]["primary_location_id"])
            self.assertEqual(subject["region_ids"],known[key]["physical_zone_ids"])
            self.assertFalse(subject["geographic_authority_promotion"])
            self.assertIn("UNMEASURED",subject["metric_clearance_route_length_terrain_dimensions"])
            home=json.loads((ROOT/subject["homeland_card"]).read_text())
            self.assertEqual(home["character_id"],key)
            self.assertEqual(home["primary_location_id"],subject["primary_location_id"])
            self.assertEqual(home["physical_zone_ids"],subject["region_ids"])
            self.assertEqual(home.get("primary_access_route_ids",[]),subject["existing_route_ids"])
            self.assertTrue(subject["spatial_engine_enrichment"])

    def test_not_one_lineup_background_promoted_as_atlas_new_location(self):
        artifact=json.loads(REFERENCE.read_text())
        self.assertIn("VISUAL_LINEUP",json.loads((ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json").read_text())["status"])
        for item in artifact["subjects"]:
            self.assertIn("map distances",item["source_image_not_valid_for"].lower())
            self.assertTrue(item["approved_artwork_mood_only"])
            self.assertTrue(item["primary_location_id"].startswith("LOC-"))

if __name__=="__main__":
    unittest.main()
