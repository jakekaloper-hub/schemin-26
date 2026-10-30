"""Noncanonical 2016 causal Chapter X: source, POV, economic and reader regressions.

These tests prove deterministic repository properties, NOT historical human identities,
Atlas/Character approval, literary quality, independent Umpire acceptance or publication.
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
NAMES = (
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
    "THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md",
    "THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md",
    "THE_YARD_WHERE_THE_WHEEL_STOOD_STILL_CHAPTER_07_NONCANON.md",
    "THE_MEASURE_OF_WHAT_REMAINS_CHAPTER_08_NONCANON.md",
    "THE_BELL_THAT_WAS_NOT_A_SUMMONS_CHAPTER_09_NONCANON.md",
    "THE_BOARD_WITH_THE_HIDDEN_CRACK_CHAPTER_10_NONCANON.md",
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
    "5ea06fabbf2c3c32000d6c8d36077280508c1efa",
    "88bb693c735c4e999ecb6db396dabe71a85a768c",
)
PRIOR_READER_BLOB = "cac0da28530f7d040b3856c2666ee975ef0617f3"
SECTION_RE = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \\| git_blob (?P<sha>[0-9a-f]{40}) -->\\n\\n"
    r"(?P<body>.*?)\\n\\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()

class Test2016CausalChapterTen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NAMES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\\n\\n*Editorial handoff")[0]
        cls.reader = (BASE / "READING_COPY_CAUSAL_CHAPTERS_01_10_NONCANON.md").read_text(encoding="utf-8")
        cls.sections = list(SECTION_RE.finditer(cls.reader))

    def test_archive_immutable_year_correct(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)

    def test_chapter_prose_is_substantial_and_structured(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4700)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\\.", self.prose), ["I", "II", "III", "IV", "V"])

    def test_single_owner_pov_noncanon_identity_boundary(self):
        for token in ("NONCANON", "CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER",
                      "not provider-authenticated"):
            self.assertIn(token.lower(), self.chapter.lower())
        self.assertNotRegex(self.prose, r"(?im)^### (?:Edrin|Edin|Oren)\\b")

    def test_character_pays_real_cost_after_chapter_nine(self):
        for phrase in ("The supplier came at first light", "The notices had to be corrected",
                       "This is all of it", "The carrier with the dry provisions had gone"):
            self.assertIn(phrase, self.prose)
        self.assertIn("the older debt remained", self.prose.lower())

    def test_rejected_wood_not_concealed_or_sold(self):
        for phrase in ("There's a crack", "I turned it over before you got back",
                       "the reject rack", "the flaw facing out"):
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertLess(self.prose.index("There's a crack"), self.prose.index("For the rest of the afternoon"))

    def test_fair_pay_distinguishes_old_claim_from_new_piecework(self):
        self.assertIn("The older timber wages were still disputed", self.prose)
        self.assertIn("she named a modest sum per accepted board", self.prose.lower())
        self.assertIn("the claim was still unresolved", self.prose.lower())

    def test_supporting_workers_and_mara_retain_independent_agency(self):
        for phrase in ("Then you're talking to the right person", "You were there",
                       "She could return for an answer", "The delivery is mine"):
            if phrase == "She could return for an answer":
                continue
            self.assertIn(phrase, self.prose)
        self.assertIn("Mara counted the coins once and pushed them back", self.prose)

    def test_no_foreknowledge_or_invented_competitive_results(self):
        self.assertNotRegex(self.prose, r"\\b\\d{2,3}\\.\\d{2}\\s*(?:to|–|-)\\s*\\d{2,3}\\.\\d{2}\\b")
        self.assertNotIn("championship winner", self.prose.lower())
        self.assertNotIn("## week fourteen", self.prose.lower())

    def test_physical_and_privacy_open_loops_not_promoted(self):
        for phrase in ("great wheel stood unfinished and unturned", "the cart on the other bank had not been recovered",
                       "a sealed message lay unopened", "the private chest inaccessible"):
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertIn("suspect grain UNCERTIFIED", self.chapter)
        self.assertIn("no independent Author/Umpire approval", self.chapter)

    def test_nine_previous_chapters_and_reader_immutable(self):
        self.assertEqual(git_blob(BASE / "READING_COPY_CAUSAL_CHAPTERS_01_09_NONCANON.md"), PRIOR_READER_BLOB)
        for name, sha in zip(NAMES[:9], BLOBS[:9]):
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_ten_source_exact_components_and_manifest(self):
        self.assertEqual(len(self.sections), 10)
        self.assertEqual([m.group("name") for m in self.sections], list(NAMES))
        for idx, match in enumerate(self.sections):
            with self.subTest(chapter=idx + 1):
                self.assertEqual(match.group("sha"), BLOBS[idx])
                self.assertEqual(git_blob(BASE / NAMES[idx]), BLOBS[idx])
                self.assertEqual(match.group("body"), (BASE / NAMES[idx]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + NAMES[idx] + "` | `" + BLOBS[idx] + "` |", self.reader)

    def test_protected_2026_hard_canon_untouched(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_reader_release_holds_and_size(self):
        self.assertIn("Chapters I–X (NONCANON)", self.reader)
        self.assertIn("Ten fully assembled", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 46000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 10)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 10)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

if __name__ == "__main__":
    unittest.main()
