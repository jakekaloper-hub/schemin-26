import unittest
from world.atlas.spatial.wide_corridor_route_gate import expand,evaluate
class WideCorridorTests(unittest.TestCase):
 def test_expansion(self):
  self.assertEqual(len(expand({(2,2)},5,1)),9)
  with self.assertRaises(ValueError):expand({(2,2)},5,-1)
 def test_all_scenarios(self):
  a=evaluate();self.assertEqual(len(a['results']),9)
  self.assertTrue(all(len(v['segments'])==4 for v in a['results']))
 def test_risk_penalty_reduces_contacts_or_preserves(self):
  for variant in evaluate()['results']:
   for segment in variant['segments']:
    a=segment['options'];self.assertGreaterEqual(a[0]['corridor_contacts'],a[-1]['corridor_contacts'])
 def test_deterministic_fail_closed(self):
  a=evaluate();self.assertEqual(a,evaluate());self.assertEqual(a['acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
