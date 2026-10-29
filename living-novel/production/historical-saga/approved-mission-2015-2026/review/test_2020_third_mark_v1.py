"""Fail-closed source, chronology and preservation checks for NONCANON 2020 historical novel.

These tests validate source-to-prose boundaries, not literary acceptance, historical
human ownership, approved Atlas geography, external Umpire review, or publication.
"""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
ROOT = HERE.parent / "manuscript" / "2020-third-mark"
TEXT = ROOT / "THE_THIRD_MARK_CAUSAL_READING_V1_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V1.json"
SCORES = REPO / "living-novel/production/full-rewrite-2026/evidence/G01_2020_FULL_WEEKLY_MATCHUPS.json"
ROOM = REPO / "living-novel/production/full-rewrite-2026/G04_HISTORICAL_SEASON_STORY_ROOM_PACKETS.json"
MATRIX = REPO / "living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md"
SUCCESSION = REPO / "living-novel/history/CHAMPIONSHIP_SUCCESSION.md"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
MOVEMENTS = [
    "Three Clear Panes",
    "The Pane That Would Not Come Out",
    "The Unpaired Square",
    "What the Third Place Measured",
]

def blob_sha(path):
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()

def fmt_points(value):
    return f"{Decimal(str(value)):.2f}"

def register_pov_passes(reg):
    return reg["primary_pov_ids"] == ["CHAR-JAKE-KALOPER"] and all(
        scene["pov_character_id"] == "CHAR-JAKE-KALOPER"
        and scene["pov_class"] == "PRINCIPAL_CHARACTER"
        for scene in reg["scenes"]
    )

