"""Chapter LII: 52-section exact reader; limited POV, noncanon historical firewall and release HOLD."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_MAN_WHO_HAD_NOT_VANISHED_CHAPTER_52_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_52_NONCANON.md"
PRIOR = "READING_COPY_CAUSAL_CHAPTERS_01_51_NONCANON.md"
CHAPTER_SHA = "f78b68521e622e3c60ee9e8ee42534f57fee8c2c"
READER_SHA = "9133694e759ac689cfd5b240e9b670b3d921b501"
PRIOR_SHA = "40a07dc448a9a7643ea3460fab665f68e8e495ec"
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

class ChapterFiftyTwo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.rows = rows(cls.reader)
        cls.prior_rows = rows(cls.prior)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 53)))

    def test_02_final_manifest_row(self):
        self.assertEqual(self.rows[-1], (52, CHAPTER, CHAPTER_SHA, 5604))

    def test_03_complete_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 52)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 52)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_04_all_assembled_sources_exact(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(source(self.reader, name, sha), (BASE / name).read_text().strip())
                self.assertEqual(len((BASE / name).read_text().split()), words)

    def test_05_all_sources_blob_pinned(self):
        for n, name, sha, _ in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_06_previous_reader_blob_unchanged(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_07_previous_manifest_exact(self):
        self.assertEqual(self.rows[:51], self.prior_rows)

    def test_08_previous_sections_exact(self):
        for _, name, sha, _ in self.prior_rows:
            with self.subTest(source=name):
                self.assertEqual(source(self.reader, name, sha), source(self.prior, name, sha))

    def test_09_chapter_blob(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_10_reader_blob(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_11_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5604)

    def test_12_substantial_narrative(self):
        self.assertGreaterEqual(len(self.prose.split()), 4900)

    def test_13_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_14_reader_header(self):
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–LII (NONCANON)"))
        self.assertIn("Fifty-two fully assembled", self.reader)

    def test_15_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 303892)

    def test_16_historical_provenance_firewall(self):
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)

    def test_17_exclusive_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(Edrin|Edin|Oren)\b")

    def test_18_return_is_real_fictional_turn(self):
        self.assertIn('Tovin made a sound so quiet Jake first took it for a cough.', self.prose)
        self.assertIn('"Aven?"', self.prose)
        self.assertIn('"Yes."', self.prose)

    def test_19_remaining_seven_unlocated(self):
        self.assertIn("Seven other travelers remained unlocated", self.prose)
        self.assertIn("no person present had learned what happened to those seven", self.prose)

    def test_20_hessa_and_ilyen_not_in_scene(self):
        self.assertIn("Hessa and Ilyen had gone out that morning", self.prose)
        self.assertIn("Hessa and Ilyen walked in search", self.prose)

    def test_21_witness_does_not_confirm_other_fates(self):
        self.assertIn('I don\'t know.', self.prose)
        self.assertIn('I can\'t tell you what happened to the others.', self.prose)

    def test_22_four_witness_coins_remain(self):
        self.assertIn("Four had already gone toward Sela's portable floor", self.prose)
        self.assertIn("I still have half the coins", self.prose)

    def test_23_no_official_watch_granted(self):
        self.assertIn("He was not an officer.", self.prose)
        self.assertIn("No law had appeared out of the argument.", self.prose)

    def test_24_no_old_aven_collision(self):
        self.assertNotRegex(self.prior, r"\bAven\b")

    def test_25_main_canon_protected(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_26_archive_protected(self):
        self.assertEqual(git_blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

    def test_27_qa_release_holds(self):
        qa = (BASE / "CHAPTER_52_SOURCE_EDITORIAL_QA_RECEIPT.md").read_text()
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, qa)

    def test_28_chapter_hold(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("Founder approval remain outstanding", self.chapter)

    def test_29_reader_prior_51_markers_unchanged(self):
        for _, name, sha, _ in self.prior_rows:
            self.assertEqual(self.reader.count(f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"), 1)

    def test_30_no_matchup_made_up_in_prose(self):
        self.assertNotRegex(self.prose, r"\b(\d{2,3}\.\d{1,2}|Week [0-9]+|league standings)\b")

if __name__ == "__main__":
    unittest.main()
