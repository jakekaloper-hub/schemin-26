import unittest
from world.atlas.spatial.terrain_occlusion_gate import elevation,occluded,audit
class OcclusionTests(unittest.TestCase):
 def test_flat_clear_and_blocked(self):
  g=[[0]*5 for _ in range(5)]
  self.assertFalse(occluded([0,0,10],[200,200,10],g))
  self.assertTrue(occluded([0,0,-1],[200,200,-1],g))
 def test_hill_blocks_sight(self):
  g=[[0]*5 for _ in range(5)];g[2][2]=100
  self.assertTrue(occluded([0,100,10],[200,100,10],g))
 def test_grid_outside(self):self.assertIsNone(elevation([[0]*5 for _ in range(5)],-5,5))
 def test_reproducibility_and_hold(self):
  a=audit();self.assertEqual(a,audit());self.assertEqual(len(a['views']),3)
  self.assertEqual(a['approval'],'HOLD')
 def test_input_guard(self):
  with self.assertRaises(ValueError):occluded([0,0,0],[1,1,1],[[0]*3 for _ in range(3)],samples=1)
if __name__=='__main__':unittest.main()
