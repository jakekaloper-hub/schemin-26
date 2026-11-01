"""Chapter LVI: noncanonical 2016 historical source-exact continuation reader (no monolith claim)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md"
CONTINUATION = "READING_COPY_CAUSAL_CHAPTERS_56_FORWARD_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
QA = "CHAPTER_56_SOURCE_EDITORIAL_QA_RECEIPT.md"
CHAPTER_SHA = "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2"
CONTINUATION_SHA = "be596c9f1b172fad7c85f0dfacb0ce30838cc46b"
PRIOR_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    payload = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\x00" + payload).hexdigest()

class ChapterFiftySix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / CONTINUATION).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]
        cls.qa = (BASE / QA).read_text()

    def test_01_source_git_blob(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_02_reader_git_blob(self):
        self.assertEqual(git_blob(BASE / CONTINUATION), CONTINUATION_SHA)

    def test_03_existing_55_reader_immutable(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_04_reader_is_continuation_not_false_monolith(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Continuation"))
        self.assertIn("DOES NOT replace", self.reader)

    def test_05_one_source_marker(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 1)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 1)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_CONTINUATION_COPY -->"), 1)

    def test_06_source_exact_assembly(self):
        a = "<!-- BEGIN 2016_CAUSAL " + CHAPTER + " | git_blob " + CHAPTER_SHA + " -->"
        z = "<!-- END 2016_CAUSAL " + CHAPTER + " -->"
        self.assertEqual(self.reader.split(a, 1)[1].split(z, 1)[0].strip(), self.chapter.strip())

    def test_07_manifest_source_row(self):
        self.assertIn("| 56 | " + CHAPTER + " | " + CHAPTER_SHA + " | 5178 |", self.reader)

    def test_08_chapter_whitespace_words(self):
        self.assertEqual(len(self.chapter.split()), 5178)

    def test_09_substantial_prose(self):
        self.assertGreaterEqual(len(self.prose.split()), 4800)

    def test_10_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_11_sole_authorized_principal_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin|Oren)\b")

    def test_12_not_verified_history(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_13_cart_six_joint_owners(self):
        for name in ("Brast", "Neris", "Dovan", "Tovin", "Ilyen", "Hessa"):
            self.assertIn(name, self.prose)
        self.assertIn("Six still owned it", self.prose)

    def test_14_collar_taken_without_joint_consent(self):
        self.assertIn('"I took the collar," Tovin said.', self.prose)
        self.assertIn("without me", self.prose)

    def test_15_inaccessible_lodging_not_granted_as_success(self):
        self.assertIn("a climb Dovan could not safely manage", self.prose)
        self.assertIn("The trader offered a portion returned", self.prose)

    def test_16_noncanonical_buyer_bargain(self):
        self.assertIn("The buyer named the advance", self.prose)
        self.assertIn("until the next evening", self.prose)

    def test_17_collar_not_suddenly_returned(self):
        self.assertIn("They left without the collar", self.prose)
        self.assertIn("The cart was protected against one kind of accident", self.prose)

    def test_18_hessa_absent_property_still_hers(self):
        self.assertIn("Hessa remained away, still an owner", self.prose)
        self.assertIn("she cannot give consent to a new sale", self.prose)

    def test_19_ilyen_local_choice_persists(self):
        self.assertIn("Ilyen had stayed in the settlement", self.prose)
        self.assertIn("Ilyen remained behind", self.prose)

    def test_20_injury_continuity(self):
        self.assertIn("injured leg", self.prose)
        self.assertIn("one arm held close", self.prose)

    def test_21_missing_seven_not_resolved(self):
        self.assertIn("Seven companions who had disappeared", self.prose)
        self.assertIn("seven still missing were no closer", self.prose)

    def test_22_aven_does_not_buy_ownership_or_forgiveness(self):
        self.assertIn("Aven's", self.prose)
        self.assertIn('"You offered to be necessary."', self.prose)
        self.assertIn("the offer remained unaccepted", self.prose)

    def test_23_false_witness_debt_preserved(self):
        self.assertIn("four coins", self.prose)
        self.assertIn("Pell's wages", self.prose)

    def test_24_protected_2026_main_unchanged(self):
        for name, expected in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / name), expected)

    def test_25_historical_evidence_unchanged(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_26_author_review_not_independent(self):
        for term in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(term=term):
                self.assertIn(term, self.qa)

    def test_27_no_false_verified_monolith(self):
        self.assertIn("not a 56-chapter monolithic copy", self.qa)
        self.assertNotIn("56-section source-exact full reader assembled", self.qa)

if __name__ == "__main__":
    unittest.main()
