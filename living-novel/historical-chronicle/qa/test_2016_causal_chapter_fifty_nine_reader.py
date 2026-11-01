"""Chapter LIX: source-exact four-chapter reader, bowl arithmetic and canon/firewall regression."""
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
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_59_NONCANON.md"
READER_SHA = "9bc9196f5349999c7a2b14b8c4b586ffc5129c48"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_58_NONCANON.md"
PREVIOUS_SHA = "b524a6e690f153503bf114e5d9818dd4da6755aa"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_59_SOURCE_EDITORIAL_QA_RECEIPT.md"
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

class ChapterFiftyNine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_four_source_blob_pins(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(file=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_new_reader_blob_pin(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_03_all_four_source_sections_exact(self):
        for name, sha, _ in SOURCES:
            with self.subTest(file=name):
                beginning = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
                ending = f"<!-- END 2016_CAUSAL {name} -->"
                self.assertEqual(self.reader.count(beginning), 1)
                self.assertEqual(self.reader.count(ending), 1)
                self.assertEqual(
                    self.reader.split(beginning, 1)[1].split(ending, 1)[0].strip(),
                    (BASE / name).read_text().strip(),
                )

    def test_04_exactly_four_source_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 4)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 4)

    def test_05_manifest_source_sha_and_words(self):
        for i, (name, sha, words) in enumerate(SOURCES, 56):
            with self.subTest(chapter=i):
                self.assertIn(f"| {i} | {name} | {sha} | {words} |", self.reader)

    def test_06_reader_total_whitespace_words(self):
        self.assertEqual(len(self.reader.split()), 19480)

    def test_07_reader_scope_not_false_monolith(self):
        self.assertIn("holds only Chapters LVI, LVII, LVIII and LIX", self.reader)
        self.assertIn("A monolithic 59-chapter assembled reader is not claimed", self.reader)

    def test_08_preserve_original_fifty_five_reader(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_09_preserve_previous_three_chapter_reader(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_10_new_chapter_substantial(self):
        self.assertEqual(len(self.chapter.split()), 5051)

    def test_11_narrative_prose_substantial(self):
        self.assertGreaterEqual(len(self.prose.split()), 4400)

    def test_12_six_literary_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_only_registered_jake_viewpoint(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_14_owner_binding_unverified(self):
        self.assertIn("2016 owner/team binding remains unverified", self.chapter)
        self.assertIn("59 consecutive Jake-limited historical chapters", self.qa)

    def test_15_no_fantasy_scoring_in_prose(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_16_seven_unlocated_eight_before_aven(self):
        self.assertIn("Eight travelers had been missing before Aven returned", self.prose)
        self.assertIn("Seven travelers remained unlocated", self.prose)

    def test_17_hessa_still_away_and_ilyen_local(self):
        self.assertIn("Hessa had gone away separately", self.prose)
        self.assertIn("Ilyen remains local", self.qa)

    def test_18_seven_bowls_initially(self):
        self.assertIn("Fara had turned seven bowls upside down", self.prose)
        self.assertIn("The seven vessels had become six", self.prose)

    def test_19_bowl_break_not_replaced(self):
        self.assertIn("The bowl broke in two large pieces", self.prose)
        self.assertIn("No one fetched another", self.prose)

    def test_20_five_basket_sixth_borrowed(self):
        self.assertIn("Five bowls went into Fara's basket", self.prose)
        self.assertIn("a sixth had been carried off to hold water", self.prose)

    def test_21_six_intact_after_return_not_seven(self):
        self.assertIn("there were six shapes along the counter again", self.prose)
        self.assertIn("Fara had not fetched a seventh", self.prose)
        self.assertIn("Seven bowls appear at the shop", self.qa)

    def test_22_no_missing_death_falsely_asserted(self):
        self.assertIn("We don't know", self.prose)
        self.assertIn("no death, discovery, forgiveness", self.qa)

    def test_23_nella_does_not_perform_another_claim(self):
        self.assertIn('"Not tonight."', self.prose)
        self.assertIn("must not be mistaken for absolution", self.qa)

    def test_24_no_new_official_commemoration(self):
        self.assertIn("nor had any official announced a ceremony", self.prose)
        self.assertIn("no public institution or lasting memorial", self.qa)

    def test_25_aven_neris_unreconciled(self):
        self.assertIn("without a public reconciliation", self.prose)
        self.assertIn("Aven remains unreconciled", self.qa)

    def test_26_cart_six_owners_buyer_collateral_unchanged(self):
        self.assertIn("Six travelers still owned the cart", self.prose)
        self.assertIn("buyer still held the collar", self.prose)
        self.assertIn("cart disabled", self.qa)

    def test_27_restitution_not_forgiveness(self):
        self.assertIn("four false-witness coins Jake had returned", self.prose)
        self.assertIn("Jake has zero remaining false-witness coins", self.qa)

    def test_28_fire_and_injuries_persist(self):
        self.assertIn("The meadow had burned recently", self.prose)
        self.assertIn("Neris/Dovan injuries remain", self.qa)

    def test_29_independent_gates_still_unmet(self):
        for word in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(word=word):
                self.assertIn(word, self.qa)

    def test_30_protected_hard_canon_unmodified(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob_sha(ROOT / name), sha)

    def test_31_historical_archive_unchanged(self):
        file = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(file), ARCHIVE_SHA)

    def test_32_source_evidence_separate_from_fiction(self):
        self.assertIn("not authenticated 2016 ESPN/Flaim events", self.chapter)
        self.assertIn("no verified ESPN scores", self.qa)
        self.assertIn("No new approved geography", self.qa) if "No new approved geography" in self.qa else self.assertIn("unapproved Atlas proposal", self.qa)

if __name__ == "__main__":
    unittest.main()
