import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("roster",ROOT/"living-novel/os/adapters/flaim/build_multi_season_roster_deltas.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ArchiveQualityTests(unittest.TestCase):
 def test_all_eleven_years_have_twelve_team_slots(self):
  for y in range(2015,2026):
   self.assertEqual(len(m.build(y)["teams"]),12)
 def test_early_snapshots_not_promoted_to_verified_roster_history(self):
  for y in (2015,2016,2017):
   d=m.build(y)
   self.assertTrue(all(not t["appeared_ids"] and not t["departed_ids"] for t in d["teams"]))
 def test_later_seasons_reveal_actual_observed_changes(self):
  for y in range(2018,2026):
   d=m.build(y)
   self.assertGreater(sum(len(t["appeared_ids"]) for t in d["teams"]),0)
if __name__=="__main__":unittest.main()
