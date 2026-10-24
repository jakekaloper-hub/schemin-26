import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("season_division_reader",ROOT/"living-novel/os/adapters/season_division_reader.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
DATA=json.loads((ROOT/"world/data/divisions.json").read_text())
class SeasonalDivisionTests(unittest.TestCase):
 def test_current_membership(self):
  x=mod.season_divisions(season=2026,division_data=DATA)
  self.assertEqual(len(x["assignments"]),12)
  self.assertEqual(x["assignments"][1],"DIV-BURGERS")
 def test_every_earlier_year_is_unknown(self):
  for y in range(2015,2026):
   x=mod.season_divisions(season=y,division_data=DATA)
   self.assertEqual(x["status"],"UNKNOWN_HISTORICAL_DIVISIONS")
   self.assertFalse(x["assignments"])
 def test_evidenced_prior_year(self):
  x=mod.season_divisions(season=2022,division_data=DATA,season_evidence={"season":2022,"source":"audited_period_fixture","divisions":[{"id":"DIV-WINGS","team_ids":[1,2]}]})
  self.assertEqual(x["assignments"][1],"DIV-WINGS")
 def test_wrong_year_rejected(self):
  with self.assertRaises(ValueError):
   mod.season_divisions(season=2022,division_data=DATA,season_evidence={"season":2026,"source":"current","divisions":[]})
 def test_duplicate_assignment_rejected(self):
  with self.assertRaises(ValueError):
   mod.season_divisions(season=2022,division_data=DATA,season_evidence={"season":2022,"source":"test","divisions":[{"id":"A","team_ids":[2]},{"id":"B","team_ids":[2]}]})
if __name__=="__main__":unittest.main()
