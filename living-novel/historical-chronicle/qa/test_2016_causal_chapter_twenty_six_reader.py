"""Chapter XXVI noncanonical causal reader regressions.

These are mechanical/content-boundary tests, NOT character, Atlas,
independent Authors Council, Umpire or Founder canon approvals.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_BOARD_AT_THE_OPEN_DOOR_CHAPTER_26_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_26_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_25_NONCANON.md"
CHAPTER_SHA = "5957266328b8035684c59a1e8c0501f657e05d59"
READER_SHA = "0027269704900b8ecb9d7a10c958cec963bd1df0"
PREVIOUS_SHA = "7e2bd8b000523441785eacf34bb741f58530b5f1"
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
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$", doc, re.M)]

def passage(doc, name, sha):
    first = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    last = f"<!-- END 2016_CAUSAL {name} -->"
    assert doc.count(first) == 1 and doc.count(last) == 1, name
    return doc.split(first, 1)[1].split(last, 1)[0].strip()

class TwentySixChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_source_and_order(self):
        self.assertEqual([r[0] for r in self.manifest], list(range(1, 27)))
        self.assertEqual(self.manifest[-1][1:], (CHAPTER, CHAPTER_SHA, len(self.chapter.split())))
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 26)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 26)

    def test_02_source_exact_assembly_all_26(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                src = (BASE / name).read_text(encoding="utf-8")
                self.assertEqual(passage(self.reader, name, sha), src.strip())
                self.assertEqual(len(src.split()), words)

    def test_03_git_blob_sources_match_manifest(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_04_previous_reader_immutable(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.old_manifest, self.manifest[:25])

    def test_05_previous_25_passages_unchanged(self):
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(passage(self.reader, name, sha), passage(self.old, name, sha))

    def test_06_substantial_five_movement_fiction(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5500)
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
        self.assertIn("### Editorial handoff", self.chapter)
        self.assertIn("The Board at the Open Door", self.chapter)

    def test_07_owner_exclusive_pov_provenance_boundary(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        self.assertIn("NOT an authenticated historical ESPN owner-slot association", self.chapter)
        for disallowed in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(disallowed, self.prose)

    def test_08_real_paid_hours_no_kiln_reopening(self):
        for phrase in (
            "Four hours, if you work all four",
            "The kiln is still shut",
            "The four hours ended before the work ended",
            "Aren counted out the agreed payment for four hours of outside work",
            "The kiln was still closed",
        ):
            self.assertIn(phrase, self.prose)

    def test_09_eren_commission_completed_and_paid(self):
        for phrase in (
            "The woman tested the chalk in the bare center",
            "counted out the payment into Eren's palm",
            "The work was finished",
            "Eren's sign was hanging over a real doorway",
        ):
            self.assertIn(phrase, self.prose)

    def test_10_sign_makes_no_false_meal_promise(self):
        for phrase in (
            "My picture isn't going to promise something the kitchen can't make",
            "You can make them large enough to read from the turn",
            "The panel took the writing and released it",
        ):
            self.assertIn(phrase, self.prose)

    def test_11_vessa_safety_and_eren_future_hold(self):
        for phrase in (
            "The watch is covered tonight",
            "I didn't promise the next season",
            "The crossing will stay shut until I say otherwise",
        ):
            self.assertIn(phrase, self.prose)

    def test_12_money_and_unsent_letter_not_conflated(self):
        for phrase in (
            "No cart was leaving for the lower market that night",
            "He folded the letter and put it under the whetstone, unsealed",
            "They did not pay the pledge by being saved",
        ):
            self.assertIn(phrase, self.prose)

    def test_13_historical_archive_unmodified(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(path), ARCHIVE_SHA)

    def test_14_protected_2026_manuscripts_unmodified(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / name), sha)

    def test_15_new_reader_fingerprint_and_editorial_hold(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)
        self.assertGreaterEqual(len(self.reader.split()), 140000)
        self.assertIn("Twenty-six fully assembled", self.reader)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("no founder-only promotion, merge or publication", self.chapter.lower())

if __name__ == "__main__":
    unittest.main()
