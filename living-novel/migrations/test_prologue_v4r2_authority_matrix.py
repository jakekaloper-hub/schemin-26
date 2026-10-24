"""Fail closed on unsupported Prologue Atlas and historical approval claims."""
import json,unittest
from pathlib import Path
BASE=Path(__file__).parent
M=json.loads((BASE/"PROLOGUE_V4R2_ATLAS_HISTORICAL_SOURCE_MATRIX.json").read_text())
S=json.loads((BASE/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V4R2.json").read_text())
class Qualification(unittest.TestCase):
 def test_exact_manuscript(self):
  self.assertEqual(M["manuscript_blob"],S["manuscript_blob_sha"])
 def test_scene_coverage_and_parent_not_certified(self):
  self.assertEqual({x["scene_id"] for x in M["scenes"]},{x["scene_id"] for x in S["scenes"]})
  self.assertEqual(12,len(M["scenes"]))
  self.assertTrue(all(x["parent_registry_present"] for x in M["scenes"]))
  self.assertTrue(all(x["approval_status"]=="EDITORIAL_QUALIFICATION_NOT_DOMAIN_SIGNOFF" for x in M["scenes"]))
 def test_historical_truth_not_promoted(self):
  self.assertIn("DIRECT_ESPN_HISTORICAL_OUTCOMES_VERIFIED",M["history_rules"]["2025_podium"])
  self.assertTrue(M["espn_2025_verified"]["seasonComplete"])
  self.assertEqual([1,2,3],[t["finalRank"] for t in M["espn_2025_verified"]["results"]])
  self.assertTrue(all(t["outcomeConfidence"]=="explicit" for t in M["espn_2025_verified"]["results"]))
  self.assertNotIn("PRIMARY_ESPN_2025_PODIUM_EVIDENCE",M["remaining_gates"])
  self.assertIn("INDEPENDENT_EVIDENCE_BASED_UMPIRE_ACCEPTANCE",M["remaining_gates"])
if __name__=="__main__":unittest.main()
