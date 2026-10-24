import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_phase2_handoff import build_phase2_handoff as build

class HandoffTests(unittest.TestCase):
    def test_basin_three_consumer_convergence(self):
        p=build("LOC-LEAGUE-CHAMBER",2026,5)
        self.assertTrue(p["ok"])
        self.assertEqual(p["memo_location_packet"]["civilization_context"]["context_id"],p["shared_context_id"])
        self.assertEqual(p["novel_location_packet"]["civilization_context"]["context_id"],p["shared_context_id"])
        self.assertEqual(p["visual_world_packet"]["civilization_context"]["context_id"],p["shared_context_id"])
        self.assertFalse(p["publication_eligible"])

    def test_other_basin_anchors(self):
        for loc in ("LOC-LEAGUE-ARCHIVE","LOC-PITTSYS-BOOK"):
            with self.subTest(loc=loc):
                self.assertTrue(build(loc,2026,5)["ok"])

    def test_unverified_historical_season_rejected(self):
        self.assertEqual(build("LOC-LEAGUE-CHAMBER",2025,5)["code"],"UNVERIFIED_SEASON")

    def test_invented_location_rejected(self):
        self.assertEqual(build("LOC-FAKE",2026,5)["code"],"LOCATION_PACKET_NOT_READY")

if __name__=="__main__":
    unittest.main()
