"""Week 5 companion Chronicle: deterministic archival/source and integrity checks.

These are technical assertions only. They cannot authenticate owners, approve
invented geography, provide independent editorial review or promote hard canon.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W04 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W04.md"
W05 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W05.md"
CONTINUITY = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
ARCHIVE_BLOB = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W04_BLOB = "cbe0a6f38c09fe1346cd6ee417c5b2e34593ae6b"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def fmt(number):
    return f"{Decimal(str(number)):.2f}"

class Test2023WeekFiveChronicle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(x["matchups"] for x in cls.archive["weeks"] if x["week"] == 5)
        cls.manuscript = W05.read_text(encoding="utf-8")
        cls.sections = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.manuscript)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.manuscript)
        cls.continuity = json.loads(CONTINUITY.read_text(encoding="utf-8"))

    def test_archival_source_bytes_pinned(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertEqual(self.archive["year"], 2023)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")

    def test_six_scored_fixtures_cover_twelve_unique_slots(self):
        self.assertEqual(len(self.rows), 6)
        ids = [side for row in self.rows for side in (row["home_id"], row["away_id"])]
        self.assertEqual(len(ids), 12)
        self.assertEqual(set(ids), set(range(1, 13)))

    def test_six_substantial_scenes_not_outlines(self):
        self.assertEqual([h[0] for h in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.sections), 7)
        self.assertGreaterEqual(len(self.manuscript.split()), 5200)
        for i, section in enumerate(self.sections[1:], 1):
            with self.subTest(section=i):
                self.assertGreaterEqual(len(section.split()), 430)
                self.assertGreaterEqual(section.count("\n\n"), 6)

    def test_exact_score_winner_margin_and_home_away_each_scene(self):
        winners = [10, 5, 1, 11, 3, 4]
        for i, (row, section) in enumerate(zip(self.rows, self.sections[1:])):
            with self.subTest(matchup=i + 1):
                self.assertIn(f'{row["home"].strip()} (home), {fmt(row["hp"])}', section)
                self.assertIn(f'{row["away"].strip()} (away), {fmt(row["ap"])}', section)
                self.assertIn(f'Margin **{abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"]))):.2f}**', section)
                actual_winner = "HOME" if row["hp"] > row["ap"] else "AWAY"
                self.assertEqual(row["winner"], actual_winner)
                winner_id = row["home_id"] if actual_winner == "HOME" else row["away_id"]
                self.assertEqual(winner_id, winners[i])
                winner = row["home"].strip() if actual_winner == "HOME" else row["away"].strip()
                self.assertIn(f"Winner: **{winner} (slot {winner_id})**", section)

    def test_first_slot_one_win_after_four_defeats(self):
        five = [
            next(r for r in week["matchups"] if 1 in (r["home_id"], r["away_id"]))
            for week in self.archive["weeks"][:5]
        ]
        winners = [
            (r["home_id"] if r["winner"] == "HOME" else r["away_id"]) for r in five
        ]
        self.assertEqual([x == 1 for x in winners], [False, False, False, False, True])
        self.assertEqual(fmt(five[4]["hp"]), "182.48")
        self.assertEqual(fmt(five[4]["ap"]), "129.42")
        self.assertIn("first victory", self.manuscript.lower())
        self.assertIn("1–4", self.manuscript)
        self.assertIn("Margin **53.06**", self.sections[3])

    def test_source_fact_vs_invention_boundary(self):
        for needle in [
            "NONCANON", "PROPOSED FICTION / HISTORICAL ATLAS HOLD",
            "user-attested, not provider-authenticated",
            "Home/away competition fields do not identify physical venues",
            "original ESPN provider SHA", "The Fourth Address",
        ]:
            self.assertIn(needle, self.manuscript)
        self.assertNotRegex(self.manuscript, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_pov_lock_and_weather_identity(self):
        self.assertIn("Only Jake (", self.manuscript)
        self.assertIn("limited interior viewpoint", self.manuscript)
        self.assertIn("Four separate 2023 Benedict banners", self.manuscript)
        self.assertIn("Two Dreaded Snake is the exact 2023 archival banner", self.manuscript)
        self.assertIn("not a speaking or human-shaped being", self.manuscript)
        self.assertIn("does not authenticate fictional actions", self.manuscript)
        self.assertIn("six mandatory novel chapters", self.manuscript)

    def test_no_future_week_sports_result_leak(self):
        self.assertIn("No Week 6+ outcome enters the characters' knowledge", self.manuscript)
        sixth = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 6)
        # Distinctive exact Week-6 scoreboard pairs must not appear as a quoted verdict.
        for row in sixth:
            self.assertNotIn(f'{row["home"].strip()} {fmt(row["hp"])}; {row["away"].strip()} {fmt(row["ap"])}', self.manuscript)

    def test_week_four_manuscript_byte_identical(self):
        self.assertEqual(blob(W04), W04_BLOB)
        self.assertIn("The Price of the Other Bank", W04.read_text(encoding="utf-8"))

    def test_continuity_coverage_increment(self):
        c = self.continuity
        self.assertIn(c["phase"], ["WEEK_01_05_DRAFT_NONCANON", "WEEK_01_06_DRAFT_NONCANON", "WEEK_01_07_DRAFT_NONCANON"])
        self.assertIn(c["story_time_cutoff"], ["after scoring week 5 only", "after scoring week 6 only", "after scoring week 7 only"])
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:5], [1, 2, 3, 4, 5])
        self.assertEqual(m["regular_season_matchups_total"], 84)
        self.assertGreaterEqual(m["verified_matchups"], 30)
        self.assertGreaterEqual(m["regular_season_matchups_covered"], 30)
        self.assertGreaterEqual(m["prose_entries"], 30)
        self.assertTrue(m["week5_complete"])
        self.assertEqual(c["principal_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual(c["historical_transactions_asserted"], 0)
        self.assertTrue(c["drafts"]["fifth_week"].endswith("/W05.md"))
        self.assertIn(c["ci_week5"]["status"], [
            "PENDING_NEW_EXACT_HEAD_WORKFLOW", "SUCCESS_AT_TESTED_COMMIT"
        ])
        if c["ci_week5"]["status"] == "SUCCESS_AT_TESTED_COMMIT":
            self.assertRegex(c["ci_week5"]["tested_commit"], r"^[a-f0-9]{40}$")
            self.assertEqual(c["ci_week5"]["workflow_runs"]["novel_os_ci"], 40851834785)

    def test_hard_manuscript_bytes_unchanged(self):
        for name, expected in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), expected)

if __name__ == "__main__":
    unittest.main()
