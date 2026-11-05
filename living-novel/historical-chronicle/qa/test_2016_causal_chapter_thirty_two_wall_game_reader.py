"""Chapter XXXII V2: mechanical source-exact checks; NOT independent acceptance."""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_CART_AT_THE_FAR_TURN_THE_WALL_THAT_THREW_IT_BACK_CH32_V2_NONCANON.md"
ORIGINAL = "THE_CART_AT_THE_FAR_TURN_CHAPTER_32_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_32_TWENTY_NINE_PARTS_WALL_GAME_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_31_TWENTY_EIGHT_PARTS_PALM_CART_NONCANON.md"
CHAPTER_SHA = "57c2e3a1c229bd2fd28e1b7610dc93950f213a54"
ORIGINAL_SHA = "081a086921bbfabfa4e8344b0de94a711259ad44"
READER_SHA = "831f2dcdabe35d28047bd423a221b37d54422233"
PRIOR_SHA = "779b807748555c930e8485538180e9878395d7eb"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M)]
def passage(text, name, sha):
    begin = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(begin) == 1 and text.count(end) == 1, name
    return text.split(begin + "\n\n", 1)[1].split("\n\n" + end, 1)[0]

class ChapterThirtyTwoWallGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.original = (BASE / ORIGINAL).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.old_rows = rows(cls.prior)
        cls.scene = "### V. The wall that threw it back" + cls.chapter.split(
            "### V. The wall that threw it back", 1)[1].split("### VI. What can be carried home", 1)[0]

    def test_01_chapter_sha(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
    def test_02_original_sha(self):
        self.assertEqual(blob(BASE / ORIGINAL), ORIGINAL_SHA)
    def test_03_prior_reader_sha(self):
        self.assertEqual(blob(BASE / PRIOR), PRIOR_SHA)
    def test_04_new_reader_sha(self):
        self.assertEqual(blob(BASE / READER), READER_SHA)
    def test_05_six_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M),
                         ["I", "II", "III", "IV", "V", "VI"])
    def test_06_new_scene_words(self):
        self.assertEqual(len(self.scene.split()), 1968)
        for phrase in ("The ball went on the roof", "Both boots were on the wrong side of the line",
                       "There's a table needs shifting soon", "The yard is closed"):
            self.assertIn(phrase, self.scene)
    def test_07_original_first_four_movements_verbatim(self):
        marker = "### I. A room made too small"
        self.assertEqual(self.original.split(marker, 1)[1].split("### V. What can be carried home", 1)[0],
                         self.chapter.split(marker, 1)[1].split("### V. The wall that threw it back", 1)[0])
    def test_08_original_final_movement_verbatim(self):
        self.assertEqual(self.original.split("### V. What can be carried home", 1)[1],
                         self.chapter.split("### VI. What can be carried home", 1)[1])
    def test_09_manifest_order(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 30)))
        self.assertEqual(self.rows[-1], (29, CHAPTER, CHAPTER_SHA, 8281))
    def test_10_prior_rows_preserved(self):
        self.assertEqual(self.rows[:28], self.old_rows)
    def test_11_29_balanced_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 29)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 29)
    def test_12_source_exact_29_components(self):
        for part, name, sha, words in self.rows:
            with self.subTest(part=part):
                src = (BASE / name).read_text()
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(len(src.split()), words)
                self.assertEqual(passage(self.reader, name, sha), src.rstrip("\n"))
    def test_13_prior_28_bodies_verbatim(self):
        for part, name, sha, _ in self.old_rows:
            with self.subTest(part=part):
                self.assertEqual(passage(self.reader, name, sha), passage(self.prior, name, sha))
    def test_14_word_counts(self):
        self.assertEqual(len(self.chapter.split()), 8281)
        self.assertEqual(sum(w for _, _, _, w in self.rows), 205327)
        self.assertIn("Source component words including metadata: 205327", self.reader)
    def test_15_one_proposed_owner_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("UNAUTHENTICATED", self.chapter)
        for forbidden in ("Edrin", "Edin"):
            self.assertNotIn(forbidden, self.scene)
    def test_16_continuity(self):
        for phrase in ("The short bell did not ring",
                       "Ina had accepted the fitting and paid the separate fee",
                       "Orrel still had no confirmed word of Pell"):
            self.assertIn(phrase, self.chapter)
    def test_17_archive_unchanged(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
    def test_18_protected_canon_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)
    def test_19_noncanon_gates(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION", self.reader)
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL", self.reader)
    def test_20_no_invented_league_truth(self):
        self.assertIn("invented secondary-world fiction, not historical ESPN/Flaim data", self.reader)
        self.assertIn("historical owner-slot linkage is UNAUTHENTICATED", self.reader)

if __name__ == "__main__":
    unittest.main()
