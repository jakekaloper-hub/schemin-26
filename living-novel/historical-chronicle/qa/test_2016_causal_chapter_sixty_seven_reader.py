"""Chapter LXVII: exact 2016 source preservation, twelve-chapter reader and dramatic guards."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCES = [
    ("THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md", "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2", 5178),
    ("THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md", "d2a483e2d6b90e79b9d858525a1e19ae7657648c", 4471),
    ("THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md", "23a33fe476aa980667060bde07561861b4111959", 4564),
    ("THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md", "9eb451c84168e452971d29d82f7e7d9f14972dfc", 5051),
    ("THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md", "46cf50294a7e34afe465a5d738e2d66bea48edbe", 5277),
    ("THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md", "ddccc87b4a7a0a381d567e700adec17f821d57f4", 5665),
    ("THE_FRAME_ABOVE_THE_ASH_CHAPTER_62_NONCANON.md", "56e058db1178899d476b9487c99c54364199af2f", 5094),
    ("WHERE_THE_RAIN_WENT_CHAPTER_63_NONCANON.md", "5406813aa81203ccb75399b33f57c4a3bdb0d355", 5679),
    ("THE_HAND_BEHIND_THE_WALL_CHAPTER_64_NONCANON.md", "3edb40570163f6d1144c49f77408075ba2482418", 5640),
    ("THE_ROAD_WITH_NO_WHEELS_CHAPTER_65_NONCANON.md", "7cba39c259874917a6b31ded8ca0bde7d2c07b5e", 5098),
    ("WHERE_HESSA_STOOD_CHAPTER_66_NONCANON.md", "ce5e0f1274ebcd7e2d2f4056886c608a969f63c2", 4817),
    ("THE_ONE_WHO_WALKED_IN_CHAPTER_67_NONCANON.md", "bf20178df8402b14e827b3364dd38618ce675c82", 4767),
]
CHAPTER = SOURCES[-1][0]
CHAPTER_SHA = SOURCES[-1][1]
READER = "READING_COPY_CAUSAL_CHAPTERS_56_67_NONCANON.md"
READER_SHA = "b245e52e66807de2c44ede6aa863728387e18459"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_66_NONCANON.md"
PREVIOUS_SHA = "8abc9a463f5d0d2eb36b7862af15afce3c435df6"
PRIOR_55 = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
PRIOR_55_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
HISTORY_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
QA = "CHAPTER_67_SOURCE_EDITORIAL_QA_RECEIPT.md"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterSixtySeven(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.qa = (BASE / QA).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_prior_chapter_files_pinned(self):
        for filename, sha, _ in SOURCES[:-1]:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_new_chapter_blob(self):
        self.assertEqual(blob_sha(BASE / CHAPTER), CHAPTER_SHA)

    def test_03_new_reader_blob(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_04_wrapped_sources_exact(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                begin = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
                end = f"<!-- END 2016_CAUSAL {filename} -->"
                self.assertEqual(self.reader.count(begin), 1)
                self.assertEqual(self.reader.count(end), 1)
                wrapped = self.reader.split(begin, 1)[1].split(end, 1)[0].strip()
                self.assertEqual(wrapped, (BASE / filename).read_text(encoding="utf-8").strip())

    def test_05_twelve_wrappers_only(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 12)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 12)

    def test_06_manifest_exact(self):
        for chapter_number, (filename, sha, words) in enumerate(SOURCES, 56):
            with self.subTest(chapter=chapter_number):
                self.assertIn(f"| {chapter_number} | {filename} | {sha} | {words} |", self.reader)

    def test_07_manuscript_whitespace_words(self):
        self.assertEqual(len(self.chapter.split()), 4767)

    def test_08_prose_whitespace_words(self):
        self.assertEqual(len(self.prose.split()), 4336)

    def test_09_reader_whitespace_words(self):
        self.assertEqual(len(self.reader.split()), 61763)

    def test_10_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)

    def test_11_old_continuation_retained(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_12_fifty_five_prior_source_retained(self):
        self.assertEqual(blob_sha(BASE / PRIOR_55), PRIOR_55_SHA)

    def test_13_historical_2016_fixture_digest_retained(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(p), HISTORY_SHA)

    def test_14_hard_canon_four_sources_retained(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob_sha(ROOT / path), sha)

    def test_15_noncanon_and_release_hold(self):
        self.assertIn("DRAFT / NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("NO MERGE / CANON PROMOTION / PUBLICATION", self.qa)

    def test_16_exclusive_proposed_principal_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("67 consecutive Jake-limited historical chapters", self.qa)

    def test_17_no_retired_narrators(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_18_no_conflated_sports_events(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_19_new_survivor_arrival(self):
        self.assertIn("The stranger put a hand against the post", self.prose)

    def test_20_ilyens_identification_by_action(self):
        self.assertIn("You always ask for the spoon like that", self.prose)

    def test_21_seven_to_six_explicit_in_narrative(self):
        self.assertIn("one of the seven had walked back", self.prose)
        self.assertIn("six people still unlocated", self.prose)

    def test_22_no_unearned_missing_person_death_verdict(self):
        self.assertIn("I didn't see him die", self.prose)
        self.assertIn("I cannot", self.prose)

    def test_23_hessa_no_retrospective_rescue_credit(self):
        self.assertIn("I came back yesterday without finding him. Both things are true", self.prose)

    def test_24_new_witness_refuses_unverified_route(self):
        self.assertIn("I can't show them from here", self.prose)
        self.assertIn("I can't lead you on a road I couldn't find twice", self.prose)

    def test_25_father_keeps_separate_blanket_ownership(self):
        self.assertIn("It belonged to someone absent", self.prose)
        self.assertIn("One more night", self.prose)

    def test_26_esi_roof_only_spot_tested(self):
        self.assertIn("Still leaking", self.prose)
        self.assertIn("look again after the next rain", self.prose)

    def test_27_cart_not_miraculously_repaired(self):
        self.assertIn("cart's bare axle", self.prose)
        self.assertIn("collar was still at the buyer's place", self.prose)

    def test_28_remaining_social_debt_and_water(self):
        self.assertIn("Fara's marked trough remained untrusted", self.prose)
        self.assertIn("Meric measured a piece of timber", self.prose)

    def test_29_reader_not_full_monolithic_novel(self):
        self.assertIn("A monolithic 67-chapter assembled reader is not claimed", self.reader)
        self.assertIn("DRAFT / INDEPENDENT EDITORIAL HOLD", self.reader)

    def test_30_governance_challenges_explicit(self):
        for phrase in ["Authors Council", "Atlas", "Umpire", "historical", "67 consecutive"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.qa)

if __name__ == "__main__":
    unittest.main()
