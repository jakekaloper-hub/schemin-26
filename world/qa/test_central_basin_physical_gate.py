import unittest
from world.atlas.spatial.physical_candidate_gate import evaluate
class TestPhysicalGate(unittest.TestCase):
 def test_deterministic_and_noncanonical(self):
  a=evaluate();self.assertEqual(a,evaluate());self.assertEqual(a['acceptance'],'HOLD')
  self.assertTrue(all(not s['geometry_approved'] for s in a['results']))
 def test_three_surfaces_and_valid_flow_counts(self):
  a=evaluate();self.assertEqual(len(a['results']),3)
  for s in a['results']:
   self.assertEqual(s['drainage_edge_count']+s['candidate_sink_count'],33**2)
 def test_candidate_sites_present(self):
  for s in evaluate()['results']:
   self.assertEqual(len(s['landmark_relief']),5)
   self.assertTrue(all(not p['site_certified'] for p in s['landmark_relief']))
if __name__=='__main__':unittest.main()
