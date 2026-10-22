import unittest
from world.atlas.spatial.river_floodplain_gate import evaluate,analyze_surface
class RiverFloodTests(unittest.TestCase):
 def test_determinism(self):
  self.assertEqual(evaluate(),evaluate())
 def test_three_landmark_screens(self):
  r=evaluate();self.assertEqual(len(r['results']),3)
  self.assertTrue(all(len(x['landmarks'])==5 for x in r['results']))
 def test_fail_closed(self):
  r=evaluate();self.assertEqual(r['acceptance'],'HOLD')
  self.assertTrue(all(not v['floodplain_certified'] for v in r['results']))
 def test_channel_exposure_on_sloped_grid(self):
  g=[[10-y for x in range(7)] for y in range(7)]
  r=analyze_surface(g,channel_threshold=3)
  self.assertGreater(r['channel_cells'],0)
  self.assertGreaterEqual(r['near_channel_low_cells'],r['channel_cells'])
 def test_flat_routing_reaches_boundaries(self):
  a=evaluate()
  self.assertTrue(all(x['unresolved_flat_interior_cells']==0 for x in a['results']))
  self.assertTrue(any(x['routed_flat_interior_cells']>0 for x in a['results']))
 def test_priority_flood_parent_graph_has_no_orphans(self):
  from world.atlas.spatial.candidate_comparison import compare_candidates
  from world.atlas.spatial.outlet_gate import drain_to_boundary
  for c in compare_candidates()['variants']:
   a=drain_to_boundary(c['heightfield']);n=len(c['heightfield'])
   parents={(x,y):(u,v) for x,y,u,v in a['routing_parents']}
   roots={tuple(x) for x in a['terminal_boundary_cells']}
   self.assertEqual(len(parents)+len(roots),n*n)
   for point in parents:
    seen=set();p=point
    while p in parents:
     self.assertNotIn(p,seen);seen.add(p);p=parents[p]
    self.assertIn(p,roots)
 def test_invalid_parameters(self):
  with self.assertRaises(ValueError):analyze_surface([[1]],stage_m=-1)
if __name__=='__main__':unittest.main()
