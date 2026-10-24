"""Real fixture regression for 2022 archived matchup chronology and playoff semantics."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "living-novel/os/adapters/flaim/validate_historical_2022.py"
spec = importlib.util.spec_from_file_location("validate_historical_2022", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json"

class Historical2022Tests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    def test_real_fixture_bracket(self):
        result = mod.validate_extract(self.doc)
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(result["week_count"], 17)
        self.assertEqual(result["record_count"], 105)
        self.assertEqual(result["singles"], 6)
        self.assertEqual(result["title"]["winner_team_id"], 9)
        self.assertEqual(result["title"]["score"], [111.56, 78.3])
    def test_reject_fabricated_champion(self):
        doc = json.loads(json.dumps(self.doc))
        title = next(x for x in doc["rows"] if x["week"] == 17 and x["tier"] == "WINNERS_BRACKET")
        title["winner"] = "AWAY"
        result = mod.validate_extract(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any("contradiction" in x for x in result["issues"]))
    def test_reject_broken_semifinal_to_final(self):
        doc = json.loads(json.dumps(self.doc))
        semi = next(x for x in doc["rows"] if x["week"] == 16 and x["tier"] == "WINNERS_BRACKET")
        semi["winner"] = "HOME" if semi["winner"] == "AWAY" else "AWAY"
        result = mod.validate_extract(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any("finalist" in x for x in result["issues"]))
    def test_reject_singleton_as_decided_win(self):
        doc = json.loads(json.dumps(self.doc))
        lone = next(x for x in doc["rows"] if x.get("away_team_id") is None)
        lone["winner"] = "HOME"
        self.assertFalse(mod.validate_extract(doc)["valid"])
    def test_reject_week_omission(self):
        doc = json.loads(json.dumps(self.doc))
        doc["weeks_queried"].pop()
        self.assertFalse(mod.validate_extract(doc)["valid"])

if __name__ == "__main__":
    unittest.main()
