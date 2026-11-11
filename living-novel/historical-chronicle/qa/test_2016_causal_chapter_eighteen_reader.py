"""Source-exact, draft-only regression for 2016 causal Chapter XVIII.
No ESPN result or editor approval can be inferred from a green test run.
Run: python3 -m unittest living-novel/historical-chronicle/qa/test_2016_causal_chapter_eighteen_reader.py -v
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "THE_RIVER_KEPT_NO_PLACE_CHAPTER_18_NONCANON.md"
LAST = "READING_COPY_CAUSAL_CHAPTERS_01_17_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_18_NONCANON.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ORIGINALS = [
    ("living-novel/manuscript/PROLOGUE_DRAFT_V1.md", "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0"),
    ("living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md", "26a17f05eb0565e7648c29add03ee9580ec933c3"),
    ("living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md", "30fcf23a3eb8872fa0fb4dff029fe30044141121"),
    ("living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md", "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"),
]
EXPECTED_ARCHIVE = "6dbec1fe2537139f3a97c6a78250e2bae082a518"

def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()

def rows(text):
    m = re.findall(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", text, flags=re.M)
    return [(int(n), name, sha, int(words)) for n, name, sha, words in m]

def embedded(text, name, sha):
    opening = "<!-- BEGIN 2016_CAUSAL " + name + " | git_blob " + sha + " -->"
    closing = "<!-- END 2016_CAUSAL " + name + " -->"
    assert text.count(opening) == 1 and text.count(closing) == 1
    return text.split(opening, 1)[1].split(closing, 1)[0].strip()

class ChapterEighteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.old = (BASE / LAST).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)

    def test_eighteen_ordered_manifest_rows(self):
        self.assertEqual([x[0] for x in self.manifest], list(range(1, 19)))
        self.assertEqual(self.manifest[-1][1], NEW)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 18)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 18)

    def test_all_eighteen_components_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                contents = (BASE / name).read_text()
                self.assertEqual(embedded(self.reader, name, sha), contents.strip())
                self.assertEqual(len(contents.split()), words)

    def test_manifest_git_blobs_are_real(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(blob_sha(BASE / name), sha)

    def test_prior_seventeen_unchanged(self):
        self.assertEqual(self.old_manifest, self.manifest[:17])
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(embedded(self.reader, name, sha), embedded(self.old, name, sha))
        self.assertEqual(blob_sha(BASE / LAST), "7ba3cf83ff59d187929a71861c1d053abbb05140")

    def test_chapter_is_substantial_five_movement_fiction(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4800)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 5)
        self.assertIn("The river moved past both of them", self.chapter)

    def test_only_one_eligible_owner_interior(self):
        opening = self.chapter.split("### I.", 1)[0]
        prose = self.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]
        self.assertIn("CHAR-JAKE-KALOPER", opening)
        self.assertIn("Sole limited interior viewpoint", opening)
        for retired in ("Edrin", "Edin", "Master Oren"):
            self.assertNotIn(retired, prose)

    def test_second_day_wage_and_return_not_reconciliation(self):
        self.assertIn("two groups, one for the first day and one for the second", self.chapter)
        self.assertIn("Jake set off inland.", self.chapter)
        self.assertIn("has NOT reached the shelter", self.chapter)
        self.assertIn("DELIVERY UNCONFIRMED", self.chapter)

    def test_fictional_second_day_not_fabricated_league_result(self):
        prose = self.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]
        self.assertNotIn("ESPN", prose)
        self.assertNotIn("Week 14", prose)
        self.assertNotIn("postseason", prose.lower())
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", prose))

    def test_protected_hard_canon_has_exact_blob_fingerprints(self):
        for name, pinned in ORIGINALS:
            self.assertEqual(blob_sha(ROOT / name), pinned)

    def test_pinned_historical_archive_is_untouched(self):
        self.assertEqual(blob_sha(ARCHIVE), EXPECTED_ARCHIVE)
        self.assertIn("2016 scoring slot 1", self.chapter)

    def test_gates_explicitly_remain_hold(self):
        for phrase in ("NONCANON", "independent editorial HOLD", "Founder canon/publication approval NOT GRANTED"):
            self.assertIn(phrase, self.chapter)
        self.assertIn("Founder-only canon/publication gates remain", self.reader)

    def test_reader_total_and_new_last_source(self):
        self.assertGreater(len(self.reader.split()), 90000)
        self.assertGreater(len(self.reader), len(self.old))
        self.assertIn("Chapters I–XVIII", self.reader)
        self.assertEqual(self.manifest[-1][2], blob_sha(BASE / NEW))

if __name__ == "__main__":
    unittest.main()
