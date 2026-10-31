"""Source and negative-guard tests for a 2023 NONCANON causal reading.

GitHub CI PASS is technical evidence only, not owner identity, Atlas validation,
independent author/umpire review, Founder canon approval or publication.
"""
import hashlib
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
ROOT = HERE.parent / "manuscript" / "2023-fourth-address"
TEXT = ROOT / "THE_FOURTH_ADDRESS_CAUSAL_READING_V1_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V1.json"
SCORES = REPO / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
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
    "The Name on the Outside",
    "The Keeper of Seven Days",
    "The Person Who Was There",
    "The Other Kind of Victory",
]
RANGES = [(1, 4), (5, 7), (8, 14), (15, 17)]


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def safe_principal_pov(reg):
    return (reg["primary_pov_ids"] == ["CHAR-JAKE-KALOPER"]
            and all(s["pov_character_id"] == "CHAR-JAKE-KALOPER"
                    and s["pov_class"] == "PRINCIPAL_CHARACTER" for s in reg["scenes"]))


def anchor_matches(row, anchor):
    mine_home = row["home_id"] == 1
    mine = row["hp"] if mine_home else row["ap"]
    other = row["ap"] if mine_home else row["hp"]
    return (
        Decimal(str(mine)) == Decimal(anchor["team_1_points"])
        and Decimal(str(other)) == Decimal(anchor["opponent_points"])
        and anchor["opponent_slot"] == (row["away_id"] if mine_home else row["home_id"])
        and anchor["tier"] == row["tier"]
        and anchor["team1_home"] is mine_home
        and anchor["outcome"] == ("WIN" if mine > other else "LOSS" if mine < other else "TIE")
    )


