import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.central_basin_pilot import build_central_basin_pilot

class CentralBasinPilotTests(unittest.TestCase):
    def setUp(self):
        self.packet=build_central_basin_pilot()
        self.assertTrue(self.packet["ok"],self.packet)

    def test_exact_three_source_anchors(self):
        ids={x["id"] for x in self.packet["shared_world_facts"]["anchors"]}
        self.assertEqual(ids,{"LOC-LEAGUE-CHAMBER","LOC-LEAGUE-ARCHIVE","LOC-PITTSYS-BOOK"})
        self.assertTrue(all(x["source_provenance"] for x in self.packet["shared_world_facts"]["anchors"]))

    def test_archive_chamber_verified_direct_route(self):
        leg=self.packet["shared_world_facts"]["verified_route_legs"][0]["route"]
        self.assertEqual(leg["route_ids"],["ROUTE-ARCHIVE-CHAMBER"])

    def test_book_path_uses_existing_via_points(self):
        leg=self.packet["shared_world_facts"]["verified_route_legs"][1]["route"]
        self.assertEqual(set(leg["route_ids"]),{"ROUTE-BASIN-MARKET"})
        self.assertIn("LOC-SOUTHERN-SPEEDWAY",leg["location_path"])
        self.assertIn("LOC-DK-MUD-HILL",leg["location_path"])

    def test_memo_and_novel_same_world_facts(self):
        self.assertEqual(self.packet["memo_packet"]["world_facts"],self.packet["novel_packet"]["world_facts"])
        self.assertEqual(self.packet["memo_packet"]["publication_status"],"UNPUBLISHED_INTERPRETIVE_DEMO")
        self.assertEqual(self.packet["novel_packet"]["publication_status"],"UNPUBLISHED_INTERPRETIVE_DEMO")

    def test_no_new_pov_or_character_art(self):
        self.assertIn("NO_NAMED_NPCS",self.packet["novel_packet"]["restrictions"])
        self.assertIn("TWELVE_OWNER_POV_ONLY",self.packet["novel_packet"]["pov_rule"])
        self.assertFalse(self.packet["environment_art_view"]["character_rendering_allowed"])

if __name__=="__main__":
    unittest.main()
