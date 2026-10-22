import unittest
from world.atlas.spatial.landmark_surface_reconciliation import reconcile
class SurfaceReconciliationTests(unittest.TestCase):
 def test_five_unchanged_identity_records(self):
  a=reconcile();self.assertEqual(len(a['placements']),5)
  self.assertEqual(len({v['location_id'] for v in a['placements']}),5)
  self.assertTrue(all(v['original_landmark_geometry_preserved'] for v in a['placements']))
 def test_ground_contact_is_terrain_derived(self):
  for v in reconcile()['placements']:
   self.assertEqual(v['derived_ground_contact_xyz_candidate'][:2],v['xy_candidate'])
   self.assertEqual(v['derived_ground_contact_xyz_candidate'][2],v['terrain_ground_z_candidate'])
 def test_no_fabricated_foundation_types(self):
  a=reconcile();self.assertEqual(a['acceptance'],'HOLD')
  self.assertTrue(all(x['structure_or_platform_height']=='UNRESOLVED' and not x['derived_ground_contact_approved'] for x in a['placements']))
 def test_determinism(self):self.assertEqual(reconcile(),reconcile())
if __name__=='__main__':unittest.main()
