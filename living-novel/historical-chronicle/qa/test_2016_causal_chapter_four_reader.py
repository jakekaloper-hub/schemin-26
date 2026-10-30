"""2016 causal-novel Chapter IV and exact four-component reader assertions.

These tests do not authenticate human-owner identity, period geography, literary
approval, Umpire independence or Founder canon/publication acceptance.
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
SOURCE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
FILES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
    "THE_WORK_OF_UNTURNED_THINGS_CHAPTER_03_NONCANON.md",
    "WHAT_THE_WALL_KEPT_CHAPTER_04_NONCANON.md",
]
BLOBS = [
    "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
    "f9bf0721c989d30bfd09189388b93293ba3a8ce0",
    "8994f9e443a6313dee217dfd5f92aedeff7bd88c",
]
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_04_NONCANON.md"
SECTION = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def points(x):
    return Decimal(str(x)).quantize(Decimal("0.01"))

class Test2016CausalChapterFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.chapter = (BASE / FILES[-1]).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("---\n\n*Editorial handoff")[0]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.sections = list(SECTION.finditer(cls.reader))

    def test_pinned_2016_archive(self):
        self.assertEqual(blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.data["year"], 2016)

    def test_week_ten_slot_one_defeat_exact(self):
        rows = next(w["matchups"] for w in self.data["weeks"] if w["week"] == 10)
        matches = [r for r in rows if r["home_id"] == 1 or r["away_id"] == 1]
        self.assertEqual(len(matches), 1)
        m = matches[0]
        self.assertEqual((m["home_id"], m["away_id"], m["winner"]), (1, 6, "AWAY"))
        self.assertEqual((points(m["hp"]), points(m["ap"])), (Decimal("82.12"), Decimal("125.84")))
        self.assertIn("82.12 to 125.84", self.prose)

    def test_week_eleven_distinct_hyenas_accurate(self):
        rows = next(w["matchups"] for w in self.data["weeks"] if w["week"] == 11)
        matches = [r for r in rows if r["home_id"] == 1 or r["away_id"] == 1]
        self.assertEqual(len(matches), 1)
        m = matches[0]
        self.assertEqual((m["home_id"], m["away_id"], m["winner"]), (12, 1, "HOME"))
        self.assertEqual((points(m["hp"]), points(m["ap"])), (Decimal("114.72"), Decimal("100.10")))
        self.assertIn("114.72 to 100.10", self.prose)
        self.assertIn("another distinct team entry", self.prose.lower())

    def test_substantial_causal_unit_and_time_passage(self):
        self.assertGreaterEqual(len(self.chapter.split()), 3800)
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\. ", self.chapter), ["I", "II", "III", "IV", "V"])
        self.assertIn("two days later", self.prose)
        self.assertIn("A week later", self.prose)
        self.assertNotIn("## Week Ten", self.prose)
        self.assertNotIn("## Week Eleven", self.prose)

    def test_first_three_chapters_and_protected_2026_unchanged_in_manifest(self):
        for i in range(3):
            self.assertEqual(blob(BASE / FILES[i]), BLOBS[i])
        self.assertNotIn("living-novel/manuscript/", FILES[-1])

    def test_one_approved_owner_pov_only(self):
        for term in ("NONCANON", "CHAR-JAKE-KALOPER", "HOLD", "not provider-authenticated"):
            self.assertIn(term.lower(), self.chapter.lower())
        self.assertNotRegex(self.prose, r"(?m)^### (Edrin|Edin|Oren)\b")
        self.assertNotIn("El Niño said", self.prose)

    def test_expired_canvas_not_secretly_reused(self):
        for term in ("market awning", "original three-night canvas returned",
                     "another", "strictly temporary"):
            self.assertIn(term.lower(), self.chapter.lower())
        self.assertIn("not the canvas that had sheltered", self.prose.lower())

    def test_distinct_claimants_and_open_repairs(self):
        for term in ("woman with the chest", "key", "missing claimant", "separate",
                     "unbuilt", "unpaid", "closed", "unopened"):
            self.assertIn(term.lower(), self.chapter.lower())
        self.assertIn("The absent claimant was a different person", self.prose)
        self.assertNotIn("the missing claimant was found", self.prose.lower())

    def test_real_four_part_exact_reader_not_summary(self):
        self.assertEqual(len(self.sections), 4)
        self.assertEqual([s.group("name") for s in self.sections], FILES)
        for i, item in enumerate(self.sections):
            with self.subTest(filename=FILES[i]):
                self.assertEqual(item.group("sha"), BLOBS[i])
                self.assertEqual(blob(BASE / FILES[i]), BLOBS[i])
                self.assertEqual(item.group("body"), (BASE / FILES[i]).read_text(encoding="utf-8").rstrip())
                self.assertIn("| `" + FILES[i] + "` |", self.reader)

    def test_reader_status_and_length(self):
        self.assertGreaterEqual(len(self.reader.split()), 17000)
        self.assertIn("Chapters I–IV (NONCANON)", self.reader)
        self.assertIn("independent Authors Council/Umpire", self.reader)
        self.assertIn("HOLD", self.reader)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reader)

if __name__ == "__main__":
    unittest.main()
