"""Noncanonical 2023 Week 8 Chronicle archival provenance and continuity regression.
Cannot certify human owners, Atlas placement, literary review, or publication.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
W07 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W07.md"
W08 = ROOT / "living-novel/historical-chronicle/seasons/2023/weeks/W08.md"
CONT = ROOT / "living-novel/historical-chronicle/seasons/2023/CONTINUITY.json"
SOURCE_SHA = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
W07_SHA = "d54c16e34ff9766e6d09599181e62d99deae0409"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def score(x):
    return f"{Decimal(str(x)):.2f}"

class Test2023EighthWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 8)
        cls.story = W08.read_text(encoding="utf-8")
        cls.continuity = json.loads(CONT.read_text(encoding="utf-8"))
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", cls.story)
        cls.scenes = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.story)[1:]

    def test_archive_source_blob_and_year(self):
        self.assertEqual(git_blob(ARCHIVE), SOURCE_SHA)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertEqual(self.archive["year"], 2023)

    def test_all_twelve_archive_slots_once(self):
        self.assertEqual(len(self.rows), 6)
        slots = [sid for r in self.rows for sid in (r["home_id"], r["away_id"])]
        self.assertEqual(len(slots), 12)
        self.assertEqual(set(slots), set(range(1,13)))

    def test_winner_sequence_and_consistent_scores(self):
        ids = []
        for r in self.rows:
            home_win = Decimal(str(r["hp"])) > Decimal(str(r["ap"]))
            self.assertEqual(r["winner"], "HOME" if home_win else "AWAY")
            ids.append(r["home_id"] if home_win else r["away_id"])
        self.assertEqual(ids, [9, 12, 3, 4, 10, 11])

    def test_exact_home_away_scores_and_margin_in_each_scene(self):
        for idx, (r, scene) in enumerate(zip(self.rows, self.scenes),1):
            with self.subTest(scene=idx):
                self.assertIn(f'{r["home"].strip()} (home), {score(r["hp"])}',scene)
                self.assertIn(f'{r["away"].strip()} (away), {score(r["ap"])}',scene)
                h = r["winner"] == "HOME"
                name = r["home"].strip() if h else r["away"].strip()
                slot = r["home_id"] if h else r["away_id"]
                self.assertIn(f"Winner: **{name} (slot {slot})**",scene)
                margin = abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))
                self.assertIn(f"Margin **{margin:.2f}**",scene)

    def test_six_full_scenes_substantial_prose(self):
        self.assertEqual([h[0] for h in self.headings],["I","II","III","IV","V","VI"])
        self.assertEqual(len(self.scenes), 6)
        self.assertGreaterEqual(len(self.story.split()), 5000)
        for i, scene in enumerate(self.scenes,1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()), 650)
                self.assertGreaterEqual(scene.count("\n\n"), 9)

    def test_week_eight_slot_one_record(self):
        fixtures = [next(r for r in w["matchups"] if 1 in (r["home_id"],r["away_id"])) for w in self.archive["weeks"][:8]]
        wins = [(r["home_id"] if r["winner"] == "HOME" else r["away_id"]) == 1 for r in fixtures]
        self.assertEqual(wins, [False,False,False,False,True,True,True,False])
        self.assertIn("3–5",self.story)
        self.assertIn("142.10–205.16",self.story)

    def test_authority_and_proposed_fiction_gates(self):
        for phrase in ("NONCANON", "PROPOSED FICTION / HISTORICAL ATLAS HOLD",
                       "user-attested, not provider-authenticated", "original ESPN provider SHA",
                       "Home/away competition fields do not identify physical venues",
                       "Only Jake", "limited interior viewpoint", "four distinct 2023 Benedict banners",
                       "not a speaking or human-shaped being", "No Week 9+ result enters"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.story)
        self.assertNotRegex(self.story,r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_no_week_nine_score_leak(self):
        nine = next(w["matchups"] for w in self.archive["weeks"] if w["week"] == 9)
        for r in nine:
            self.assertNotIn(f'{r["home"].strip()} (home), {score(r["hp"])}',self.story)

    def test_previous_manuscript_exact_bytes(self):
        self.assertEqual(git_blob(W07), W07_SHA)
        self.assertIn("The Names on Both Banks", W07.read_text(encoding="utf-8"))

    def test_2023_continuity_append_and_hold(self):
        c = self.continuity
        self.assertIn(c["phase"], ["WEEK_01_08_DRAFT_NONCANON", "WEEK_01_09_DRAFT_NONCANON", "WEEK_01_10_DRAFT_NONCANON", "WEEK_01_11_DRAFT_NONCANON"])
        self.assertIn(c["story_time_cutoff"], ["after scoring week 8 only", "after scoring week 9 only", "after scoring week 10 only", "after scoring week 11 only"])
        m = c["matchup_coverage"]
        self.assertEqual(m["scoring_weeks_complete"][:8],list(range(1,9)))
        self.assertEqual(m["regular_season_matchups_total"],84)
        self.assertGreaterEqual(m["regular_season_matchups_covered"],48)
        self.assertGreaterEqual(m["prose_entries"],48)
        self.assertTrue(m["week8_complete"])
        self.assertEqual(c["drafts"]["eighth_week"],str(W08.relative_to(ROOT)))

    def test_pov_release_and_provenance_still_held(self):
        c = self.continuity
        self.assertEqual(c["principal_pov_ids"],["CHAR-JAKE-KALOPER"])
        self.assertEqual(c["other_owner_povs"],"NONE")
        self.assertEqual(c["source"]["raw_provider_sha"],"UNKNOWN")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")
        self.assertEqual(c["historical_transactions_asserted"],0)
        self.assertEqual(c["world_atlas_status"],"UNAPPROVED_PROPOSED_STAGING")
        self.assertEqual(c["ci_week8"]["independent_umpire"],"NOT_OBTAINED")

    def test_protected_main_hard_canon_exact_bytes(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT/"living-novel/manuscript"/name),sha)

if __name__ == "__main__":
    unittest.main()
