import unittest
from world.atlas.spatial.crossing_infrastructure_gate import classify
class CrossingInfrastructureTests(unittest.TestCase):
 def test_all_variants(self):
  a=classify();self.assertEqual(len(a['results']),9)
  self.assertTrue(all(len(v['segments'])==4 for v in a['results']))
 def test_contact_triggers_review(self):
  all_segments=[x for v in classify()['results'] for x in v['segments']]
  self.assertTrue(any(x['corridor_contacts_high_penalty']>0 for x in all_segments))
  for x in all_segments:
   self.assertFalse(x['historical_approval'])
   self.assertIsNone(x['crossing_type_selected'])
   if x['corridor_contacts_high_penalty']:
    self.assertEqual(x['classification'],'CROSSING_REVIEW_REQUIRED')
 def test_deterministic_hold(self):
  a=classify();self.assertEqual(a,classify());self.assertEqual(a['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
