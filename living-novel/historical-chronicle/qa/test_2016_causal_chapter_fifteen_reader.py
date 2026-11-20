"""NONCANON 2016 causal Chapter XV and exact fifteen-chapter source assembly.
These mechanical checks are not an independent literary/Umpire approval.
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
CHAPTER = "THE_PASSAGE_NO_ONE_COULD_SELL_CHAPTER_15_NONCANON.md"
CHAPTER_SHA = "5bac0a5028acf452790c61ec41391660e86abb9e"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_14_NONCANON.md"
PREVIOUS_SHA = "f106411e875c17952eb6d2f87f248f3e78b6f93d"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_15_NONCANON.md"
READER_SHA = "15edfc5fb050e00cca7b68c41061e538aa01aca7"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->",
    re.S,
)

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class ChapterFifteen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("\n---\n")[0]
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
        cls.matches = list(SECTIONS.finditer(cls.reader))
        cls.before = list(SECTIONS.finditer(cls.old))

    def test_retained_2016_archive_pinned_and_not_fresh(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)
        self.assertIn("not freshly verified ESPN", self.reader)

    def test_chapter_blob_and_actual_five_movement_prose(self):
        self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose),
                         ["I", "II", "III", "IV", "V"])

    def test_owner_pov_is_exclusive(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("PRINCIPAL_CHARACTER", self.chapter)
        self.assertIn("sole interior", self.chapter)
        self.assertNotRegex(self.prose, r"(?im)^### (Edrin|Edin|Oren)\b")

    def test_temporal_cutoff_and_real_owner_firewall(self):
        self.assertIn("before any 2016 postseason character foreknowledge", self.chapter)
        self.assertIn("does not provider-authenticate", self.chapter)
        self.assertNotRegex(self.prose, r"\b\d{2,3}\.\d{2}\s*(?:to|–|-)\s*\d{2,3}\.\d{2}\b")

    def test_new_external_world_has_independent_decisions(self):
        self.assertIn("The boat isn't the orchard.", self.prose)
        self.assertIn("I mean to remain afloat on this one.", self.prose)
        self.assertIn("they can tell us whether they're taking the rest", self.prose)
        self.assertIn("People with nothing to carry can always say a road is too difficult", self.prose)

    def test_open_obligations_and_separate_grain(self):
        self.assertIn("UNFINISHED / UNTURNED", self.chapter)
        self.assertIn("UNSIGNED / UNPROVEN", self.chapter)
        self.assertIn("UNRECOVERED", self.chapter)
        self.assertIn("NOT ACCEPTED OR CONSUMED", self.chapter)
        self.assertIn("separate from the suspect shelter grain", self.chapter)

    def test_noncanon_external_approvals_not_invented(self):
        self.assertIn("NONCANON", self.chapter)
        self.assertIn("Atlas", self.chapter)
        self.assertIn("Umpire", self.chapter)
        self.assertIn("no merge, Founder canon promotion or publication authorized", self.chapter)

    def test_reader_source_blob_pinned(self):
        self.assertEqual(blob(BASE / READER), READER_SHA)

    def test_previous_reader_unchanged(self):
        self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(len(self.before), 14)

    def test_all_fifteen_reader_components_source_exact(self):
        self.assertEqual(len(self.matches), 15)
        for match in self.matches:
            with self.subTest(name=match.group("name")):
                path = BASE / match.group("name")
                self.assertTrue(path.is_file())
                self.assertEqual(blob(path), match.group("sha"))
                self.assertEqual(match.group("body"), path.read_text(encoding="utf-8").rstrip())
        self.assertEqual(self.matches[-1].group("name"), CHAPTER)
        self.assertEqual(self.matches[-1].group("sha"), CHAPTER_SHA)

    def test_prior_fourteen_sections_byte_preserved(self):
        for before, after in zip(self.before, self.matches):
            self.assertEqual(before.group(0), after.group(0))

    def test_reader_manifest_and_substantial_volume(self):
        self.assertIn("Chapters I–XV (NONCANON)", self.reader)
        self.assertIn("Fifteen fully assembled", self.reader)
        self.assertIn("| 15 | " + chr(96) + CHAPTER + chr(96) + " | " + chr(96) + CHAPTER_SHA + chr(96) + " |", self.reader)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 15)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertGreaterEqual(len(self.reader.split()), 74000)

    def test_2026_protected_hard_canon_is_preserved(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
