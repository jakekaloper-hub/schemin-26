#!/usr/bin/env python3
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BUILD=ROOT/"world"/"atlas"/"interactive"/"build_interactive_atlas.py"
OUT=ROOT/"world"/"atlas"/"interactive"/"SCHEMIN_ATLAS_INTERACTIVE.html"
spec=importlib.util.spec_from_file_location("atlas_build",BUILD);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Phase4Tests(unittest.TestCase):
 def load(self,p):return json.loads((ROOT/p).read_text())
 def test_counts(self):
  self.assertEqual(len(self.load("world/data/physical_zones.json")["regions"]),7)
  self.assertEqual(len(self.load("world/data/locations.json")["locations"]),23)
  self.assertEqual(len(self.load("world/data/routes.json")["routes"]),18)
  self.assertEqual(len(self.load("world/data/atlas_location_candidates.json")["candidates"]),48)
 def test_output_deterministic(self):
  before=OUT.read_text() if OUT.exists() else ""
  m.main(); after=OUT.read_text()
  self.assertEqual(before,after)
 def test_candidate_not_active_marker(self):
  text=OUT.read_text()
  self.assertNotIn('data-location="CAND-',text)
  self.assertNotIn('data-location="CAND-CHAMP-LAST-FIELD"',text)
 def test_editorial_catalog_is_nonspatial(self):
  text=OUT.read_text()
  self.assertIn("Catalog only. No map coordinates are asserted.",text)
 def test_structural_reference_link_supported(self):
  self.assertIn("STRUCTURAL_PLATE.svg",OUT.read_text())
 def test_active_ids_embedded(self):
  text=OUT.read_text()
  for l in self.load("world/data/locations.json")["locations"]:
   self.assertIn(l["id"],text)
if __name__=="__main__":unittest.main(verbosity=2)
