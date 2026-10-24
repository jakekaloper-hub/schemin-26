import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_hydration import build_central_basin_hydration

class HydrationTests(unittest.TestCase):
    def test_existing_shared_contract_fields(self):
        payload=build_central_basin_hydration()
        self.assertTrue(payload["ok"])
        contract=(ROOT/payload["contract"]).read_text()
        for key in ("LOC_ID","REGION_ZONE","ARRIVAL_ROUTE","ENTERING_WORLD_STATE","PRIOR_MEMORY",
                    "ORDINARY_WORLD_LIFE","MATERIAL_CONSTRAINTS","PUBLIC_KNOWLEDGE","POV_KNOWLEDGE",
                    "EVENT_DELTA","DEPARTURE_STATE","IMAGE_TELLS","PROSE_TELLS","UNKNOWN_FORBIDDEN_INVENTIONS"):
            self.assertIn(key,contract)
            self.assertIn(key,payload)

    def test_unverified_weekly_state_fails_publication_gate(self):
        p=build_central_basin_hydration()
        self.assertFalse(p["publication_eligible"])
        self.assertIn("UNKNOWN",p["ENTERING_WORLD_STATE"])
        self.assertEqual(p["EVENT_DELTA"],"NONE_PROPOSED")

    def test_memo_novel_share_exact_facts(self):
        p=build_central_basin_hydration()
        self.assertEqual(p["memo_packet"]["world_facts"],p["novel_packet"]["world_facts"])

if __name__=="__main__":
    unittest.main()