class Test2023FourthAddressV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT.read_text(encoding="utf-8")
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.archive = json.loads(SCORES.read_text(encoding="utf-8"))
        cls.room = next(x for x in json.loads(ROOM.read_text(encoding="utf-8"))["story_room"] if x["season"] == 2023)
        cls.parts = re.split(r"(?m)^## [IVX]+\. [^\n]+\n", cls.text)
        cls.rows = [
            dict(row, week=week["week"])
            for week in cls.archive["weeks"]
            for row in week["matchups"]
        ]
        cls.team1 = {
            w: next(r for r in cls.rows if r["week"] == w and 1 in (r.get("home_id"), r.get("away_id")))
            for w in range(1, 18)
        }

    def test_protected_main_canon_blob_integrity(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(REPO / "living-novel/manuscript" / path), sha)

    def test_complete_four_movement_chapter_not_outline(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. ([^\n]+)$", self.text)
        self.assertEqual(headings, list(zip(["I", "II", "III", "IV"], HEADINGS)))
        self.assertEqual(len(self.parts), 5)
        self.assertGreaterEqual(len(self.text.split()), 4500)
        self.assertEqual(self.reg["word_count_including_frontmatter"], len(self.text.split()))
        self.assertEqual([s["heading"] for s in self.reg["scenes"]], HEADINGS)
        for index, scene in enumerate(self.reg["scenes"], 1):
            self.assertEqual(scene["passage_words"], len(self.parts[index].split()))
            self.assertGreaterEqual(scene["passage_words"], 850)

    def test_only_canonical_owner_principal_and_corruption_guard(self):
        self.assertTrue(safe_principal_pov(self.reg))
        altered = json.loads(json.dumps(self.reg))
        altered["scenes"][1]["pov_character_id"] = "EDRIN"
        self.assertFalse(safe_principal_pov(altered))
        self.assertNotRegex(" ".join(self.parts[1:]), r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertIn("**not** by authenticated historical human-owner identification", self.text)
        self.assertIn("invented secondary-world material", self.text)

    def test_2023_archive_has_exact_week_count_and_unpaired_status(self):
        self.assertEqual(self.archive["year"], 2023)
        self.assertEqual(self.archive["source"], "Flaim ESPN 1417621")
        self.assertEqual([w["week"] for w in self.archive["weeks"]], list(range(1, 18)))
        self.assertEqual([len(w["matchups"]) for w in self.archive["weeks"]], [6]*14 + [7]*3)
        self.assertEqual(len(self.rows), 105)
        unpaired = [r for r in self.rows if r["week"] >= 15 and r["winner"] == "UNDECIDED"]
        self.assertGreaterEqual(len(unpaired), 1)
        self.assertTrue(all(r.get("away_id") is None for r in unpaired))
        self.assertEqual(self.reg["source_week_record_count"], 105)

    def test_seventeen_team1_score_pairs_tier_and_story_presence(self):
        self.assertEqual(sum(len(x["source_score_anchors"]) for x in self.reg["scenes"]), 17)
        for i, scene in enumerate(self.reg["scenes"], 1):
            lo, hi = RANGES[i-1]
            self.assertEqual(scene["foreground_source_weeks"], list(range(lo, hi+1)))
            self.assertEqual(scene["story_time_cutoff"].split("Week ")[1].split()[0], str(hi))
            for anchor in scene["source_score_anchors"]:
                with self.subTest(week=anchor["week"]):
                    row = self.team1[anchor["week"]]
                    self.assertTrue(anchor_matches(row, anchor))
                    self.assertIn(anchor["team_1_points"], self.parts[i])
                    self.assertIn(anchor["opponent_points"], self.parts[i])

    def test_negative_corruption_of_score_is_detected(self):
        anchor = dict(self.reg["scenes"][2]["source_score_anchors"][-2])
        self.assertTrue(anchor_matches(self.team1[13], anchor))
        anchor["team_1_points"] = "144.77"
        self.assertFalse(anchor_matches(self.team1[13], anchor))

    def test_early_defeat_rebound_and_one_point_four_hundredths(self):
        outcomes = [("WIN" if (r["hp"] if r["home_id"] == 1 else r["ap"])
                     > (r["ap"] if r["home_id"] == 1 else r["hp"]) else "LOSS")
                    for r in (self.team1[w] for w in range(1, 15))]
        self.assertEqual(outcomes[:4], ["LOSS"]*4)
        self.assertEqual(outcomes[4:7], ["WIN"]*3)
        self.assertEqual(Decimal("184.75") - Decimal("183.46"), Decimal("1.29"))
        self.assertEqual(Decimal("144.76") - Decimal("143.72"), Decimal("1.04"))
        self.assertIn("1.29", self.parts[1])
        self.assertIn("1.04", self.parts[3])

    def test_consolation_not_mislabeled_as_title(self):
        for week in (15, 16, 17):
            self.assertEqual(self.team1[week]["tier"], "LOSERS_CONSOLATION_LADDER")
        self.assertEqual([self.team1[w]["winner"] for w in (15,16,17)], ["HOME", "HOME", "HOME"])
        # Week 16's HOME result belongs to the opponent, not to Jake.
        self.assertEqual([self.reg["scenes"][-1]["source_score_anchors"][i]["outcome"] for i in range(3)], ["WIN", "LOSS", "WIN"])
        self.assertIn("could not return Jake to the title bracket", self.parts[4])
        self.assertIn("Eggs Benedict defeated Arm Chair GM", self.parts[4])

    def test_championship_is_late_and_separate(self):
        c = self.room["championship"]
        self.assertEqual(self.reg["championship"], c)
        self.assertEqual((c["winner_team_id"], c["runnerup_team_id"], c["final_scoring_week"]), (12, 11, 17))
        self.assertEqual((Decimal(str(c["winner_points"])), Decimal(str(c["runnerup_points"]))), (Decimal("192.88"), Decimal("140.76")))
        for prefinal in self.parts[1:4]:
            self.assertNotIn("192.88", prefinal)
            self.assertNotIn("140.76", prefinal)
        self.assertIn("192.88", self.parts[4])
        self.assertIn("140.76", self.parts[4])

    def test_six_other_fixture_anchors_really_exist(self):
        self.assertEqual(len(self.reg["additional_verified_event_anchors"]), 6)
        for a in self.reg["additional_verified_event_anchors"]:
            with self.subTest(week=a["week"]):
                matched = [r for r in self.rows if r["week"] == a["week"]
                           and r["home_id"] == a["home_team_id"] and r.get("away_id") == a["away_team_id"]]
                self.assertEqual(len(matched), 1)
                r = matched[0]
                self.assertEqual((a["home_points"], a["away_points"]), (f'{r["hp"]:.2f}', f'{r["ap"]:.2f}'))
                self.assertEqual((a["winner"], a["tier"]), (r["winner"], r["tier"]))

    def test_four_distinct_benedict_names_do_not_mean_same_owner(self):
        yearnames = {name.strip() for r in self.rows for name in (r.get("home"),r.get("away")) if name}
        self.assertTrue({"Benedict Kenobi", "Benedict Arnold", "Benedict Coomhersnatch", "Eggs Benedict"} <= yearnames)
        self.assertIn("historical human-owner", self.text)
        self.assertEqual(self.reg["other_historical_team_owner_binding"], "UNKNOWN_DO_NOT_PROJECT_2026_OWNER_IDS")
        self.assertFalse(self.reg["full_history_claim"])

    def test_all_weeks_source_hashes_and_release_hold(self):
        self.assertEqual(self.reg["source_week_coverage"], list(range(1,18)))
        self.assertEqual(self.reg["foreground_source_weeks"], list(range(1,18)))
        self.assertEqual(self.reg["background_unforegrounded_weeks"], [])
        self.assertEqual(git_blob(TEXT), self.reg["manuscript_git_blob"])
        self.assertEqual(git_blob(SCORES), self.reg["sports_evidence_git_blob"])
        self.assertEqual(git_blob(ROOM), self.reg["championship_source_git_blob"])
        self.assertEqual(git_blob(MATRIX), self.reg["source_authority_matrix_blob"])
        self.assertEqual(git_blob(LINEAGE), self.reg["owner_lineage_git_blob"])
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertEqual(self.reg["historical_venue_status"], "PROPOSED_UNAPPROVED")
        for gate in ("independent_editorial_acceptance", "independent_umpire_acceptance",
                     "founder_canon_promotion", "canonical_merge", "publication_authorized"):
            self.assertFalse(self.reg[gate])


if __name__ == "__main__":
    unittest.main()
