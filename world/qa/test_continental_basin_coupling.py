import unittest
from world.atlas.spatial.continental_basin_coupling import inspect
class CouplingTests(unittest.TestCase):
 def test_all_candidate_cells_accounted_for(self):
  for p in inspect()['results']:
   self.assertEqual(p['cells'],p['hypothetical_south_receiving_cells']+p['unresolved_other_edge_receiving_cells'])
   self.assertTrue(p['all_terminal_roots_identified'])
 def test_preserves_zone_references(self):
  for p in inspect()['results']:
   self.assertEqual(p['target_region'],'REG-SOUTHERN-WETLANDS')
 def test_can_not_promote_unapproved_outlets(self):
  a=inspect();self.assertEqual(a['acceptance'],'HOLD')
  self.assertTrue(all(not p['geographically_approved'] for p in a['results']))
 def test_determinism(self):self.assertEqual(inspect(),inspect())
if __name__=='__main__':unittest.main()
