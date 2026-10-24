"""Regression gates for imported historical playoff evidence."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PLAYOFF=ROOT/"living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
LEDGER=ROOT/"living-novel/history/PLAYOFF_ARCHAEOLOGY.md"
CHAMP=ROOT/"living-novel/history/CHAMPIONSHIP_SUCCESSION_MACHINE_INDEX_2015_2026.json"

class PlayoffHistoryTests(unittest.TestCase):
    def test_matchups_scores_and_sources(self):
        data=json.loads(PLAYOFF.read_text(encoding="utf-8"))
        self.assertEqual(len(data["matchups"]),12)
        self.assertEqual(sorted(set(row["season"] for row in data["matchups"])),[2022,2023,2024,2025])
        for row in data["matchups"]:
            self.assertGreater(row["winner_score"],row["loser_score"])
            self.assertAlmostEqual(row["margin"],row["winner_score"]-row["loser_score"])
            self.assertEqual(row["provenance"],["living-novel/history/PLAYOFF_ARCHAEOLOGY.md"])
        self.assertFalse(data["raw_ESPN_refetch_in_this_operation"])
    def test_matches_ledger_and_champions(self):
        source=LEDGER.read_text(encoding="utf-8")
        rows=json.loads(PLAYOFF.read_text(encoding="utf-8"))["matchups"]
        champions={s["season"]:s["champion"]["team_name"] for s in json.loads(CHAMP.read_text(encoding="utf-8"))["seasons"]}
        for r in rows:
            text=f'{r["winner"]} {r["winner_score"]:.2f} defeated {r["loser"]} {r["loser_score"]:.2f}.'
            self.assertIn(text,source)
            if r["round"]=="championship":
                self.assertEqual(r["winner"],champions[r["season"]])
        self.assertEqual(sum(r["round"]=="championship" for r in rows),4)
if __name__=="__main__":
    unittest.main()
