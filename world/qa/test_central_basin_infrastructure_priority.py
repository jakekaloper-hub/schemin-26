import unittest
from world.atlas.spatial.infrastructure_priority_gate import evaluate,connected_pairs
class InfrastructurePriorityTests(unittest.TestCase):
 def test_connected_pairs(self):self.assertEqual(connected_pairs([['a','b','c'],['d','e']]),4)
 def test_all_highwater_scenarios(self):self.assertEqual(len(evaluate()['results']),9)
 def test_rank_and_no_promotion(self):
  for row in evaluate()['results']:
   gains=[x['restored_connected_pairs'] for x in row['candidate_single_edge_repairs']]
   self.assertEqual(gains,sorted(gains,reverse=True))
   self.assertFalse(row['winner_authorized'])
  self.assertEqual(evaluate()['acceptance'],'HOLD')
 def test_repeatability(self):self.assertEqual(evaluate(),evaluate())
if __name__=='__main__':unittest.main()
