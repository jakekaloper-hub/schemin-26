import unittest
from world.atlas.spatial.mesh_visibility_gate import geometry,segment_hits_triangle,audit
class MeshVisibilityTests(unittest.TestCase):
 def test_mesh_topology(self):
  vertices,faces=geometry();self.assertEqual(len(vertices),1089);self.assertEqual(len(faces),2048)
 def test_segment_hit_and_miss(self):
  a=(0,0,0);b=(1,0,0);c=(0,1,0)
  self.assertTrue(segment_hits_triangle((.2,.2,1),(.2,.2,-1),a,b,c))
  self.assertFalse(segment_hits_triangle((2,2,1),(2,2,-1),a,b,c))
 def test_determinism_and_no_false_promotion(self):
  a=audit();self.assertEqual(a,audit());self.assertEqual(a['acceptance'],'HOLD')
 def test_all_views_reuse_five_ids(self):
  for v in audit()['camera_checks']:self.assertEqual(len(v['landmarks']),5)
if __name__=='__main__':unittest.main()
