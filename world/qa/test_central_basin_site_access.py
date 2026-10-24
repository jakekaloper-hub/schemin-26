import unittest
from world.atlas.spatial.site_access_gate import evaluate
class SiteAccessTests(unittest.TestCase):
 def test_routes_and_sites(self):
  a=evaluate();self.assertEqual(len(a['sites']),5)
  self.assertEqual(len(a['segments']),4)
  self.assertTrue(all(not x['route_feasible_approved'] for x in a['segments']))
 def test_determinism(self):self.assertEqual(evaluate(),evaluate())
 def test_invalid_parameters(self):
  with self.assertRaises(ValueError):evaluate(samples=1)
 def test_no_canon_promotion(self):self.assertEqual(evaluate()['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
