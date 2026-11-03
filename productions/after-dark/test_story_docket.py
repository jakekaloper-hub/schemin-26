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
class WeeklyEnrichmentTests(unittest.TestCase):
 def setUp(self):
  self.doc=json.loads((ROOT/"productions/after-dark/fixtures/p3c_week7_week8_editorial_cards.json").read_text())
 def test_all_12_with_opponents(self):
  self.assertEqual(len(self.doc["cards"]),12)
  for c in self.doc["cards"]:
   self.assertIn(c["week7_reported"]["result"],("WIN","LOSS"))
   self.assertEqual(c["week8_preview"]["result"],"UNDECIDED")
 def test_all_games_symmetric(self):
  by={c["team_id"]:c for c in self.doc["cards"]}
  for c in by.values():
   for key in ("week7_reported","week8_preview"):
    m=c[key];other=by[m["opponent_id"]][key]
    self.assertEqual(other["opponent_id"],c["team_id"])
    self.assertNotEqual(m["home_away"],other["home_away"])
 def test_no_unapproved_novel_claims(self):
  for c in self.doc["cards"]:
   self.assertEqual(c["novel_continuity"]["approval"],"UNRESOLVED")
   self.assertEqual(c["last_known_week7_location"],"UNKNOWN")
   self.assertIn("PROVISIONAL",c["intelligence_class"])

if __name__=="__main__": unittest.main(verbosity=2)
