import unittest
from world.atlas.spatial.outlet_gate import drain_to_boundary,audit
class OutletTests(unittest.TestCase):
 def test_closed_depression_conditioned(self):
  g=[[5,5,5],[5,0,5],[5,5,5]]
  a=drain_to_boundary(g)
  self.assertEqual(a['raised_cells'],1)
  self.assertEqual(a['interior_terminal_sinks'],0)
  self.assertTrue(a['all_cells_boundary_reachable'])
 def test_reproducible_three_candidates(self):
  a=audit();self.assertEqual(a,audit())
  self.assertEqual(len(a['results']),3)
  self.assertTrue(all(x['boundary_reachable'] for x in a['results']))
 def test_no_promotion(self):
  self.assertFalse(audit()['outlet_geography_approved'])
 def test_invalid_rejected(self):
  with self.assertRaises(ValueError):drain_to_boundary([[1,2],[3,4]])
if __name__=='__main__':unittest.main()
