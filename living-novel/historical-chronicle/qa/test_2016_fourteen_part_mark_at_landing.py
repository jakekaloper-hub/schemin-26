"""NONCANON 2016 Ch XVII V2 / fourteen-part developmental edition regression.

Technical provenance checks are not historical owner authentication or literary approval.
"""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = DIR / "READING_COPY_2016_CAUSAL_CH01_17_FOURTEEN_PARTS_MARK_AT_LANDING_V2_NONCANON.md"
OLD = DIR / "READING_COPY_2016_CAUSAL_CH01_16_THIRTEEN_PARTS_ROOF_THAT_TRAVELED_V2_NONCANON.md"
V2_NAME = "THE_HOURS_BETWEEN_HAMMERS_THE_MARK_AT_THE_LANDING_CH17_V2_NONCANON.md"
ORIGINAL_NAME = "THE_HOURS_BETWEEN_HAMMERS_CHAPTER_17_NONCANON.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def rows(text: str):
    return [
        (int(n), filename, sha, int(words))
        for n, filename, sha, words in re.findall(
            r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$",
            text, flags=re.M,
        )
    ]


def embedded(reader: str, filename: str, sha: str):
    begin = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->\n\n"
    end = f"\n\n<!-- END 2016_CAUSAL {filename} -->"
    at = reader.index(begin) + len(begin)
    return reader[at: reader.index(end, at)]


class Test2016FourteenPartMarkAtLanding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = NEW.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.chapter = (DIR / V2_NAME).read_text(encoding="utf-8")
        cls.original = (DIR / ORIGINAL_NAME).read_text(encoding="utf-8")
        cls.manifest = rows(cls.text)

    def test_fourteen_parts_numbered(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 15)))

    def test_last_source_is_chapter_xvii_v2(self):
        self.assertEqual(self.manifest[-1][1], V2_NAME)

    def test_source_blob_ids_match_every_file(self):
        for n, filename, sha, words in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(blob((DIR / filename).read_bytes()), sha)

    def test_embedded_text_exact_for_all_fourteen(self):
        for n, filename, sha, words in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.text, filename, sha).rstrip("\n"), (DIR / filename).read_text().rstrip("\n"))

    def test_word_count_per_body_and_total(self):
        for n, filename, sha, words in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(len((DIR / filename).read_text().split()), words)
        self.assertEqual(sum(r[3] for r in self.manifest), 90945)
        self.assertIn("Source words including chapter metadata: 90945", self.text)

    def test_first_thirteen_reading_segments_unchanged(self):
        oldrows = rows(self.old)
        self.assertEqual(self.manifest[:13], oldrows)
        for n, filename, sha, words in oldrows:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.text, filename, sha), embedded(self.old, filename, sha))

    def test_original_chapter_preserved_and_new_section_added(self):
        self.assertGreater(len(self.chapter.split()), len(self.original.split()) + 1500)
        self.assertIn("### V. The Mark at the Landing", self.chapter)
        self.assertIn("### VI. The hour after work", self.chapter)
        self.assertIn("### V. The hour after work", self.original)

    def test_open_cargo_question_without_false_receipt(self):
        self.assertIn("No cloth unloaded at the works. No condition decided.", self.chapter)
        self.assertIn("The original binding stays intact", self.chapter)
        self.assertIn("No cloth unloaded", self.chapter)

    def test_second_day_and_wages_not_claimed_complete(self):
        self.assertIn("His second day had not yet begun.", self.chapter)
        self.assertIn("his old shelter pledge and debts remain UNPAID", self.chapter)

    def test_single_provisional_pov(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("No Edrin/Edin", self.chapter)

    def test_draft_gate_explicit(self):
        self.assertIn("NONCANON", self.text)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL", self.text)
        self.assertIn("NO MERGE", self.text)

    def test_archive_2016_unchanged(self):
        self.assertEqual(blob(ARCHIVE.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_protected_2026_hard_manuscript_untouched(self):
        pinned = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for name, sha in pinned.items():
            with self.subTest(name=name):
                self.assertEqual(blob((ROOT / "living-novel/manuscript" / name).read_bytes()), sha)


if __name__ == "__main__":
    unittest.main()
