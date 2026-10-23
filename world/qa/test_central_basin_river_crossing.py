import unittest
from world.atlas.spatial.river_crossing_gate import screen
class CrossingTests(unittest.TestCase):
 def test_three_models_four_segments(self):
  a=screen();self.assertEqual(len(a['results']),3)
  self.assertTrue(all(len(r['segments'])==4 for r in a['results']))
 def test_no_bridge_invented(self):
  for model in screen()['results']:
   for s in model['segments']:
    self.assertEqual(s['bridge_ford_causeway_type'],'NOT_ESTABLISHED')
    self.assertFalse(s['route_infrastructure_approved'])
 def test_repeatable(self):self.assertEqual(screen(),screen())
 def test_invalid_step(self):
  with self.assertRaises(ValueError):screen(0)
if __name__=='__main__':unittest.main()
