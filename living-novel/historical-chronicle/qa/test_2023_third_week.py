"""2023 Chronicle Week 3 noncanonical source/POV/protection regression.

The assertions validate manuscript/source concordance, not prose quality,
historical owner joins, Atlas approval, Umpire signoff or canon promotion.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W03 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W03.md"
CONTINUITY = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def score(n):
    return f"{Decimal(str(n)):.2f}"


class Test2023ThirdWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = W03.read_text(encoding="utf-8")
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(week["matchups"] for week in cls.data["weeks"] if week["week"] == 3)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.text)
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.text)

    def test_source_integrity_and_complete_week(self):
        self.assertEqual(git_blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.data["year"], 2023)
        self.assertEqual(len(self.rows), 6)
        ids = [i for r in self.rows for i in (r["home_id"], r["away_id"])]
        self.assertEqual(len(ids), 12)
        self.assertEqual(set(ids), set(range(1, 13)))

    def test_six_distinct_substantial_literary_scenes(self):
        self.assertEqual([n for n, _ in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.parts), 7)
        self.assertGreaterEqual(len(self.text.split()), 3400)
        for section in self.parts[1:]:
            self.assertGreaterEqual(len(section.split()), 360)

    def test_six_source_rows_score_margin_and_banner(self):
        for section, row in zip(self.parts[1:], self.rows):
            with self.subTest(slots=(row["home_id"], row["away_id"])):
                self.assertIn(f'{row["home"].strip()} (home), {score(row["hp"])}', section)
                self.assertIn(f'{row["away"].strip()} (away), {score(row["ap"])}', section)
                margin = abs(Decimal(str(row["hp"])) - Decimal(str(row["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**", section)
                self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_third_consecutive_team_one_loss_and_narrow_margin(self):
        weekly = [next(row for row in w["matchups"] if 1 in (row["home_id"], row["away_id"])) for w in self.data["weeks"][:3]]
        self.assertEqual([r["winner"] for r in weekly], ["HOME", "AWAY", "AWAY"])
        self.assertEqual([score(r["away_id"] == 1 and r["ap"] or r["hp"]) for r in weekly],
                         ["113.02", "113.35", "183.46"])
        self.assertEqual(score(weekly[2]["away_id"] == 1 and weekly[2]["hp"] or weekly[2]["ap"]), "184.75")
        self.assertIn("third consecutive defeat", self.text)
        self.assertIn("Margin **1.29**", self.parts[2])

    def test_historical_separation_and_future_knowledge_gate(self):
        self.assertIn("NONCANON", self.text)
        self.assertIn("HISTORICAL ATLAS HOLD", self.text)
        self.assertIn("Home/away does not identify a physical venue", self.text)
        self.assertIn("user-attested, not provider-authenticated", self.text)
        self.assertIn("No character knows a Week 4+ result", self.text)
        self.assertIn("The Fourth Address", self.text)
        self.assertNotRegex(self.text, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_fantasy_entities_and_owner_firewall(self):
        self.assertIn("storm-name/banner without speech or humanoid form", self.text)
        self.assertIn("exact 2023 archival banner", self.text)
        self.assertIn("Four separate 2023 Benedict team labels", self.text)
        self.assertNotIn("real owner", self.parts[3].lower())

    def test_protected_book_one_main_blobs(self):
        for filename, expected in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / filename), expected)

    def test_continuity_register_reconciles_with_prose(self):
        c = json.loads(CONTINUITY.read_text(encoding="utf-8"))
        # This suite guards the immutable Week 3 contribution even after later weeks
        # append to the shared season manifest. Do not require a stale final-week phase.
        self.assertRegex(c["phase"], r"^WEEK_01_(?:0[1-9]|1[0-4])_DRAFT_NONCANON$")
        self.assertGreaterEqual(int(c["phase"].split("_")[2]),3)
        self.assertEqual(c["matchup_coverage"]["scoring_weeks_complete"][:3], [1, 2, 3])
        self.assertGreaterEqual(c["matchup_coverage"]["verified_matchups"], 18)
        self.assertGreaterEqual(c["matchup_coverage"]["prose_entries"], 18)
        self.assertTrue(c["matchup_coverage"]["week3_complete"])
        self.assertIn("CHAR-JAKE-KALOPER", c["principal_pov_ids"])
        self.assertEqual(c["historical_transactions_asserted"], 0)


if __name__ == "__main__":
    unittest.main()
