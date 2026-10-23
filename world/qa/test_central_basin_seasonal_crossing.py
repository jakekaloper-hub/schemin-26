import unittest
from world.atlas.spatial.seasonal_crossing_gate import evaluate
class SeasonalCrossingTests(unittest.TestCase):
 def test_27_scenarios_four_segments(self):
  a=evaluate();self.assertEqual(len(a['results']),27)
  self.assertTrue(all(len(x['segments'])==4 for x in a['results']))
 def test_high_water_never_certifies_fords(self):
  for row in evaluate()['results']:
   for s in row['segments']:
    self.assertFalse(s['ford_certified']);self.assertFalse(s['passability_approved'])
    if row['scenario']=='HIGH_WATER' and s['candidate_channel_contact']:
     self.assertNotIn('FORD_REVIEW',s['possible_review_options'])
 def test_determinism_hold(self):
  a=evaluate();self.assertEqual(a,evaluate());self.assertEqual(a['approval'],'HOLD')
if __name__=='__main__':unittest.main()
