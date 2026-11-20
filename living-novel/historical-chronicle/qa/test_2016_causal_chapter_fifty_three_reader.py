"""Chapter LIII: source-exact 53-section reading copy and noncanonical continuity safeguards."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_SHADOW_THAT_CAME_HOME_CHAPTER_53_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_53_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_52_NONCANON.md"
CHAPTER_SHA = "daee3be5efb4123bf6651e74dc3fc3594d219ddb"
READER_SHA = "5c90592df3dd59603cc59116972790443c81658a"
PRIOR_SHA = "9133694e759ac689cfd5b240e9b670b3d921b501"
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
    return [(int(n), filename, sha, int(words)) for n, filename, sha, words in re.findall(
        r"^\| ([0-9]+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| ([0-9]+) \|$",
        doc, re.M
    )]

def section(doc, filename, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {filename} -->"
    assert doc.count(opening) == doc.count(closing) == 1, filename
    return doc.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterFiftyThree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 54)))

    def test_02_final_manifest_row(self):
        self.assertEqual(self.rows[-1], (53, CHAPTER, CHAPTER_SHA, 5333))

    def test_03_all_section_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 53)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 53)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_full_source_exactness(self):
        for _, name, sha, words in self.rows:
            with self.subTest(name=name):
                content = (BASE / name).read_text()
                self.assertEqual(section(self.reader, name, sha), content.strip())
                self.assertEqual(len(content.split()), words)

    def test_05_all_source_blob_hashes(self):
        for _, name, sha, _ in self.rows:
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_prior_reader_unchanged(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_prior_manifest_unchanged(self):
        self.assertEqual(self.rows[:52], self.prior_rows)

    def test_08_all_prior_assembled_sections_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(name=name):
                self.assertEqual(section(self.reader, name, sha), section(self.prior, name, sha))

    def test_09_chapter_blob(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_whitespace_words(self):
        self.assertEqual(len(self.chapter.split()), 5333)

    def test_12_substantial_new_prose(self):
        self.assertGreaterEqual(len(self.prose.split()), 4500)

    def test_13_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_reader_title_and_status(self):
        self.assertTrue(self.reader.startswith(
            "# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–LIII (NONCANON)"
        ))
        self.assertIn("Fifty-three fully assembled", self.reader)

    def test_15_reader_whitespace_words(self):
        self.assertEqual(len(self.reader.split()), 309321)

    def test_16_historical_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_17_exclusive_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin|Oren)\b")

    def test_18_no_seven_fates_certified(self):
        self.assertIn("Seven others remained unlocated", self.prose)
        self.assertIn("no new word had arrived from the inland road", self.prose)

    def test_19_hessa_ilyen_absent(self):
        self.assertIn("Hessa and Ilyen had already gone", self.prose)
        self.assertIn("None of them had heard from Hessa or Ilyen", self.prose)

    def test_20_injury_continuity(self):
        self.assertIn("Neris was holding her injured arm", self.prose)
        self.assertIn("the injured leg made every movement slow", self.prose)

    def test_21_nella_initiates_play(self):
        self.assertIn('"The Eighth Comes Home."', self.prose)
        self.assertIn("Nella was already drawing customers", self.prose)

    def test_22_unsupported_drowning_stopped(self):
        self.assertIn('"The river kept their names," Nella announced.', self.prose)
        self.assertIn('"No river," Neris answered.', self.prose)

    def test_23_refunds_visible(self):
        self.assertIn("Each person who wanted a refund could take back what they had paid", self.prose)
        self.assertIn("Two did so immediately", self.prose)

    def test_24_fara_cost_and_safety(self):
        self.assertIn("The lamp was needed", self.prose)
        self.assertIn("Fara moved the lamp toward her counter", self.prose)
        self.assertIn("She did not refund the lamp money", self.prose)

    def test_25_aven_no_reunion_claim(self):
        self.assertIn("Aven came across the lane only after the crowd thinned", self.prose)
        self.assertIn("The conversation in Ina's lower room that morning had not restored", self.prose)

    def test_26_sela_family_continuity(self):
        self.assertIn("the removable floor", self.prose)
        self.assertIn("Tam had arranged his three kings", self.prose)

    def test_27_witness_coins_and_pell_unresolved(self):
        self.assertIn("Four of the eight coins remained", self.prose)
        self.assertIn("Pell had not regained the lost wage", self.prose)

    def test_28_protected_2026_canon_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_29_historical_archive_protected(self):
        self.assertEqual(git_blob(
            ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        ), ARCHIVE_SHA)

    def test_30_self_audit_not_independent_acceptance(self):
        qa = (BASE / "CHAPTER_53_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)
