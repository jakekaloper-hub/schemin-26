import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_production_bridge import validate_preproduction_bridge

class ProductionBridgeTests(unittest.TestCase):
    def test_memo_real_manifest_and_novel_contract_are_loaded(self):
        p=validate_preproduction_bridge()
        self.assertTrue(p["ok"])
        self.assertEqual(p["memo"]["publication_id"],"memo.2026.week-04")
        self.assertEqual(p["production_gate"],"HOLD")

    def test_real_novel_validator_rejects_empty_pov(self):
        p=validate_preproduction_bridge({})
        self.assertIn("MISSING_CHARACTER_ID",p["novel"]["pov_validation_errors"])
        self.assertIn("MISSING_STORY_TIME_CUTOFF",p["novel"]["pov_validation_errors"])

    def test_memo_and_novel_are_both_nonpublishable(self):
        p=validate_preproduction_bridge()
        self.assertFalse(p["memo"]["can_assemble_page"])
        self.assertFalse(p["novel"]["can_publish_scene"])
        self.assertEqual(p["memo"]["context"]["world_facts"],p["novel"]["context"]["world_facts"])

if __name__=="__main__":
    unittest.main()
