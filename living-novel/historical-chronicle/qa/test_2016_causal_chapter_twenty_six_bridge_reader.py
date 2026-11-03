"""Source-exact NONCANON 2016 23-part edition: original Chapters I–XXVI.

Mechanical tests only. No historical manager authentication or Umpire acceptance.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "READING_COPY_2016_CAUSAL_CH01_26_TWENTY_THREE_PARTS_OPEN_DOOR_NONCANON.md"
OLD = "READING_COPY_2016_CAUSAL_CH01_25_TWENTY_TWO_PARTS_UNSTRUCK_BELL_V2_NONCANON.md"
CH25 = "THE_MILE_BEYOND_THE_WEIGH_STONES_THE_UNSTRUCK_BELL_CH25_V2_NONCANON.md"
CH26 = "THE_BOARD_AT_THE_OPEN_DOOR_CHAPTER_26_NONCANON.md"
OLD_SHA = "57e85e48b4d03c16f0b318f163888d8a59f0de62"
CH25_SHA = "49b1929c26a2feea252f98e88cdf982880f50a6f"
CH26_SHA = "5957266328b8035684c59a1e8c0501f657e05d59"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(w)) for n, name, sha, w in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", text, re.M)]

def embedded(text, name, sha):
    first = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    last = f"<!-- END 2016_CAUSAL {name} -->"
    assert text.count(first) == text.count(last) == 1, name
    return text.split(first, 1)[1].split(last, 1)[0].strip()

class TwentyThreePartBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = (BASE / NEW).read_text()
        cls.previous_reader = (BASE / OLD).read_text()
        cls.chapter25 = (BASE / CH25).read_text()
        cls.chapter26 = (BASE / CH26).read_text()
        cls.manifest = rows(cls.reader)
        cls.previous = rows(cls.previous_reader)

    def test_01_manifest_contains_twenty_three_ordered_parts(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 24)))
        self.assertEqual(len(self.previous), 22)
        self.assertEqual(self.manifest[-2][1], CH25)
        self.assertEqual(self.manifest[-1][1], CH26)

    def test_02_every_part_is_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(part=n):
                source = (BASE / name).read_text()
                self.assertEqual(embedded(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_03_every_manifest_sha_is_real_git_blob(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(blob(BASE / name), sha)

    def test_04_prior_reader_unchanged(self):
        self.assertEqual(blob(BASE / OLD), OLD_SHA)
        self.assertEqual(self.manifest[:22], self.previous)

    def test_05_prior_twenty_two_embedded_bodies_unchanged(self):
        for n, name, sha, _ in self.previous:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.reader, name, sha),
                                 embedded(self.previous_reader, name, sha))

    def test_06_chapter25_v2_and_original_chapter26_immutable(self):
        self.assertEqual(blob(BASE / CH25), CH25_SHA)
        self.assertEqual(blob(BASE / CH26), CH26_SHA)

    def test_07_chapter_boundary_proves_arrival_without_wages(self):
        self.assertIn("He had crossed the entire distance and acquired no wage", self.chapter25)
        self.assertIn("No hours had been entered", self.chapter25)
        self.assertIn("The kiln remains closed at Chapter XXVI opening", self.chapter25)

    def test_08_four_hours_only_earned_next_day(self):
        self.assertIn("### I. An hour that belonged to somebody", self.chapter26)
        self.assertIn("Four hours, if you work all four", self.chapter26)
        self.assertIn("He had been paid for four hours", self.chapter26)
        self.assertIn("The kiln was still closed", self.chapter26)

    def test_09_safety_authority_and_independent_agency(self):
        self.assertIn("Vessa", self.chapter25)
        self.assertIn("Vessa", self.chapter26)
        self.assertIn("Noll", self.chapter25)
        self.assertIn("Noll", self.chapter26)
        self.assertIn("Eren", self.chapter26)
        self.assertIn("Vessa retains independent kiln safety authority", self.reader)

    def test_10_no_unearned_financial_or_letter_settlement(self):
        self.assertIn("They did not pay the pledge by being saved", self.chapter26)
        self.assertIn("He folded the letter and put it under the whetstone, unsealed", self.chapter26)
        self.assertIn("unsent", self.chapter26.lower())

    def test_11_proposed_twelve_owner_interior_and_historical_hold(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.reader)
        self.assertIn("Historical 2016 owner identity is unverified", self.reader)
        for forbidden in ("Edrin", "Edin"):
            self.assertNotIn(forbidden, self.chapter26)

    def test_12_retained_competitive_archive_exact(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(path), ARCHIVE_SHA)

    def test_13_hard_canon_exactly_preserved(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_14_source_words_and_noncanon_gate(self):
        self.assertEqual(sum(words for _, _, _, words in self.manifest), 158161)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 23)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 23)
        self.assertIn("NO CANON PROMOTION", self.reader)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL", self.reader)

if __name__ == "__main__":
    unittest.main()
