import unittest
from world.atlas.spatial.landscape_experiment import build_landscape

class LandscapeTests(unittest.TestCase):
    def test_reproducible_and_source_bound(self):
        a=build_landscape()
        self.assertEqual(a,build_landscape())
        self.assertEqual(a["region_id"],"REG-CENTRAL-BASIN")
        self.assertEqual(a["status"],"DERIVED_SYNTHETIC_NOT_CANON")
    def test_every_flow_edge_descends(self):
        a=build_landscape()
        h=a["heightfield"]
        self.assertTrue(a["flow_edges"])
        self.assertTrue(all(h[j][i]>h[y][x] for i,j,x,y in a["flow_edges"]))
    def test_accumulation_conservation(self):
        a=build_landscape()
        self.assertEqual(sum(a["flow_accumulation"][j][i] for i,j in a["sinks"]),a["n"]**2)
    def test_season_keeps_geometry(self):
        a,b=build_landscape(when="2026-10-21"),build_landscape(when="2026-12-21")
        self.assertEqual(a["heightfield"],b["heightfield"])
        self.assertNotEqual(a["season_temperature_c_hypothetical"],b["season_temperature_c_hypothetical"])
    def test_invalid_grid_rejected(self):
        with self.assertRaises(ValueError): build_landscape(n=5)
    def test_no_extra_canonicity(self):
        a=build_landscape()
        self.assertIn("NO_WATERSHED_APPROVAL",a["explicit_limitations"])
if __name__=="__main__":unittest.main()
