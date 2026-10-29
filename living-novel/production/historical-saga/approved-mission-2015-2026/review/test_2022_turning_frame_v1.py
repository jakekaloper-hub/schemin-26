"""Provenance and chronology negative guards for 2022 NONCANON causal reading.

These checks prove archive consistency, not editorial merit, human owner binding,
Atlas acceptance, Umpire signoff or canonical publication.
"""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
ROOT = HERE.parent / "manuscript" / "2022-turning-frame"
TEXT = ROOT / "THE_FRAME_THEY_COULD_TURN_CAUSAL_READING_V1_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V1.json"
SCORES = REPO / "living-novel/production/full-rewrite-2026/evidence/G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json"
ROOM = REPO / "living-novel/production/full-rewrite-2026/G04_HISTORICAL_SEASON_STORY_ROOM_PACKETS.json"
MATRIX = REPO / "living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md"
LINEAGE = REPO / "living-novel/history/OWNER_LINEAGE.md"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
HEADINGS = [
    "A Place to Hang the Exception",
    "The Painted Side",
    "Twelve Hundredths",
    "What the Frame Held",
]


def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def owner_firewall(reg):
    return reg["primary_pov_ids"] == ["CHAR-JAKE-KALOPER"] and all(
        s["pov_character_id"] == "CHAR-JAKE-KALOPER" and s["pov_class"] == "PRINCIPAL_CHARACTER"
        for s in reg["scenes"]
    )


