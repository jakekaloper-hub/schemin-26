"""Chapter LVIII: source-exact continuation, causal consequences, evidence boundary, and protected canon."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
FIRST = "THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md"
SECOND = "THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md"
THIRD = "THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_56_58_NONCANON.md"
QA = "CHAPTER_58_SOURCE_EDITORIAL_QA_RECEIPT.md"
SOURCES = (
    (FIRST, "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2", 5178),
    (SECOND, "d2a483e2d6b90e79b9d858525a1e19ae7657648c", 4471),
    (THIRD, "23a33fe476aa980667060bde07561861b4111959", 4564),
)
READER_SHA = "b524a6e690f153503bf114e5d9818dd4da6755aa"
PRIOR_55_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
PRIOR_56_57_SHA = "e1887ccd99841b50741689f2f6d7b67160571794"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterFiftyEight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / THIRD).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_all_three_sources_are_pinned(self):
        for name, sha, _ in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_02_reader_pinned(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_03_source_exact_assembly(self):
        for name, sha, _ in SOURCES:
            with self.subTest(name=name):
                begin = "<!-- BEGIN 2016_CAUSAL " + name + " | git_blob " + sha + " -->"
                end = "<!-- END 2016_CAUSAL " + name + " -->"
                self.assertEqual(self.reader.count(begin), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(
                    self.reader.split(begin, 1)[1].split(end, 1)[0].strip(),
                    (BASE / name).read_text().strip(),
                )

    def test_04_exact_three_reader_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 3)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 3)

    def test_05_manifest_words_and_hashes(self):
        for i, (name, sha, words) in enumerate(SOURCES, 56):
            with self.subTest(chapter=i):
                self.assertIn(f"| {i} | {name} | {sha} | {words} |", self.reader)

    def test_06_reader_total_words(self):
        self.assertEqual(len(self.reader.split()), 14397)

    def test_07_reader_scope_not_misrepresented(self):
        self.assertIn("holds only Chapters LVI, LVII and LVIII", self.reader)
        self.assertIn("monolithic 58-chapter assembled reader is not claimed", self.reader)

    def test_08_old_fifty_five_reader_unchanged(self):
        self.assertEqual(git_blob(BASE / "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"), PRIOR_55_SHA)

    def test_09_prior_two_chapter_continuation_unchanged(self):
        self.assertEqual(git_blob(BASE / "READING_COPY_CAUSAL_CHAPTERS_56_57_NONCANON.md"), PRIOR_56_57_SHA)

    def test_10_substantial_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 4564)

    def test_11_substantial_narrative(self):
        self.assertGreaterEqual(len(self.prose.split()), 4000)

    def test_12_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_jake_is_only_interior_owner(self):
        self.assertIn("Sole interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_14_no_claim_historical_owner_authenticated(self):
        self.assertIn("2016 owner/team binding remains unverified", self.chapter)
        self.assertIn("not authenticated 2016 league events", self.chapter)

    def test_15_no_sports_claims_in_prose(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|playoff|touchdown|quarterback|Week [0-9]+)\b")

    def test_16_older_false_witness_money_two_parts(self):
        self.assertIn("eight coins", self.prose)
        self.assertIn("Four had gone into the removable floor", self.prose)
        self.assertIn("Four remained in his pouch", self.prose)

    def test_17_pell_lost_haul_chance_and_injury(self):
        self.assertIn("Pell had lost a chance to work", self.prose)
        self.assertIn("His wrist, injured when the first freight was lost", self.prose)

    def test_18_four_coins_restituted_without_completeness(self):
        self.assertIn("Pell took the four coins one at a time", self.prose)
        self.assertIn("part of what my lie cost you", self.prose)
        self.assertIn("I don't have the rest of what you might have earned", self.prose)

    def test_19_pell_earns_separate_money_from_work(self):
        self.assertIn("he paid the agreed amount to Pell and the younger worker", self.prose)
        self.assertIn("One sum came from work he had performed", self.prose)

    def test_20_no_forgiveness_auto_purchased(self):
        self.assertIn("Pell had accepted them as partial restitution", self.prose)
        self.assertIn("not as wages, vindication, forgiveness", self.prose)

    def test_21_false_account_remains_unrecovered(self):
        self.assertIn("The lie itself had not been retrieved from Orrel's pages", self.prose)

    def test_22_jake_shelter_debt_not_auto_paid(self):
        self.assertIn("Jake still owed shelter payment to Esi", self.prose)

    def test_23_buyer_extension_expires_without_collateral_promotion(self):
        self.assertIn("The time he offered is past", self.prose)
        self.assertIn("He says yesterday's bargain no longer binds him", self.prose)
        self.assertIn("the buyer still has collar", self.qa.lower())

    def test_24_cart_six_owners_hessa_away(self):
        self.assertIn("Six cart owners still own their cart", self.qa)
        self.assertIn("Hessa was absent", self.prose)

    def test_25_disappeared_seven_still_missing(self):
        self.assertIn("seven people still unlocated", self.prose)

    def test_26_injury_remains(self):
        for fragment in ("Neris and Dovan bore injuries", "Pell's wrist"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.prose + self.qa)

    def test_27_unknown_fire_origin_and_ecology(self):
        self.assertIn("cause of the fire and its lasting effect", self.prose)
        self.assertIn("fire origin unknown", self.qa)

    def test_28_no_invented_official_road_authority(self):
        self.assertIn("No watch was assigned", self.prose)
        self.assertIn("No road was pronounced safe", self.prose)

    def test_29_no_independent_review_claim(self):
        for term in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(term=term):
                self.assertIn(term, self.qa)

    def test_30_protected_2026_hard_canon(self):
        for file, sha in PROTECTED.items():
            with self.subTest(file=file):
                self.assertEqual(git_blob(ROOT / file), sha)

    def test_31_historical_source_archive_unchanged(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(p), ARCHIVE_SHA)

    def test_32_no_historical_owner_or_atlas_promotion(self):
        self.assertIn("No new ESPN/Flaim scores", self.qa)
        self.assertIn("unverified 2016 owner", self.qa)
        self.assertIn("secondary-world proposals", self.qa)

if __name__ == "__main__":
    unittest.main()
