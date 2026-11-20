"""Noncanonical Chapter XXXI V2 and 28-part source-exact 2016 reader.

Only mechanical provenance and continuity checks. PASS is not editorial, Umpire,
historical identity, or Founder acceptance.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_HORSE_THAT_CAME_WITHOUT_A_CART_THE_CART_THAT_FIT_IN_A_PALM_CH31_V2_NONCANON.md"
ORIGINAL = "THE_HORSE_THAT_CAME_WITHOUT_A_CART_CHAPTER_31_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_31_TWENTY_EIGHT_PARTS_PALM_CART_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_30_TWENTY_SEVEN_PARTS_HANDLE_ACROSS_TABLE_NONCANON.md"
CHAPTER_SHA = "bbde1f7ab6f93a038056152b2c371f4b6853dafd"
ORIGINAL_SHA = "057de527cd24fc09a81e689f60c0dac834622791"
READER_SHA = "779b807748555c930e8485538180e9878395d7eb"
PRIOR_SHA = "c7d970b54e7b00db54a83f2c93550efed0a3941b"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M)]

def passage(text, name, sha):
    begin = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(begin) == 1 and text.count(end) == 1, name
    return text.split(begin + "\n\n", 1)[1].split("\n\n" + end, 1)[0]

class ChapterThirtyOnePalmCart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.original = (BASE / ORIGINAL).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.old_rows = rows(cls.prior)
        cls.scene = "### V. The cart that fit in a palm" + cls.chapter.split(
            "### V. The cart that fit in a palm", 1)[1].split(
            "### VI. What remained in the yard", 1)[0]

    def test_01_chapter_blob_pinned(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_02_original_chapter_preserved(self):
        self.assertEqual(blob(BASE / ORIGINAL), ORIGINAL_SHA)

    def test_03_prior_reader_preserved(self):
        self.assertEqual(blob(BASE / PRIOR), PRIOR_SHA)

    def test_04_current_reader_blob_pinned(self):
        self.assertEqual(blob(BASE / READER), READER_SHA)

    def test_05_six_chapter_movements_in_order(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M),
                         ["I", "II", "III", "IV", "V", "VI"])

    def test_06_substantial_new_prose_not_just_notes(self):
        self.assertEqual(len(self.scene.split()), 1940)
        for phrase in ("a very poor horse", "difficulty of paying workers",
                       "I can find another seed", "the other road smaller"):
            self.assertIn(phrase, self.scene)

    def test_07_original_first_four_movements_verbatim(self):
        start = "### I. The payment in daylight"
        before = self.original.split(start, 1)[1].split("### V. What remained in the yard", 1)[0]
        after = self.chapter.split(start, 1)[1].split("### V. The cart that fit in a palm", 1)[0]
        self.assertEqual(before, after)

    def test_08_original_final_movement_verbatim(self):
        before = self.original.split("### V. What remained in the yard", 1)[1].split("\n---\n", 1)[0]
        after = self.chapter.split("### VI. What remained in the yard", 1)[1].split("\n---\n", 1)[0]
        self.assertEqual(before, after)

    def test_09_reader_manifest_order_and_last_entry(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 29)))
        self.assertEqual(self.rows[-1], (28, CHAPTER, CHAPTER_SHA, 7733))

    def test_10_prior_27_source_rows_unchanged(self):
        self.assertEqual(self.rows[:27], self.old_rows)

    def test_11_28_balanced_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 28)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 28)

    def test_12_source_exact_28_embedded_components(self):
        for part, name, sha, words in self.rows:
            with self.subTest(part=part):
                source = (BASE / name).read_text()
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(len(source.split()), words)
                self.assertEqual(passage(self.reader, name, sha), source.rstrip("\n"))

    def test_13_first_27_embedded_bodies_verbatim(self):
        for part, name, sha, _ in self.old_rows:
            with self.subTest(part=part):
                self.assertEqual(passage(self.reader, name, sha), passage(self.prior, name, sha))

    def test_14_component_word_total_correct(self):
        self.assertEqual(len(self.chapter.split()), 7733)
        self.assertEqual(sum(words for _, _, _, words in self.rows), 197046)
        self.assertIn("Source component words including metadata: 197046", self.reader)

    def test_15_only_proposed_jake_principal_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("UNAUTHENTICATED", self.chapter)
        for forbidden in ("Edrin", "Edin"):
            self.assertNotIn(forbidden, self.scene)

    def test_16_loop_accounting(self):
        for phrase in ("I stood surety for no one", "Eren counted them herself",
                       "No one had returned from the orchard road",
                       "outside sorting wage", "the stoneworks kiln passage is sealed",
                       "no verified delivery or reply"):
            self.assertIn(phrase, self.chapter)

    def test_17_archival_evidence_still_immutable(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_18_protected_hard_canon_blobs_still_immutable(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_19_holds_remain_explicit(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION", self.reader)
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL", self.reader)

if __name__ == "__main__":
    unittest.main()
