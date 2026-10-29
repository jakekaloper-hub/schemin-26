"""2023 Week 4 Chronicle: archival score joins, POV limits and protected-canon gates.

Technical tests do NOT constitute literary/Umpire/Atlas approval, owner authentication
or permission to merge or publish.
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
W04 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W04.md"
CONTINUITY = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    content = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def score(value):
    return f"{Decimal(str(value)):.2f}"


class Test2023FourthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 4)
        cls.prose = W04.read_text(encoding="utf-8")
        cls.week3 = W03.read_text(encoding="utf-8")
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.prose)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.prose)
        cls.continuity = json.loads(CONTINUITY.read_text(encoding="utf-8"))

    def test_archive_blob_and_2023_week_four_selection(self):
        self.assertEqual(git_blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.archive["year"], 2023)
        self.assertEqual(len(self.rows), 6)

    def test_all_twelve_team_slots_once(self):
        ids = [side for row in self.rows for side in (row["home_id"], row["away_id"])]
        self.assertEqual(len(ids), 12)
        self.assertEqual(set(ids), set(range(1, 13)))

    def test_six_substantial_individual_encounters(self):
        self.assertEqual([h[0] for h in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.parts), 7)
        self.assertGreaterEqual(len(self.prose.split()), 4100)
        for i, p in enumerate(self.parts[1:], 1):
            with self.subTest(section=i):
                self.assertGreaterEqual(len(p.split()), 430)

    def test_six_pairings_scores_winners_and_margins(self):
        expected_winners = [2, 7, 10, 11, 9, 12]
        for i, (p, row) in enumerate(zip(self.parts[1:], self.rows), 1):
            with self.subTest(matchup=i):
                self.assertIn(f'{row["home"].strip()} (home), {score(row["hp"])}', p)
                self.assertIn(f'{row["away"].strip()} (away), {score(row["ap"])}', p)
                margin = abs(Decimal(str(row["hp"])) - Decimal(str(row["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**", p)
                winner = "HOME" if row["hp"] > row["ap"] else "AWAY"
                self.assertEqual(row["winner"], winner)
                winner_slot = row["home_id"] if winner == "HOME" else row["away_id"]
                self.assertEqual(winner_slot, expected_winners[i-1])

    def test_slot_one_four_consecutive_results(self):
        pairings = [
            next(r for r in w["matchups"] if 1 in (r["home_id"], r["away_id"]))
            for w in self.archive["weeks"][:4]
        ]
        self.assertEqual([r["winner"] for r in pairings], ["HOME", "AWAY", "AWAY", "AWAY"])
        scores = [score(r["hp"] if r["home_id"] == 1 else r["ap"]) for r in pairings]
        self.assertEqual(scores, ["113.02", "113.35", "183.46", "103.24"])
        self.assertEqual(score(pairings[3]["ap"]), "160.64")
        self.assertIn("fourth consecutive defeat", self.prose)
        self.assertIn("Margin **57.40**", self.parts[2])

    def test_pov_and_future_knowledge_boundaries(self):
        self.assertIn("NONCANON", self.prose)
        self.assertIn("HISTORICAL ATLAS HOLD", self.prose)
        self.assertIn("user-attested, not provider-authenticated", self.prose)
        self.assertIn("Home/away competition fields do not identify physical venues", self.prose)
        self.assertIn("Jake (", self.prose)
        self.assertIn("alone carries limited interior viewpoint", self.prose)
        self.assertIn("No Week 5+ outcome enters the characters' knowledge", self.prose)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_no_owner_or_weather_personification(self):
        self.assertIn("Four distinct 2023 Benedict banners", self.prose)
        self.assertIn("Two Dreaded Snake is the exact historical banner", self.prose)
        self.assertIn("not a speaking or human-shaped being", self.prose)
        self.assertIn("not six mandatory novel chapters", self.prose)
        self.assertIn("The Fourth Address", self.prose)
        self.assertIn("Varn", self.prose)
        self.assertIn("Sena", self.prose)
        self.assertIn("ferryman's daughter", self.prose)

    def test_continuity_manifest_preserves_week_four_under_later_append(self):
        c = self.continuity
        self.assertIn(c["phase"], ["WEEK_01_04_DRAFT_NONCANON", "WEEK_01_05_DRAFT_NONCANON", "WEEK_01_06_DRAFT_NONCANON", "WEEK_01_07_DRAFT_NONCANON", "WEEK_01_08_DRAFT_NONCANON", "WEEK_01_09_DRAFT_NONCANON", "WEEK_01_10_DRAFT_NONCANON", "WEEK_01_11_DRAFT_NONCANON"])
        self.assertIn(c["story_time_cutoff"], ["after scoring week 4 only", "after scoring week 5 only", "after scoring week 6 only", "after scoring week 7 only", "after scoring week 8 only", "after scoring week 9 only", "after scoring week 10 only", "after scoring week 11 only"])
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:4], [1, 2, 3, 4])
        self.assertGreaterEqual(m["verified_matchups"], 24)
        self.assertGreaterEqual(m["prose_entries"], 24)
        self.assertGreaterEqual(m["regular_season_matchups_covered"], 24)
        self.assertEqual(m["regular_season_matchups_total"], 84)
        self.assertTrue(m["week4_complete"])
        self.assertEqual(c["historical_transactions_asserted"], 0)
        self.assertEqual(c["principal_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertTrue(c["drafts"]["fourth_week"].endswith("/W04.md"))
        # A CI receipt may be appended after the original manuscript/test commit.
        self.assertIn(c["ci_week4"]["status"], [
            "PENDING_NEW_EXACT_HEAD_WORKFLOW", "SUCCESS_AT_TESTED_COMMIT"])
        if c["ci_week4"]["status"] == "SUCCESS_AT_TESTED_COMMIT":
            self.assertRegex(c["ci_week4"]["tested_commit"], r"^[a-f0-9]{40}$")
            self.assertEqual(c["ci_week4"]["workflow_runs"]["novel_os_ci"], 40843878646)

    def test_preserves_week_three_and_hard_canon_bytes(self):
        self.assertIn("The Road With No Owner", self.week3)
        self.assertEqual(len(re.findall(r"(?m)^## [IVX]+\.", self.week3)), 6)
        for name, expected in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), expected)


if __name__ == "__main__":
    unittest.main()
