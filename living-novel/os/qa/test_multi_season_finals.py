"""Protect independently retrieved champion finals across varying playoff formats."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json"
class FinalsTests(unittest.TestCase):
 def setUp(self):
  self.doc=json.loads(EVIDENCE.read_text())
 def test_eleven_unique_seasons(self):
  years=[r["season"] for r in self.doc["finals"]]
  self.assertEqual(years,list(range(2015,2026)))
 def test_final_has_two_distinct_teams_and_actual_victory(self):
  for e in self.doc["finals"]:
   with self.subTest(year=e["season"]):
    self.assertNotEqual(e["winner_team_id"],e["runnerup_team_id"])
    self.assertGreater(e["winner_points"],e["runnerup_points"])
 def test_older_final_week_not_forced_to_17(self):
  for e in self.doc["finals"]:
   expected=16 if e["season"] in range(2015,2021) else 17
   self.assertEqual(e["final_scoring_week"],expected)
 def test_2018_tenth_of_point_is_not_final(self):
  e=next(x for x in self.doc["finals"] if x["season"]==2018)
  self.assertEqual((e["winner_team_id"],e["winner_points"],e["runnerup_points"]),(8,160.69,153.26))
 def test_2022_accords_week_17_full_extract(self):
  raw=json.loads((ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json").read_text())
  final=next(r for r in raw["rows"] if r["week"]==17 and r["tier"]=="WINNERS_BRACKET")
  e=next(r for r in self.doc["finals"] if r["season"]==2022)
  self.assertEqual(e["winner_team_id"],final["home_team_id"])
  self.assertEqual(e["winner_points"],final["home_points"])
if __name__=="__main__": unittest.main()
