#!/usr/bin/env python3
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=json.loads((ROOT/"productions/after-dark/fixtures/p3c_twelve_story_docket.json").read_text())
class DocketTest(unittest.TestCase):
 def test_all_twelve(self):
  self.assertEqual(len(D["cards"]),12)
  self.assertEqual({x["team_id"] for x in D["cards"]},set(range(1,13)))
 def test_complete_provenance(self):
  for x in D["cards"]:
   self.assertEqual(len(x["provenance"]),2)
   self.assertEqual(x["canon_status"],"DERIVED_EDITORIAL_ONLY")
 def test_no_made_up_presence(self):
  for x in D["cards"]:
   self.assertEqual(x["current_physical_whereabouts"],"UNKNOWN")
   self.assertEqual(x["guest_appearance"],"HOLD_ROUTE_AND_STORY_TIME")
 def test_records_are_consistent(self):
  for x in D["cards"]:
   self.assertEqual(x["previous_season"]["year"],2025)
   self.assertEqual(x["current_through_week_7"]["year"],2026)
   self.assertTrue(x["editorial_tension"].endswith("?"))
if __name__=="__main__": unittest.main(verbosity=2)
