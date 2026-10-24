import copy
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import unittest

modpath = Path(__file__).resolve().parents[1] / "data-gateway/weekly_matchup_receipt.py"
spec = importlib.util.spec_from_file_location("weekly_matchup_receipt", modpath)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def capture():
    return {"provider":"flaim","platform":"espn","league_id":"1417621",
        "season_year":2026,"week":6,"captured_at":"2026-10-22T18:00:00Z",
        "matchups":[{"matchupPeriodId":6,
          "home":{"teamId":i,"teamName":f"Team {i}","currentPoints":90.0},
          "away":{"teamId":i+1,"teamName":f"Team {i+1}","currentPoints":92.0},
          "winner":"AWAY"} for i in range(1,13,2)]}

class WeeklyReceiptTests(unittest.TestCase):
    def test_valid(self):
        d=m.normalize(capture(), now=datetime(2026,10,22,18,30,tzinfo=timezone.utc))
        self.assertEqual(len(d["matchups"]),6)
        self.assertFalse(d["meta"]["stale"])
        self.assertFalse(d["meta"]["end_to_end_live_certified"])
    def test_stale(self):
        d=m.normalize(capture(), now=datetime(2026,10,23,tzinfo=timezone.utc))
        self.assertTrue(d["meta"]["stale"])
    def test_duplicate(self):
        d=capture()
        d["matchups"][0]["away"]["teamId"]=1
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)
    def test_wrong_week(self):
        d=capture()
        d["matchups"][0]["matchupPeriodId"]=5
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)
    def test_wrong_league(self):
        d=capture();d["league_id"]="999"
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)
    def test_future(self):
        with self.assertRaises(m.WeeklyMatchupError):
            m.normalize(capture(), now=datetime(2026,10,21,tzinfo=timezone.utc))
    def test_no_timezone(self):
        d=capture();d["captured_at"]="2026-10-22T18:00:00"
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)
    def test_missing_side(self):
        d=capture();d["matchups"][0]["away"]=None
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)
    def test_unknown_winner(self):
        d=capture();d["matchups"][0]["winner"]="PROBABLE"
        with self.assertRaises(m.WeeklyMatchupError):m.normalize(d)

if __name__=="__main__":unittest.main()
