import unittest
from world.atlas.spatial.crossing_sensitivity_gate import evaluate
class CrossingSensitivityTests(unittest.TestCase):
 def test_settings_and_comparison(self):
  a=evaluate(thresholds=(10,45),widths=(0,1));self.assertEqual(len(a['results']),12)
  self.assertTrue(all(len(r['route_segments'])==4 for r in a['results']))
 def test_wider_corridor_never_reduces_contacts(self):
  a=evaluate(thresholds=(25,),widths=(0,1,2))['results']
  for i in range(0,len(a),3):self.assertLessEqual(a[i]['segments_with_contact'],a[i+1]['segments_with_contact']);self.assertLessEqual(a[i+1]['segments_with_contact'],a[i+2]['segments_with_contact'])
 def test_fail_closed(self):
  self.assertEqual(evaluate(thresholds=(45,),widths=(0,))['approval'],'HOLD')
  with self.assertRaises(ValueError):evaluate(thresholds=(0,))
if __name__=='__main__':unittest.main()
