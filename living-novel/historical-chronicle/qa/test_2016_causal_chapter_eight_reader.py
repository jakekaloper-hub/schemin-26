"""Regression checks for source-exact noncanonical 2016 causal Chapter VIII.

These tests cannot establish real human-owner identity, literary acceptance,
approved historical material culture, Atlas certification or Umpire approval.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
NAMES = (
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
    "THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md",
    "THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md",
    "THE_YARD_WHERE_THE_WHEEL_STOOD_STILL_CHAPTER_07_NONCANON.md",
    "THE_MEASURE_OF_WHAT_REMAINS_CHAPTER_08_NONCANON.md",
)
BLOBS = (
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
    "8994f9e443a6313dee217dfd5f92aedeff7bd88c",
    "40d12860e93d9393b18d7771c427061c82e46c8c",
    "4e3d655895847e9910b7e8c69349fb2b09c94b4b",
    "419e7f6775d0205cf1b49dba5629500245ac59a8",
    "5266de4f74ee1b9154672acfc7c5f50dc881347c",
)
PRIOR_READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_07_NONCANON.md"
PRIOR_BLOB = "060176ee8e3cb0548ec72e378ca4c7137765a442"
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_08_NONCANON.md"
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)
HARD_CANON = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Test2016CausalChapterEight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NAMES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reader))

    def test_archive_pinned_year_and_no_owner_certification(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)
        self.assertIn("not proof of human Jake", self.chapter)

    def test_eighth_chapter_length_and_five_movements(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4700)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose), ["I", "II", "III", "IV", "V"])
        self.assertIn("# The Measure of What Remains", self.chapter)

    def test_non_recap_causal_drama_and_independent_craft(self):
        for phrase in ("a smaller test piece", "I do, if it is mine.", "the stool",
                       "she wrote an answer in her own hand"):
            self.assertIn(phrase, self.prose)
        self.assertNotIn("## Week Fourteen", self.prose)

    def test_wheel_not_activated_and_no_premature_commission(self):
        for phrase in ("The great wheel outside", "never turned", "it isn't signed",
                       "a test he could trust"):
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertNotIn("the great wheel began to turn", self.prose.lower())
        self.assertNotIn("the commission was paid", self.prose.lower())

    def test_continuity_of_separate_irreversible_holds(self):
        for phrase in ("The old disputed timber wages", "doubtful grain",
                       "a cart remained trapped", "singer's destination",
                       "lower crossing unsafe"):
            self.assertIn(phrase.lower(), self.chapter.lower())
        self.assertNotIn("the grain was safe to eat", self.prose.lower())

    def test_exclusive_principal_pov_and_human_firewall(self):
        for token in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON", "HOLD"):
            self.assertIn(token, self.chapter)
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertIn("no secondary-character interiority", self.chapter)

    def test_predecessor_reader_and_chapter_blobs_immutable(self):
        self.assertEqual(git_blob(PRIOR_READER), PRIOR_BLOB)
        for name, sha in zip(NAMES[:7], BLOBS[:7]):
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_eight_component_source_exact_assembly(self):
        self.assertEqual(len(self.sections), 8)
        self.assertEqual([x.group("name") for x in self.sections], list(NAMES))
        for i, match in enumerate(self.sections):
            with self.subTest(chapter=i+1):
                self.assertEqual(match.group("sha"), BLOBS[i])
                self.assertEqual(git_blob(BASE / NAMES[i]), BLOBS[i])
                self.assertEqual(match.group("body"), (BASE / NAMES[i]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `"+NAMES[i]+"` | `"+BLOBS[i]+"` |", self.reader)

    def test_protected_hard_canon_not_mutated(self):
        hard = ROOT / "living-novel/manuscript"
        for name, sha in HARD_CANON.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(hard / name), sha)

    def test_reader_has_open_approval_holds_and_no_release(self):
        self.assertIn("Chapters I–VIII (NONCANON)", self.reader)
        self.assertIn("Eight fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 35500)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 8)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 8)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

if __name__ == "__main__":
    unittest.main()