class Test2020ThirdMarkV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT.read_text(encoding="utf-8")
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.scores = json.loads(SCORES.read_text(encoding="utf-8"))
        cls.room = next(r for r in json.loads(ROOM.read_text(encoding="utf-8"))["story_room"]
                        if r["season"] == 2020)
        cls.by_week = {}
        for w in cls.scores["weeks"]:
            rows = [m for m in w["matchups"] if 1 in (m.get("home_id"), m.get("away_id"))]
            if rows:
                assert len(rows) == 1
                cls.by_week[w["week"]] = rows[0]
        cls.parts = re.split(r"(?m)^## [IVX]+\. ", cls.text)

    def test_protected_hard_canon_unchanged(self):
        for filename, expected in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(REPO / "living-novel/manuscript" / filename), expected)

    def test_substantial_four_movement_fiction(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", self.text)
        self.assertEqual([t[0] for t in headings], ["I", "II", "III", "IV"])
        self.assertEqual([t[1] for t in headings], MOVEMENTS)
        self.assertGreaterEqual(len(self.text.split("## I. ", 1)[1].split()), 3500)
        self.assertEqual(len(self.reg["scenes"]), 4)
        self.assertEqual([s["heading"] for s in self.reg["scenes"]], MOVEMENTS)

    def test_only_canonical_owner_principal_pov_and_negative(self):
        self.assertTrue(register_pov_passes(self.reg))
        mutated = json.loads(json.dumps(self.reg))
        mutated["scenes"][0]["pov_character_id"] = "EDRIN"
        self.assertFalse(register_pov_passes(mutated))
        self.assertNotRegex(self.text.split("## I. ", 1)[1], r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_score_anchor_sources_and_onpage_representation(self):
        self.assertEqual(self.scores["year"], 2020)
        for scene in self.reg["scenes"]:
            passage = self.parts[int(scene["scene_id"][-2:])]
            for anchor in scene["source_score_anchors"]:
                with self.subTest(scene=scene["scene_id"], week=anchor["week"]):
                    row = self.by_week[anchor["week"]]
                    home = row["home_id"] == 1
                    pts = row["hp"] if home else row["ap"]
                    opp = row.get("ap") if home else row.get("hp")
                    opp_slot = row.get("away_id") if home else row.get("home_id")
                    self.assertEqual(Decimal(str(pts)), Decimal(str(anchor["team_1_points"])))
                    self.assertEqual(anchor["opponent_slot"], opp_slot)
                    self.assertIn(fmt_points(pts), passage)
                    if opp is None:
                        self.assertIsNone(anchor["opponent_points"])
                        self.assertEqual(anchor["outcome"], "UNPAIRED_NO_OPPONENT")
                    else:
                        self.assertEqual(Decimal(str(opp)), Decimal(str(anchor["opponent_points"])))
                        self.assertEqual(anchor["outcome"], "WIN" if pts > opp else "LOSS")
                        self.assertIn(fmt_points(opp), passage)

    def test_fourteen_is_unpaired_not_a_played_win(self):
        row = self.by_week[14]
        self.assertEqual(row["tier"], "WINNERS_BRACKET")
        self.assertIsNone(row.get("away_id"))
        self.assertIsNone(row.get("ap"))
        self.assertEqual(row["winner"], "UNDECIDED")
        self.assertIn("the space for an opponent was blank", self.parts[3])
        self.assertIn("not license Jake to announce a victory", self.parts[3])

    def test_foreground_and_background_coverage_no_full_season_claim(self):
        foreground = [w for s in self.reg["scenes"] for w in s["source_weeks"]]
        background = self.reg["background_unforegrounded_weeks"]
        self.assertEqual(set(foreground) | set(background), set(range(1, 17)))
        self.assertFalse(set(foreground) & set(background))
        self.assertEqual(len(foreground), 13)
        self.assertEqual(background, [8, 11, 12])
        self.assertFalse(self.reg["full_history_claim"])

    def test_championship_temporal_cutoff_and_precise_margin(self):
        final = self.room["championship"]
        self.assertEqual(final["winner_team_id"], 10)
        self.assertEqual(final["runnerup_team_id"], 8)
        self.assertEqual(final["final_scoring_week"], 16)
        self.assertEqual(Decimal(str(final["winner_points"])), Decimal("189.19"))
        self.assertEqual(Decimal(str(final["runnerup_points"])), Decimal("188.44"))
        self.assertEqual(Decimal(str(final["winner_points"])) - Decimal(str(final["runnerup_points"])), Decimal("0.75"))
        self.assertEqual(self.reg["championship"], final)
        self.assertEqual(len(self.parts), 5)
        for p in self.parts[1:4]:
            self.assertNotIn("189.19", p)
            self.assertNotIn("188.44", p)
        self.assertIn("189.19", self.parts[4])
        self.assertIn("188.44", self.parts[4])
        self.assertIn("The Grinch, 12-1", SUCCESSION.read_text(encoding="utf-8"))
        self.assertIn("twelve victories and one defeat", self.parts[3])
        self.assertEqual(self.reg["scenes"][-1]["story_time_cutoff"],
                         "after all 2020 Week 16 outcomes were certified")

    def test_period_result_paths_preserved(self):
        expected = {1:"WIN", 2:"WIN", 3:"WIN", 4:"LOSS", 5:"LOSS", 6:"LOSS",
                    7:"WIN", 9:"LOSS", 10:"LOSS", 13:"WIN", 15:"LOSS", 16:"WIN"}
        actual = {}
        for w in expected:
            r = self.by_week[w]
            h = r["home_id"] == 1
            p = r["hp"] if h else r["ap"]
            q = r["ap"] if h else r["hp"]
            actual[w] = "WIN" if p > q else "LOSS"
        self.assertEqual(actual, expected)
        self.assertEqual(self.room["game_row_count"], 97)
        self.assertEqual(self.reg["scoring_periods_known"], list(range(1, 17)))
        empty = next(w for w in self.scores["weeks"] if w["week"] == 17)
        self.assertEqual(empty["matchups"], [])
        self.assertEqual(self.reg["empty_source_weeks"][0]["week"], 17)

    def test_provenance_and_release_gates(self):
        self.assertEqual(blob_sha(SCORES), self.reg["sports_evidence_git_blob"])
        self.assertEqual(blob_sha(ROOM), self.reg["championship_source_git_blob"])
        self.assertEqual(blob_sha(MATRIX), self.reg["source_authority_matrix_blob"])
        self.assertIn("no authenticated human-owner binding", self.text)
        self.assertIn("invented secondary-world staging", self.text)
        self.assertEqual(self.reg["owner_association"],
                         "USER_ATTESTED_CONNECTED_ACCOUNT_SLOT_1_LITERARY_CANDIDATE_NOT_AUTHENTICATED_HUMAN_OWNER")
        self.assertEqual(self.reg["historical_venue_status"], "PROPOSED_UNAPPROVED")
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        for key in ("independent_editorial_acceptance", "independent_umpire_acceptance",
                    "founder_canon_promotion", "canonical_merge", "publication_authorized"):
            self.assertFalse(self.reg[key])

if __name__ == "__main__":
    unittest.main()
