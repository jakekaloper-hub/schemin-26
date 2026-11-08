import json,unittest
from pathlib import Path
from ScheminBridge.build_region_packets import compile_regions
R=Path(__file__).resolve().parents[1]
class RegionTests(unittest.TestCase):
 def test_region_coverage(self):
  a=json.loads((R/"canonical_regions_snapshot.json").read_text())
  b=json.loads((R/"generated/world_preview_manifest.json").read_text())
  out=compile_regions(a,b)
  self.assertEqual(len(out["regions"]),7)
  self.assertEqual(sum(len(x["location_ids"]) for x in out["regions"]),23)
 def test_no_canon_promotion(self):
  a=json.loads((R/"canonical_regions_snapshot.json").read_text())
  b=json.loads((R/"generated/world_preview_manifest.json").read_text())
  self.assertTrue(all(not x["publishable"] for x in compile_regions(a,b)["regions"]))
