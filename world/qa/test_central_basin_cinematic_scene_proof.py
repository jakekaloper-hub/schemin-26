import unittest
from world.atlas.spatial.cinematic_scene_proof import build
class CinematicProofTests(unittest.TestCase):
 def test_reproducible_and_three_cameras(self):
  a=build();self.assertEqual(a,build());self.assertEqual(a['camera_count'],3)
 def test_exact_landmarks_shared(self):
  a=build();self.assertEqual(len(a['landmarks']),5)
  self.assertEqual(len({p['location_id'] for p in a['landmarks']}),5)
 def test_no_promotion_or_unearned_render_claims(self):
  a=build();self.assertEqual(a['approval'],'NOT_CANON_NOT_VISUALLY_REVIEWED')
  self.assertIn('NO_RENDERED_PLATES',a['render_status'])
if __name__=='__main__':unittest.main()
