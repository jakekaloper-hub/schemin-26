"""Chapter LV — governed 55-section source-exact causal reading copy, noncanon."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_SHAPE_OF_A_RETURN_CHAPTER_55_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_54_NONCANON.md"
CHAPTER_SHA = "c7b0f7f2cdff0684b408c991861e79a792641c83"
READER_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
PRIOR_SHA = "9a369d6a75f95b6dd78e6c34f50bc8624068e65f"
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
    normalized = doc.replace(chr(96), "")
    return [(int(n), name.strip(), sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| ([0-9]+) \| ([^|]+) \| ([0-9a-f]{40}) \| ([0-9]+) \|$", normalized, re.M
    )]

def section(doc, filename, sha):
    opening = "<!-- BEGIN 2016_CAUSAL " + filename + " | git_blob " + sha + " -->"
    closing = "<!-- END 2016_CAUSAL " + filename + " -->"
    assert doc.count(opening) == doc.count(closing) == 1, filename
    return doc.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterFiftyFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_numbers(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 56)))

    def test_02_manifest_latest(self):
        self.assertEqual(self.rows[-1], (55, CHAPTER, CHAPTER_SHA, 5934))

    def test_03_marker_counts(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 55)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 55)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_source_exact_sections(self):
        for _, name, sha, words in self.rows:
            with self.subTest(name=name):
                source = (BASE / name).read_text()
                self.assertEqual(section(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_05_source_github_blob_sha(self):
        for _, name, sha, _ in self.rows:
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_previous_reader_unchanged(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_previous_manifest_unchanged(self):
        self.assertEqual(self.rows[:54], self.prior_rows)

    def test_08_previous_sections_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(name=name):
                self.assertEqual(section(self.reader, name, sha), section(self.prior, name, sha))

    def test_09_chapter_sha(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_sha(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_words(self):
        self.assertEqual(len(self.chapter.split()), 5934)

    def test_12_substantial_narrative_prose(self):
        self.assertGreaterEqual(len(self.prose.split()), 5500)

    def test_13_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_reader_title(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–LV (NONCANON)"))
        self.assertIn("Fifty-five fully assembled", self.reader)

    def test_15_reader_words(self):
        self.assertEqual(len(self.reader.split()), 320793)

    def test_16_owner_restriction(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin|Oren)\b")

    def test_17_no_invented_competitive_event(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertIn("NOT provider-authenticated", self.chapter)

    def test_18_hessa_ilyen_return(self):
        self.assertIn("A pair of figures stood at the bend", self.prose)
        self.assertIn("Hessa", self.prose)
        self.assertIn("Ilyen", self.prose)

    def test_19_aven_speaks_but_not_verified(self):
        self.assertIn("I left them", self.prose)
        self.assertIn("I don't know where they went after I left", self.prose)

    def test_20_no_automatic_forgiveness(self):
        self.assertIn("Did you forgive him?", self.prose)
        self.assertIn("You should be sorry you made the searching necessary", self.prose)

    def test_21_ilyen_independent_choice(self):
        self.assertIn("I cannot set out again tomorrow", self.prose)
        self.assertIn("I can stop walking", self.prose)
        self.assertIn("I will ask here", self.prose)

    def test_22_hessa_voluntary_departure(self):
        self.assertIn("And if I go alone?", self.prose)
        self.assertIn("Hessa went down the lane alone", self.prose)

    def test_23_missing_seven_unresolved(self):
        self.assertIn("Hessa's sister remained unlocated", self.prose)
        self.assertIn("Ilyen's brother remained unlocated", self.prose)

    def test_24_neris_injury_persists(self):
        self.assertIn("one arm held close to her body", self.prose)
        self.assertIn("Her arm remained close to her body", self.prose)

    def test_25_dovan_injury_persists(self):
        self.assertIn("Dovan appeared from the alcove, using his stick", self.prose)
        self.assertIn("Dovan watched from the covered alcove, leaning on his stick", self.prose)

    def test_26_shared_cart_undivided(self):
        self.assertIn("six-person cart", self.prose)
        self.assertIn("six still owned it", self.prose)

    def test_27_fara_repair_not_rewritten(self):
        self.assertIn("mended awning", self.prose)
        self.assertIn("The bell still hung silent", self.prose)

    def test_28_false_witness_debt_not_disappeared(self):
        self.assertIn("four false-witness coins", self.prose)
        self.assertIn("Pell's lost wages were still lost", self.prose)

    def test_29_protected_main_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_30_historical_archive_preserved(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_31_editorial_hold(self):
        qa = (BASE / "CHAPTER_55_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)

if __name__ == "__main__":
    unittest.main()
