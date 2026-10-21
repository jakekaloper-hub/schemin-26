import unittest
from world.atlas.spatial.mesh_export import render_obj
class MeshTest(unittest.TestCase):
    def test_deterministic_obj(self):
        a=render_obj(n=9,step_m=50)
        self.assertEqual(a,render_obj(n=9,step_m=50))
        self.assertEqual(sum(x.startswith("v ") for x in a.splitlines()),81)
        self.assertEqual(sum(x.startswith("f ") for x in a.splitlines()),128)
        self.assertIn("NOT CANON",a)
if __name__=="__main__":unittest.main()
