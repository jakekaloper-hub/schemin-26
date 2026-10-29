"""Noncanonical 2023 Week 9 Chronicle — 12 archival, temporal and protected-canon guards.
Green tests do NOT establish provider owner identity, Atlas acceptance, literary review or canon.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W08 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W08.md"
W09 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W09.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W08_SHA = "d1713f9f4b95643545983f0f2a8b3376e62e3c99"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def score(v):
    return f"{Decimal(str(v)):.2f}"

class Test2023NinthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 9)
        cls.story = W09.read_text(encoding="utf-8")
        cls.continuity = json.loads(CONT.read_text(encoding="utf-8"))
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.story)
        cls.scenes = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.story)[1:]

    def test_source_is_pinned_archived_2023_flaim(self):
        self.assertEqual(git_blob(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertEqual(self.archive["year"], 2023)
        self.assertIn("Raw ESPN SHA unavailable", self.archive["limits"])

    def test_six_matchups_have_all_twelve_disjoint_archive_slots(self):
        self.assertEqual(len(self.rows), 6)
        slots = [x for r in self.rows for x in (r["home_id"], r["away_id"])]
        self.assertEqual(len(slots), 12)
        self.assertEqual(set(slots), set(range(1, 13)))

    def test_archive_winner_sequence_and_scores(self):
        winning = []
        for row in self.rows:
            self.assertEqual(row["winner"], "HOME" if Decimal(str(row["hp"])) > Decimal(str(row["ap"])) else "AWAY")
            winning.append(row["home_id"] if row["winner"] == "HOME" else row["away_id"])
        self.assertEqual(winning, [4, 11, 7, 3, 5, 9])

    def test_each_scene_preserves_exact_home_away_winner_margin(self):
        self.assertEqual(len(self.scenes), 6)
        for index, (r, scene) in enumerate(zip(self.rows, self.scenes), 1):
            with self.subTest(scene=index):
                self.assertIn(f'{r["home"].strip()} (home), {score(r["hp"])}', scene)
                self.assertIn(f'{r["away"].strip()} (away), {score(r["ap"])}', scene)
                home_wins = r["winner"] == "HOME"
                winner = r["home"].strip() if home_wins else r["away"].strip()
                slot = r["home_id"] if home_wins else r["away_id"]
                self.assertIn(f"Winner: **{winner} (slot {slot})**", scene)
                margin = abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**", scene)

    def test_six_material_scenes_and_connected_opening(self):
        self.assertEqual([i for i, _ in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertGreaterEqual(len(self.story.split()), 5500)
        self.assertTrue(self.story.index("The heat failed") < self.story.index("## I."))
        for idx, scene in enumerate(self.scenes, 1):
            with self.subTest(scene=idx):
                self.assertGreaterEqual(len(scene.split()), 650)
                self.assertGreaterEqual(scene.count("\n\n"), 10)

    def test_proposed_slot_one_record_is_3_wins_6_losses(self):
        fixtures = [next(r for r in w["matchups"] if 1 in (r["home_id"],r["away_id"])) for w in self.archive["weeks"][:9]]
        winning = [(r["home_id"] if r["winner"] == "HOME" else r["away_id"]) == 1 for r in fixtures]
        self.assertEqual(winning, [False,False,False,False,True,True,True,False,False])
        self.assertIn("3–6", self.story)
        self.assertIn("144.12–137.40", self.story)

    def test_source_to_fiction_firewall_is_explicit(self):
        for phrase in (
            "NONCANON", "PROPOSED FICTION / HISTORICAL ATLAS HOLD",
            "user-attested, not provider-authenticated",
            "Home/away competition fields do not identify physical venues",
            "Four distinct Benedict banners", "El Niño banner",
            "sole proposed principal interior viewpoint", "No Week 10+ result",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.story)

    def test_banned_viewpoints_and_future_leak_are_absent(self):
        self.assertNotRegex(self.story, r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertNotRegex(self.story, r"(?i)El Niño\s+(?:said|spoke|walked|thought|asked|smiled)")
        ten = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 10)
        for r in ten:
            self.assertNotIn(f'{r["home"].strip()} (home), {score(r["hp"])}', self.story)
            self.assertNotIn(f'{r["away"].strip()} (away), {score(r["ap"])}', self.story)

    def test_previous_week_eight_manuscript_bytes_preserved(self):
        self.assertEqual(git_blob(W08), W08_SHA)
        self.assertIn("The Bell Without a Tongue", W08.read_text(encoding="utf-8"))

    def test_append_only_continuity_counts_54_of_84(self):
        c = self.continuity
        self.assertIn(c["phase"], ["WEEK_01_09_DRAFT_NONCANON", "WEEK_01_10_DRAFT_NONCANON", "WEEK_01_11_DRAFT_NONCANON", "WEEK_01_12_DRAFT_NONCANON"])
        self.assertIn(c["story_time_cutoff"], ["after scoring week 9 only", "after scoring week 10 only", "after scoring week 11 only", "after scoring week 12 only"])
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:9], list(range(1, 10)))
        self.assertGreaterEqual(m["regular_season_matchups_covered"], 54)
        self.assertEqual(m["regular_season_matchups_total"], 84)
        self.assertGreaterEqual(m["prose_entries"], 54)
        self.assertTrue(m["week8_complete"])
        self.assertTrue(m["week9_complete"])
        self.assertEqual(c["drafts"]["ninth_week"], str(W09.relative_to(ROOT)))

    def test_canon_and_editorial_holds_remain_fail_closed(self):
        c = self.continuity
        self.assertEqual(c["principal_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual(c["other_owner_povs"], "NONE")
        self.assertEqual(c["source"]["raw_provider_sha"], "UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"], "UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"], 0)
        self.assertEqual(c["world_atlas_status"], "UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week9"]["independent_umpire"], "NOT_OBTAINED")

    def test_four_main_protected_manuscript_blobs_untouched(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
