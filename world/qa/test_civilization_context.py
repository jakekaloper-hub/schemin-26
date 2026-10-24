#!/usr/bin/env python3
"""Mission #175: civilization context integration and negative tests."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from world.engine.civilization_context import resolve_civilization_context

class CivilizationContextTests(unittest.TestCase):
    def test_seven_regions_and_unique_contexts(self):
        regions = json.loads((ROOT / "world/data/physical_zones.json").read_text())["regions"]
        self.assertEqual(len(regions), 7)
        for region in regions:
            with self.subTest(region=region["id"]):
                context = resolve_civilization_context(region["id"])
                self.assertTrue(context["ok"], context)
                self.assertEqual(context["region_id"], region["id"])
                self.assertEqual(context["status"], "READ_ONLY_INTERPRETIVE_CONTEXT")
                self.assertTrue(context["ordinary_life"])
                self.assertTrue(context["economic_activities"])
                self.assertEqual(len(context["provenance"]), 4)
                self.assertIn("NO_NAMED_NPCS", context["restrictions"])
                self.assertNotIn("CANON_MUTATION", context["consumer_permissions"])

    def test_anchors_match_existing_locations(self):
        locations = {x["id"]: x for x in json.loads((ROOT / "world/data/locations.json").read_text())["locations"]}
        for region in json.loads((ROOT / "world/data/physical_zones.json").read_text())["regions"]:
            context = resolve_civilization_context(region["id"])
            for anchor in context["anchor_locations"]:
                self.assertEqual(locations[anchor["id"]]["physical_zone_id"], region["id"])

    def test_central_basin_context_available_for_all_consumers(self):
        c = resolve_civilization_context("REG-CENTRAL-BASIN")
        self.assertTrue(c["ok"])
        self.assertIn("MEMO_CONTEXT", c["consumer_permissions"])
        self.assertIn("NOVEL_CONTEXT", c["consumer_permissions"])
        self.assertIn("ATLAS_READ_ONLY", c["consumer_permissions"])
        self.assertIn("ART_ENVIRONMENT_ONLY", c["consumer_permissions"])

    def test_unknown_region_fails_closed(self):
        self.assertEqual(resolve_civilization_context("REG-INVENTED")["error"], "UNKNOWN_REGION")

    def test_read_only_no_file_mutations(self):
        paths = [ROOT / p for p in ("world/data/physical_zones.json", "world/data/settlements.json", "world/data/economies.json", "world/data/locations.json")]
        before = [p.read_bytes() for p in paths]
        resolve_civilization_context("REG-CENTRAL-BASIN")
        self.assertEqual(before, [p.read_bytes() for p in paths])

if __name__ == "__main__":
    unittest.main()