class Test2022TurningFrameV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT.read_text(encoding="utf-8")
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.sports = json.loads(SCORES.read_text(encoding="utf-8"))
        cls.room = next(x for x in json.loads(ROOM.read_text(encoding="utf-8"))["story_room"] if x["season"] == 2022)
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.text)
        cls.team1 = {
            w: next(m for m in cls.sports["rows"] if m["week"] == w and 1 in (m.get("home_team_id"), m.get("away_team_id")))
            for w in range(1, 18)
        }

    def test_hard_canon_remains_byte_identical_to_main_baseline(self):
        for name, expected in PROTECTED.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob(REPO / "living-novel/manuscript" / name), expected)

    def test_four_substantial_movement_prose(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", self.text)
        self.assertEqual(headings, list(zip(["I", "II", "III", "IV"], HEADINGS)))
        self.assertEqual(len(self.parts), 5)
        self.assertGreaterEqual(len(self.text.split()), 4000)
        self.assertEqual([s["heading"] for s in self.reg["scenes"]], HEADINGS)
        self.assertEqual(self.reg["word_count_including_frontmatter"], len(self.text.split()))
        self.assertEqual(sum(s["passage_words"] for s in self.reg["scenes"]), sum(len(s.split()) for s in self.parts[1:]))

    def test_exclusive_principal_viewpoint_negative_guard(self):
        self.assertTrue(owner_firewall(self.reg))
        changed = json.loads(json.dumps(self.reg))
        changed["scenes"][2]["pov_character_id"] = "EDRIN"
        self.assertFalse(owner_firewall(changed))
        self.assertNotRegex(" ".join(self.parts[1:]), r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertIn("not authenticated by the historical provider", self.text)
        self.assertIn("invented secondary-world staging", self.text)

    def test_historical_extract_scope_and_no_unpaired_win_promotion(self):
        self.assertEqual((self.sports["season"], self.sports["league_id"]), (2022, 1417621))
        self.assertEqual(len(self.sports["rows"]), 105)
        self.assertEqual(self.sports["retrieval_date"], "2026-10-17")
        self.assertEqual(sum(w["pairings"] for w in self.sports["weeks_queried"]), 105)
        self.assertEqual([w["week"] for w in self.sports["weeks_queried"]], list(range(1, 18)))
        red = [r for r in self.sports["rows"] if r.get("home_team_id") == 2 or r.get("away_team_id") == 2]
        regular = [r for r in red if r["week"] <= 14]
        self.assertEqual(len(regular), 14)
        won = sum((r["winner"] == "HOME") if r["home_team_id"] == 2 else (r["winner"] == "AWAY") for r in regular)
        self.assertEqual(won, 13)
        w15 = next(r for r in red if r["week"] == 15)
        self.assertEqual(w15["winner"], "UNDECIDED")
        self.assertIsNone(w15.get("away_team_id"))
        self.assertEqual(self.reg["week15_red_record"]["source_status"], "UNPAIRED_WINNERS_BRACKET_RECORD_NOT_A_CERTIFIED_HEAD_TO_HEAD_VICTORY")

    def test_seventeen_team1_fixtures_have_exact_source_score_pairs(self):
        self.assertEqual(len(self.team1), 17)
        self.assertEqual(sum(len(s["source_score_anchors"]) for s in self.reg["scenes"]), 17)
        for index, scene in enumerate(self.reg["scenes"], 1):
            for anchor in scene["source_score_anchors"]:
                with self.subTest(scene=index, week=anchor["week"]):
                    row = self.team1[anchor["week"]]
                    home = row["home_team_id"] == 1
                    ours = row["home_points"] if home else row["away_points"]
                    theirs = row["away_points"] if home else row["home_points"]
                    opp_id = row["away_team_id"] if home else row["home_team_id"]
                    self.assertEqual(Decimal(str(ours)), Decimal(anchor["team_1_points"]))
                    self.assertEqual(Decimal(str(theirs)), Decimal(anchor["opponent_points"]))
                    self.assertEqual(anchor["opponent_slot"], opp_id)
                    self.assertEqual(anchor["tier"], row["tier"])
                    self.assertEqual(anchor["outcome"], "WIN" if ours > theirs else "LOSS")
                    self.assertIn(anchor["team_1_points"], self.parts[index])
                    self.assertIn(anchor["opponent_points"], self.parts[index])

    def test_six_additional_historical_records_are_real_and_distinct(self):
        self.assertEqual(len(self.reg["additional_verified_event_anchors"]), 6)
        for anchor in self.reg["additional_verified_event_anchors"]:
            with self.subTest(week=anchor["week"], slots=(anchor["home_team_id"], anchor["away_team_id"])):
                matches = [r for r in self.sports["rows"] if r["week"] == anchor["week"]
                           and (r["home_team_id"], r.get("away_team_id")) == (anchor["home_team_id"], anchor["away_team_id"])]
                self.assertEqual(len(matches), 1)
                row = matches[0]
                self.assertEqual(anchor["home_points"], f'{row["home_points"]:.2f}')
                self.assertEqual(anchor["away_points"], f'{row["away_points"]:.2f}')
                self.assertEqual(anchor["winner"], row["winner"])
                self.assertEqual(anchor["tier"], row["tier"])

    def test_week14_twelve_hundredths_and_postseason_promotion_firewall(self):
        week14 = self.team1[14]
        self.assertEqual((week14["home_team_id"], week14["away_team_id"]), (1, 12))
        self.assertEqual(Decimal(str(week14["away_points"])) - Decimal(str(week14["home_points"])), Decimal("0.12"))
        self.assertEqual(self.team1[15]["tier"], "WINNERS_BRACKET")
        self.assertEqual(self.team1[15]["winner"], "AWAY")
        for week in [16, 17]:
            self.assertEqual(self.team1[week]["tier"], "WINNERS_CONSOLATION_LADDER")
        self.assertIn("did not reopen the title bracket", self.parts[4])
        self.assertIn("Twelve hundredths", self.parts[3])

    def test_champion_and_semifinal_separated_by_time(self):
        c = self.room["championship"]
        self.assertEqual(self.reg["championship"], c)
        self.assertEqual((c["winner_team_id"], c["runnerup_team_id"], c["final_scoring_week"]), (9, 10, 17))
        self.assertEqual((Decimal(str(c["winner_points"])), Decimal(str(c["runnerup_points"]))), (Decimal("111.56"), Decimal("78.30")))
        for part in self.parts[1:4]:
            self.assertNotIn("111.56", part)
            self.assertNotIn("78.30", part)
            self.assertNotIn("116.32", part)
            self.assertNotIn("97.96", part)
        for score in ["111.56", "78.30", "116.32", "97.96"]:
            self.assertIn(score, self.parts[4])
        self.assertEqual(self.reg["scenes"][-1]["story_time_cutoff"], "after certification of Week 17 championship")

    def test_every_scoring_period_accounted_with_no_false_full_chronicle_claim(self):
        allweeks = [w for s in self.reg["scenes"] for w in s["foreground_source_weeks"]]
        self.assertEqual(allweeks, list(range(1, 18)))
        self.assertEqual(self.reg["background_unforegrounded_weeks"], [])
        self.assertEqual(self.reg["source_week_record_count"], 105)
        self.assertFalse(self.reg["full_history_claim"])
        self.assertIn("all 105", self.reg["omitted_event_ledger"])

    def test_provenance_sha_and_review_gates(self):
        self.assertEqual(git_blob(TEXT), self.reg["manuscript_git_blob"])
        self.assertEqual(git_blob(SCORES), self.reg["sports_evidence_git_blob"])
        self.assertEqual(git_blob(ROOM), self.reg["championship_source_git_blob"])
        self.assertEqual(git_blob(MATRIX), self.reg["source_authority_matrix_blob"])
        self.assertEqual(git_blob(LINEAGE), self.reg["owner_lineage_git_blob"])
        self.assertEqual(self.reg["historical_venue_status"], "PROPOSED_UNAPPROVED")
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertEqual(self.reg["owner_association"], "USER_ATTESTED_CONNECTED_ACCOUNT_SLOT_1_LITERARY_CANDIDATE_NOT_AUTHENTICATED_HUMAN_OWNER")
        for gate in ("independent_editorial_acceptance", "independent_umpire_acceptance", "founder_canon_promotion", "canonical_merge", "publication_authorized"):
            self.assertFalse(self.reg[gate])

if __name__ == "__main__":
    unittest.main()
