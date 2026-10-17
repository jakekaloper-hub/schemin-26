import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("roster_delta",ROOT/"living-novel/os/adapters/flaim/build_2022_all_team_roster_deltas.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class AllRosterTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.build()
 def test_all_twelve_distinct(self):
  self.assertEqual([t["historical_team_id"] for t in self.data["teams"]],list(range(1,13)))
 def test_all_have_weekly_roster_samples(self):
  self.assertTrue(all(t["week1_count"]>=15 and t["week14_count"]>=15 for t in self.data["teams"]))
 def test_no_trade_attribution(self):
  self.assertTrue(all(t["transaction_cause"]=="UNKNOWN" for t in self.data["teams"]))
 def test_red_delta(self):
  r=self.data["teams"][1];self.assertEqual((len(r["arrivals_observed"]),len(r["departures_observed"])),(9,7))
 def test_no_conjured_player(self):
  self.assertTrue(all(all(name for name in t["arrivals_observed"]+t["departures_observed"]) for t in self.data["teams"]))
if __name__=="__main__":unittest.main()
