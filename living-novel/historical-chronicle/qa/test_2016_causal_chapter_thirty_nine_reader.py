"""Chapter XXXIX source-exact reading copy and protected-main regression (NONCANON)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_STREET_THAT_TURNED_BLUE_CHAPTER_39_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_39_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_38_NONCANON.md"
CHAPTER_SHA = "529fa222dcd1cbf254d5a7235249f4240e29ba66"
READER_SHA = "15165b0e6e98f1a0d274a02fa2d613ad1ea048ac"
PREVIOUS_SHA = "730f61196ba8c084a2c8c3721966b494ac12f2eb"
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

class ThirtyNineChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = manifest_rows(cls.reader)
        cls.old_manifest = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_exact_39(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 40)))
        self.assertEqual(self.manifest[-1], (39, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_reader_has_39_exact_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 39)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 39)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_39_sections_source_exact(self):
        for number, name, sha, words in self.manifest:
            with self.subTest(chapter=number):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_all_39_component_git_blobs(self):
        for number, name, sha, _ in self.manifest:
            with self.subTest(chapter=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_38_sections_not_changed(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:38], self.old_manifest)
        for number, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=number):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_new_reader_git_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_substantial_six_movement_chapter(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertGreaterEqual(len(self.reader.split()), 223000)

    def test_08_exclusive_twelve_owner_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_09_physical_dye_turn_and_closure(self):
        self.assertIn("The loose stave", self.prose)
        self.assertIn("The water had found a route behind the wall.", self.prose)
        self.assertIn("The work that was closed", self.chapter)
        self.assertIn("Ina suspends wet dye work", self.chapter)

    def test_10_narrow_water_safety_not_certified(self):
        self.assertIn("local water safety is **NOT CERTIFIED**", self.chapter)
        self.assertIn("She would not refill it from the gutter", self.prose)
        self.assertNotIn("safe to drink now", self.prose)

    def test_11_prior_physical_continuity_preserved(self):
        self.assertIn("Eight displaced travelers and one cart have departed", self.chapter)
        self.assertIn("six, including Hessa and an infant", self.chapter)
        self.assertIn("Fara's inherited awning is permanently shortened", self.chapter)
        self.assertIn("Mael has returned alive", self.chapter)
        self.assertIn("Pell is at Ina's with an injured ankle", self.chapter)

    def test_12_no_scoring_facts_in_fiction(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertIn("UNAUTHENTICATED", self.chapter)

    def test_13_protected_hard_manuscript_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_14_historical_evidence_archive_unchanged(self):
        source = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(source), ARCHIVE_SHA)

    def test_15_noncanon_release_hold(self):
        self.assertTrue(self.chapter.startswith("# The Street That Turned Blue"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XXXIX"))
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        for gate in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(gate, self.chapter)

if __name__ == "__main__":
    unittest.main()
