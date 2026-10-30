"""Mechanical NONCANON Chapter XIII and exact 2016 causal reader checks.

Not author approval, historical identity authentication, or a Umpire verdict.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
CHAPTER = "THE_DOOR_THAT_FED_THE_FIRE_CHAPTER_13_NONCANON.md"
CHAPTER_SHA = "f238e02a331467db03060f66ff711b65f5a92d04"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_12_NONCANON.md"
PREVIOUS_SHA = "962b15a3a4a25e1fd7a1cae116febed79ff046f0"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_13_NONCANON.md"
READER_SHA = "761395226ade49cfbf907697ee7b41411cb9c3e2"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \\| git_blob (?P<sha>[0-9a-f]{40}) -->\\n\\n"
    r"(?P<body>.*?)\\n\\n<!-- END 2016_CAUSAL (?P=name) -->",
    re.S
)

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()

class ChapterThirteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("\\n---\\n")[0]
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
        cls.matches = list(SECTIONS.finditer(cls.reader))
        cls.before = list(SECTIONS.finditer(cls.old))

    def test_archival_source_pinned_not_new_live_claim(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(json.loads(ARCHIVE.read_text())["year"], 2016)

    def test_chapter_stable_substantive_and_movements(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertGreaterEqual(len(self.chapter.split()), 5000)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\\.", self.prose),
                         ["I", "II", "III", "IV", "V"])

    def test_exclusive_principal_pov_and_firewall(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("PRINCIPAL_CHARACTER", self.chapter)
        self.assertIn("not provider-authenticated", self.chapter)
        self.assertNotRegex(self.prose, r"(?im)^### (Edrin|Edin|Oren)\\b")

    def test_no_postseason_foreknowledge_or_fabricated_scores(self):
        self.assertIn("before any 2016 postseason character foreknowledge", self.chapter)
        self.assertNotRegex(self.prose, r"\\b\\d{2,3}\\.\\d{2}\\s*(?:to|–|-)\\s*\\d{2,3}\\.\\d{2}\\b")

    def test_fire_has_cost_without_belated_triumph(self):
        self.assertIn("I opened the door", self.prose)
        self.assertIn("now you've given the fire a way down", self.prose)
        self.assertIn("The worker was alive, but the mill was damaged", self.prose)

    def test_daughter_agency_and_unproved_trial(self):
        self.assertIn("There's no trial in a room we can't enter", self.prose)
        self.assertIn("They asked", self.prose)
        self.assertIn("UNSIGNED / UNPROVEN", self.chapter)

    def test_explicit_noncanonical_atlas_and_independent_hold(self):
        self.assertIn("NONCANON", self.chapter)
        self.assertIn("Atlas", self.chapter)
        self.assertIn("Umpire", self.chapter)
        self.assertIn("No independent reviewers", self.chapter)

    def test_prior_reader_pinned_immutable(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(len(self.before), 12)

    def test_all_thirteen_source_exact(self):
        self.assertEqual(len(self.matches), 13)
        for m in self.matches:
            with self.subTest(m=m.group("name")):
                p = BASE / m.group("name")
                self.assertTrue(p.is_file())
                self.assertEqual(blob(p), m.group("sha"))
                self.assertEqual(m.group("body"), p.read_text(encoding="utf-8").rstrip())
        self.assertEqual(self.matches[-1].group("name"), CHAPTER)
        self.assertEqual(self.matches[-1].group("sha"), CHAPTER_SHA)

    def test_all_twelve_prior_assemblies_preserved(self):
        for a, b in zip(self.before, self.matches):
            self.assertEqual(a.group(0), b.group(0))

    def test_reader_exact_blob_and_manifest(self):
        self.assertEqual(blob(BASE / READER), READER_SHA)
        self.assertIn("Chapters I–XIII (NONCANON)", self.reader)
        self.assertIn("Thirteen fully assembled", self.reader)
        self.assertIn("| 13 | `"+CHAPTER+"` | `"+CHAPTER_SHA+"` |", self.reader)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 13)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertGreaterEqual(len(self.reader.split()), 63000)

    def test_protected_2026_main_manuscript_bytes(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
