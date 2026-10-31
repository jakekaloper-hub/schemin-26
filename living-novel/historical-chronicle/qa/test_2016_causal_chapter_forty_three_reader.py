"""NONCANON Chapter XLIII: source-exact assembly, author-side continuity and preservation.

Automated assertions do not constitute independent literary or Umpire approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_NAME_HE_SOLD_CHAPTER_43_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_43_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_42_NONCANON.md"
CHAPTER_SHA = "c4e3705531e1c4589ac95845df15ccc108da6fd3"
READER_SHA = "fead5b8dd40f2410e7b919b441737704c2311e53"
PREVIOUS_SHA = "92b280d66d5be876411bfa35f9f6b45e319d5519"
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

def manifest_rows(text):
    pattern = r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$"
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(pattern, text, re.M)]

def section(text, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    finish = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(start) == text.count(finish) == 1, (name, "source markers")
    return text.split(start, 1)[1].split(finish, 1)[0].strip()

class FortyThreeChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.rows = manifest_rows(cls.reader)
        cls.previous_rows = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_ordered_complete_manifest(self):
        self.assertEqual([row[0] for row in self.rows], list(range(1, 44)))
        self.assertEqual(self.rows[-1], (43, CHAPTER, CHAPTER_SHA, 7089))

    def test_02_43_noncanonical_source_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 43)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 43)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_source_text_embedded_exact(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                src = (BASE / name).read_text()
                self.assertEqual(section(self.reader, name, sha), src.strip())
                self.assertEqual(len(src.split()), words)

    def test_04_all_sources_have_true_git_blobs(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_reader_frozen(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.rows[:42], self.previous_rows)
        for n, name, sha, words in self.previous_rows:
            with self.subTest(chapter=n):
                self.assertEqual(section(self.reader, name, sha), section(self.previous, name, sha))

    def test_06_exact_new_blob_identities(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_substantial_connected_six_part_chapter(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertEqual(len(self.chapter.split()), 7089)
        self.assertGreater(len(self.prose.split()), 6000)
        self.assertGreater(len(self.reader.split()), 253000)

    def test_08_reader_title_and_status(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLIII (NONCANON)"))
        self.assertIn("Forty-three fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)

    def test_09_intentional_false_statement_not_inferred_fact(self):
        self.assertIn("I saw the second horse being taken toward that northern road", self.prose)
        self.assertIn("He had not.", self.prose)
        self.assertIn("I wrote it for payment", self.prose)

    def test_10_specific_signed_withdrawal(self):
        self.assertIn("I, Jake, did not see the second horse", self.prose)
        self.assertIn("My earlier statement", self.prose)
        self.assertIn("Both pages go", self.prose)

    def test_11_payment_persists_without_restitution_fiction(self):
        self.assertIn("Eight small coins", self.prose)
        self.assertIn("The eight coins remained in his pouch", self.prose)
        self.assertIn("he had not paid them toward his shelter debt", self.prose)

    def test_12_likely_harm_not_claimed_as_event(self):
        self.assertIn("eight people who left on that road", self.prose)
        self.assertIn("not a fact about the eight", self.prose)
        self.assertIn("No second horse, freight, cart", self.chapter)

    def test_13_supporting_character_agency(self):
        for name in ("Orrel", "Meric", "Eren", "Pell", "Mael", "Ina", "Fara", "Hessa", "Sela", "Nella", "Tam"):
            self.assertIn(name, self.chapter)

    def test_14_existing_social_and_material_continuity(self):
        for token in ("two dry orders", "wet dye", "twenty-one-night", "red sky", "awning", "cart", "donkey", "camp"):
            self.assertIn(token, self.chapter)

    def test_15_no_old_plot_reset(self):
        for token in ("Hessa's missing sister", "Esi's letter", "escaped bird", "kiln passage", "second horse", "shelter debt"):
            self.assertIn(token, self.chapter)

    def test_16_only_twelve_owner_interiority(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_17_no_fabricated_competitive_history_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertNotRegex(self.prose, r"\bWeek \d+\b")

    def test_18_protected_main_manuscript_not_changed(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_19_archival_2016_facts_not_changed(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(path), ARCHIVE_SHA)

    def test_20_no_merge_canon_publication_claim(self):
        for key in ("NONCANON / INDEPENDENT EDITORIAL HOLD", "UNAUTHENTICATED", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(key, self.chapter)

if __name__ == "__main__":
    unittest.main()
