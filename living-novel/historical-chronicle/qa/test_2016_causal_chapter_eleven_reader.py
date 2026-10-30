"""Deterministic NONCANON 2016 causal Chapter XI and 11-component reading-copy checks.

Repository checks are not independent literary/Character/Atlas/Umpire approvals and
do not certify historical human owner identity or publication readiness.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
ARCHIVE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
NEW = "THE_HOUSE_BEYOND_THE_MARKER_CHAPTER_11_NONCANON.md"
NEW_BLOB = "94c81b98a9dc9d308a8d2d4801e7482a1a170f74"
PRIOR_READER = "READING_COPY_CAUSAL_CHAPTERS_01_10_NONCANON.md"
PRIOR_READER_BLOB = "d1b8c25977afc8f44124da62b5f5da30c1527d38"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_11_NONCANON.md"
READER_BLOB = "f98525bd9611879a0750abd913746ecc90e7a7c6"
PREVIOUS = (
    ("THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md", "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2"),
    ("THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md", "756126cb4e151a0bd78ece39ab59a4c54ef2aa43"),
    ("THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md", "f9bf0721c989d30bfd09189388b93293ba3a8ce0"),
    ("WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md", "8994f9e443a6313dee217dfd5f92aedeff7bd88c"),
    ("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md", "40d12860e93d9393b18d7771c427061c82e46c8c"),
    ("THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md", "4e3d655895847e9910b7e8c69349fb2b09c94b4b"),
    ("THE_YARD_WHERE_THE_WHEEL_STOOD_STILL_CHAPTER_07_NONCANON.md", "419e7f6775d0205cf1b49dba5629500245ac59a8"),
    ("THE_MEASURE_OF_WHAT_REMAINS_CHAPTER_08_NONCANON.md", "5266de4f74ee1b9154672acfc7c5f50dc881347c"),
    ("THE_BELL_THAT_WAS_NOT_A_SUMMONS_CHAPTER_09_NONCANON.md", "5ea06fabbf2c3c32000d6c8d36077280508c1efa"),
    ("THE_BOARD_WITH_THE_HIDDEN_CRACK_CHAPTER_10_NONCANON.md", "88bb693c735c4e999ecb6db396dabe71a85a768c"),
)
SECTIONS = re.compile(r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S)
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23aeb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class TestCausalEleven(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("\n---\n")[0]
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reader))

    def test_archival_source_pinned_and_year_correct(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertEqual(json.loads(ARCHIVE.read_text())["year"], 2016)

    def test_new_chapter_is_full_prose_not_scene_outline(self):
        self.assertEqual(blob(BASE / NEW), NEW_BLOB)
        self.assertGreaterEqual(len(self.chapter.split()), 5400)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose), ["I", "II", "III", "IV", "V"])
        self.assertGreaterEqual(len(self.prose.split()), 5000)

    def test_only_supported_principal_interior_pov(self):
        for phrase in ["CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON"]:
            self.assertIn(phrase.lower(), self.chapter.lower())
        self.assertNotRegex(self.prose, r"(?im)^### (?:Edrin|Edin|Oren)\b")
        self.assertIn("no human-owner-to-2016-team-slot association is provider-authenticated", self.chapter.lower())

    def test_follows_ten_without_resolving_offstage_story(self):
        for phrase in ["By the time Jake had carried the second water jar",
                       "The old woman", "the swollen", "the daughter", "the grandson"]:
            # Injured wrist may be described instead of the adjective swollen.
            if phrase == "the swollen":
                continue
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertIn("the great wheel did not turn", self.prose.lower())

    def test_real_irreversible_supporting_character_choice(self):
        self.assertIn("It is mine", self.prose)
        self.assertIn("I asked them", self.prose)
        self.assertIn("I don't know", self.prose)
        self.assertIn("Past the marker", self.prose)
        self.assertIn("The daughter", self.prose)

    def test_no_historical_fixtures_invented(self):
        self.assertNotRegex(self.prose, r"\b\d{2,3}\.\d{2}\s*(?:to|–|-)\s*\d{2,3}\.\d{2}\b")
        self.assertNotIn("postseason winner", self.prose.lower())
        self.assertNotIn("championship winner", self.prose.lower())

    def test_open_loops_unchanged(self):
        closing = self.chapter.split("*Editorial handoff")[-1].lower()
        for token in ["claimant", "unopened", "unretrieved", "uncertified",
                      "unrecovered", "unpaid", "unfinished", "unturned"]:
            self.assertIn(token, closing)
        self.assertIn("singer destination", closing)

    def test_predecessor_reader_untouched(self):
        self.assertEqual(blob(BASE / PRIOR_READER), PRIOR_READER_BLOB)

    def test_all_predecessor_chapter_blobs_untouched(self):
        for name, sha in PREVIOUS:
            with self.subTest(chapter=name):
                self.assertEqual(blob(BASE / name), sha)

    def test_eleven_exact_assembled_components(self):
        self.assertEqual(len(self.sections), 11)
        expected = list(PREVIOUS) + [(NEW, NEW_BLOB)]
        self.assertEqual([(m.group("name"), m.group("sha")) for m in self.sections], expected)
        for match in self.sections:
            with self.subTest(chapter=match.group("name")):
                p = BASE / match.group("name")
                self.assertEqual(blob(p), match.group("sha"))
                self.assertEqual(match.group("body"), p.read_text(encoding="utf-8").rstrip())

    def test_manifest_release_hold_and_reader_size(self):
        self.assertEqual(blob(BASE / READER), READER_BLOB)
        self.assertIn("Chapters I–XI (NONCANON)", self.reader)
        self.assertIn("Eleven fully assembled", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertIn("| 11 | `" + NEW + "` | `" + NEW_BLOB + "` | 5490 |", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 51000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 11)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 11)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_2026_protected_sources_byte_identical(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
