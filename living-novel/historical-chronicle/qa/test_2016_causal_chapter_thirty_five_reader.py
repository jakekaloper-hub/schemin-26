"""Source-exact Chapter XXXV 2016 causal reader regression; NONCANON, not editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_COAT_THAT_DID_NOT_BELONG_CHAPTER_35_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_35_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_34_NONCANON.md"
CHAPTER_SHA = "bb4e2904bead10f403d4eda279cd9eeaf983032e"
READER_SHA = "75deb978aa788747bf6beaf32e8a2fd6ea530c05"
PREVIOUS_SHA = "0822c85b9cf936fe319701b16c74726e6a1a0441"
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

class ThirtyFiveChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_order_and_last_source(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 36)))
        self.assertEqual(self.manifest[-1], (35, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_balanced_source_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 35)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 35)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_35_chapters_source_exact(self):
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
        self.assertGreaterEqual(len(self.reader.split()), 197000)

    def test_07_exclusive_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("remains UNAUTHENTICATED", self.chapter)
        for forbidden in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(forbidden, self.prose)

    def test_08_return_is_real_in_scene_not_exoneration(self):
        for phrase in ("The man on the upper steps was wearing a coat too large for him.",
                       "I ran.", "Come inside while you can"):
            self.assertIn(phrase, self.prose)

    def test_09_ina_retains_accountability_and_agency(self):
        for phrase in ("Because it was waiting for you.",
                       "I believe you came home",
                       "That isn't the same as saying there is nothing left to answer for"):
            self.assertIn(phrase, self.prose)

    def test_10_jake_cost_is_not_false_wage(self):
        self.assertIn("We filled the benches at the bell", self.prose)
        self.assertIn("No new Jake wage", self.chapter)
        self.assertIn("He had not earned a wage today", self.prose)

    def test_11_missing_driver_second_horse_and_freight_unresolved(self):
        for phrase in ("I don't know where he is now", "I couldn't tell who",
                       "Mael had not been found", "neither had the second horse or the freight"):
            self.assertIn(phrase, self.prose)

    def test_12_existing_open_loops_not_falsely_closed(self):
        for phrase in ("kiln passage beyond them remained barred",
                       "Mev's delivery was still unconfirmed",
                       "unpaid shelter debt had not shifted"):
            self.assertIn(phrase, self.prose)

    def test_13_history_and_biography_firewall(self):
        self.assertIn("no new 2016 competition result", self.chapter)
        self.assertIn("invented secondary-world", self.chapter)
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
        self.assertIn("Thirty-five fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("No independently authenticated Authors Council", self.chapter)
        self.assertIn("NO MERGE, NO CANON PROMOTION, NO PUBLICATION", self.chapter)

if __name__ == "__main__":
    unittest.main()
