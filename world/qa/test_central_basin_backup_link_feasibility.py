import unittest
from world.atlas.spatial.backup_link_feasibility import evaluate
class BackupFeasibilityTests(unittest.TestCase):
 def test_nine_configurations(self):
  r=evaluate();self.assertEqual(len(r['results']),9)
  self.assertTrue(all(len(v['alternatives'])==3 for v in r['results']))
 def test_no_false_green(self):
  r=evaluate();self.assertEqual(r['acceptance'],'HOLD')
  self.assertTrue(all(not v['high_water_redundancy_approved'] for v in r['results']))
 def test_determinism(self):self.assertEqual(evaluate(),evaluate())
if __name__=='__main__':unittest.main()
