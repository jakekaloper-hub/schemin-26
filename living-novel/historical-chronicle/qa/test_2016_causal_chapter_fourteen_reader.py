"""Mechanical checks for NONCANON 2016 causal Chapter XIV and exact reader.

No historical human-owner authentication, independent editor approval or Umpire ruling.
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
CHAPTER = "WHAT_WAS_LEFT_IN_THE_YARD_CHAPTER_14_NONCANON.md"
CHAPTER_SHA = "f76ec3ae5245bccf57a8df2a3f3d76001319c68e"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_13_NONCANON.md"
PREVIOUS_SHA = "761395226ade49cfbf907697ee7b41411cb9c3e2"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_14_NONCANON.md"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->",
    re.S
)

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class ChapterFourteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("\n---\n")[0]
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
        cls.matches = list(SECTIONS.finditer(cls.reader))
        cls.before = list(SECTIONS.finditer(cls.old))

    def test_archival_source_pinned(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)

    def test_new_chapter_sha_and_substantial_five_movements(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertGreaterEqual(len(self.chapter.split()), 5000)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose),
                         ["I", "II", "III", "IV", "V"])

    def test_only_owner_interiority_and_no_retired_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("PRINCIPAL_CHARACTER", self.chapter)
        self.assertNotRegex(self.prose, r"(?im)^### (Edrin|Edin|Oren)\b")
        self.assertIn("sole interior", self.chapter)

    def test_no_postseason_foreknowledge_or_false_scoring(self):
        self.assertIn("before any 2016 postseason character foreknowledge", self.chapter)
        self.assertNotRegex(self.prose, r"\b\d{2,3}\.\d{2}\s*(?:to|–|-)\s*\d{2,3}\.\d{2}\b")
        self.assertIn("does not provider-authenticate", self.chapter)

    def test_earned_interpersonal_and_material_consequence(self):
        self.assertIn("The burned worker", self.prose)
        self.assertIn("the work there must be kept apart", self.prose)
        self.assertIn("I didn't examine it", self.prose)
        self.assertIn("will not move the measures", self.prose)

    def test_ongoing_unfinished_wheel_and_noncontract(self):
        self.assertIn("UNFINISHED / UNTURNED", self.chapter)
        self.assertIn("UNSIGNED / UNPROVEN", self.chapter)
        self.assertIn("That is not a contract with the buyer", self.prose)
        self.assertIn("not restore the mill", self.chapter)

    def test_noncanon_external_holds(self):
        self.assertIn("NONCANON", self.chapter)
        self.assertIn("Atlas", self.chapter)
        self.assertIn("Umpire", self.chapter)
        self.assertIn("No real external purchase", self.chapter)
        self.assertIn("no independent Author/Umpire approval is claimed", self.chapter)

    def test_old_reader_fingerprint_and_thirteen_components(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(len(self.before), 13)

    def test_all_fourteen_components_exact(self):
        self.assertEqual(len(self.matches), 14)
        for match in self.matches:
            with self.subTest(name=match.group("name")):
                target = BASE / match.group("name")
                self.assertTrue(target.is_file())
                self.assertEqual(blob(target), match.group("sha"))
                self.assertEqual(match.group("body"), target.read_text(encoding="utf-8").rstrip())
        self.assertEqual(self.matches[-1].group("name"), CHAPTER)
        self.assertEqual(self.matches[-1].group("sha"), CHAPTER_SHA)

    def test_prior_thirteen_segments_preserved_byte_identically(self):
        for prev, curr in zip(self.before, self.matches):
            self.assertEqual(prev.group(0), curr.group(0))

    def test_reader_manifest_and_volume(self):
        self.assertIn("Chapters I–XIV (NONCANON)", self.reader)
        self.assertIn("Fourteen fully assembled", self.reader)
        self.assertIn("| 14 | `"+CHAPTER+"` | `"+CHAPTER_SHA+"` |", self.reader)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 14)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertGreaterEqual(len(self.reader.split()), 68000)

    def test_protected_2026_main_blobs_unchanged(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
