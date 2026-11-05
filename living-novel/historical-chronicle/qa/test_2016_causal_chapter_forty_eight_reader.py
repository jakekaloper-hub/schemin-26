"""Chapter XLVIII source-exact reader assembly, protected authority and literary provenance tests."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_MORNING_OF_SMALL_LOAVES_CHAPTER_48_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_48_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_47_NONCANON.md"
CHAPTER_SHA = "7641b297fa5ff72f79f67edaf3b5a8428c21bed7"
READER_SHA = "0357d03c303e8a4d41227c19f4a623079975b87b"
PREVIOUS_SHA = "ff2a5892b39bbd94e6dfb67572600002cc53fcf0"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(w)) for n, name, sha, w in re.findall(
        r"^\| ([0-9]+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| ([0-9]+) \|$", text, re.M)]

def section(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == text.count(end) == 1, name
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class ChapterFortyEight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PREVIOUS).read_text()
        cls.items = rows(cls.reader)
        cls.before = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([r[0] for r in self.items], list(range(1, 49)))
        self.assertEqual(self.items[-1], (48, CHAPTER, CHAPTER_SHA, 5642))

    def test_02_source_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 48)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 48)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_exact_all_sources(self):
        for number, name, sha, expected_words in self.items:
            with self.subTest(number=number):
                self.assertEqual(section(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), expected_words)

    def test_04_blob_integrity_all_chapters(self):
        for number, name, sha, _ in self.items:
            with self.subTest(number=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_preserved_prior_reader(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.items[:47], self.before)
        for _, name, sha, _ in self.before:
            with self.subTest(name=name):
                self.assertEqual(section(self.reader, name, sha), section(self.prior, name, sha))

    def test_06_current_blob_integrity(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_movements_substantial_prose(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)
        self.assertEqual(len(self.chapter.split()), 5642)
        self.assertGreater(len(self.prose.split()), 4900)
        self.assertEqual(len(self.reader.split()), 281259)

    def test_08_draft_status_explicit(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLVIII (NONCANON)"))
        self.assertIn("Forty-eight fully assembled", self.reader)
        self.assertIn("INDEPENDENT EDITORIAL HOLD", self.chapter)

    def test_09_no_verified_esports_fabrication(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_10_twelve_owner_interior_boundary(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin)\b")

    def test_11_rope_causes_material_loss(self):
        self.assertIn("The driver waited no longer. She cut the rope with her own small knife.", self.prose)
        self.assertIn("Flour poured through a seam", self.prose)
        self.assertIn("Tomorrow's flour is not yet in the bin.", self.prose)

    def test_12_fara_and_driver_independent_action(self):
        self.assertIn("She would not bake from it.", self.prose)
        self.assertIn("two loaves of the promised size", self.prose)
        self.assertIn("partial contribution", self.prose)

    def test_13_hessa_and_sela_material_agency(self):
        self.assertIn("Hessa arrived at the table house", self.prose)
        self.assertIn("one smaller loaf", self.prose)
        self.assertIn("Tam may have one bowl", self.prose)

    def test_14_garran_contested_not_empowered(self):
        self.assertIn("The rope had been stretched", self.prose)
        self.assertIn("There was no rope across it.", self.prose)
        self.assertIn("no official watch is recognized", self.reader)

    def test_15_old_moral_and_financial_loops(self):
        for phrase in ("Four of the eight false-witness coins", "Pell's lost wage", "twenty-one-night", "Orrel", "Sela net-mender identity overlap"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.chapter)

    def test_16_unchanged_protected_main(self):
        for rel, sha in PROTECTED.items():
            with self.subTest(rel=rel):
                self.assertEqual(git_blob(ROOT / rel), sha)

    def test_17_unchanged_2016_archive(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_18_independent_hold_not_approval(self):
        qa = (BASE / "CHAPTER_48_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, qa)

if __name__ == "__main__":
    unittest.main()
