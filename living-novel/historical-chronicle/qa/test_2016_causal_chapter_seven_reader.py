"""NONCANON 2016 causal Chapter VII and exact seven-chapter reading assembly.

This checks reproducible source linkage, scene constraints, and textual continuity.
It cannot approve fictional Atlas geography, human owner identity, the prose's
literary quality, independent review, canon promotion, or publication.
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
NAMES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
    "THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md",
    "THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md",
    "THE_YARD_WHERE_THE_WHEEL_STOOD_STILL_CHAPTER_07_NONCANON.md",
]
BLOBS = [
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
    "8994f9e443a6313dee217dfd5f92aedeff7bd88c",
    "40d12860e93d9393b18d7771c427061c82e46c8c",
    "4e3d655895847e9910b7e8c69349fb2b09c94b4b",
    "419e7f6775d0205cf1b49dba5629500245ac59a8",
]
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_07_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_06_NONCANON.md"
PREVIOUS_SHA = "21f750ebfce30f3f8b80e1ef326a47e84598a9d2"
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Test2016CausalChapterSeven(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.chapter = (BASE / NAMES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.sections = list(SECTIONS.finditer(cls.reader))

    def test_historical_archive_is_pinned_not_live(self):
        self.assertEqual(blob(ARCHIVE), ARCHIVE_SHA)
        self.assertEqual(self.archive["year"], 2016)
        self.assertIn("not a claim about the actual owner", self.chapter)
        self.assertIn("NOT provider-authenticated", self.chapter)
        self.assertIn("no postseason outcomes", self.chapter)

    def test_chapter_has_substantive_five_part_scene(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4600)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ", self.prose), ["I", "II", "III", "IV", "V"])
        self.assertIn("# The Yard Where the Wheel Stood Still", self.chapter)

    def test_external_pressure_not_matchup_recap(self):
        self.assertIn("The first sound Jake heard at the mill", self.prose)
        self.assertIn("the return channel", self.prose)
        self.assertIn("The cart remained in the rut.", self.prose)
        self.assertNotIn("## Week Fourteen", self.prose)

    def test_unturned_wheel_and_independent_worker_agency(self):
        for phrase in ("The shaft is still wrong", "It has never held a suspended load",
                       "Then give me work I can answer for.", "No great wheel had turned"):
            self.assertIn(phrase, self.prose)
        self.assertNotIn("the great wheel began to turn", self.prose.lower())

    def test_borrowed_shed_expires_and_suspect_grain_not_certified(self):
        for phrase in ("The borrowed ones can go after", "They finished clearing the borrowed bay",
                       "Those are still on the stones", "Not until I know what it is"):
            self.assertIn(phrase, self.prose)
        self.assertNotIn("the grain was certified safe", self.prose.lower())

    def test_live_jeopardy_resolved_without_hazardous_bridge_crossing(self):
        self.assertIn("The high path reaches that bank", self.prose)
        self.assertIn("Then we take the strain off it before we unfasten it.", self.prose)
        self.assertIn("The animal came free.", self.prose)
        self.assertNotIn("Jake crossed the broken bridge", self.prose)

    def test_material_and_emotional_open_loops_carried_forward(self):
        for token in ("the singer had not reappeared", "Mara still held the unopened sealed message",
                      "the private chest", "The supplier's invoice",
                      "The great wheel remained upright and unfinished"):
            self.assertIn(token, self.prose)
        self.assertIn("suspect grain is not certified edible", self.chapter)

    def test_principal_pov_and_noncanon_release_firewall(self):
        for token in ("CHAR-JAKE-KALOPER", "PRINCIPAL_CHARACTER", "NONCANON", "HOLD"):
            self.assertIn(token, self.chapter)
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertIn("No secondary-character interiority", self.chapter)
        self.assertIn("Nothing is merged, promoted or published", self.chapter)

    def test_previous_reader_and_six_manuscripts_unchanged(self):
        self.assertEqual(blob(PREVIOUS), PREVIOUS_SHA)
        for name, sha in zip(NAMES[:6], BLOBS[:6]):
            with self.subTest(name=name):
                self.assertEqual(blob(BASE / name), sha)

    def test_exact_seven_chapter_manifest_and_assembly(self):
        self.assertEqual(len(self.sections), 7)
        self.assertEqual([m.group("name") for m in self.sections], NAMES)
        for i, match in enumerate(self.sections):
            with self.subTest(name=NAMES[i]):
                self.assertEqual(match.group("sha"), BLOBS[i])
                self.assertEqual(blob(BASE / NAMES[i]), BLOBS[i])
                self.assertEqual(match.group("body"), (BASE / NAMES[i]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + NAMES[i] + "` | `" + BLOBS[i] + "` |", self.reader)

    def test_reader_release_gates_and_full_length(self):
        self.assertIn("Chapters I–VII (NONCANON)", self.reader)
        self.assertIn("Seven fully assembled", self.reader)
        self.assertIn("independent Authors Council/Umpire review", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertGreaterEqual(len(self.reader.split()), 31000)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 7)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 7)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

if __name__ == "__main__":
    unittest.main()
