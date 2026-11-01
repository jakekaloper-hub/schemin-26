"""2016 causal Chapter LX: five-chapter exact continuation and noncanon/continuity gates."""
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
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_60_NONCANON.md"
READER_SHA = "0f9f925555f0c98ddf1c4eb7fd11ca3e232c8bb7"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_59_NONCANON.md"
PREVIOUS_SHA = "9bc9196f5349999c7a2b14b8c4b586ffc5129c48"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_60_SOURCE_EDITORIAL_QA_RECEIPT.md"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\x00" + raw).hexdigest()

class ChapterSixty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\\n---\\n", 1)[0]

    def test_01_five_source_git_blob_pins(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_reader_blob_pin(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_03_every_section_source_exact(self):
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

    def test_04_five_markers_not_a_monolith(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 5)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 5)

    def test_05_manifest_per_chapter_sha_words(self):
        for i, (name, sha, words) in enumerate(SOURCES, 56):
            self.assertIn(f"| {i} | {name} | {sha} | {words} |", self.reader)

    def test_06_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 24771)

    def test_07_reader_scope_no_false_60_chapter_claim(self):
        self.assertIn("holds only Chapters LVI, LVII, LVIII, LIX and LX", self.reader)
        self.assertIn("A monolithic 60-chapter assembled reader is not claimed", self.reader)

    def test_08_previous_continuation_preserved(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_09_fifty_five_reader_preserved(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_10_new_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5277)

    def test_11_narrative_word_count(self):
        self.assertEqual(len(self.prose.split()), 4684)

    def test_12_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_owner_identity_and_solo_pov(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)

    def test_14_no_archivist_pov(self):
        self.assertNotRegex(self.prose, r"\\b(?:Edrin|Edin|Oren)\\b")

    def test_15_period_owner_binding_unverified(self):
        self.assertIn("Historical 2016 owner-to-team authentication is absent", self.chapter)
        self.assertIn("60 consecutive Jake-limited chapters", self.qa)

    def test_16_no_fantasy_outcome_or_matchup_dressing(self):
        self.assertNotRegex(self.prose, r"\\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\\b")

    def test_17_previous_eight_now_seven(self):
        self.assertIn("Eight travelers had been missing", self.prose)
        self.assertIn("Seven travelers remained unlocated", self.prose)

    def test_18_no_new_missing_person_discovery(self):
        self.assertIn("NONE is attributed to a missing person", self.chapter)
        self.assertIn("Seven unlocated at entry", self.qa)

    def test_19_six_intact_bowls_from_prior_chapter(self):
        self.assertIn("Fara had six unbroken bowls", self.prose)
        self.assertIn("The broken one was not among them", self.prose)

    def test_20_cloth_identification_is_limited(self):
        self.assertIn("I'm certain I remember sewing a repair", self.prose)
        self.assertIn("I'm not certain where the cloth has been since", self.prose)

    def test_21_post_fire_marks_not_missing_person_proof(self):
        self.assertIn("Someone walked here after the fire", self.prose)
        self.assertIn("The two things need not belong to the same journey", self.prose)

    def test_22_far_shore_motion_not_assigned(self):
        self.assertIn('"I saw something move"', self.prose)
        self.assertIn("There was no reply", self.prose)

    def test_23_ilyen_chooses_route_and_companion(self):
        self.assertIn("At first light, then", self.prose)
        self.assertIn("If Meric allows the hour", self.prose)

    def test_24_tovin_knows_stones_no_cart_claim(self):
        self.assertIn("Tovin knows the stones", self.prose)
        self.assertIn("The cart stays blocked", self.prose)

    def test_25_injuries_unchanged(self):
        self.assertIn("Neris's injured arm", self.prose)
        self.assertIn("Dovan sat on a low bench, his injured leg", self.prose)

    def test_26_hessa_absent_and_uninformed(self):
        self.assertIn("Hessa was away on a search", self.prose)
        self.assertIn("Hessa remains away and uninformed", self.qa)

    def test_27_aven_not_reconciled_or_given_exclusive_role(self):
        self.assertIn("Aven who had come back alone", self.prose)
        self.assertIn("Aven–Neris unreconciled", self.qa)

    def test_28_iron_collar_still_with_buyer(self):
        self.assertIn("its iron collar still held by the buyer", self.prose)
        self.assertIn("The six-owner cart stays immobilized", self.qa)

    def test_29_no_earned_coin_invented_at_esi(self):
        self.assertIn("Esi met him with the tally board", self.prose)
        self.assertIn("He had no coin to put beside it", self.prose)
        self.assertIn("initial Chapter LX draft incorrectly invented", self.qa)

    def test_30_prior_pell_restitution_not_reversed(self):
        self.assertIn("returning four false-witness coins to Pell", self.prose)
        self.assertIn("ZERO", self.qa)

    def test_31_protected_hard_canon_blob_pins(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob_sha(ROOT / name), sha)

    def test_32_historical_2016_archive_unchanged(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(archive), ARCHIVE_SHA)

    def test_33_author_self_review_cannot_promote(self):
        for tag in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(tag, self.qa)

    def test_34_editorial_risks_dont_claim_independent_approval(self):
        self.assertIn("Repetition:", self.qa)
        self.assertIn("Terrain logic:", self.qa)
        self.assertIn("Owner POV imbalance:", self.qa)
        self.assertIn("independent acceptance NOT received", self.qa)

    def test_35_no_historical_owner_motive_asserted_as_fact(self):
        self.assertIn("not historical ESPN/Flaim data", self.chapter)
        self.assertIn("no historical scoring event is foregrounded".lower(), self.qa.lower())

if __name__ == "__main__":
    unittest.main()
