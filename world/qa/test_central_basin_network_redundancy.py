import unittest
from world.atlas.spatial.network_redundancy_gate import evaluate
class RedundancyTests(unittest.TestCase):
 def test_minimality(self):
  a=evaluate();self.assertEqual(a['existing_edge_count'],4)
  self.assertEqual(a['minimum_added_links'],1)
  self.assertTrue(a['minimum_topological_solutions'])
 def test_noncanonical(self):
  a=evaluate();self.assertEqual(a['acceptance'],'HOLD')
  self.assertTrue(all(not p['approved_route'] for x in a['minimum_topological_solutions'] for p in x['proposed_links']))
 def test_deterministic(self):self.assertEqual(evaluate(),evaluate())
if __name__=='__main__':unittest.main()
