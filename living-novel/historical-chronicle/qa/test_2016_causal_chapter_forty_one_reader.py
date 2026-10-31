"""Chapter XLI source-exact assembly, POV, continuity and canon-preservation checks.

All proof is author-side technical only; no independent editorial approval is claimed.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_MARKS_AT_THE_CROSSROADS_CHAPTER_41_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_41_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_40_NONCANON.md"
CHAPTER_SHA = "4526f2c278167c43630aa10732f10e47a8fb1ef1"
READER_SHA = "14ce93a324f62cf00307625c486bdbc17e4dd5f4"
PREVIOUS_SHA = "ecc93dfe2100ed68f9aa49e59c0427fc2dbf6295"
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


def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", text, re.M)]


def extract(reader, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(opening) == reader.count(closing) == 1
    return reader.split(opening, 1)[1].split(closing, 1)[0].strip()


class FortyOneChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous_manifest = rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_is_ordered_41_and_word_count_current(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 42)))
        self.assertEqual(self.manifest[-1], (41, CHAPTER, CHAPTER_SHA, 7884))

    def test_02_all_markers_present_once(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 41)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 41)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_source_exact_for_all_41(self):
        for number, name, sha, words in self.manifest:
            with self.subTest(number=number):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_manifest_git_blob_integrity_all_41(self):
        for number, name, sha, _ in self.manifest:
            with self.subTest(number=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_40_reader_frozen_and_exact(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:40], self.previous_manifest)
        for number, name, sha, _ in self.previous_manifest:
            with self.subTest(number=number):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_new_reader_hash_pinned(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_new_prose_is_substantial_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 7500)
        self.assertGreaterEqual(len(self.reader.split()), 237000)

    def test_08_exclusive_twelve_owner_interior_focalizer(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_09_continuity_from_chapter_forty(self):
        for marker in ("six", "twenty-one nights", "apprentice", "boat-cover maker",
                       "Orin", "Hessa", "blue", "cart", "Ina"):
            self.assertIn(marker, self.chapter)

    def test_10_new_turn_is_actual_not_an_outline(self):
        for marker in ("Sela", "Corin", "Lysa", "Daro", "the chalk door",
                       "tools", "No one had finished the six chalk strokes"):
            self.assertIn(marker, self.prose)

    def test_11_private_shelter_not_unapproved_public_law(self):
        self.assertIn("neither public lodging nor law", self.chapter)
        self.assertIn("not a public shelter or law", self.chapter.lower())
        self.assertNotIn("official public refuge was established", self.prose)

    def test_12_no_fabricated_water_or_route_certification(self):
        self.assertIn("water safety", self.chapter)
        self.assertIn("unverified open patch", self.chapter)
        self.assertNotIn("safe to drink now", self.prose)

    def test_13_freight_and_fire_remain_unresolved(self):
        for marker in ("Hessa's missing sister", "second horse", "distant fire",
                       "Mael and Pell", "Esi's letter", "escaped bird", "kiln passage"):
            self.assertIn(marker, self.chapter)
        self.assertNotIn("the missing freight was recovered", self.prose)

    def test_14_no_invented_competitive_claims_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertNotRegex(self.prose, r"\b(?:Week [0-9]+|playoff|championship)\b")

    def test_15_main_hard_canon_blobs_preserved(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_16_2016_evidence_blob_preserved(self):
        f = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(f), ARCHIVE_SHA)

    def test_17_noncanon_and_founder_gates_explicit(self):
        self.assertTrue(self.chapter.startswith("# The Marks at the Crossroads"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLI"))
        for token in ("NONCANON / INDEPENDENT EDITORIAL HOLD", "NO MERGE",
                      "NO CANON PROMOTION", "NO PUBLICATION", "UNAUTHENTICATED"):
            self.assertIn(token, self.chapter)

    def test_18_no_main_protected_authority_replaced(self):
        self.assertIn("independent Umpire", self.reader)
        self.assertIn("Neither the official 2016 Historical Chronicle nor protected", self.reader)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_19_material_character_autonomy_survives(self):
        for character in ("Sela", "Hessa", "Ina", "Corin", "Lysa", "Eren",
                          "Fara", "apprentice"):
            self.assertIn(character, self.prose)
        self.assertIn("He hasn't agreed to work for me again", self.prose)


if __name__ == "__main__":
    unittest.main()
