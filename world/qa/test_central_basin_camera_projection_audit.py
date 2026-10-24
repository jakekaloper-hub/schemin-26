import unittest
from world.atlas.spatial.camera_projection_audit import audit,project
class CameraProjectionTests(unittest.TestCase):
 def test_deterministic_three_views(self):
  a=audit();self.assertEqual(a,audit());self.assertEqual(len(a['views']),3)
  self.assertEqual(len({v['mesh_sha256'] for v in a['views']}),1)
 def test_five_landmarks_in_every_projection(self):
  for v in audit()['views']:
   self.assertEqual(len(v['projections']),5)
   self.assertEqual(len({p['location_id'] for p in v['projections']}),5)
 def test_behind_camera_rejected(self):
  c={'xyz':[0,0,0],'look_at':[0,10,0]}
  self.assertFalse(project(c,[0,-1,0])['in_front'])
 def test_unapproved(self):
  self.assertIn('NOT_CANON',audit()['approval'])
if __name__=='__main__':unittest.main()
