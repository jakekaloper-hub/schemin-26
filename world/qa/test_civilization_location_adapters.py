"""Real invocation of existing Memo/Novel Location Control Plane adapter functions."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"world/location-control-plane/adapters"))
from memo_adapter import compile_memo_location_packet
from novel_adapter import compile_novel_location_packet

class AdapterInvocationTests(unittest.TestCase):
    def test_same_context_through_existing_production_adapters(self):
        m=compile_memo_location_packet("LOC-LEAGUE-CHAMBER")
        n=compile_novel_location_packet("LOC-LEAGUE-CHAMBER")
        self.assertEqual(m["status"],"READY_FOR_SEMANTIC_QA")
        self.assertEqual(n["status"],"READY_FOR_SEMANTIC_QA")
        self.assertEqual(m["civilization_context"]["context_id"],n["civilization_context"]["context_id"])
        self.assertEqual(m["civilization_context"]["ordinary_life"],n["civilization_context"]["ordinary_life"])
        self.assertEqual(m["civilization_context_status"],"INTERPRETIVE_NON_PROMOTING")

    def test_all_three_basin_anchors_resolve(self):
        for loc in ("LOC-LEAGUE-CHAMBER","LOC-LEAGUE-ARCHIVE","LOC-PITTSYS-BOOK"):
            with self.subTest(loc=loc):
                for adapter in (compile_memo_location_packet,compile_novel_location_packet):
                    p=adapter(loc)
                    self.assertEqual(p["civilization_context"]["region_id"],"REG-CENTRAL-BASIN")

    def test_bad_location_stays_blocked(self):
        for adapter in (compile_memo_location_packet,compile_novel_location_packet):
            p=adapter("LOC-INVENTED")
            self.assertNotIn("civilization_context",p)
            self.assertNotIn(p["status"],{"READY_FOR_SEMANTIC_QA","READY_FOR_RENDER"})

    def test_unresolved_context_fails_closed(self):
        with patch("world.engine.civilization_consumers.resolve_scene_context",return_value={"ok":False,"code":"INVALID_LOCATION_ANCHOR"}):
            for adapter in (compile_memo_location_packet,compile_novel_location_packet):
                p=adapter("LOC-LEAGUE-CHAMBER")
                self.assertEqual(p["status"],"HUMAN_REVIEW_REQUIRED")
                self.assertIn("CIVILIZATION_CONTEXT_UNRESOLVED",p["review_blockers"])

if __name__=="__main__":
    unittest.main()
