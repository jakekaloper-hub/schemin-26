import unittest
from world.atlas.spatial.network_recovery_gate import evaluate
class RecoveryTests(unittest.TestCase):
 def test_nine_highwater_configurations(self):
  r=evaluate();self.assertEqual(len(r['results']),9)
  self.assertTrue(all(len(x['segment_recovery'])==4 for x in r['results']))
 def test_no_false_certification(self):
  r=evaluate();self.assertEqual(r['acceptance'],'HOLD')
  self.assertTrue(all(not a['full_network_recovery_certified'] for a in r['results']))
 def test_deterministic(self):self.assertEqual(evaluate(),evaluate())
if __name__=='__main__':unittest.main()
