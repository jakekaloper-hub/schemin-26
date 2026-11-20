"""Noncanonical 2016 Chapter XII / source-exact twelve-chapter reader checks.

These are mechanical provenance and continuity guards, not literary approval,
historical human-owner authentication, independent Umpire review, or release.
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
NEW = "THE_PRICE_OF_A_VOICE_CHAPTER_12_NONCANON.md"
NEW_BLOB = "722cc9318e744d7ab8fdae5fdd4fb0af775d1745"
PRIOR_READER = "READING_COPY_CAUSAL_CHAPTERS_01_11_NONCANON.md"
PRIOR_READER_BLOB = "f98525bd9611879a0750abd913746ecc90e7a7c6"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_12_NONCANON.md"
READER_BLOB = "962b15a3a4a25e1fd7a1cae116febed79ff046f0"
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
    ("THE_HOUSE_BEYOND_THE_MARKER_CHAPTER_11_NONCANON.md", "94c81b98a9dc9d308a8d2d4801e7482a1a170f74"),
)
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

class Test2016CausalTwelve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NEW).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("\n---\n")[0]
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reader))

    def test_archival_year_and_immutable_source(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)

    def test_new_prose_substantive_and_five_movements(self):
        self.assertEqual(blob(BASE / NEW), NEW_BLOB)
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertGreaterEqual(len(self.prose.split()), 5700)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose),
                         ["I", "II", "III", "IV", "V"])

    def test_single_canonical_owner_interior_pov_scope(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("one of the twelve owner characters", self.chapter)
        self.assertIn("not provider-authenticated", self.chapter.lower())
        self.assertNotRegex(self.prose, r"(?im)^### (?:Edrin|Edin|Oren)\b")
        self.assertNotIn("el niño was a man", self.prose.lower())

    def test_novel_causality_without_inventing_league_results(self):
        self.assertIn("Chapter XI", self.chapter)
        self.assertIn("Week 13", self.chapter)
        self.assertIn("but precede any character knowledge of the 2016 postseason", self.chapter)
        self.assertNotRegex(self.prose, r"\b\d{2,3}\.\d{2}\s*(?:to|–|-)\s*\d{2,3}\.\d{2}\b")

    def test_singer_agency_and_unresolved_refunds(self):
        self.assertIn("I won't perform under those tickets", self.prose)
        self.assertIn("some people received their money back", self.prose.lower())
        self.assertIn("not all", self.prose.lower())
        self.assertIn("You promised them my work", self.prose)

    def test_shelter_consent_firewall(self):
        self.assertIn("We have received no such agreement", self.prose)
        self.assertIn("Mara has not agreed", self.prose)
        self.assertIn("No revenue is promised to, received by, or disbursed from the shelter", self.chapter)

    def test_continuity_carries_old_woman_and_boy(self):
        self.assertIn("old woman's cup", self.prose.lower())
        self.assertIn("bench had not been replaced", self.prose.lower())
        self.assertIn("boy", self.prose.lower())

    def test_open_loop_safeguards(self):
        tail = self.chapter.split("### Editorial handoff")[-1].lower()
        for phrase in ["claimant", "unopened", "inaccessible", "uncertified",
                       "unrecovered", "unpaid", "unturned", "unknown"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, tail)

    def test_predecessor_reader_immutable(self):
        self.assertEqual(blob(BASE / PRIOR_READER), PRIOR_READER_BLOB)

    def test_all_prior_chapter_blobs_immutable(self):
        for name, sha in PREVIOUS:
            with self.subTest(name=name):
                self.assertEqual(blob(BASE / name), sha)

    def test_twelve_source_exact_ordered_components(self):
        self.assertEqual(len(self.sections), 12)
        expected = list(PREVIOUS) + [(NEW, NEW_BLOB)]
        self.assertEqual([(m.group("name"), m.group("sha")) for m in self.sections], expected)
        for match in self.sections:
            with self.subTest(name=match.group("name")):
                source = BASE / match.group("name")
                self.assertEqual(blob(source), match.group("sha"))
                self.assertEqual(match.group("body"), source.read_text(encoding="utf-8").rstrip())

    def test_reader_manifest_and_noncanonical_hold(self):
        self.assertEqual(blob(BASE / READER), READER_BLOB)
        self.assertIn("Chapters I–XII (NONCANON)", self.reader)
        self.assertIn("Twelve fully assembled", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertIn("| 12 | `" + NEW + "` | `" + NEW_BLOB + "` |", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 58000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 12)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 12)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_2026_protected_hard_canon_blobs(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / "living-novel/manuscript" / name), sha)

if __name__ == "__main__":
    unittest.main()
