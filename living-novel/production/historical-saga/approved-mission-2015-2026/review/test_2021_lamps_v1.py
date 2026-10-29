"""Source-bounded negative-guard tests for NONCANON 2021 lamp-network chapter.

These are technical provenance and continuity checks, not an independent author,
Umpire, Atlas approval or endorsement of the invented secondary-world events.
"""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
ROOT = HERE.parent / "manuscript" / "2021-lamps"
TEXT = ROOT / "THE_KEEPER_OF_THE_UNLIT_LAMPS_CAUSAL_READING_V1_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V1.json"
SCORES = REPO / "living-novel/production/full-rewrite-2026/evidence/G01_2021_FULL_WEEKLY_MATCHUPS.json"
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
    "A Lamp Cannot Promise the Road",
    "The Messenger Who Did Not Wait",
    "The Distance of Six Hundredths",
    "The Place Left for Darkness",
]

def git_blob(path):
    contents = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(contents)).encode() + b"\0" + contents).hexdigest()

def valid_owner_only(reg):
    return reg["primary_pov_ids"] == ["CHAR-JAKE-KALOPER"] and all(
        s["pov_character_id"] == "CHAR-JAKE-KALOPER"
        and s["pov_class"] == "PRINCIPAL_CHARACTER"
        for s in reg["scenes"]
    )

