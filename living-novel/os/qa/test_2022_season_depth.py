"""2022 season depth: ensure draft/weekly/roster evidence remains source-safe."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("builder",ROOT/"living-novel/os/adapters/flaim/build_2022_season_intelligence.py")
builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
class SeasonDepthTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.packet=builder.build()
 def test_twelve_team_profiles(self):
  t=self.packet["teams"];self.assertEqual(len(t),12)
  self.assertEqual(len({x["historical_team_id"] for x in t}),12)
  self.assertTrue(all(x["owner_identity"]=="UNKNOWN" for x in t))
 def test_draft_selection_keeper_evidence(self):
  t=self.packet["teams"];self.assertEqual(sum(x["draft_profile"]["pick_count"] for x in t),204)
  self.assertEqual(sum(x["draft_profile"]["keeper_flag_count"] for x in t),24)
  self.assertTrue(all(x["draft_profile"]["preseason_grade"]=="UNAVAILABLE_NO_VINTAGE_PROJECTIONS" for x in t))
 def test_all_team_week_cutoffs(self):
  self.assertTrue(all([x["week"] for x in t["weekly_sequence"]]==list(range(1,18)) for t in self.packet["teams"]))
 def test_source_record_trajectory(self):
  r={t["historical_team_id"]:t for t in self.packet["teams"]}
  self.assertEqual(r[2]["regular_season_record"],"13-1")
  self.assertEqual(r[9]["regular_season_record"],"7-7")
 def test_roster_deltas_not_claimed_transactions(self):
  ds=self.packet["red_roster_deltas"];self.assertEqual(len(ds),4)
  self.assertTrue(all(x["cause"]=="UNKNOWN_NOT_A_CONFIRMED_TRADE_OR_WAIVER" for x in ds))
  self.assertEqual([(len(x["appeared"]),len(x["departed"])) for x in ds],[(2,2),(3,3),(8,6),(1,1)])
if __name__=="__main__":unittest.main()
