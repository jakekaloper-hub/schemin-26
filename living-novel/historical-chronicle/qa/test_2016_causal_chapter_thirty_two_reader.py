"""2016 causal Chapter XXXII source-exact reading copy tests; not an independent editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_CART_AT_THE_FAR_TURN_CHAPTER_32_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_32_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_31_NONCANON.md"
CHAPTER_SHA = "081a086921bbfabfa4e8344b0de94a711259ad44"
READER_SHA = "a30d1abcb91eafd80c73771aa33a34c245444751"
PREVIOUS_SHA = "61df63802ae7000c06dde9efaf1ff1856f99d312"
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
        r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M
    )]

def passage(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == 1 and text.count(end) == 1
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class ThirtyTwoChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_complete_and_ordered(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 33)))
        self.assertEqual(self.manifest[-1], (32, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_balanced_source_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 32)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 32)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_source_exact_32_components(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(passage(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_source_git_blob_manifest(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(blob(BASE / name), sha)

    def test_05_previous_reader_unchanged(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:-1], self.old_manifest)

    def test_06_literary_volume_and_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertGreaterEqual(len(self.reader.split()), 175000)

    def test_07_only_owner_principal_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("2016 league scoring slot remains UNAUTHENTICATED", self.chapter)
        for removed in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(removed, self.prose)

    def test_08_guided_party_returns_bounded(self):
        for phrase in ("They returned after the midday bell", "We stayed under a farmer's roof before dark", "I wouldn't take two people over unfamiliar ground"):
            self.assertIn(phrase, self.prose)

    def test_09_empty_cart_not_missing_person_resolution(self):
        for phrase in ("A cart", "Neither brought Pell", "And no person", "Pell, the driver, the second horse or the missing freight"):
            self.assertIn(phrase, self.prose)

    def test_10_no_ratified_surety_or_freight_verdict(self):
        self.assertIn("the old surety paper again", self.prose)
        self.assertIn("The paper had not been signed", self.prose)
        self.assertIn("no human fate or freight outcome inferred", self.chapter)

    def test_11_eren_distinct_craft_payments_and_actions(self):
        for phrase in ("I would pay for a copy", "counted out the rest of Eren's payment", "The price is for fitting", "accepted the fitting and paid the separate fee"):
            self.assertIn(phrase, self.prose)

    def test_12_mare_bounded_care_not_magic_cure(self):
        for phrase in ("The stable woman led her", "No cart, saddle or load was attached", "mare was being tended"):
            self.assertIn(phrase, self.prose)
        self.assertIn("without claiming cure", self.chapter)

    def test_13_pay_kiln_and_letter_boundaries(self):
        self.assertIn("no sorting shift to offer", self.prose)
        self.assertIn("kiln passage, which remained closed", self.prose)
        self.assertIn("no confirmed word of delivery", self.prose)

    def test_14_protected_canon_and_facts_unchanged(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_15_readback_and_independent_hold(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(blob(BASE / READER), READER_SHA)
        self.assertIn("Thirty-two fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("No Authors Council, historical Librarian, period Character Canon/Atlas, Umpire or Founder accepted", self.chapter)

if __name__ == "__main__":
    unittest.main()
