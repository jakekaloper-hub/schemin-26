"""2016 historical causal Chapter LXV: ten source-exact chapters, agency and release gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCES = [["THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md","410285ab80b12c4ea9f07840b51bbd7ddc79dfb2",5178],["THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md","d2a483e2d6b90e79b9d858525a1e19ae7657648c",4471],["THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md","23a33fe476aa980667060bde07561861b4111959",4564],["THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md","9eb451c84168e452971d29d82f7e7d9f14972dfc",5051],["THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md","46cf50294a7e34afe465a5d738e2d66bea48edbe",5277],["THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md","ddccc87b4a7a0a381d567e700adec17f821d57f4",5665],["THE_FRAME_ABOVE_THE_ASH_CHAPTER_62_NONCANON.md","56e058db1178899d476b9487c99c54364199af2f",5094],["WHERE_THE_RAIN_WENT_CHAPTER_63_NONCANON.md","5406813aa81203ccb75399b33f57c4a3bdb0d355",5679],["THE_HAND_BEHIND_THE_WALL_CHAPTER_64_NONCANON.md","3edb40570163f6d1144c49f77408075ba2482418",5640],["THE_ROAD_WITH_NO_WHEELS_CHAPTER_65_NONCANON.md","7cba39c259874917a6b31ded8ca0bde7d2c07b5e",5098]]
CHAPTER = "THE_ROAD_WITH_NO_WHEELS_CHAPTER_65_NONCANON.md"
CHAPTER_SHA = "7cba39c259874917a6b31ded8ca0bde7d2c07b5e"
READER = "READING_COPY_CAUSAL_CHAPTERS_56_65_NONCANON.md"
READER_SHA = "e5c128ef7c7a9a2c4348de7846727a099c12ba7f"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_64_NONCANON.md"
PREVIOUS_SHA = "35876dc97fac32ca33984ead06f618dedc5cbedf"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
QA = "CHAPTER_65_SOURCE_EDITORIAL_QA_RECEIPT.md"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterSixtyFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_pinned_ten_chapter_blobs(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)
    def test_02_pinned_new_chapter_blob(self):
        self.assertEqual(blob_sha(BASE / CHAPTER), CHAPTER_SHA)
    def test_03_pinned_reader_blob(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)
    def test_04_ten_exact_source_wrappers(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
                end = f"<!-- END 2016_CAUSAL {filename} -->"
                self.assertEqual(self.reader.count(start), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(self.reader.split(start, 1)[1].split(end, 1)[0].strip(), (BASE / filename).read_text().strip())
    def test_05_ten_delimiter_pairs(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 10)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 10)
    def test_06_source_manifest_rows(self):
        for number, (filename, sha, words) in enumerate(SOURCES, 56):
            self.assertIn(f"| {number} | {filename} | {sha} | {words} |", self.reader)
    def test_07_word_count_chapter(self):
        self.assertEqual(len(self.chapter.split()), 5098)
    def test_08_word_count_narrative(self):
        self.assertEqual(len(self.prose.split()), 4766)
    def test_09_word_count_reader(self):
        self.assertEqual(len(self.reader.split()), 52100)
    def test_10_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)
    def test_11_prior_reader_untouched(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)
    def test_12_first_fifty_five_untouched(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)
    def test_13_archival_evidence_untouched(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(p), ARCHIVE_SHA)
    def test_14_four_protected_canon_blobs_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob_sha(ROOT / path), sha)
    def test_15_released_canon_gate_held(self):
        self.assertIn("DRAFT / NONCANON", self.qa)
        self.assertIn("NO MERGE / CANON PROMOTION / PUBLICATION", self.qa)
    def test_16_exclusive_proposed_jake_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("65 consecutive Jake-limited historical chapters", self.qa)
    def test_17_no_retired_narrators(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")
    def test_18_no_unverified_real_league_outcomes(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|quarterback|touchdown|Week [0-9]+)\b")
    def test_19_dovan_controls_departure(self):
        self.assertIn("I want to walk as far as Fara's place", self.prose)
    def test_20_dovan_refuses_unrequested_assistance(self):
        self.assertIn("Don't tell me what my leg has decided", self.prose)
    def test_21_dovan_support_not_rushed(self):
        self.assertIn("I'll ask", self.prose)
    def test_22_barrows_concrete_physical_constraint(self):
        self.assertIn("The near basket will lift off", self.prose)
    def test_23_basket_removed_with_consent(self):
        self.assertIn("waited for his nod", self.prose)
    def test_24_fara_shop_requires_no_geographical_fiction_as_fact(self):
        self.assertIn("Fara was sorting dry containers", self.prose)
    def test_25_trough_not_falsely_cleared(self):
        self.assertIn("The trough outside remained withheld", self.prose)
    def test_26_ilyens_warning_partly_misrepeated_and_corrected(self):
        self.assertIn("He repeated its substance without taking the paper, leaving out the part about the far willow", self.prose)
    def test_27_no_unsupported_hessa_contact(self):
        self.assertIn("neither Dovan nor Ilyen pretended that saying them in Meric's yard delivered a warning beyond it", self.prose)
    def test_28_voluntary_request_for_arm(self):
        self.assertIn("May I have your arm as far as the next wall", self.prose)
    def test_29_return_not_complete_recovery(self):
        self.assertIn("Longer coming back", self.prose)
    def test_30_dovan_sets_rest_choice(self):
        self.assertIn("I mean to sit here and do nothing", self.prose)
    def test_31_cart_unresolved_not_repaired(self):
        self.assertIn("The six owners had not agreed to leave it", self.prose)
    def test_32_hessa_has_independent_consent(self):
        self.assertIn("She has her own", self.prose)
    def test_33_peg_repair_work_remains_real(self):
        self.assertIn("You've learned something", self.prose)
        self.assertIn("He gave Jake another piece of wood", self.prose)
    def test_34_noncannon_open_loops_recorded(self):
        self.assertIn("Seven fictional travelers still missing", self.qa)
        self.assertIn("six-owner cart still disabled", self.qa)
    def test_35_no_external_or_umpire_acceptance_invented(self):
        self.assertIn("This is author-side self-challenge only", self.qa)
        self.assertIn("No actual independent Authors Council", self.qa)
    def test_36_explicit_non_monolith(self):
        self.assertIn("A monolithic 65-chapter assembled reader is not claimed", self.reader)
        self.assertIn("DRAFT / INDEPENDENT EDITORIAL HOLD", self.reader)

if __name__ == "__main__":
    unittest.main()
