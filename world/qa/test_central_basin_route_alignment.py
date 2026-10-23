import unittest
from world.atlas.spatial.route_alignment_gate import evaluate,pathfind
class AlignmentTests(unittest.TestCase):
 def test_three_variants_and_four_segments(self):
  x=evaluate();self.assertEqual(len(x['results']),3)
  self.assertTrue(all(len(v['segments'])==4 for v in x['results']))
 def test_endpoints_and_penalty_monotonic_contacts(self):
  for v in evaluate()['results']:
   for s in v['segments']:
    a=s['alternatives'];self.assertEqual(len(a),3)
    self.assertTrue(all(p['endpoint_ids_preserved'] and not p['road_approved'] for p in a))
    self.assertGreaterEqual(a[0]['channel_contact_cells'],a[-1]['channel_contact_cells'])
 def test_repeatability_and_hold(self):
  self.assertEqual(evaluate(),evaluate());self.assertEqual(evaluate()['acceptance'],'HOLD')
 def test_out_of_grid(self):
  with self.assertRaises(ValueError):pathfind([[0]*3 for _ in range(3)],(-50,0),(50,50),set())
if __name__=='__main__':unittest.main()
