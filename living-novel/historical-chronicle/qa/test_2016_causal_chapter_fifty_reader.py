"""Chapter L: source-exact assembly, provenance, 12-owner POV and independent gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_NIGHT_BELOW_THE_ROOM_CHAPTER_50_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_50_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_49_NONCANON.md"
CHAPTER_SHA = "920d3fda6c9f366d9c56e45745b8db117c8e3fa8"
READER_SHA = "7c8a95b606be41b0f75b20708b0037832021fd04"
PRIOR_SHA = "8bd1b5f3d0e8661c0ee67a47bdbbe18c5285dc4c"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\\| ([0-9]+) \\| \\x60([^\\x60]+)\\x60 \\| \\x60([0-9a-f]{40})\\x60 \\| ([0-9]+) \\|$", text, re.M)]

def source(text, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(opening) == text.count(closing) == 1, name
    return text.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterFifty(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\\n---\\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 51)))

    def test_02_final_manifest_row(self):
        self.assertEqual(self.rows[-1], (50, CHAPTER, CHAPTER_SHA, 5637))

    def test_03_fifty_complete_marker_pairs(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 50)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 50)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_assembled_sections_source_exact(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(source(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_05_all_source_blobs_pinned(self):
        for n, name, sha, _ in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_prior_reader_immutable(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_prior_manifest_rows_immutable(self):
        self.assertEqual(self.rows[:49], self.prior_rows)

    def test_08_prior_sections_identical(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(source=name):
                self.assertEqual(source(self.reader, name, sha), source(self.prior, name, sha))

    def test_09_current_chapter_sha(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_sha(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 5637)

    def test_12_prose_length(self):
        self.assertGreaterEqual(len(self.prose.split()), 4900)

    def test_13_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_reader_noncanonical_header(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–L (NONCANON)"))
        self.assertIn("Fifty fully assembled", self.reader)

    def test_15_reader_words(self):
        self.assertEqual(len(self.reader.split()), 292402)

    def test_16_history_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_17_exclusive_owner_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\\b(Edrin|Edin)\\b")

    def test_18_real_structural_failure_not_a_rumor(self):
        self.assertIn("the fourth stair folded against the third", self.prose)
        self.assertIn("a larger piece of the landing had settled", self.prose)

    def test_19_joint_cart_property_damaged_not_sold(self):
        self.assertIn("Use it to get us down. Not for anything else.", self.prose)
        self.assertIn("One broke under the falling block", self.prose)

    def test_20_lodging_promise_not_silently_repaired(self):
        self.assertIn("You said twenty-one nights", self.prose)
        self.assertIn("We won't be using that room tonight", self.prose)
        self.assertIn("One night", self.prose)

    def test_21_remaining_three_have_agency(self):
        for name in ("Neris", "Dovan", "Tovin"):
            with self.subTest(name=name):
                self.assertIn(name, self.prose)

    def test_22_new_names_not_collisions_in_prior_copy(self):
        for name in ("Neris", "Dovan", "Tovin"):
            with self.subTest(name=name):
                self.assertNotRegex(self.prior, r"\\b" + re.escape(name) + r"\\b")

    def test_23_absent_three_remain_unlocated(self):
        self.assertIn("Hessa and two companions were somewhere along an inland track", self.prose)
        self.assertIn("They would not know until someone met them or they returned", self.prose)

    def test_24_important_separate_entities_respected(self):
        self.assertIn("Sela's family still used its own removable floor", self.prose)
        self.assertIn("Pell's lost wage had not been restored", self.prose)
        self.assertIn("Its clapper was still stored away", self.prose)

    def test_25_protected_main_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_26_historical_source_archive_untouched(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_27_independent_review_not_counterfeited(self):
        qa = (BASE / "CHAPTER_50_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)

if __name__ == "__main__":
    unittest.main()
