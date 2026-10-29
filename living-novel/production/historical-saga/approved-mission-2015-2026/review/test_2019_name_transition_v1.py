"""Fail-closed regressions for NONCANON 2019 league-name transition reader.

Validates certified league-name and team-slot events; does NOT certify
historical human-owner identity, Atlas geography, literary merit,
an Author Council/Umpire review, or canon/publication authority.
"""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
ROOT = HERE.parent / "manuscript" / "2019-name-transition"
TEXT = ROOT / "THE_NAME_DID_NOT_CARRY_THE_WEIGHT_CAUSAL_READING_V1_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V1.json"
SCORES = REPO / "living-novel/production/full-rewrite-2026/evidence/G01_2019_FULL_WEEKLY_MATCHUPS.json"
ERA = REPO / "living-novel/history/HISTORICAL_ERAS.md"
STORY_ROOM = REPO / "living-novel/production/full-rewrite-2026/G04_HISTORICAL_SEASON_STORY_ROOM_PACKETS.json"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob_sha(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

class Test2019NameTransitionV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT.read_text(encoding="utf-8")
        cls.story = cls.text.split("## I. The Letters Under the Cloth", 1)[1]
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.scores = json.loads(SCORES.read_text(encoding="utf-8"))
        cls.era = ERA.read_text(encoding="utf-8")
        cls.room = json.loads(STORY_ROOM.read_text(encoding="utf-8"))
        cls.by_week = {}
        for entry in cls.scores["weeks"]:
            fixtures = [m for m in entry["matchups"] if 1 in (m["home_id"], m["away_id"])]
            if fixtures:
                cls.by_week[entry["week"]] = fixtures[0]

    def test_protected_prologue_and_chapters_i_iii_are_identical(self):
        for fn, sha in PROTECTED.items():
            with self.subTest(file=fn):
                self.assertEqual(git_blob_sha(REPO / "living-novel/manuscript" / fn), sha)

    def test_substantial_continuous_four_movement_prose(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", self.text)
        self.assertEqual([x[0] for x in headings], ["I", "II", "III", "IV"])
        self.assertEqual([x[1] for x in headings], [
            "The Letters Under the Cloth", "What the Roof Required",
            "The Eighth Defeat", "A Name with Room Behind It",
        ])
        self.assertGreaterEqual(len(self.story.split()), 3700)
        self.assertEqual(len(self.reg["scenes"]), 4)

    def test_only_canonical_jake_is_pov(self):
        self.assertEqual(self.reg["primary_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertTrue(all(s["pov_character_id"] == "CHAR-JAKE-KALOPER" and
                            s["pov_class"] == "PRINCIPAL_CHARACTER"
                            for s in self.reg["scenes"]))
        self.assertNotRegex(self.story, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_verified_name_change_is_bounded_and_cause_unknown(self):
        self.assertEqual(self.scores["year"], 2019)
        self.assertIn("The League of Thrones", self.era)
        self.assertIn("Pro Schemin' Football League", self.era)
        self.assertEqual(self.reg["historical_rename_cause"], "UNKNOWN")
        self.assertEqual(self.reg["historical_venue_status"], "PROPOSED_UNAPPROVED")
        self.assertIn("The reason for that real-world renaming is **UNKNOWN**", self.text)

    def test_sporting_anchor_rows_match_flaim_evidence(self):
        for scene in self.reg["scenes"]:
            for anchor in scene["source_score_anchors"]:
                with self.subTest(week=anchor["week"]):
                    row = self.by_week[anchor["week"]]
                    self.assertIn(anchor["opponent_slot"], [row["home_id"], row["away_id"]])
                    self.assertEqual(1 in [row["home_id"], row["away_id"]], True)
                    actual_j = row["hp"] if row["home_id"] == 1 else row["ap"]
                    actual_o = row["ap"] if row["home_id"] == 1 else row["hp"]
                    self.assertEqual(Decimal(str(actual_j)), Decimal(str(anchor["team_1_points"])))
                    self.assertEqual(Decimal(str(actual_o)), Decimal(str(anchor["opponent_points"])))
                    self.assertEqual("WIN" if actual_j > actual_o else "LOSS", anchor["outcome"])

    def test_weeks_2_through_9_defeats_and_week_10_win(self):
        self.assertEqual(set(self.by_week), set(range(1, 17)))
        for n in range(2, 10):
            r = self.by_week[n]
            j = r["hp"] if r["home_id"] == 1 else r["ap"]
            o = r["ap"] if r["home_id"] == 1 else r["hp"]
            self.assertLess(j, o)
        r = self.by_week[10]
        self.assertGreater(r["hp"] if r["home_id"] == 1 else r["ap"],
                           r["ap"] if r["home_id"] == 1 else r["hp"])
        self.assertIn("Eight consecutive defeats", self.text)

    def test_all_16_team_slot_periods_accounted_but_not_all_dramatized(self):
        exposed = [n for s in self.reg["scenes"] for n in s["source_weeks"]]
        background = self.reg["background_unforegrounded_weeks"]
        self.assertEqual(set(exposed) | set(background), set(range(1, 17)))
        self.assertFalse(set(exposed) & set(background))
        self.assertEqual(len(exposed), 12)
        self.assertEqual(len(background), 4)
        self.assertFalse(self.reg["full_history_claim"])

    def test_postseason_champion_not_foreshadowed_as_known(self):
        room2019 = [x for x in self.room["story_room"] if x["season"] == 2019][0]
        self.assertEqual(room2019["championship"]["winner_team_id"], 3)
        self.assertEqual(room2019["championship"]["final_scoring_week"], 16)
        self.assertEqual(room2019["championship"]["winner_points"], 158.3)
        parts = re.split(r"(?m)^## [IVX]+\. ", self.text)
        self.assertEqual(len(parts), 5)
        for passage in parts[1:4]:
            self.assertNotIn("The championship belonged", passage)
        self.assertIn("The championship belonged", parts[4])
        self.assertEqual(self.reg["scenes"][-1]["story_time_cutoff"],
                         "2019 postseason, after Week 16 completion")

    def test_fiction_boundary_and_release_hold(self):
        self.assertIn("NONCANON", self.text)
        self.assertIn("NOT approved Atlas geography", self.text)
        self.assertIn("not independently established", self.text)
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertFalse(self.reg["independent_editorial_acceptance"])
        self.assertFalse(self.reg["independent_umpire_acceptance"])
        self.assertFalse(self.reg["founder_canon_promotion"])
        self.assertFalse(self.reg["canonical_merge"])
        self.assertFalse(self.reg["publication_authorized"])

if __name__ == "__main__":
    unittest.main()
