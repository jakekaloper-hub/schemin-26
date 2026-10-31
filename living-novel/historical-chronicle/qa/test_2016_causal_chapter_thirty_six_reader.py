"""Source-exact Chapter XXXVI reader regression; noncanon, not editorial acceptance."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_ASH_AT_FARAS_DOOR_CHAPTER_36_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_36_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_35_NONCANON.md"
CHAPTER_SHA = "7a893b228e9c0bf21504c837b216763080ec6e09"
READER_SHA = "32d4dd8868a558e1a7a774fb8d3730c4b7129160"
PREVIOUS_SHA = "75deb978aa788747bf6beaf32e8a2fd6ea530c05"
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

def manifest_rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", text, re.M)]

def extract_passage(reader, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(opening) == reader.count(closing) == 1
    return reader.split(opening, 1)[1].split(closing, 1)[0].strip()

class ThirtySixChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old_reader = (BASE / PREVIOUS).read_text()
        cls.manifest = manifest_rows(cls.reader)
        cls.old_manifest = manifest_rows(cls.old_reader)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_has_thirty_six_exact_order(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 37)))
        self.assertEqual(self.manifest[-1], (36, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_balanced_source_exact_boundaries(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 36)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 36)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_thirty_six_passages_match_source(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(extract_passage(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_git_blob_manifest_hashes_match(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_thirty_five_reader_preserved(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:-1], self.old_manifest)

    def test_06_substantial_six_movement_fiction(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 6500)
        self.assertGreaterEqual(len(self.reader.split()), 204000)

    def test_07_exclusive_principal_pov_and_guard(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("remains UNAUTHENTICATED", self.chapter)
        for unlicensed in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(unlicensed, self.prose)

    def test_08_invented_ash_not_claimed_historical_fact(self):
        self.assertIn("No real league result", self.chapter)
        self.assertIn("the origin of ash is not proved", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_09_awning_loss_is_observed_not_magically_repaired(self):
        for phrase in ("The first ash lay on the rim of the water bowl",
                       "That was my mother's canvas",
                       "The burn had eaten three narrow holes"):
            self.assertIn(phrase, self.prose)

    def test_10_travelers_have_independent_decision_and_count(self):
        for phrase in ("Fourteen, including the baby",
                       "the carts would stay through morning",
                       "That doesn't tell me where my sister is"):
            self.assertIn(phrase, self.prose)

    def test_11_eren_and_vessa_close_hazardous_route(self):
        for phrase in ("I marked it closed", "The passage is still closed",
                       "She added a second line below the arrow"):
            self.assertIn(phrase, self.prose)

    def test_12_jake_arrival_is_not_an_unearned_wage(self):
        self.assertIn("I'll count the hours when the work is done", self.prose)
        self.assertIn("no hours or wages are credited", self.chapter)
        self.assertIn("This was an instruction, not a wage receipt", self.prose)

    def test_13_old_open_loops_not_falsely_closed(self):
        for phrase in ("missing carrier freight", "Mev-to-Esi letter receipt unknown",
                       "Lysa/Corin still unmarried", "unsafe kiln passage remains closed"):
            self.assertIn(phrase, self.chapter)

    def test_14_protected_canon_and_archive_hash_guard(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)
        for p, expected in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT / p), expected)

    def test_15_reader_chapter_hash_and_no_automatic_promotion(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)
        self.assertIn("Thirty-six fully assembled", self.reader)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("No independent acceptance is established", self.chapter)
        self.assertIn("NO MERGE, NO CANON PROMOTION, NO PUBLICATION", self.chapter)

if __name__ == "__main__":
    unittest.main()
