import copy
import json
import unittest
from pathlib import Path
from world.atlas.spatial.surface_validation import validate_surface
DATA=Path(__file__).resolve().parents[1]/"atlas/spatial/central_basin_surface_candidate_v1.json"
class TestSurface(unittest.TestCase):
    def setUp(self):
        self.d=json.loads(DATA.read_text())
    def test_baseline(self): self.assertEqual(validate_surface(self.d),[])
    def test_invalid_polygon(self):
        self.d["footprints"][0]["ring"]=[[0,0],[100,100],[0,100],[100,0]]
        self.assertIn("INVALID_FOOTPRINT",validate_surface(self.d))
    def test_grid_out_of_bounds(self):
        self.d["footprints"][0]["ring"][0]=[-1,0]
        self.assertIn("FOOTPRINT_OUTSIDE_GRID",validate_surface(self.d))
    def test_uphill(self):
        self.d["drainage"][1]["surface_z"]=60
        self.assertIn("UPHILL_FLOW",validate_surface(self.d))
    def test_surface_height_mismatch(self):
        self.d["drainage"][0]["surface_z"]=100
        self.assertIn("DRAINAGE_ELEVATION_MISMATCH",validate_surface(self.d))
    def test_route_identity(self):
        self.d["route_geometries"][0]["route_id"]="ROUTE-INVENTED"
        self.assertIn("ROUTE_ID_DRIFT",validate_surface(self.d))
    def test_season_status(self):
        self.d["seasonal_fields"][0]["status"]="CANON"
        self.assertIn("SEASON_AUTHORITY_DRIFT",validate_surface(self.d))
    def test_date_consistency(self):
        self.d["seasonal_fields"][0]["date"]="2035-01-01"
        self.assertIn("SEASON_DATE_DRIFT",validate_surface(self.d))
if __name__=="__main__": unittest.main()
