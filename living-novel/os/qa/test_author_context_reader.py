"""Regression tests for chronology and unknown owner attribution in AuthorContext."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("author_context_reader", ROOT / "living-novel/os/adapters/author_context_reader.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class ContextReaderTests(unittest.TestCase):
    def setUp(self):
        self.domains = json.loads((ROOT / "world/data/owner_domains.json").read_text())
        self.rows = [
            {"season": 2022, "week": 1, "home_team_id": 2, "away_team_id": 4, "home_points": 119.56, "away_points": 117.66, "winner": "HOME"},
            {"season": 2022, "week": 2, "home_team_id": 2, "away_team_id": 1, "home_points": 125, "away_points": 99, "winner": "HOME"},
            {"season": 2026, "week": 4, "home_team_id": 1, "away_team_id": 5, "home_points": 157.33, "away_points": 139.67, "winner": "HOME"},
            {"season": 2026, "week": 5, "home_team_id": 5, "away_team_id": 12, "home_points": 141.44, "away_points": 184.91, "winner": "AWAY"},
        ]
    def query(self, name, year, week, **kw):
        return module.author_context(character_id=name, scene_year=year, scene_week=week,
                                     owner_domains=self.domains, historical_rows=self.rows, **kw)
    def test_historical_identity_not_inferred(self):
        x = self.query("CHAR-KEVIN-ZEEK", 2022, 2)
        self.assertTrue(x["historical_owner_identity_unknown"])
        self.assertEqual(x["character_matchups"], [])
        self.assertEqual(len(x["other_public_matchups"]), 2)
    def test_historical_identity_explicitly_licensed(self):
        x = self.query("CHAR-KEVIN-ZEEK", 2022, 1, known_identity_links={"CHAR-KEVIN-ZEEK":[2]})
        self.assertEqual(len(x["character_matchups"]), 1)
        self.assertEqual(x["historical_domain_state"], "UNKNOWN")
    def test_future_results_filtered(self):
        x = self.query("CHAR-WILSON-LOOK", 2026, 4)
        self.assertEqual(len(x["character_matchups"]), 1)
        self.assertEqual(x["character_matchups"][0]["week"], 4)
    def test_reject_unregistered_owner(self):
        with self.assertRaises(module.AuthorContextError):
            self.query("CHAR-EDRIN", 2026, 4)
    def test_invalid_week(self):
        with self.assertRaises(module.AuthorContextError):
            self.query("CHAR-WILSON-LOOK", 2026, 22)

if __name__ == "__main__":
    unittest.main()
