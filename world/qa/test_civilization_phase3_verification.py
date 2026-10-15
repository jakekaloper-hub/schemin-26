import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_phase3_verification import verify_week3_recap_context as verify

class Phase3VerificationTests(unittest.TestCase):
    def test_real_fact_and_existing_production_adapters(self):
        r=verify()
        self.assertTrue(r["ok"])
        self.assertEqual(r["source_event"]["winner_score"],"136.73")
        self.assertEqual(r["source_event"]["loser_score"],"114.50")
        self.assertEqual(r["scene_context"]["memo_packet"]["civilization_context"]["context_id"],r["scene_context"]["context_id"])
        self.assertEqual(r["scene_context"]["novel_packet"]["civilization_context"]["context_id"],r["scene_context"]["context_id"])
        self.assertEqual(r["scene_context"]["visual_packet"]["civilization_context"]["context_id"],r["scene_context"]["context_id"])
        self.assertFalse(r["publication_eligible"])

    def test_repeatability(self):
        self.assertEqual(verify(),verify())

    def test_invalid_site_fails_closed(self):
        self.assertEqual(verify("LOC-NOT-REAL")["code"],"LOCATION_HANDOFF_FAILED")

    def test_modified_fact_fails_closed(self):
        with patch("world.engine.civilization_phase3_verification.FACT") as path:
            path.read_text.return_value="unverified"
            self.assertEqual(verify()["code"],"VERIFIED_FACT_NOT_FOUND")

if __name__=="__main__":
    unittest.main()
