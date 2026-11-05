"""Source-exact Chapter XXXIV 2016 causal reader regression; noncanon and not editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_BEES_IN_THE_WEDDING_ARCH_CHAPTER_34_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_34_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_33_NONCANON.md"
CHAPTER_SHA = "6793680804005b9af165cf26b63d1d52c34c233e"
READER_SHA = "0822c85b9cf936fe319701b16c74726e6a1a0441"
PREVIOUS_SHA = "72f7b9ae92627cc5bc8f63562a710b9a26d959d0"
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
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M
    )]

def passage(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == 1 and text.count(end) == 1
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class ThirtyFourChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_order_and_last_source(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 35)))
        self.assertEqual(self.manifest[-1], (34, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_balanced_source_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 34)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 34)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_34_chapters_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(passage(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_git_blob_manifest_exact(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(blob(BASE / name), sha)

    def test_05_previous_reader_preserved(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:-1], self.old_manifest)

    def test_06_substantial_five_movement_prose(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertGreaterEqual(len(self.chapter.split()), 7000)
        self.assertGreaterEqual(len(self.reader.split()), 190000)

    def test_07_exclusive_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("2016 league scoring slot remains UNAUTHENTICATED", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_08_swarm_conflict_is_action_not_an_omen_verdict(self):
        for phrase in ("Keret arrived without the solemnity", "The arch is not holding", "A good part of them are in"):
            self.assertIn(phrase, self.prose)

    def test_09_arch_removed_and_gate_reclaimed(self):
        for phrase in ("The branch came down in one piece", "The arch was gone", "The gate belongs to Fara"):
            self.assertIn(phrase, self.prose)

    def test_10_lysa_autonomy_remains_explicit(self):
        for phrase in ("I haven't changed that today", "I wasn't leaving the settlement", "I have work here"):
            self.assertIn(phrase, self.prose)

    def test_11_corin_makes_independent_consequential_choice(self):
        for phrase in ("I can take it down", "I tied it. I gave leave to take it down", "I don't want my uncle to speak for me"):
            self.assertIn(phrase, self.prose)

    def test_12_existing_open_loops_not_falsely_closed(self):
        for phrase in ("Vessa had not declared the unsafe kiln passage open",
                       "The message he had paid Mev to carry toward Esi had not been confirmed delivered",
                       "No confirmed news had reached him"):
            self.assertIn(phrase, self.prose)

    def test_13_history_and_biography_firewall(self):
        self.assertIn("No new 2016 competition facts are introduced", self.chapter)
        self.assertIn("proposed secondary-world invention", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_14_protected_hard_canon_and_archive_unchanged(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_15_exact_artifacts_and_noncanonical_hold(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(blob(BASE / READER), READER_SHA)
        self.assertIn("Thirty-four fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("No independently authenticated Authors Council", self.chapter)
        self.assertIn("NO MERGE, NO CANON PROMOTION, NO PUBLICATION", self.chapter)

if __name__ == "__main__":
    unittest.main()
