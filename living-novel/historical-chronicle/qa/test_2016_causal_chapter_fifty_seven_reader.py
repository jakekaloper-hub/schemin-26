"""Chapter LVII: source-exact, noncanonical 2016 continuation and hard-canon preservation."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
FIRST = "THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md"
SECOND = "THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_56_57_NONCANON.md"
QA = "CHAPTER_57_SOURCE_EDITORIAL_QA_RECEIPT.md"
FIRST_SHA = "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2"
SECOND_SHA = "d2a483e2d6b90e79b9d858525a1e19ae7657648c"
READER_SHA = "e1887ccd99841b50741689f2f6d7b67160571794"
PRIOR_READER_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
PRIOR_CONTINUATION_SHA = "be596c9f1b172fad7c85f0dfacb0ce30838cc46b"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a67cf1a67cf1a67cf1a67cf1a67",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
# Prologue fixture SHA is filled from the verified predecessor, not a guessed value.
PROTECTED["living-novel/manuscript/PROLOGUE_DRAFT_V1.md"] = "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0"

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterFiftySeven(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first = (BASE / FIRST).read_text()
        cls.chapter = (BASE / SECOND).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_prior_chapter_blob_immutable(self):
        self.assertEqual(git_blob(BASE / FIRST), FIRST_SHA)

    def test_02_new_chapter_blob(self):
        self.assertEqual(git_blob(BASE / SECOND), SECOND_SHA)

    def test_03_continuation_reader_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_04_prior_55_chapter_reader_immutable(self):
        self.assertEqual(git_blob(BASE / "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"), PRIOR_READER_SHA)

    def test_05_old_one_chapter_continuation_immutable(self):
        self.assertEqual(git_blob(BASE / "READING_COPY_CAUSAL_CHAPTERS_56_FORWARD_NONCANON.md"), PRIOR_CONTINUATION_SHA)

    def test_06_two_source_markers_only(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 2)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 2)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_CONTINUATION_COPY -->"), 1)

    def test_07_source_exact_assembly_56_and_57(self):
        for name, sha, expected in ((FIRST, FIRST_SHA, self.first), (SECOND, SECOND_SHA, self.chapter)):
            with self.subTest(chapter=name):
                start = "<!-- BEGIN 2016_CAUSAL " + name + " | git_blob " + sha + " -->"
                end = "<!-- END 2016_CAUSAL " + name + " -->"
                self.assertEqual(self.reader.count(start), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(self.reader.split(start, 1)[1].split(end, 1)[0].strip(), expected.strip())

    def test_08_manifest_both_rows(self):
        self.assertIn("| 56 | " + FIRST + " | " + FIRST_SHA + " | 5178 |", self.reader)
        self.assertIn("| 57 | " + SECOND + " | " + SECOND_SHA + " | 4471 |", self.reader)

    def test_09_reader_not_full_57_monolith(self):
        self.assertIn("DOES NOT replace", self.reader)
        self.assertIn("A monolithic 57-chapter assembled reader is not claimed", self.reader)

    def test_10_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 4471)

    def test_11_substantial_narrative(self):
        self.assertEqual(len(self.prose.split()), 4292)

    def test_12_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_authorized_jake_limited_only(self):
        self.assertIn("sole principal interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_14_not_espena_or_flaim_fiction_facts(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertIn("NOT provider-authenticated", self.chapter)

    def test_15_environment_event_not_historical_claim(self):
        self.assertIn("explicitly invented secondary-world fiction", self.chapter)
        self.assertIn("The ground beyond was black", self.prose)

    def test_16_unknown_cause(self):
        self.assertIn('"Did you see how it began?"', self.prose)
        self.assertIn("He could not see the source", self.prose)

    def test_17_no_false_fire_safety_certainty(self):
        self.assertIn("I cannot tell how far the fire has spread", self.prose)
        self.assertIn("The river was a boundary, but not a guarantee", self.prose)

    def test_18_ilyen_agency_and_no_invented_witnesses(self):
        self.assertIn("Ilyen was at the path", self.prose)
        self.assertIn("The fire doesn't make every stranger a witness", self.prose)

    def test_19_damaged_cart_remains_disabled(self):
        self.assertIn("the six owners' consent", self.prose)
        self.assertIn("still lay at the buyer's table", self.prose)
        self.assertIn("Still blocked. Still ours. Still not safe to move", self.prose)

    def test_20_hessa_absent_and_no_identity_invention(self):
        self.assertIn("Hessa alone somewhere beyond the settlement", self.prose)
        self.assertIn("The fire doesn't make every stranger a witness", self.prose)

    def test_21_missing_seven_unresolved(self):
        self.assertIn("seven still unlocated", self.prose)
        self.assertIn("seven people had gone missing", self.prose)

    def test_22_injury_still_material(self):
        self.assertIn("injured arm", self.prose)
        self.assertIn("injured leg", self.prose)
        self.assertIn("Dovan", self.prose)
        self.assertIn("Neris", self.prose)

    def test_23_aven_not_instantly_reconciled(self):
        self.assertIn("Aven's single board assistance", self.qa)
        self.assertIn("No embrace followed", self.prose)

    def test_24_existing_pell_false_witness_debt(self):
        self.assertIn("four coins Jake carried", self.prose)
        self.assertIn("Pell", self.prose)
        self.assertIn("lost wages", self.prose)

    def test_25_no_invented_public_institution(self):
        self.assertIn("He did not announce the beginning of a watch", self.prose)
        self.assertIn("No one called the gathering a council", self.prose)

    def test_26_no_auto_approval_in_author_review(self):
        for term in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(term=term):
                self.assertIn(term, self.qa)

    def test_27_protected_hard_2026_manuscript(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / name), sha)

    def test_28_historical_source_evidence_unchanged(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(path), ARCHIVE_SHA)

    def test_29_qa_exact_count_and_scope(self):
        self.assertIn("9,787 whitespace-separated words", self.qa)
        self.assertIn("4,292 narrative words", self.qa)
        self.assertIn("No assembled 57-chapter monolith", self.qa)

if __name__ == "__main__":
    unittest.main()
