"""NONCANON Chapter XVII reader regression; must run on a checked-out PR #243 branch.

This test does not approve historic identities, fictional geography or canon promotion.
"""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
READER = DIR / "READING_COPY_CAUSAL_CHAPTERS_01_17_NONCANON.md"
PREVIOUS = DIR / "READING_COPY_CAUSAL_CHAPTERS_01_16_NONCANON.md"
CHAPTER_17 = "THE_HOURS_BETWEEN_HAMMERS_CHAPTER_17_NONCANON.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()


def manifest(text: str) -> list[tuple[int, str, str, int]]:
    return [
        (int(n), name, sha, int(words))
        for n, name, sha, words in re.findall(
            r"^[|] ([0-9]+) [|] `([^`]+)` [|] `([a-f0-9]{40})` [|] ([0-9]+) [|]$",
            text, re.MULTILINE,
        )
    ]


def get_embedded(text: str, name: str, sha: str) -> str:
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->\n\n"
    end = f"\n\n<!-- END 2016_CAUSAL {name} -->"
    left = text.index(start) + len(start)
    right = text.index(end, left)
    return text[left:right]


class Test2016CausalChapterSeventeenReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text()
        cls.previous = PREVIOUS.read_text()
        cls.rows = manifest(cls.reader)
        cls.chapter = (DIR / CHAPTER_17).read_text()

    def test_exact_seventeen_chapter_rows(self):
        self.assertEqual([n for n, *_ in self.rows], list(range(1, 18)))

    def test_source_text_exact_for_all_seventeen_chapters(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(get_embedded(self.reader, name, sha).rstrip("\n"), (DIR / name).read_text().rstrip("\n"))

    def test_all_seventeen_git_blob_references_match_bytes(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob((DIR / name).read_bytes()), sha)

    def test_manifest_words_match_all_seventeen(self):
        for n, name, sha, words in self.rows:
            with self.subTest(chapter=n):
                self.assertEqual(len((DIR / name).read_text().split()), words)

    def test_all_original_sixteen_reading_segments_preserved(self):
        first = "<!-- BEGIN 2016_CAUSAL THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md"
        last = "<!-- END 2016_CAUSAL THE_WORK_THAT_CROSSED_BACK_CHAPTER_16_NONCANON.md -->"
        a = self.previous[self.previous.index(first): self.previous.index(last) + len(last)]
        b = self.reader[self.reader.index(first): self.reader.index(last) + len(last)]
        self.assertEqual(a, b)

    def test_new_prose_substantive(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4500)
        self.assertIn("### V. The hour after work", self.chapter)

    def test_single_authorized_focal_character(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("No Edrin/Edin", self.chapter)

    def test_proposed_location_and_noncanon_holds_explicit(self):
        self.assertIn("NONCANON", self.chapter)
        self.assertIn("Atlas", self.chapter)
        self.assertIn("HOLD", self.chapter)
        self.assertIn("NONCANON", self.reader)

    def test_stoneworks_day_one_not_return(self):
        self.assertIn("His second day had not yet begun.", self.chapter)
        self.assertIn("DELIVERY UNCONFIRMED", self.chapter)
        self.assertIn("UNPAID", self.chapter)

    def test_archive_git_blob_unchanged(self):
        self.assertEqual(git_blob(ARCHIVE.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_protected_2026_opening_blobs_unchanged(self):
        pinned = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for name, sha in pinned.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob((ROOT / "living-novel/manuscript" / name).read_bytes()), sha)


if __name__ == "__main__":
    unittest.main()
