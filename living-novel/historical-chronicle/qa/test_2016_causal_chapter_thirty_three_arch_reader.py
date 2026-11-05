"""Chapter XXXIII V2: source-exact thirty-part regression. Mechanical only; NOT independent review."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_FEAST_WITH_NO_VOWS_BRANCHES_ABOVE_GATE_CH33_V2_NONCANON.md"
OLD = "THE_FEAST_WITH_NO_VOWS_CHAPTER_33_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_33_THIRTY_PARTS_BRANCHES_ABOVE_GATE_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_32_TWENTY_NINE_PARTS_WALL_GAME_NONCANON.md"
NEW_SHA = "263029a150d97cab3eaaf6ffdc0ada0c3c371485"
OLD_SHA = "3d7f1375a9f848e363ee35198daf824dd4bf2813"
READER_SHA = "1d8a7fb08f7111d222887ec7d97d18db2dd54151"
PRIOR_SHA = "831f2dcdabe35d28047bd423a221b37d54422233"
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
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M)]

def body(text, name, sha):
    begin = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(begin) == 1 and text.count(end) == 1, name
    return text.split(begin + "\n\n", 1)[1].split("\n\n" + end, 1)[0]

class ChapterThirtyThreeArch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.orig = (BASE / OLD).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.old_rows = rows(cls.prior)
        cls.scene = "### V. The branches above the gate" + cls.chapter.split(
            "### V. The branches above the gate", 1)[1].split("### VI. What remained when the guests were gone", 1)[0]

    def test_01_chapter_blob(self):
        self.assertEqual(blob(BASE / NEW), NEW_SHA)
    def test_02_original_chapter_untouched(self):
        self.assertEqual(blob(BASE / OLD), OLD_SHA)
    def test_03_prior_reader_untouched(self):
        self.assertEqual(blob(BASE / PRIOR), PRIOR_SHA)
    def test_04_new_reader_blob(self):
        self.assertEqual(blob(BASE / READER), READER_SHA)
    def test_05_six_ordered_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M), ["I", "II", "III", "IV", "V", "VI"])
    def test_06_substantial_new_scene(self):
        self.assertEqual(len(self.scene.split()), 1446)
        for phrase in ("You wanted a wife", "the branches, not the colors", "I don't think I could listen to it now", "a passage that would have to be used again tomorrow"):
            self.assertIn(phrase, self.scene)
    def test_07_arch_retained_for_next_chapter(self):
        self.assertIn("The bound branches remained above the gate", self.chapter)
        self.assertIn("Fara had seen the exchange from the food table.", self.chapter)
        self.assertNotIn("When the arch came down", self.chapter)
        follow = (BASE / "THE_BEES_IN_THE_WEDDING_ARCH_CHAPTER_34_NONCANON.md").read_text()
        self.assertIn("Bees had gathered on the central branch of the arch", follow)
        self.assertIn("That was supposed to be taken down last night.", follow)
    def test_08_source_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 31)))
        self.assertEqual(self.rows[-1], (30, NEW, NEW_SHA, 8715))
    def test_09_previous_manifest_preserved(self):
        self.assertEqual(self.rows[:29], self.old_rows)
    def test_10_thirty_balanced_component_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 30)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 30)
    def test_11_all_parts_source_exact(self):
        for n, name, sha, words in self.rows:
            with self.subTest(part=n):
                src = (BASE / name).read_text()
                self.assertEqual(blob(BASE / name), sha)
                self.assertEqual(len(src.split()), words)
                self.assertEqual(body(self.reader, name, sha), src.rstrip("\n"))
    def test_12_previous_29_parts_identical(self):
        for n, name, sha, words in self.old_rows:
            with self.subTest(part=n):
                self.assertEqual(body(self.reader, name, sha), body(self.prior, name, sha))
    def test_13_new_source_word_totals(self):
        self.assertEqual(len(self.chapter.split()), 8715)
        self.assertEqual(sum(w for _, _, _, w in self.rows), 214042)
        self.assertIn("Source component words including metadata: 214042", self.reader)
    def test_14_sole_principal_proposed_owner(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("UNAUTHENTICATED", self.chapter)
        for forbidden in ("Edrin", "Edin"):
            self.assertNotIn(forbidden, self.scene)
    def test_15_open_loops_preserved(self):
        for marker in ("Pell, the driver, second horse and freight missing",
                       "Mev's delivery of his message to Esi unconfirmed",
                       "shared shed", "no wedding occurs"):
            self.assertIn(marker.lower(), self.chapter.lower())
    def test_16_historical_archive_unchanged(self):
        self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
    def test_17_protected_2026_canon_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)
    def test_18_governance_holds(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION", self.reader)
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL", self.reader)

if __name__ == "__main__":
    unittest.main()
