import unittest
from world.atlas.spatial.seasonal_network_resilience import evaluate,components
class SeasonalNetworkTests(unittest.TestCase):
 def test_all_scenarios(self):
  r=evaluate();self.assertEqual(len(r['results']),27)
  self.assertTrue(all(row['base_route_edges']==4 for row in r['results']))
 def test_closure_can_disconnect(self):
  r=evaluate()['results'];self.assertTrue(any(not row['all_landmarks_connected'] for row in r if row['season']=='HIGH_WATER'))
  self.assertTrue(all(row['closed_edges_hypothesis']==0 for row in r if row['season']!='HIGH_WATER'))
 def test_components(self):
  self.assertEqual(components({'a','b','c'},[('a','b')]),[['a','b'],['c']])
 def test_deterministic_hold(self):
  a=evaluate();self.assertEqual(a,evaluate());self.assertEqual(a['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
