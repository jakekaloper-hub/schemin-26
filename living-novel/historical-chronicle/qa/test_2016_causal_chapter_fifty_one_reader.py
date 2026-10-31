"""Chapter LI: source-exact 51-chapter assembly, historical firewall, causal consequences and release HOLD."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "WHAT_THE_SIX_COULD_NOT_CARRY_CHAPTER_51_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_51_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_50_NONCANON.md"
CHAPTER_SHA = "6a431144823bc64973f0b57ee5d05f7f1f20cc25"
READER_SHA = "40a07dc448a9a7643ea3460fab665f68e8e495ec"
PRIOR_SHA = "7c8a95b606be41b0f75b20708b0037832021fd04"
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
        r"^\| ([0-9]+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| ([0-9]+) \|$", text, re.M)]

def source(text, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(opening) == text.count(closing) == 1, name
    return text.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterFiftyOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 52)))

    def test_02_final_manifest_row(self):
        self.assertEqual(self.rows[-1], (51, CHAPTER, CHAPTER_SHA, 5744))

    def test_03_complete_marker_pairs(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 51)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 51)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_assembled_sources_exact(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(source(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_05_all_component_blobs_pinned(self):
        for n, name, sha, _ in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_prior_reader_unchanged(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_previous_manifest_unchanged(self):
        self.assertEqual(self.rows[:50], self.prior_rows)

    def test_08_previous_sections_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(source=name):
                self.assertEqual(source(self.reader, name, sha), source(self.prior, name, sha))

    def test_09_chapter_blob_exact(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_blob_exact(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5744)

    def test_12_substantial_narrative_prose(self):
        self.assertGreaterEqual(len(self.prose.split()), 5000)

    def test_13_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_fifty_one_reader_header(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–LI (NONCANON)"))
        self.assertIn("Fifty-one fully assembled", self.reader)

    def test_15_exact_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 298266)

    def test_16_historical_evidence_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_17_only_owner_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin)\b")

    def test_18_real_return_not_false_summons(self):
        self.assertIn("The three who had taken the inland track returned", self.prose)

    def test_19_missing_eight_not_found(self):
        self.assertIn("Eight people are missing and eight people remain missing.", self.prose)

    def test_20_separate_decisions_noncoerced(self):
        self.assertIn("I am not going again", self.prose)
        self.assertIn("I will go", self.prose)
        self.assertIn("We will not take the cart", self.prose)

    def test_21_property_not_sold_or_transferred(self):
        self.assertIn("would not allow Brast, Dovan, Neris or Tovin to sell her share", self.prose)
        self.assertIn("not to surrender any claim to it", self.prose)

    def test_22_stair_unrepaired(self):
        self.assertIn("had not opened the upper floor or declared it fit", self.prose)
        self.assertIn("Nothing that he had seen restored the room", self.prose)

    def test_23_bounded_second_floor_night(self):
        self.assertIn("a second night only after moving sealed orders", self.prose)
        self.assertIn("It would not hold indefinitely.", self.prose)

    def test_24_new_fictional_names_no_prior_collision(self):
        for name in ("Ilyen", "Brast"):
            with self.subTest(name=name):
                self.assertNotRegex(self.prior, r"\b" + re.escape(name) + r"\b")

    def test_25_protected_main_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_26_historical_archive_unchanged(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_27_no_independent_acceptance_fabricated(self):
        qa = (BASE / "CHAPTER_51_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)

    def test_28_noncano_release_boundary(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("Founder approval remain outstanding", self.chapter)

if __name__ == "__main__":
    unittest.main()
