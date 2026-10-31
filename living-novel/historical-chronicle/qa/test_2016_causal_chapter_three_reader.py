"""Noncanonical 2016 causal Chapter III and exact three-chapter reading-copy QA.

Deterministic source and structure checks are not historical-owner authentication,
Atlas/Character canon approval, literary acceptance or an independent Umpire.
"""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
SOURCE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
FILES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
]
BLOBS = [
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
]
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_03_NONCANON.md"
SECTIONS = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def score(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))

class Test2016CausalChapterThree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.chapter = (BASE / FILES[2]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.matches = list(SECTIONS.finditer(cls.reader))

    def test_source_is_same_archived_2016_evidence(self):
        self.assertEqual(git_blob(SOURCE), SOURCE_BLOB)
        self.assertEqual(self.source["year"], 2016)

    def test_w8_scoring_slot_one_result_is_correct(self):
        rows = next(x["matchups"] for x in self.source["weeks"] if x["week"] == 8)
        matches = [x for x in rows if x["home_id"] == 1 or x["away_id"] == 1]
        self.assertEqual(len(matches), 1)
        row = matches[0]
        self.assertEqual((row["home_id"], row["away_id"], row["winner"]), (1, 10, "HOME"))
        self.assertEqual((score(row["hp"]), score(row["ap"])), (Decimal("85.90"), Decimal("59.28")))
        self.assertIn("85.90 to 59.28", self.prose)

    def test_w9_loss_is_retained_but_not_brought_forward_in_day_scene(self):
        rows = next(x["matchups"] for x in self.source["weeks"] if x["week"] == 9)
        matches = [x for x in rows if x["home_id"] == 1 or x["away_id"] == 1]
        self.assertEqual(len(matches), 1)
        row = matches[0]
        self.assertEqual((row["home_id"], row["away_id"], row["winner"]), (9, 1, "HOME"))
        self.assertEqual((score(row["hp"]), score(row["ap"])), (Decimal("122.10"), Decimal("97.32")))
        self.assertNotIn("122.10", self.prose)
        self.assertNotIn("97.32", self.prose)
        self.assertIn("deliberately OMITTED", self.chapter)

    def test_substantial_five_movement_causal_prose(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4300)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ", self.chapter), ["I", "II", "III", "IV", "V"])
        self.assertNotIn("## Week Eight", self.prose)
        self.assertNotIn("## Week Nine", self.prose)

    def test_pov_and_world_rights_are_hold_not_claimed(self):
        for term in ("NONCANON", "CHAR-JAKE-KALOPER", "proposed fiction", "HOLD"):
            self.assertIn(term, self.chapter)
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertNotIn("El Niño said", self.prose)

    def test_canvas_and_singer_were_not_silently_appropriated(self):
        for term in ("singer", "printer", "permission", "seamstress",
                     "canvas owner", "canvas had been", "own coat"):
            self.assertIn(term, self.prose.lower())
        self.assertIn("a new bargain", self.prose.lower())

    def test_worker_and_wheel_have_actual_discrete_decisions(self):
        for term in ("two mornings", "unsafe lift", "wheelwright", "daughter",
                     "repaired heel", "refused", "inspection"):
            self.assertIn(term, self.prose.lower())
        self.assertIn("The wheel remained still", self.prose)

    def test_unpaid_obligations_and_missing_person_remain_open(self):
        for term in ("unpaid", "closed", "missing claimant", "Mara", "bowl"):
            self.assertIn(term.lower(), self.chapter.lower())
        self.assertIn("UNKNOWN", self.chapter)
        self.assertIn("not a", self.prose.lower())

    def test_three_component_manifest_has_genuine_git_blobs(self):
        self.assertEqual(len(self.matches), 3)
        self.assertEqual([m.group("name") for m in self.matches], FILES)
        for idx, m in enumerate(self.matches):
            with self.subTest(file=FILES[idx]):
                self.assertEqual(m.group("sha"), BLOBS[idx])
                self.assertEqual(git_blob(BASE / FILES[idx]), BLOBS[idx])
                self.assertEqual(m.group("body"), (BASE / FILES[idx]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + FILES[idx] + "` | `" + BLOBS[idx] + "` |", self.reader)

    def test_reader_is_substantial_and_keeps_release_holds(self):
        self.assertGreaterEqual(len(self.reader.split()), 13000)
        self.assertIn("Chapters I–III (NONCANON)", self.reader)
        self.assertIn("Founder-only canon/publication", self.reader)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reader)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL"), 3)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL"), 3)

if __name__ == "__main__":
    unittest.main()
