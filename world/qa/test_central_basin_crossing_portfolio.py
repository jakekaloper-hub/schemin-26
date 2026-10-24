import unittest
from world.atlas.spatial.crossing_portfolio_gate import evaluate
class CrossingPortfolioTests(unittest.TestCase):
 def test_nine_scenarios(self):self.assertEqual(len(evaluate()['results']),9)
 def test_minimum_edges_and_no_canon(self):
  for r in evaluate()['results']:
   self.assertEqual(r['minimum_repairs_for_full_connectivity'],r['initial_component_count']-1)
   self.assertFalse(r['approved_infrastructure'])
   self.assertTrue(all(len(p)==r['minimum_repairs_for_full_connectivity'] for p in r['all_minimum_portfolios']))
 def test_repeatable_hold(self):
  a=evaluate();self.assertEqual(a,evaluate());self.assertEqual(a['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
