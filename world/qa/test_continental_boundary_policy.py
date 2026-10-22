import unittest
from world.atlas.spatial.outlet_gate import drain_to_boundary
from world.atlas.spatial.continental_basin_coupling import inspect
class BoundaryPolicyTests(unittest.TestCase):
 def test_selected_south_receives_all_synthetic_cells(self):
  for v in inspect()['results']:
   self.assertEqual(v['hypothetical_south_receiving_cells'],1089)
   self.assertEqual(v['unresolved_other_edge_receiving_cells'],0)
   self.assertFalse(v['geographically_approved'])
 def test_explicit_outlet_rejects_interior(self):
  with self.assertRaises(ValueError):drain_to_boundary([[3]*3 for _ in range(3)],{(1,1)})
 def test_empty_outlet_rejected(self):
  with self.assertRaises(ValueError):drain_to_boundary([[3]*3 for _ in range(3)],set())
 def test_one_permitted_boundary(self):
  a=drain_to_boundary([[9,9,9],[9,0,9],[9,9,9]],{(1,0)})
  self.assertEqual(a['boundary_outlets'],1)
  self.assertEqual(a['outlet_policy'],'EXPLICIT_PERMITTED_BOUNDARY')
if __name__=='__main__':unittest.main()
