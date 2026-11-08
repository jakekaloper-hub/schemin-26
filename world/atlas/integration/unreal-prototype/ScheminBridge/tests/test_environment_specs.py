import json,unittest
from pathlib import Path
from ScheminBridge.build_environment_specs import compile_specs
P=Path(__file__).resolve().parents[1]/"generated/world_preview_manifest.json"
class EnvironmentTests(unittest.TestCase):
 def test_specs_all_locations(self):
  out=compile_specs(json.loads(P.read_text()))
  self.assertEqual(len(out["specifications"]),23)
 def test_preserve_landmark_labels(self):
  original=json.loads(P.read_text())["locations"]
  out=compile_specs(json.loads(P.read_text()))["specifications"]
  a={x["id"]:x["landmarks"] for x in original}
  for s in out:self.assertEqual([p["source_label"] for p in s["landmark_proxies"]],a[s["location_id"]])
 def test_fail_closed(self):
  out=compile_specs(json.loads(P.read_text()))
  self.assertTrue(all(not x["character_assets_allowed"] and not x["publication_allowed"] for x in out["specifications"]))
