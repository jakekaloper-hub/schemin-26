"""Second-week six-match literary Chronicle integrity, noncanon."""
from decimal import Decimal
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W01 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W01.md"
W02 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W02.md"


def money(n):
    return f"{Decimal(str(n)):.2f}"


def source_rows():
    archive = json.loads(SOURCE.read_text(encoding="utf-8"))
    return next(w["matchups"] for w in archive["weeks"] if w["week"] == 2)


class Test2023SecondWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week1 = W01.read_text(encoding="utf-8")
        cls.week2 = W02.read_text(encoding="utf-8")
        cls.rows = source_rows()
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.week2)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. (.+)$", cls.week2)

    def test_six_events_twelve_distinct_slots(self):
        self.assertEqual(len(self.rows), 6)
        ids = [i for row in self.rows for i in (row["home_id"], row["away_id"])]
        self.assertEqual(set(ids), set(range(1, 13)))
        self.assertEqual(len(ids), 12)

    def test_prose_six_substantial_events(self):
        self.assertEqual([h[0] for h in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.parts), 7)
        self.assertGreaterEqual(len(self.week2.split()), 2900)
        for i, section in enumerate(self.parts[1:], 1):
            with self.subTest(section=i):
                self.assertGreaterEqual(len(section.split()), 260)

    def test_recorded_score_and_margin_each_match(self):
        for i, row in enumerate(self.rows, 1):
            with self.subTest(row=(row["home_id"], row["away_id"])):
                p = self.parts[i]
                self.assertIn(f'{row["home"].strip()} (home), {money(row["hp"])}', p)
                self.assertIn(f'{row["away"].strip()} (away), {money(row["ap"])}', p)
                gap = abs(Decimal(str(row["hp"])) - Decimal(str(row["ap"])))
                self.assertIn(f'Margin **{gap:.2f}**', p)
                self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_jake_candidate_source_pair_and_second_loss(self):
        week1 = json.loads(SOURCE.read_text(encoding="utf-8"))["weeks"][0]["matchups"]
        first = next(r for r in week1 if 1 in (r["home_id"], r["away_id"]))
        second = next(r for r in self.rows if 1 in (r["home_id"], r["away_id"]))
        self.assertEqual(first["away_id"], 1)
        self.assertEqual(second["home_id"], 1)
        self.assertEqual(money(first["ap"]), "113.02")
        self.assertEqual(money(second["hp"]), "113.35")
        self.assertEqual(second["winner"], "AWAY")

    def test_owner_pov_and_weather_guards(self):
        self.assertNotRegex(self.week2, r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertIn("Jake is the only character with interiority", self.week2)
        self.assertIn("not provider-authenticated", self.week2)
        self.assertIn("El Niño is never a speaking humanoid", self.week2)
        self.assertIn("HISTORICAL ATLAS HOLD", self.week2)
        self.assertIn("NONCANON", self.week2)

    def test_no_historical_transaction_or_location_claim(self):
        self.assertIn("home does not prove physical venue", self.week2)
        self.assertIn("not evidence of a business transaction", self.week2)
        self.assertIn("Week 3+ outcomes are not known", self.week2)
        self.assertIn("not an additional required causal chapter", self.week2)

    def test_causality_distinct_from_first_week(self):
        self.assertIn("The Cloth Nobody Owned", (ROOT / "living-novel/historical-chronicle/seasons/2023/PROLOGUE.md").read_text(encoding="utf-8"))
        self.assertIn("six knots", self.week1.lower())
        self.assertIn("six knots", self.week2.lower())
        self.assertIn("Fourth Address", self.week2)


if __name__ == "__main__":
    unittest.main()
