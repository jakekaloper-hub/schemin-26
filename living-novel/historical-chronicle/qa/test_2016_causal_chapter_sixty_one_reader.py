"""2016 causal Chapter LXI: six-chapter source-exact continuation and fail-closed author/continuity gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCES = (
    ("THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md", "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2", 5178),
    ("THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md", "d2a483e2d6b90e79b9d858525a1e19ae7657648c", 4471),
    ("THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md", "23a33fe476aa980667060bde07561861b4111959", 4564),
    ("THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md", "9eb451c84168e452971d29d82f7e7d9f14972dfc", 5051),
    ("THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md", "46cf50294a7e34afe465a5d738e2d66bea48edbe", 5277),
    ("THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md", "ddccc87b4a7a0a381d567e700adec17f821d57f4", 5665),
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_61_NONCANON.md"
READER_SHA = "bf4b36516beb945c4df419829816b8c1ced297f4"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_60_NONCANON.md"
PREVIOUS_SHA = "0f9f925555f0c98ddf1c4eb7fd11ca3e232c8bb7"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_61_SOURCE_EDITORIAL_QA_RECEIPT.md"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


class ChapterSixtyOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_source_git_blob_pins(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_new_reader_git_blob_pin(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_03_six_source_exact_reader_sections(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
                end = f"<!-- END 2016_CAUSAL {filename} -->"
                self.assertEqual(self.reader.count(start), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(
                    self.reader.split(start, 1)[1].split(end, 1)[0].strip(),
                    (BASE / filename).read_text().strip(),
                )

    def test_04_six_markers_not_misrepresented_monolith(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 6)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 6)

    def test_05_manifest_contains_all_six_correct_pins(self):
        for i, (filename, sha, words) in enumerate(SOURCES, start=56):
            with self.subTest(chapter=i):
                self.assertIn(f"| {i} | {filename} | {sha} | {words} |", self.reader)

    def test_06_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 30468)

    def test_07_reader_scope_is_truthful(self):
        self.assertIn("holds only Chapters LVI, LVII, LVIII, LIX, LX and LXI", self.reader)
        self.assertIn("A monolithic 61-chapter assembled reader is not claimed", self.reader)

    def test_08_previous_continuation_unmodified(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_09_master_fifty_five_unmodified(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_10_new_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5665)

    def test_11_narrative_word_count(self):
        self.assertEqual(len(self.prose.split()), 5093)

    def test_12_six_numbered_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_only_one_named_principal_interior(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)

    def test_14_retired_archivist_names_absent_from_prose(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_15_historical_owner_binding_not_repaired_by_fiction(self):
        self.assertIn("Historical 2016 owner-to-team authentication is absent", self.chapter)
        self.assertIn("61 consecutive Jake-limited chapters", self.qa)

    def test_16_no_league_outcome_invented_in_prose(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_17_seven_missing_state_retained(self):
        self.assertIn("Eight travelers were missing", self.prose)
        self.assertIn("Seven travelers remained unlocated", self.prose)

    def test_18_reed_worker_not_missing_traveler(self):
        self.assertIn("She was not one of the seven travelers", self.prose)
        self.assertIn("the reed worker is neither one of them", self.qa)

    def test_19_pale_movement_gets_limited_evidence_based_answer(self):
        self.assertIn("My drying frame. The river moved it", self.prose)
        self.assertIn("The pale thing we could see from the high stones", self.prose)

    def test_20_rope_not_a_proven_traveler_crossing(self):
        self.assertIn("It was never meant to carry a person", self.prose)
        self.assertIn("The rope is **not** proof of a traveler crossing", self.qa)

    def test_21_merics_conditional_hour_respected(self):
        self.assertIn("One hour", self.prose)
        self.assertIn("The shadow had just touched its foot", self.prose)

    def test_22_labor_not_prepaid(self):
        self.assertIn("We'll settle what the day is worth when I've checked the posts myself", self.prose)
        self.assertIn("Jake did work (counted posts) but **received no coin**", self.qa)

    def test_23_damaged_pole_disclosed_not_concealed(self):
        self.assertIn("It cracked. I should not have done that with your timber", self.prose)
        self.assertIn("The timber is not", self.prose)

    def test_24_esi_tally_remains_owed(self):
        self.assertIn("So the number is unchanged", self.prose)
        self.assertIn("Esi's existing shelter debt remains unchanged", self.qa)

    def test_25_neris_injury_not_reset(self):
        self.assertIn("Neris came from Ina's workroom with her injured arm supported", self.prose)

    def test_26_aven_estrangement_not_erased(self):
        self.assertIn("Aven and Neris unreconciled", self.qa)

    def test_27_hessa_still_away_and_uninformed(self):
        self.assertIn("Hessa has not yet been reached or told of the map", self.chapter)
        self.assertIn("Hessa remains elsewhere and uninformed", self.qa)

    def test_28_six_bowls_after_seventh_broke(self):
        self.assertIn("six unbroken bowls stood on the counter", self.prose)

    def test_29_warning_does_not_found_institution(self):
        self.assertIn("No council, office or new law had been created", self.prose)
        self.assertIn("No new permanent memorial, council, law, rescue service", self.qa)

    def test_30_2016_historical_archive_unchanged(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(archive), ARCHIVE_SHA)

    def test_31_protected_main_hard_canon_unchanged(self):
        for filename, sha in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(ROOT / filename), sha)

    def test_32_author_side_review_does_not_auto_promote(self):
        for marker in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(marker, self.qa)

    def test_33_review_gates_open_not_falsely_green(self):
        for marker in ("independent Authors Council", "Independent", "Umpire", "HOLD"):
            self.assertIn(marker.lower(), self.qa.lower())

    def test_34_missing_characters_stay_beyond_testimony(self):
        self.assertIn("That is not the same as knowing where they went", self.prose)
        self.assertIn("I cannot tell her that the cloth crossed this river", self.prose)

    def test_35_terrain_changes_route_and_map(self):
        self.assertIn("ground gone beneath the stones", self.prose)
        self.assertIn("If someone knows better, let them correct it", self.prose)

    def test_36_no_canonical_visual_or_geo_promotion(self):
        self.assertIn("proposed secondary-world fiction", self.chapter)
        self.assertIn("candidate fiction pending Atlas review", self.qa)


if __name__ == "__main__":
    unittest.main()
