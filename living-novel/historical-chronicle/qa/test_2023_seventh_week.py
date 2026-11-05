"""2023 Week 7 Chronicle six-match provenance, POV, temporal and canon regression.

Technical assertions only: no literary, historical owner, fictional Atlas,
independent review, or canon/publishing endorsement.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W06 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W06.md"
W07 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W07.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W06_SHA = "87f8ee0b654d5e259af06e672996c58db85b81b0"
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

class Test2023SeventhWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(x["matchups"] for x in cls.archive["weeks"] if x["week"] == 7)
        cls.story = W07.read_text(encoding="utf-8")
        cls.sections = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.story)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.story)
        cls.continuity = json.loads(CONT.read_text(encoding="utf-8"))

    def test_archived_evidence_immutable(self):
        self.assertEqual(git_blob(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["year"], 2023)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")

    def test_six_archive_fixtures_cover_twelve_distinct_slots(self):
        self.assertEqual(len(self.rows), 6)
        slots = [x for r in self.rows for x in (r["home_id"], r["away_id"])]
        self.assertEqual(set(slots), set(range(1, 13)))
        self.assertEqual(len(slots), 12)

    def test_archive_winner_sequence_matches_prose(self):
        winners = [r["home_id"] if r["winner"] == "HOME" else r["away_id"] for r in self.rows]
        self.assertEqual(winners, [1, 3, 11, 9, 2, 7])
        self.assertIn("1 Benedict Kenobi", self.story)
        self.assertIn("7 The Blew Waffle's", self.story)

    def test_six_complete_individual_scenes(self):
        self.assertEqual([h[0] for h in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.sections), 7)
        self.assertGreaterEqual(len(self.story.split()), 5200)
        for i, scene in enumerate(self.sections[1:], 1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()), 540)
                self.assertGreaterEqual(scene.count("\n\n"), 8)

    def test_exact_scores_home_away_winner_and_margin_per_scene(self):
        for i, (r, scene) in enumerate(zip(self.rows, self.sections[1:]), 1):
            with self.subTest(scene=i):
                self.assertIn(f'{r["home"].strip()} (home), {points(r["hp"])}', scene)
                self.assertIn(f'{r["away"].strip()} (away), {points(r["ap"])}', scene)
                home = Decimal(str(r["hp"])) > Decimal(str(r["ap"]))
                self.assertEqual(r["winner"], "HOME" if home else "AWAY")
                name = r["home"].strip() if home else r["away"].strip()
                slot = r["home_id"] if home else r["away_id"]
                self.assertIn(f"Winner: **{name} (slot {slot})**", scene)
                margin = abs(Decimal(str(r["hp"])) - Decimal(str(r["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**", scene)

    def test_slot_one_after_week_seven_is_three_four(self):
        previous = [next(r for r in w["matchups"] if 1 in (r["home_id"], r["away_id"])) for w in self.archive["weeks"][:7]]
        wins = [r["home_id"] == 1 if r["winner"] == "HOME" else r["away_id"] == 1 for r in previous]
        self.assertEqual(wins, [False, False, False, False, True, True, True])
        self.assertIn("3–4", self.story)
        self.assertIn("124.53–102.04", self.story)

    def test_no_owner_or_atlas_promotion(self):
        for term in ["NONCANON", "PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                     "user-attested, not provider-authenticated", "original ESPN provider SHA",
                     "Home/away competition fields do not identify physical venues",
                     "Only Jake", "limited interior viewpoint",
                     "Four distinct 2023 Benedict banners", "not a speaking or human-shaped being"]:
            self.assertIn(term, self.story)
        self.assertNotRegex(self.story, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_no_week_eight_future_score_in_story(self):
        self.assertIn("No Week 8+ results enter", self.story)
        rows8 = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 8)
        for r in rows8:
            self.assertNotIn(f'{r["home"].strip()} (home), {points(r["hp"])}', self.story)

    def test_predecessor_week_six_exact_bytes(self):
        self.assertEqual(git_blob(W06), W06_SHA)
        self.assertIn("The Hour No Boat Crossed", W06.read_text(encoding="utf-8"))

    def test_continuity_is_append_only_and_complete_through_seven(self):
        c = self.continuity
        self.assertRegex(c["phase"], r"^WEEK_01_(?:0[1-9]|1[0-4])_DRAFT_NONCANON$")
        self.assertGreaterEqual(int(c["phase"].split("_")[2]),7)
        self.assertEqual(c["story_time_cutoff"], f"after scoring week {int(c['phase'].split('_')[2])} only")
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:7], list(range(1, 8)))
        self.assertGreaterEqual(m["regular_season_matchups_covered"], 42)
        self.assertGreaterEqual(m["prose_entries"], 42)
        self.assertEqual(m["regular_season_matchups_total"], 84)
        self.assertTrue(m["week7_complete"])
        self.assertTrue(m["week6_complete"])
        self.assertEqual(c["drafts"]["seventh_week"], str(W07.relative_to(ROOT)))

    def test_owner_and_release_gates_still_closed(self):
        c = self.continuity
        self.assertEqual(c["principal_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual(c["historical_transactions_asserted"], 0)
        self.assertEqual(c["other_owner_povs"], "NONE")
        self.assertEqual(c["world_atlas_status"], "UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week7"]["independent_umpire"], "NOT_OBTAINED")
        self.assertIn(c["ci_week7"]["status"], ["PENDING_EXACT_HEAD_WORKFLOW", "SUCCESS_AT_TESTED_COMMIT"])

    def test_hard_canon_files_byte_stable(self):
        for name, sha in PROTECTED.items():
            with self.subTest(file=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
