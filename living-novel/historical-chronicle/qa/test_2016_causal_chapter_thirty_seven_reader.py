"""Chapter XXXVII source-exact reader and protected-authority regression; NONCANON."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_COMPANY_THAT_CAME_APART_CHAPTER_37_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_37_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_36_NONCANON.md"
CHAPTER_SHA = "92aba7618d9d7a5ba88758be48084ded30eca4ba"
READER_SHA = "856afd4cdae27c469e68cc56abcbff0d10f1d83e"
PREVIOUS_SHA = "32d4dd8868a558e1a7a774fb8d3730c4b7129160"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def manifest_rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M)]

def extract(reader, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(opening) == reader.count(closing) == 1
    return reader.split(opening, 1)[1].split(closing, 1)[0].strip()

class ThirtySevenChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = manifest_rows(cls.reader)
        cls.old_manifest = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_exact_37(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 38)))
        self.assertEqual(self.manifest[-1], (37, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_reader_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 37)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 37)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_source_exact_all_37(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                src = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), src.strip())
                self.assertEqual(len(src.split()), words)

    def test_04_source_hashes(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_prior_reader_immutable(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:36], self.old_manifest)
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_exact_new_reader_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_movement_substantial_prose(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 6300)
        self.assertGreaterEqual(len(self.reader.split()), 210000)

    def test_08_owner_pov_restriction(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        for excluded in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(excluded, self.prose)

    def test_09_eight_plus_six_not_fourteen_departing(self):
        self.assertIn("Eight want to go while the road is passable", self.prose)
        self.assertIn("Six will stay another night", self.prose)
        self.assertIn("including Hessa and the baby", self.chapter)

    def test_10_unrepaired_awning_loss(self):
        for phrase in ("the old awning will no longer reach the outer post",
                       "She drew the line herself",
                       "The faded flower was upside down"):
            self.assertIn(phrase, self.prose)
        self.assertIn("Fara permanently shortens", self.reader)

    def test_11_work_accounted_and_no_false_wage(self):
        self.assertIn("The keeper had counted four hours in the outside yard", self.prose)
        self.assertIn("neither for the morning he had missed nor for tomorrow's work", self.prose)
        self.assertIn("paid for the supper he had eaten", self.prose)

    def test_12_fire_identity_and_unverified_history(self):
        self.assertIn("NOT a historical 2016 fire", self.chapter)
        self.assertIn("The cause of the ash was still unknown", self.prose)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_13_protected_hard_canon_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_14_historical_evidence_unchanged(self):
        evidence = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(evidence), ARCHIVE_SHA)

    def test_15_draft_gates_and_chapter_title(self):
        self.assertTrue(self.chapter.startswith("# The Company That Came Apart"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XXXVII"))
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        for marker in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(marker, self.chapter)

if __name__ == "__main__":
    unittest.main()
