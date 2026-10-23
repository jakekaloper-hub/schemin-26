import unittest
from world.atlas.spatial.crossing_robust_portfolio_gate import evaluate
class RobustPortfolioTests(unittest.TestCase):
 def test_all_27_conditions(self):
  r=evaluate();self.assertEqual(r['scenario_count'],27);self.assertEqual(r['edge_count'],4)
 def test_minimal_solution(self):
  r=evaluate();self.assertTrue(r['minimum_portfolios'])
  self.assertTrue(all(len(p)==r['minimum_permanent_repair_count'] for p in r['minimum_portfolios']))
 def test_deterministic_hold(self):
  r=evaluate();self.assertEqual(r,evaluate());self.assertEqual(r['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
