"""Source/reader regressions for the noncanonical 2016 causal Chapter IX.

These checks do not verify historical owner identities, approve any fictional
Character/Atlas facts, constitute independent literary review, or authorize release.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest

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
)
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_09_NONCANON.md"
PRIOR_READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_08_NONCANON.md"
PRIOR_BLOB = "cf182ab11be7e200a08d2e8e4bb879d6209e3c9d"
SECTION_RE = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Test2016CausalChapterNine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / NAMES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.sections = list(SECTION_RE.finditer(cls.reader))

    def test_archival_source_stable_and_year_correct(self):
        self.assertEqual(git_blob(ARCHIVE), ARCHIVE_BLOB)
        self.assertEqual(json.loads(ARCHIVE.read_text(encoding="utf-8"))["year"], 2016)

    def test_new_chapter_length_structure_and_identity_firewall(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5000)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.prose), ["I", "II", "III", "IV", "V"])
        for marker in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON", "not provider-authenticated"):
            self.assertIn(marker, self.chapter)

    def test_protagonist_takes_costly_active_action_without_certifying_a_person(self):
        for phrase in (
            "The bell was hanging in the gatehouse",
            "He handed the porter his payment for two copied notices",
            "That was your board money",
            "The new page said there was a private return point",
        ):
            self.assertIn(phrase, self.prose)
        self.assertIn("The sealed message remained unopened", self.prose)

    def test_witness_and_claimant_remain_unverified(self):
        for phrase in (
            "Two copies, one alteration, no known author.",
            "The woman had not heard a name",
        ):
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertIn("The traveler is not proved to be the missing claimant", self.chapter)
        self.assertNotIn("the claimant was found", self.prose.lower())

    def test_physical_and_economic_holds_not_silently_closed(self):
        for phrase in (
            "The great wheel stood unfinished",
            "the cart remained across the broken low crossing",
            "not yet certified the doubtful grain",
            "The sealed message remained unopened",
            "The singer was somewhere he had not been told",
        ):
            self.assertIn(phrase.lower(), self.prose.lower())
        self.assertIn("worker's older timber wages and supplier invoice unpaid", self.chapter)
        self.assertNotIn("the great wheel began to turn", self.prose.lower())

    def test_no_foreknowledge_or_new_unverified_es_score(self):
        self.assertNotRegex(self.prose, r"\b\d{2,3}\.\d{2}\s*(?:to|–|-)\s*\d{2,3}\.\d{2}\b")
        self.assertNotIn("championship winner", self.prose.lower())
        self.assertNotIn("## week fourteen", self.prose.lower())

    def test_superseded_pov_not_reintroduced(self):
        self.assertNotRegex(self.prose, r"(?im)^### (?:Edrin|Edin|Oren)\b")
        self.assertIn("Sole proposed internal POV", self.chapter)
        self.assertIn("No supporting-character interior access", self.chapter)

    def test_previous_reader_and_chapters_immutable(self):
        self.assertEqual(git_blob(PRIOR_READER), PRIOR_BLOB)
        for name, sha in zip(NAMES[:8], BLOBS[:8]):
            with self.subTest(name=name):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_nine_source_exact_components(self):
        self.assertEqual(len(self.sections), 9)
        self.assertEqual([m.group("name") for m in self.sections], list(NAMES))
        for idx, match in enumerate(self.sections):
            with self.subTest(chapter=idx + 1):
                self.assertEqual(match.group("sha"), BLOBS[idx])
                self.assertEqual(git_blob(BASE / NAMES[idx]), BLOBS[idx])
                self.assertEqual(match.group("body"), (BASE / NAMES[idx]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + NAMES[idx] + "` | `" + BLOBS[idx] + "` |", self.reader)

    def test_protected_2026_hard_manuscript_blobs_untouched(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_reader_explicit_noncanon_release_holds(self):
        self.assertIn("Chapters I–IX (NONCANON)", self.reader)
        self.assertIn("Nine fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 40000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 9)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 9)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

if __name__ == "__main__":
    unittest.main()
