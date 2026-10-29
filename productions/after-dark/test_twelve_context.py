#!/usr/bin/env python3
import json, subprocess, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"productions/after-dark/fixtures/p3c_twelve_character_context.json"
class ContinuityTests(unittest.TestCase):
 def setUp(self):
  self.data=json.loads(P.read_text())["characters"]
 def test_all_twelve_unique(self):
  self.assertEqual(len(self.data),12)
  self.assertEqual(len({x["team_id"] for x in self.data}),12)
 def test_no_home_location_masquerading_as_current(self):
  for x in self.data:
   self.assertEqual(x["last_verified_physical_whereabouts"]["status"],"UNKNOWN")
 def test_no_teleported_guest(self):
  for x in self.data:
   self.assertEqual(x["travel_to_broadcast_house"]["status"],"UNVERIFIED")
   self.assertIn("NO_IN_PERSON",x["interview"]["allowed"])
 def test_source_grounded_home_locations(self):
  locs={x["id"] for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
  for x in self.data:self.assertIn(x["canonical_home"]["location_id"],locs)
 def test_no_silent_canon(self):
  for x in self.data:self.assertEqual(x["approval"],"NONCANON_DERIVED_DRAFT")
 def test_existing_narrative_fixture(self):
  p=subprocess.run(["node",str(ROOT/"productions/after-dark/validate_p3c_narrative.cjs")],cwd=ROOT,text=True,capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr)
if __name__=="__main__":unittest.main(verbosity=2)
