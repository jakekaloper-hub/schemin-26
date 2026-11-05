"""Developmental 2016 19-part causal reader — Chapter XXII V2, NONCANON / no release authority."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = D / "READING_COPY_2016_CAUSAL_CH01_21_EIGHTEEN_PARTS_BLANK_LEAF_V2_NONCANON.md"
NEW = D / "READING_COPY_2016_CAUSAL_CH01_22_NINETEEN_PARTS_DRY_END_OF_THE_HOUSE_NONCANON.md"
CH = D / "THE_COVER_AND_THE_CARGO_DRY_END_OF_THE_HOUSE_CH22_V2_NONCANON.md"
ORIGINAL = D / "THE_COVER_AND_THE_CARGO_CHAPTER_22_NONCANON.md"
CH21 = D / "THE_BOOK_THAT_WALKED_OUT_PRICE_OF_A_BLANK_LEAF_CH21_V2_NONCANON.md"

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(value: str):
    return [(int(n), f, sha, int(words)) for n, f, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", value, re.M)]

def body(value: str, filename: str, sha: str) -> str:
    before = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->\n\n"
    after = f"\n\n<!-- END 2016_CAUSAL {filename} -->"
    return value.split(before, 1)[1].split(after, 1)[0]

class ChapterXXIINineteenPartReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text()
        cls.new = NEW.read_text()
        cls.chapter = CH.read_text()
        cls.original = ORIGINAL.read_text()
        cls.old_rows = rows(cls.old)
        cls.new_rows = rows(cls.new)

    def test_01_previous_reader_blob_pinned(self):
        self.assertEqual(blob(OLD.read_bytes()), "ca70cfa0537be1c0dc5327c858ec2e812483ea27")

    def test_02_original_ch22_blob_pinned(self):
        self.assertEqual(blob(ORIGINAL.read_bytes()), "7b2ce956d5aa2836d6f2d30a3520d8c521e870c7")

    def test_03_ch21_v2_blob_pinned(self):
        self.assertEqual(blob(CH21.read_bytes()), "8b931790f8d860d120b03ef503a8e08b8422dafa")

    def test_04_manifest_has_nineteen_parts(self):
        self.assertEqual([r[0] for r in self.new_rows], list(range(1, 20)))

    def test_05_first_eighteen_rows_unchanged(self):
        self.assertEqual(self.new_rows[:18], self.old_rows)

    def test_06_source_bytes_and_words_pinned(self):
        for i, f, sha, n in self.new_rows:
            with self.subTest(part=i):
                b = (D / f).read_bytes()
                self.assertEqual(blob(b), sha)
                self.assertEqual(len(b.decode("utf-8").split()), n)

    def test_07_all_bodies_exact(self):
        for i, f, sha, n in self.new_rows:
            with self.subTest(part=i):
                self.assertEqual(body(self.new, f, sha), (D / f).read_text().rstrip("\n"))

    def test_08_first_eighteen_bodies_exact_to_previous(self):
        for i, f, sha, n in self.old_rows:
            with self.subTest(part=i):
                self.assertEqual(body(self.old, f, sha), body(self.new, f, sha))

    def test_09_total_source_words(self):
        self.assertEqual(sum(row[3] for row in self.new_rows), 128850)
        self.assertIn("Source words including chapter metadata: 128850", self.new)

    def test_10_chapter_length_and_scene(self):
        self.assertEqual(len(self.chapter.split()), 8925)
        self.assertIn("#### The dry end of the house", self.chapter)
        self.assertIn("The first sack made its noise before anyone saw it move.", self.chapter)

    def test_11_delivery_acceptance_not_retroactively_cancelled(self):
        self.assertIn("the three measured sacks had been carried into the kitchen.", self.chapter.lower())
        self.assertIn("the agent asked for the original signed entry.", self.chapter.lower())

    def test_12_nell_retains_undelivered_cloth(self):
        self.assertIn('“This stays with me,” she said.', self.chapter)
        self.assertIn('“It\'s not back,” she said. “It\'s here with me.”', self.chapter)
        self.assertIn("remaining soap", self.chapter)

    def test_13_no_new_shelter_claim_settlement(self):
        self.assertIn("The flour could still become tomorrow's bread. Not all of it.", self.chapter)
        self.assertIn("Jake's pledge remain unresolved", self.chapter)

    def test_14_esi_agency_and_len_disability(self):
        self.assertIn("Esi took the bucket herself and carried it out.", self.chapter)
        self.assertIn("Len approached on his good side", self.chapter)

    def test_15_no_speculative_espen_history(self):
        self.assertIn("No new ESPN result", self.chapter)
        self.assertIn("No historical manager-slot identity is provider authenticated", self.chapter)
        self.assertIn("fictional, unapproved secondary-world inventions", self.chapter)

    def test_16_noncanon_release_barriers(self):
        self.assertIn("NONCANON", self.new)
        self.assertIn("NO MERGE", self.new)
        self.assertIn("NO PUBLICATION", self.new)
        self.assertIn("NO CANON PROMOTION", self.new)

    def test_17_protected_main_files_hash_identical(self):
        expected = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for fn, sha in expected.items():
            with self.subTest(file=fn):
                self.assertEqual(blob((ROOT / "living-novel/manuscript" / fn).read_bytes()), sha)

    def test_18_frozen_2016_archive(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(p.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_19_original_investigation_not_reordered(self):
        order = ["### I. The notice at the weigh-stones", "### II. What a book could buy",
                 "### III. The refused load", "### IV. The place where the leaves had gone",
                 "### V. A burden measured twice"]
        indexes = [self.chapter.index(x) for x in order]
        self.assertEqual(indexes, sorted(indexes))

    def test_20_developmental_boundaries(self):
        self.assertIn("19-Part Developmental Reading", self.new)
        self.assertIn("Founder-only", self.new)
        self.assertIn("Historical owner authentication", self.new)

if __name__ == "__main__":
    unittest.main()
