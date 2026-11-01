"""Chapter LIV: source-exact 54-section reading copy, historical and canon hold guards."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_WIDTH_OF_AN_OPEN_DOOR_CHAPTER_54_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_54_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_53_NONCANON.md"
CHAPTER_SHA = "a053640d5a4671f06b2c64892a1f5acf56e58fbe"
READER_SHA = "9a369d6a75f95b6dd78e6c34f50bc8624068e65f"
PRIOR_SHA = "5c90592df3dd59603cc59116972790443c81658a"
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

def rows(doc):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| ([0-9]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| ([0-9]+) \|$",
        doc, re.M
    )]

def section(doc, filename, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {filename} -->"
    assert doc.count(opening) == doc.count(closing) == 1, filename
    return doc.split(opening, 1)[1].split(closing, 1)[0].strip()


class ChapterFiftyFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 55)))

    def test_02_manifest_final_row(self):
        self.assertEqual(self.rows[-1], (54, CHAPTER, CHAPTER_SHA, 5356))

    def test_03_marker_counts(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 54)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 54)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_all_source_exact(self):
        for _, name, sha, words in self.rows:
            with self.subTest(name=name):
                source = (BASE / name).read_text()
                self.assertEqual(section(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_05_all_component_blob_hashes(self):
        for _, name, sha, _ in self.rows:
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_prior_reader_blob_unchanged(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_prior_manifest_unchanged(self):
        self.assertEqual(self.rows[:53], self.prior_rows)

    def test_08_all_prior_embedded_sections_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(name=name):
                self.assertEqual(section(self.reader, name, sha), section(self.prior, name, sha))

    def test_09_chapter_blob(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 5356)

    def test_12_substantial_prose(self):
        self.assertGreaterEqual(len(self.prose.split()), 4700)

    def test_13_six_connected_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_reading_copy_label(self):
        self.assertTrue(self.reader.startswith(
            "# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–LIV (NONCANON)"
        ))
        self.assertIn("Fifty-four fully assembled", self.reader)

    def test_15_reader_whitespace_words(self):
        self.assertEqual(len(self.reader.split()), 314781)

    def test_16_no_promotion_of_historical_evidence(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_17_exclusive_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin|Oren)\b")

    def test_18_injured_nreis_dovan_not_healed(self):
        self.assertIn("one arm supported by a folded cloth", self.prose)
        self.assertIn("Dovan's injured leg", self.prose)
        self.assertIn("His injured leg", self.prose)

    def test_19_ina_reclaims_business(self):
        self.assertIn("I need this part", self.prose)
        self.assertIn("I cannot give away the table", self.prose)
        self.assertIn("I haven't offered you wages", self.prose)

    def test_20_nreis_skilled_agency(self):
        self.assertIn("Your edge is failing", self.prose)
        self.assertIn("That is something I can do", self.prose)
        self.assertIn("I will earn for a separate place", self.prose)

    def test_21_fara_bounded_payment(self):
        self.assertIn("Half to begin", self.prose)
        self.assertIn("Half when the seam holds", self.prose)
        self.assertIn("paid Ina the remaining half", self.prose)

    def test_22_awning_test_not_instant_restoration(self):
        self.assertIn("The awning remained shorter than it once had been", self.prose)
        self.assertIn("The seam tightened, gave a finger's breadth", self.prose)

    def test_23_aven_boundary_not_reconciliation(self):
        self.assertIn("Ask her from there", self.prose)
        self.assertIn("I don't speak for her", self.prose)
        self.assertIn("Neris did not step closer", self.prose)

    def test_24_hessa_ilyen_absent(self):
        self.assertIn("Hessa and Ilyen, who had gone inland", self.prose)
        self.assertIn("still uninformed of Aven's return", self.prose)

    def test_25_seven_fates_unresolved(self):
        self.assertIn("Seven travelers were still unlocated", self.prose)
        self.assertIn("the fate of their relatives had not changed", self.prose)

    def test_26_shared_cart_ownership_preserved(self):
        self.assertIn("The cart belongs to six", self.prose)
        self.assertIn("the absent two retained their ownership", self.prose)
        self.assertIn("They had not divided the cart, sold it", self.prose)

    def test_27_old_debts_and_bell_remain(self):
        self.assertIn("The bell still hung above the counter without its clapper", self.prose)
        self.assertIn("Pell's lost wages remained unrestored", self.prose)
        self.assertIn("four coins he still carried from Orrel", self.prose)

    def test_28_no_repeat_thread_delivery(self):
        self.assertIn("He set his empty carrying sling", self.prose)
        self.assertNotIn("return the dry thread he had collected", self.prose)

    def test_29_protected_canon_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_30_retained_2016_evidence_blob(self):
        self.assertEqual(git_blob(
            ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        ), ARCHIVE_SHA)

    def test_31_editorial_gate_not_claimed_complete(self):
        qa = (BASE / "CHAPTER_54_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)
