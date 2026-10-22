import unittest
from world.atlas.spatial.watershed_audit import audit_watersheds
class WatershedTests(unittest.TestCase):
 def test_mass_conservation(self):
  a=audit_watersheds()
  self.assertEqual(len(a['results']),3)
  self.assertTrue(all(x['catchment_cells']==33**2 for x in a['results']))
 def test_interior_sinks_reported_not_silenced(self):
  for x in audit_watersheds()['results']:
   self.assertGreaterEqual(x['interior_sinks'],0)
   self.assertEqual(x['hydrology_accepted'],False)
 def test_cannot_auto_certify(self):
  self.assertEqual(audit_watersheds()['physical_acceptance'],'HOLD')
if __name__=='__main__':unittest.main()
