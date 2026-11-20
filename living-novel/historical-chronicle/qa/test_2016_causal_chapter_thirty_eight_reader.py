"""Chapter XXXVIII source-exact reading-copy and protected-authority regression (noncanon)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_HAND_THAT_CUT_THE_LEATHER_CHAPTER_38_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_38_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_37_NONCANON.md"
CHAPTER_SHA = "a6f7f737d2ce79542489094be374f3084f24d657"
READER_SHA = "730f61196ba8c084a2c8c3721966b494ac12f2eb"
PREVIOUS_SHA = "856afd4cdae27c469e68cc56abcbff0d10f1d83e"
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
        r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M)]

def extract(reader, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(opening) == reader.count(closing) == 1
    return reader.split(opening, 1)[1].split(closing, 1)[0].strip()

class ThirtyEightChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = manifest_rows(cls.reader)
        cls.old_manifest = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_exact_38(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 39)))
        self.assertEqual(self.manifest[-1], (38, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_reader_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 38)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 38)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_38_sections_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_all_38_component_blobs(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_37_source_sections_unchanged(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:37], self.old_manifest)
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_new_reader_has_exact_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_substantial_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 5500)
        self.assertGreaterEqual(len(self.reader.split()), 216000)

    def test_08_exclusive_twelve_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_09_ambiguous_cut_trace_narrowly_explained(self):
        self.assertIn('"I cut this."', self.prose)
        self.assertIn('"Because the horse was being pulled down."', self.prose)
        self.assertIn("The second horse stayed fast.", self.prose)

    def test_10_mael_return_not_a_freight_resolution(self):
        self.assertIn('"Where is the cart?"', self.prose)
        self.assertIn('"I don\'t know."', self.prose)
        self.assertIn("No property recovery, legal judgment or signed liability claim is invented", self.chapter)

    def test_11_traveler_and_awning_state_remain_bounded(self):
        self.assertIn("eight who departed with one cart", self.chapter)
        self.assertIn("six including Hessa and the infant", self.chapter)
        self.assertIn("Fara's shortened inherited awning remains materially smaller", self.chapter)
        self.assertIn("The escaped bird had not returned", self.prose)

    def test_12_no_unverified_game_scores_added(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertIn("historical 2016 owner-slot association remains unauthenticated", self.chapter.lower())

    def test_13_protected_2026_manuscript_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_14_historical_evidence_unchanged(self):
        source = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(source), ARCHIVE_SHA)

    def test_15_draft_hold_and_title(self):
        self.assertTrue(self.chapter.startswith("# The Hand That Cut the Leather"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XXXVIII"))
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        for gate in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(gate, self.chapter)

if __name__ == "__main__":
    unittest.main()