class Test2021LampsV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT.read_text(encoding="utf-8")
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.sports = json.loads(SCORES.read_text(encoding="utf-8"))
        cls.room = next(x for x in json.loads(ROOM.read_text(encoding="utf-8"))["story_room"]
                        if x["season"] == 2021)
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.text)
        cls.team1 = {
            w["week"]: next(m for m in w["matchups"] if 1 in (m.get("home_id"), m.get("away_id")))
            for w in cls.sports["weeks"]
        }

    def test_protected_canon_blob_hashes(self):
        for name, sha in PROTECTED.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob(REPO / "living-novel/manuscript" / name), sha)

    def test_substantial_four_movement_narrative(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", self.text)
        self.assertEqual(headings, list(zip(["I", "II", "III", "IV"], HEADINGS)))
        self.assertEqual(len(self.parts), 5)
        self.assertGreaterEqual(sum(len(x.split()) for x in self.parts[1:]), 3500)
        self.assertEqual([s["heading"] for s in self.reg["scenes"]], HEADINGS)

    def test_exclusive_canonical_pov_and_negative_mutation(self):
        self.assertTrue(valid_owner_only(self.reg))
        corrupted = json.loads(json.dumps(self.reg))
        corrupted["scenes"][0]["pov_character_id"] = "EDRIN"
        self.assertFalse(valid_owner_only(corrupted))
        self.assertNotRegex("\n".join(self.parts[1:]), r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_all_registered_scores_against_authoritative_weekly_rows(self):
        self.assertEqual(self.sports["year"], 2021)
        self.assertEqual(len(self.team1), 17)
        self.assertEqual(len(self.reg["scenes"]), 4)
        self.assertEqual(sum(len(s["source_score_anchors"]) for s in self.reg["scenes"]), 15)
        for scene_num, scene in enumerate(self.reg["scenes"], 1):
            for a in scene["source_score_anchors"]:
                with self.subTest(scene=scene_num, week=a["week"]):
                    row = self.team1[a["week"]]
                    is_home = row["home_id"] == 1
                    team_points = row["hp"] if is_home else row["ap"]
                    opponent_points = row["ap"] if is_home else row["hp"]
                    opp_id = row["away_id"] if is_home else row["home_id"]
                    self.assertEqual(Decimal(str(team_points)), Decimal(a["team_1_points"]))
                    self.assertEqual(Decimal(str(opponent_points)), Decimal(a["opponent_points"]))
                    self.assertEqual(opp_id, a["opponent_slot"])
                    self.assertEqual(a["outcome"], "WIN" if team_points > opponent_points else "LOSS")
                    self.assertEqual(a["tier"], row["tier"])
                    self.assertIn(a["team_1_points"], self.parts[scene_num])
                    self.assertIn(a["opponent_points"], self.parts[scene_num])

    def test_proven_2021_arc_and_recovery_not_fake_championship(self):
        wanted = {
            1: "WIN", 2: "WIN", 3: "WIN",
            4: "LOSS", 5: "LOSS", 6: "LOSS", 7: "LOSS",
            8: "WIN", 9: "WIN", 10: "WIN", 11: "WIN", 12: "WIN",
            13: "LOSS", 14: "LOSS", 15: "LOSS", 16: "WIN", 17: "WIN",
        }
        for w, expected in wanted.items():
            row = self.team1[w]
            ours = row["hp"] if row["home_id"] == 1 else row["ap"]
            theirs = row["ap"] if row["home_id"] == 1 else row["hp"]
            self.assertEqual("WIN" if ours > theirs else "LOSS", expected)
        self.assertEqual(self.team1[15]["tier"], "WINNERS_BRACKET")
        self.assertEqual(self.team1[16]["tier"], "WINNERS_CONSOLATION_LADDER")
        self.assertEqual(self.team1[17]["tier"], "WINNERS_CONSOLATION_LADDER")
        self.assertIn("consolation-ladder", self.parts[4])
        self.assertIn("did not reopen the path to the title", self.parts[4])

    def test_six_hundredths_and_no_reversal(self):
        r = self.team1[14]
        self.assertEqual(Decimal(str(r["ap"])) - Decimal(str(r["hp"])), Decimal("0.06"))
        self.assertEqual(r["home_id"], 1)
        self.assertEqual(r["away_id"], 2)
        self.assertIn("145.48", self.parts[3])
        self.assertIn("145.42", self.parts[3])
        self.assertIn("Six hundredths.", self.parts[3])

    def test_champion_source_and_temporal_wall(self):
        final = self.room["championship"]
        self.assertEqual(self.reg["championship"], final)
        self.assertEqual(final["final_scoring_week"], 17)
        self.assertEqual((final["winner_team_id"], final["runnerup_team_id"]), (5, 8))
        self.assertEqual((Decimal(str(final["winner_points"])), Decimal(str(final["runnerup_points"]))),
                         (Decimal("178.06"), Decimal("96.58")))
        for scene in self.parts[1:4]:
            self.assertNotIn("178.06", scene)
            self.assertNotIn("96.58", scene)
        self.assertIn("178.06", self.parts[4])
        self.assertIn("96.58", self.parts[4])
        self.assertEqual(self.reg["scenes"][-1]["story_time_cutoff"], "after certification of Week 17 championship")

    def test_exhaustive_source_period_accounting_not_exhaustive_prose(self):
        foreground = [week for scene in self.reg["scenes"] for week in scene["foreground_source_weeks"]]
        background = self.reg["background_unforegrounded_weeks"]
        self.assertEqual(sorted(foreground + background), list(range(1, 18)))
        self.assertFalse(set(foreground) & set(background))
        self.assertEqual(background, [11, 12])
        self.assertFalse(self.reg["full_history_claim"])

    def test_provenance_and_noncanonical_release_holds(self):
        self.assertEqual(git_blob(TEXT), self.reg["manuscript_git_blob"])
        self.assertEqual(git_blob(SCORES), self.reg["sports_evidence_git_blob"])
        self.assertEqual(git_blob(ROOM), self.reg["championship_source_git_blob"])
        self.assertEqual(git_blob(MATRIX), self.reg["source_authority_matrix_blob"])
        self.assertEqual(git_blob(LINEAGE), self.reg["owner_lineage_git_blob"])
        self.assertIn("not authenticated human-owner binding", self.text)
        self.assertIn("invented secondary-world staging", self.text)
        self.assertEqual(self.reg["historical_venue_status"], "PROPOSED_UNAPPROVED")
        self.assertEqual(self.reg["owner_association"],
                         "USER_ATTESTED_CONNECTED_ACCOUNT_SLOT_1_LITERARY_CANDIDATE_NOT_AUTHENTICATED_HUMAN_OWNER")
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        for key in ("independent_editorial_acceptance", "independent_umpire_acceptance",
                    "founder_canon_promotion", "canonical_merge", "publication_authorized"):
            self.assertFalse(self.reg[key])

if __name__ == "__main__":
    unittest.main()
