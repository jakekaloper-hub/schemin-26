import unittest
from world.atlas.spatial.scene_svg_render import plate
class SceneSVGTests(unittest.TestCase):
 def test_three_reproducible_plates(self):
  for i in range(3):
   s=plate(i);self.assertEqual(s,plate(i));self.assertIn('<polygon',s)
   self.assertIn('NOT CANON',s)
 def test_distinct_viewpoints(self):self.assertNotEqual(plate(0),plate(1))
if __name__=='__main__':unittest.main()
