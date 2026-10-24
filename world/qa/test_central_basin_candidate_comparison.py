import unittest
from world.atlas.spatial.candidate_comparison import compare_candidates
class TestComparison(unittest.TestCase):
 def test_three_variants_reproducible(self):
  a=compare_candidates();self.assertEqual(a,compare_candidates())
  self.assertEqual([x['variant'] for x in a['variants']],['baseline','west-ridge','central-valley'])
 def test_same_route_topology_and_no_promotion(self):
  a=compare_candidates()['variants']
  signatures=[[(x['route_id'],x['from'],x['to']) for x in c['candidate_segments']] for c in a]
  self.assertEqual(signatures[0],signatures[1]);self.assertEqual(signatures[1],signatures[2])
  self.assertTrue(all(not x['coordinate_approval'] for x in a))
 def test_candidate_terrain_is_distinct(self):
  a=compare_candidates()['variants']
  self.assertNotEqual(a[0]['heightfield'],a[1]['heightfield'])
  self.assertNotEqual(a[0]['heightfield'],a[2]['heightfield'])
 def test_grade_finite(self):
  for c in compare_candidates()['variants']:
   self.assertTrue(all(0<=seg['candidate_max_grade']<1 for seg in c['candidate_segments']))
if __name__=='__main__':unittest.main()
