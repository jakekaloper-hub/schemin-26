"""2016 historical causal Chapter LXVI: source-exact 11-part continuation and hard gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCES = [["THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md","410285ab80b12c4ea9f07840b51bbd7ddc79dfb2",5178],["THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md","d2a483e2d6b90e79b9d858525a1e19ae7657648c",4471],["THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md","23a33fe476aa980667060bde07561861b4111959",4564],["THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md","9eb451c84168e452971d29d82f7e7d9f14972dfc",5051],["THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md","46cf50294a7e34afe465a5d738e2d66bea48edbe",5277],["THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md","ddccc87b4a7a0a381d567e700adec17f821d57f4",5665],["THE_FRAME_ABOVE_THE_ASH_CHAPTER_62_NONCANON.md","56e058db1178899d476b9487c99c54364199af2f",5094],["WHERE_THE_RAIN_WENT_CHAPTER_63_NONCANON.md","5406813aa81203ccb75399b33f57c4a3bdb0d355",5679],["THE_HAND_BEHIND_THE_WALL_CHAPTER_64_NONCANON.md","3edb40570163f6d1144c49f77408075ba2482418",5640],["THE_ROAD_WITH_NO_WHEELS_CHAPTER_65_NONCANON.md","7cba39c259874917a6b31ded8ca0bde7d2c07b5e",5098],["WHERE_HESSA_STOOD_CHAPTER_66_NONCANON.md","ce5e0f1274ebcd7e2d2f4056886c608a969f63c2",4817]]
CHAPTER = "WHERE_HESSA_STOOD_CHAPTER_66_NONCANON.md"
CHAPTER_SHA = "ce5e0f1274ebcd7e2d2f4056886c608a969f63c2"
READER = "READING_COPY_CAUSAL_CHAPTERS_56_66_NONCANON.md"
READER_SHA = "8abc9a463f5d0d2eb36b7862af15afce3c435df6"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_65_NONCANON.md"
PREVIOUS_SHA = "e5c128ef7c7a9a2c4348de7846727a099c12ba7f"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
QA = "CHAPTER_66_SOURCE_EDITORIAL_QA_RECEIPT.md"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
}

def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterSixtySix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_11_pinned_sources(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_pinned_new_chapter(self):
        self.assertEqual(blob_sha(BASE / CHAPTER), CHAPTER_SHA)

    def test_03_pinned_reader(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_04_exact_source_wrappers(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                begin = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
                end = f"<!-- END 2016_CAUSAL {filename} -->"
                self.assertEqual(self.reader.count(begin), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(self.reader.split(begin, 1)[1].split(end, 1)[0].strip(), (BASE / filename).read_text().strip())

    def test_05_exact_chapter_count(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 11)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 11)

    def test_06_manifest_pins(self):
        for number, (filename, sha, words) in enumerate(SOURCES, 56):
            self.assertIn(f"| {number} | {filename} | {sha} | {words} |", self.reader)

    def test_07_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 4817)

    def test_08_narrative_words(self):
        self.assertEqual(len(self.prose.split()), 4223)

    def test_09_reader_words(self):
        self.assertEqual(len(self.reader.split()), 56946)

    def test_10_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_11_predecessor_unchanged(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_12_prior_55_unchanged(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_13_2016_archive_unchanged(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(path), ARCHIVE_SHA)

    def test_14_four_protected_hard_canon(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob_sha(ROOT / path), sha)

    def test_15_release_hold(self):
        self.assertIn("DRAFT / NONCANON", self.qa)
        self.assertIn("NO MERGE / CANON PROMOTION / PUBLICATION", self.qa)

    def test_16_only_licensed_proposed_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("66 consecutive Jake-limited historical chapters", self.qa)

    def test_17_retired_principal_narrators_absent(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_18_no_2016_sport_results_created(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_19_hessa_returns_physically(self):
        self.assertIn("Hessa had left the settlement in search of the seven", self.prose)
        self.assertIn("I came back", self.prose)

    def test_20_no_missing_person_discovery(self):
        self.assertIn("No one I could identify", self.prose)
        self.assertIn("seven people had still not been located", self.prose)

    def test_21_ilyens_warning_arrives_to_hessa(self):
        self.assertIn("I didn't receive it", self.prose)
        self.assertIn("Ilyen had stayed to mark the collapsed bank", self.prose)

    def test_22_hessa_decides_against_immediate_march(self):
        self.assertIn("Not tomorrow morning", self.prose)

    def test_23_hessa_declines_uninformed_route(self):
        self.assertIn("I can't check", self.prose)

    def test_24_cart_iron_remains_unrecovered(self):
        self.assertIn("At the buyer's place", self.prose)
        self.assertIn("I don't grant you my part of the wheel", self.prose)

    def test_25_hessa_does_not_grant_retroactive_consent(self):
        self.assertIn("Everyone who owns the cart can speak for themselves", self.prose)

    def test_26_father_owns_blanket_choice(self):
        self.assertIn("I don't want him to come back and find we put all his things away", self.prose)

    def test_27_esi_mat_has_end_date(self):
        self.assertIn("I need it the night after", self.prose)

    def test_28_roof_and_peg_remain_open(self):
        self.assertIn("The roof still leaks", self.prose)
        self.assertIn("Nella's broken-frame pegs not fitted", self.qa)

    def test_29_no_unauthorized_canon_transition(self):
        self.assertIn("NOT independent review", self.chapter)
        self.assertIn("Founder approval", self.qa)

    def test_30_reader_declares_nonmonolith(self):
        self.assertIn("A monolithic 66-chapter assembled reader is not claimed", self.reader)
        self.assertIn("DRAFT / INDEPENDENT EDITORIAL HOLD", self.reader)

if __name__ == "__main__":
    unittest.main()
