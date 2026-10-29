"""2023 Week 6 Chronicle archive, continuity and protected-source regression.

This suite cannot approve historical owner identities, Atlas placements,
literary quality, independent Umpire review or promotion to hard canon.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W05 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W05.md"
W06 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W06.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
PREVIOUS_SHA = "6ee34372a9c9b36e141b5a0513ac28bb161b0170"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def points(number):
    return f"{Decimal(str(number)):.2f}"

class Test2023SixthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 6)
        cls.story = W06.read_text(encoding="utf-8")
        cls.sections = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.story)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.story)
        cls.continuity = json.loads(CONT.read_text(encoding="utf-8"))

    def test_archived_2023_evidence_pinned(self):
        self.assertEqual(git_blob(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertEqual(self.archive["year"], 2023)

    def test_six_distinct_archive_pairs_and_winners(self):
        self.assertEqual(len(self.rows), 6)
        ids = [id_ for r in self.rows for id_ in (r["home_id"], r["away_id"])]
        self.assertEqual(set(ids), set(range(1, 13)))
        self.assertEqual(len(ids), 12)
        actual = [(r["home_id"] if r["winner"] == "HOME" else r["away_id"]) for r in self.rows]
        self.assertEqual(actual, [1, 5, 10, 11, 4, 2])

    def test_six_dramatized_not_outlined_scenes(self):
        self.assertEqual([h[0] for h in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.sections), 7)
        self.assertGreaterEqual(len(self.story.split()), 3800)
        for idx, segment in enumerate(self.sections[1:], 1):
            with self.subTest(scene=idx):
                self.assertGreaterEqual(len(segment.split()), 480)
                self.assertGreaterEqual(segment.count("\n\n"), 7)

    def test_archive_home_away_scores_winners_and_margins_in_scene(self):
        for index, (row, scene) in enumerate(zip(self.rows, self.sections[1:]), 1):
            with self.subTest(scene=index):
                self.assertIn(f'{row["home"].strip()} (home), {points(row["hp"])}', scene)
                self.assertIn(f'{row["away"].strip()} (away), {points(row["ap"])}', scene)
                self.assertIn(f'Margin **{abs(Decimal(str(row["hp"]))-Decimal(str(row["ap"]))):.2f}**', scene)
                winner_home = row["hp"] > row["ap"]
                self.assertEqual(row["winner"], "HOME" if winner_home else "AWAY")
                winning_id = row["home_id"] if winner_home else row["away_id"]
                winning_name = row["home"].strip() if winner_home else row["away"].strip()
                self.assertIn(f"Winner: **{winning_name} (slot {winning_id})**", scene)

    def test_slot_one_record_after_six_weeks(self):
        history = [next(r for r in w["matchups"] if 1 in (r["home_id"], r["away_id"])) for w in self.archive["weeks"][:6]]
        won = [(r["home_id"] if r["winner"] == "HOME" else r["away_id"]) == 1 for r in history]
        self.assertEqual(won, [False, False, False, False, True, True])
        self.assertIn("2–4", self.story)
        self.assertIn("132.20–130.02", self.story)

    def test_noncanon_and_pov_authority(self):
        for phrase in ("NONCANON", "PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "user-attested, not provider-authenticated", "original ESPN provider SHA",
                       "Only Jake", "limited interior viewpoint", "Four separate 2023 Benedict banners"):
            self.assertIn(phrase, self.story)
        self.assertNotRegex(self.story, r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertIn("not a speaking or human-shaped being", self.story)
        self.assertIn("Home/away competition fields do not identify physical venues", self.story)

    def test_week_seven_future_result_not_dramatically_leaked(self):
        self.assertIn("Week 7+ results do not enter", self.story)
        seven = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 7)
        for row in seven:
            needle = f'{row["home"].strip()} (home), {points(row["hp"])}'
            self.assertNotIn(needle, self.story)

    def test_week_five_exact_bytes_unchanged(self):
        self.assertEqual(git_blob(W05), PREVIOUS_SHA)
        self.assertIn("The Boat Without a Name", W05.read_text(encoding="utf-8"))

    def test_continuity_six_week_coverage_and_release_holds(self):
        c = self.continuity
        self.assertEqual(c["phase"], "WEEK_01_06_DRAFT_NONCANON")
        self.assertEqual(c["story_time_cutoff"], "after scoring week 6 only")
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(m["regular_season_matchups_total"], 84)
        self.assertEqual(m["regular_season_matchups_covered"], 36)
        self.assertEqual(m["prose_entries"], 36)
        self.assertTrue(m["week6_complete"])
        self.assertEqual(c["principal_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual(c["historical_transactions_asserted"], 0)
        self.assertIn(c["ci_week6"]["status"], ["PENDING_EXACT_HEAD_WORKFLOW", "SUCCESS_AT_TESTED_COMMIT"])
        if c["ci_week6"]["status"] == "SUCCESS_AT_TESTED_COMMIT":
            self.assertRegex(c["ci_week6"]["tested_commit"], r"^[a-f0-9]{40}$")
            self.assertEqual(c["ci_week6"]["workflow_runs"]["novel_os_ci"], 40859837525)
        self.assertEqual(c["ci_week6"]["independent_umpire"], "NOT_OBTAINED")

    def test_protected_hard_canon_byte_stability(self):
        for name, sha in PROTECTED.items():
            with self.subTest(file=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
