"""Chapter XLIV noncanonical reader assembly, preservation and continuity checks.

These automatic checks do NOT constitute independent literary, historical-owner, Atlas or Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_FLOOR_THAT_COULD_BE_LIFTED_CHAPTER_44_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_44_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_43_NONCANON.md"
CHAPTER_SHA = "e3250efd8dbc4df8a1dceba6b663d1f45159aaf3"
READER_SHA = "e83303d18e0485a4cc811d7ac9c12b42f28a58be"
PREVIOUS_SHA = "fead5b8dd40f2410e7b919b441737704c2311e53"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()

def manifest_rows(text):
    rows = re.findall(r"^\\| (\\d+) \\| `([^`]+)` \\| `([0-9a-f]{40})` \\| (\\d+) \\|$", text, re.M)
    return [(int(n), name, sha, int(words)) for n, name, sha, words in rows]

def section(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    finish = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == text.count(finish) == 1, (name, "source markers")
    return text.split(start, 1)[1].split(finish, 1)[0].strip()

class FortyFourChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.rows = manifest_rows(cls.reader)
        cls.previous_rows = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\\n---\\n", 1)[0]

    def test_01_manifest_44_ordered_sources(self):
        self.assertEqual([r[0] for r in self.rows], list(range(1, 45)))
        self.assertEqual(self.rows[-1], (44, CHAPTER, CHAPTER_SHA, 5857))

    def test_02_exact_44_source_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 44)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 44)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_every_source_embedded_exactly(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                src = (BASE / name).read_text()
                self.assertEqual(section(self.reader, name, sha), src.strip())
                self.assertEqual(len(src.split()), words)

    def test_04_all_44_real_git_blob_shas(self):
        for n, name, sha, _ in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_reader_preserved(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.rows[:43], self.previous_rows)
        for n, name, sha, _ in self.previous_rows:
            with self.subTest(chapter=n):
                self.assertEqual(section(self.reader, name, sha), section(self.previous, name, sha))

    def test_06_new_chapter_and_reader_sha(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_substantial_connected_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\\.", self.chapter, re.M)), 6)
        self.assertEqual(len(self.chapter.split()), 5857)
        self.assertGreater(len(self.prose.split()), 5000)
        self.assertEqual(len(self.reader.split()), 259086)

    def test_08_reader_status_and_title(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLIV (NONCANON)"))
        self.assertIn("Forty-four fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)

    def test_09_work_loss_is_not_invented_wage(self):
        self.assertIn("I did not earn a wage today", self.prose)
        self.assertIn("Pell lost a hauling chance", self.prose)
        self.assertIn("He did not earn a wage today", self.prose)

    def test_10_money_bounded_not_restitution(self):
        self.assertIn("Four coins", self.prose)
        self.assertIn("The rest are yours to answer for elsewhere", self.prose)
        self.assertIn("No payment toward my shelter debt", self.prose)

    def test_11_portable_camp_not_legal_claim(self):
        self.assertIn("Then we lift the floor", self.prose)
        self.assertIn("No one has offered us title", self.prose)
        self.assertIn("They were still outdoors", self.prose)

    def test_12_no_false_horse_fact_made_true(self):
        self.assertIn("I don't know where it went", self.prose)
        self.assertIn("Orrel's packet had not returned", self.prose)
        self.assertIn("second horse", self.chapter)

    def test_13_supporting_agency_independent(self):
        for name in ("Pell", "Ina", "Sela", "Meric", "Eren", "Hessa", "Fara", "Nella", "Tam"):
            self.assertIn(name, self.prose)

    def test_14_prior_material_consequences_retained(self):
        for token in ("two dry orders", "wet dye", "twenty-one nights", "red-sky painting", "awning", "donkey", "kiln passage"):
            self.assertIn(token, self.chapter)

    def test_15_only_canonical_owner_interiority(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\\b(?:Edrin|Edin|Oren)\\b")

    def test_16_no_competitive_history_invented_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertNotRegex(self.prose, r"\\bWeek \\d+\\b")

    def test_17_protected_opening_unmodified(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_18_2016_historical_archive_unmodified(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(path), ARCHIVE_SHA)

    def test_19_sela_collision_and_unresolved_delivery(self):
        self.assertIn("Sela net-mender", self.chapter)
        self.assertIn("not silently equated", self.chapter)
        self.assertIn("actual receipt", self.chapter)

    def test_20_no_claim_of_approval_or_release(self):
        for label in ("NONCANON / INDEPENDENT EDITORIAL HOLD", "UNAUTHENTICATED", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(label, self.chapter)

if __name__ == "__main__":
    unittest.main()
