#!/usr/bin/env python3
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BUILD=ROOT/"world"/"atlas"/"interactive"/"build_interactive_atlas.py"
OUT=ROOT/"world"/"atlas"/"interactive"/"SCHEMIN_ATLAS_INTERACTIVE.html"
spec=importlib.util.spec_from_file_location("atlas_build",BUILD);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

route_spec=importlib.util.spec_from_file_location("read_only_route_preview",ROOT/"world"/"atlas"/"interactive"/"read_only_route_preview.py")
route_view=importlib.util.module_from_spec(route_spec)
route_spec.loader.exec_module(route_view)

class Phase4Tests(unittest.TestCase):
 def load(self,p):return json.loads((ROOT/p).read_text())
 def test_counts(self):
  self.assertEqual(len(self.load("world/data/physical_zones.json")["regions"]),7)
  self.assertEqual(len(self.load("world/data/locations.json")["locations"]),23)
  self.assertEqual(len(self.load("world/data/routes.json")["routes"]),18)
  candidates=self.load("world/data/atlas_location_candidates.json")["candidates"]
  self.assertEqual(len({c["id"] for c in candidates}),len(candidates))
  self.assertIn("CAND-AFTER-DARK-BROADCAST-HOUSE",{c["id"] for c in candidates})
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
 def test_semantic_property_features_come_from_existing_registry(self):
  text=OUT.read_text()
  controls=self.load("world/location-control-plane/registries/PARENT_SUBLOCATION_REGISTRY.json")["handles"]
  self.assertEqual(len(controls),58)
  for handle in controls:
   self.assertIn(handle["handle_id"],text)
  self.assertIn("SUB::LOC-TRADE-JEDI-MOUNTAIN-BASE::HIGH-RIDGE",text)
  self.assertIn("SUB::LOC-TRADE-JEDI-MOUNTAIN-BASE::WAR-ROOM-OVERLOOK",text)
  self.assertIn("Known feature handles:",text)
  self.assertIn("site measurements UNKNOWN",text)

 def test_readonly_route_preview_trade_jedi_to_bridge(self):
  packet=route_view.read_only_preview("LOC-TRADE-JEDI-MOUNTAIN-BASE","LOC-BRIDGE-MOUNTAIN-LAKE")
  self.assertTrue(packet["ok"])
  self.assertEqual(packet["status"],"TOPOLOGICAL_PREVIEW_ONLY")
  self.assertEqual(packet["hop_count"],1)
  self.assertEqual(packet["hops"][0]["route_id"],"ROUTE-EASTERN-ASCENT")
  self.assertIsNone(packet["distance_m"])
  self.assertIsNone(packet["duration_minutes"])
  self.assertIsNone(packet["parcel_area_m2"])
  self.assertFalse(packet["canon_mutation_allowed"])
  self.assertEqual(packet["approved_cinematic_reference_uris"],[])
  self.assertTrue(packet["approved_structural_reference_uris"])

 def test_readonly_route_preview_all_twelve_owners_can_reach_network(self):
  for owner in self.load("world/data/owner_domains.json")["domains"]:
   with self.subTest(character=owner["character_id"]):
    packet=route_view.read_only_preview(owner["primary_location_id"],"LOC-LEAGUE-CHAMBER")
    self.assertTrue(packet["ok"])
    self.assertFalse(packet["canon_mutation_allowed"])
    self.assertIsNone(packet["distance_m"])

 def test_unknown_and_candidate_ids_never_become_active(self):
  for lid in ("LOC-FAKE","CAND-CHAMP-LAST-FIELD"):
   packet=route_view.read_only_preview("LOC-TRADE-JEDI-MOUNTAIN-BASE",lid)
   self.assertFalse(packet["ok"])
   self.assertEqual(packet["code"],"UNKNOWN_OR_EDITORIAL_LOCATION")

 def test_disconnected_route_fails_without_teleportation(self):
  locs=[{"id":"LOC-A","physical_zone_id":"REG-X"},{"id":"LOC-B","physical_zone_id":"REG-X"}]
  result=route_view.read_only_preview("LOC-A","LOC-B",locations=locs,routes=[],references=[])
  self.assertEqual(result["code"],"NO_ESTABLISHED_ROUTE")

 def test_invalid_route_endpoint_fails_closed(self):
  locs=[{"id":"LOC-A"},{"id":"LOC-B"}]
  with self.assertRaisesRegex(ValueError,"missing active endpoint"):
   route_view.read_only_preview("LOC-A","LOC-B",
    locations=locs,routes=[{"id":"ROUTE-INVALID","from":"LOC-A","to":"LOC-C"}],references=[])

 def test_readonly_view_is_integrated_into_interactive_atlas(self):
  text=OUT.read_text()
  for expected in ("traceApprovedRoute","routeGraph","id=\"routePlanner\"",
                   "id=\"routeStatus\"","Route topology only","active-route"):
   self.assertIn(expected,text)
  self.assertNotIn("travel ETA: ",text)
  self.assertIn("Catalog only. No map coordinates are asserted.",text)

if __name__=="__main__":unittest.main(verbosity=2)
