import json,unittest,copy
from pathlib import Path
from ScheminBridge.build_travel_graph import compile_graph
P=Path(__file__).resolve().parents[1]
class TravelTests(unittest.TestCase):
 def test_all_routes(self):
  g=compile_graph(json.loads((P/"canonical_routes_snapshot.json").read_text()),json.loads((P/"generated/world_preview_manifest.json").read_text()))
  self.assertEqual(len(g["routes"]),18)
  self.assertTrue(all(not r["approved_for_navigation"] and r["physical_distance"] is None for r in g["routes"]))
 def test_unknown_endpoint_rejected(self):
  a=json.loads((P/"canonical_routes_snapshot.json").read_text());a["routes"][0]["from"]="FAKE"
  b=json.loads((P/"generated/world_preview_manifest.json").read_text())
  with self.assertRaises(ValueError):compile_graph(a,b)
