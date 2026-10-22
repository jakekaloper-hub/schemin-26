import unittest
from unittest.mock import patch
from world.atlas.spatial.evidence_closure import evaluate
class EvidenceClosureTests(unittest.TestCase):
 def test_receipts_preserve_identity_and_nonmetric_status(self):
  r=evaluate();self.assertEqual(r['historical_observation_count'],4)
  self.assertEqual(r['landmark_identity_count'],5)
  self.assertTrue(all(not x['metric_coordinate_approved'] for x in r['receipts']))
 def test_bad_expected_landmark_set_rejected(self):
  with patch('world.atlas.spatial.evidence_closure.EXPECTED',{'LOC-BOGUS'}):
   with self.assertRaises(ValueError):evaluate()
 def test_repeatability(self):self.assertEqual(evaluate(),evaluate())
if __name__=='__main__':unittest.main()
