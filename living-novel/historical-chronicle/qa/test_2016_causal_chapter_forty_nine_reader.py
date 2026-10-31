"""Chapter XLIX: source-exact assembly, twelve-owner POV and independent approval gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_SHORE_THAT_KEPT_NO_FOOTPRINTS_CHAPTER_49_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_49_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_48_NONCANON.md"
CHAPTER_SHA = "a7640f47d11313582cdf137b1ce9bda177536960"
READER_SHA = "8bd1b5f3d0e8661c0ee67a47bdbbe18c5285dc4c"
PRIOR_SHA = "0357d03c303e8a4d41227c19f4a623079975b87b"
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
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| ([0-9]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| ([0-9]+) \|$", text, re.M)]

def source(text, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(opening) == text.count(closing) == 1, name
    return text.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterFortyNine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_complete_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 50)))

    def test_02_final_manifest_row_exact(self):
        self.assertEqual(self.rows[-1], (49, CHAPTER, CHAPTER_SHA, 5253))

    def test_03_all_source_markers_present(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 49)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 49)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_every_assembled_section_source_exact(self):
        for number, name, sha, words in self.rows:
            with self.subTest(number=number):
                self.assertEqual(source(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_05_every_source_blob_identity(self):
        for number, name, sha, _ in self.rows:
            with self.subTest(number=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_prior_reading_copy_immutable(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)
        self.assertEqual(self.rows[:48], self.prior_rows)

    def test_07_all_prior_sections_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(name=name):
                self.assertEqual(source(self.reader, name, sha), source(self.prior, name, sha))

    def test_08_current_chapter_blob(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_09_current_assembled_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_10_chapter_length(self):
        self.assertEqual(len(self.chapter.split()), 5253)
        self.assertGreaterEqual(len(self.prose.split()), 4500)

    def test_11_reader_length(self):
        self.assertEqual(len(self.reader.split()), 286636)

    def test_12_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_13_noncanonical_reader_header(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLIX (NONCANON)"))
        self.assertIn("Forty-nine fully assembled", self.reader)

    def test_14_evidence_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_15_exclusive_licensed_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin)\b")

    def test_16_messenger_lure_and_no_false_identification(self):
        for phrase in ("He gave me the cloth", "He told me to bring them to the bank.", "I didn't see a cart.", "I have no proof"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.prose)

    def test_17_hessa_independent_decision(self):
        self.assertIn("Those who choose it.", self.prose)
        self.assertIn("Three were going. Three would remain.", self.prose)
        self.assertIn("The three passed the place where Eren's sketch ended", self.prose)

    def test_18_21_night_private_lodging_retained(self):
        self.assertIn("twenty-one-night agreement", self.prose)
        self.assertIn("the three who stay", self.prose)
        self.assertIn("They would travel without it.", self.prose)

    def test_19_open_loops_not_silently_closed(self):
        for phrase in ("Hessa's sister and the other eight remain missing", "Sela net-mender name overlap remains UNRESOLVED", "Orrel's false/corrected statement packet", "Pell's lost wage"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.chapter)

    def test_20_protected_main_sources_unchanged(self):
        for rel, expected_sha in PROTECTED.items():
            with self.subTest(rel=rel):
                self.assertEqual(git_blob(ROOT / rel), expected_sha)

    def test_21_archived_historical_matchups_untouched(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_22_independent_review_not_counterfeited(self):
        qa = (BASE / "CHAPTER_49_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)

if __name__ == "__main__":
    unittest.main()
