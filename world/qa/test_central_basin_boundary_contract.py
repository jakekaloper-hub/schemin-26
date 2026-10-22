import unittest
from world.atlas.spatial.boundary_contract import audit_boundary,classify
class BoundaryContractTests(unittest.TestCase):
 def test_boundary_classification(self):
  self.assertEqual(classify((5,0),33),'south')
  self.assertEqual(classify((3,32),33),'north')
  with self.assertRaises(ValueError):classify((5,5),33)
 def test_three_candidates_preserve_macro_relations(self):
  a=audit_boundary();self.assertEqual(len(a['results']),3)
  self.assertTrue(all(x['southern_receiving_zone']=='REG-SOUTHERN-WETLANDS' for x in a['results']))
 def test_no_fake_mouths_or_certification(self):
  a=audit_boundary();self.assertEqual(a['independent_acceptance'],'HOLD')
  self.assertTrue(all(x['verified_river_mouths']==0 and not x['geographic_boundary_certified'] for x in a['results']))
if __name__=='__main__':unittest.main()
