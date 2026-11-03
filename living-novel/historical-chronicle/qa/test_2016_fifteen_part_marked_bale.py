"""2016 fifteen-part source-exact NONCANON reader, revised Chapter XVIII cargo continuity."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD = DIR / "READING_COPY_2016_CAUSAL_CH01_17_FOURTEEN_PARTS_MARK_AT_LANDING_V2_NONCANON.md"
NEW = DIR / "READING_COPY_2016_CAUSAL_CH01_18_FIFTEEN_PARTS_MARKED_BALE_V2_NONCANON.md"
CH = DIR / "THE_RIVER_KEPT_NO_PLACE_MARKED_BALE_CH18_V2_NONCANON.md"
ORIGINAL = DIR / "THE_RIVER_KEPT_NO_PLACE_CHAPTER_18_NONCANON.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

def rows(s: str):
    return [(int(n), path, sha, int(words)) for n, path, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", s, flags=re.M)]

def embedded(s: str, filename: str, sha: str):
    start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->\n\n"
    end = f"\n\n<!-- END 2016_CAUSAL {filename} -->"
    i = s.index(start) + len(start)
    return s[i:s.index(end, i)]

class Test2016FifteenPartMarkedBale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text(encoding="utf-8")
        cls.reader = NEW.read_text(encoding="utf-8")
        cls.chapter = CH.read_text(encoding="utf-8")
        cls.original = ORIGINAL.read_text(encoding="utf-8")
        cls.a = rows(cls.reader)
        cls.b = rows(cls.old)

    def test_fifteen_numbered_parts(self):
        self.assertEqual([x[0] for x in self.a], list(range(1, 16)))

    def test_old_fourteen_part_manifest_identical(self):
        self.assertEqual(self.a[:14], self.b)

    def test_all_source_blobs_match_manifest(self):
        for n, name, sha, words in self.a:
            with self.subTest(n=n):
                self.assertEqual(blob((DIR / name).read_bytes()), sha)

    def test_exact_source_bodies_embedded(self):
        for n, name, sha, words in self.a:
            with self.subTest(n=n):
                self.assertEqual(embedded(self.reader,name,sha).rstrip("\n"),(DIR/name).read_text(encoding="utf-8").rstrip("\n"))

    def test_prior_fourteen_embedded_unchanged(self):
        for n, name, sha, words in self.b:
            with self.subTest(n=n):
                self.assertEqual(embedded(self.reader,name,sha),embedded(self.old,name,sha))

    def test_counted_words_and_total(self):
        for n, name, sha, words in self.a:
            with self.subTest(n=n):
                self.assertEqual(len((DIR/name).read_text(encoding="utf-8").split()),words)
        self.assertEqual(sum(x[3] for x in self.a), 98459)
        self.assertIn("Source words including chapter metadata: 98459",self.reader)

    def test_new_fiction_substantive_and_section_numbering(self):
        self.assertGreater(len(self.chapter.split()),len(self.original.split())+1400)
        self.assertIn("### V. The part the river carried",self.chapter)
        self.assertIn("### VI. The counting on the bank",self.chapter)

    def test_cargo_custody_kept_open(self):
        self.assertIn("The original binding remains uncut",self.chapter)
        self.assertIn("it remains in my boat",self.chapter)
        self.assertIn("I did not see inside the bale",self.chapter)

    def test_time_and_payment_are_fictional(self):
        self.assertIn("Two paid fictional workdays",self.chapter)
        self.assertIn("no new league fact",self.chapter)

    def test_single_eligible_interior_and_noncanon_gate(self):
        self.assertIn("Sole limited interior viewpoint",self.chapter)
        self.assertIn("Jake alone has interior POV",self.chapter)
        self.assertIn("NO MERGE",self.reader)
        self.assertIn("NONCANON",self.reader)

    def test_archive_untouched(self):
        self.assertEqual(blob(ARCHIVE.read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_protected_main_bytes(self):
        expected={"PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a6c6d8ee723bf39fc7dfaf0",
          "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
          "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
          "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
        for name,sha in expected.items():
            with self.subTest(name=name):
                self.assertEqual(blob((ROOT/"living-novel/manuscript"/name).read_bytes()),sha)

if __name__ == "__main__": unittest.main()
