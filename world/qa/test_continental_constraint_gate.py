import unittest
from world.atlas.spatial.continental_constraint_gate import validate,CANDIDATE_EDGES
class ContinentalConstraintTests(unittest.TestCase):
 def test_baseline_preserves_zone_ontology(self):
  a=validate();self.assertEqual(len(a['edges']),4);self.assertEqual(a['coordinates'],'NONE')
 def test_repeatability(self):self.assertEqual(validate(),validate())
 def test_wrong_outlet_region(self):
  with self.assertRaises(ValueError):validate(CANDIDATE_EDGES[:-1]+(('REG-SOUTHERN-WETLANDS','REG-NORTHERN-SPINE'),))
 def test_missing_mandatory_connection(self):
  with self.assertRaises(ValueError):validate(CANDIDATE_EDGES[:-1])
 def test_cycle_rejected(self):
  with self.assertRaises(ValueError):validate(CANDIDATE_EDGES+(('REG-INNER-SEA-LITTORAL','REG-CENTRAL-BASIN'),))
 def test_unrecognized_id_rejected(self):
  with self.assertRaises(ValueError):validate(CANDIDATE_EDGES+(('REG-FAKE','REG-CENTRAL-BASIN'),))
if __name__=='__main__':unittest.main()
