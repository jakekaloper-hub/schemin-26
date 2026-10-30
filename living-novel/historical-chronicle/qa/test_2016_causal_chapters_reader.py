"""2016 draft causal-novel Chapter Two and source-exact two-chapter reader checks.

Automated tests do not prove independently reviewed fiction, Atlas/Character
authority, historical human-owner identity or Founder release acceptance.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
FILES = [
    "THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md",
    "THE_NAMES_BEYOND_THE_WALL_CHAPTER_02_NONCANON.md",
]
READER = BASE / "READING_COPY_CAUSAL_CHAPTERS_01_02_NONCANON.md"
RECEIPT = BASE / "CHAPTER_02_SOURCE_EDITORIAL_QA_RECEIPT.md"
SOURCE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
KNOWN = {
    FILES[0]: "d93505009d7dda7acc010ce1a6e5ec2bacf65ec2",
    FILES[1]: "756126cb4e151a0bd78ece39ab59a4c54ef2aa43",
}
SECTION = re.compile(
    r"<!-- BEGIN 2016_CAUSAL (?P<name>[^ |]+) \| git_blob (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- END 2016_CAUSAL (?P=name) -->", re.S
)

def blob(p):
    b = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\0" + b).hexdigest()

def points(n):
    return f"{Decimal(str(n)):.2f}"

class Test2016CausalReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.chapter1 = (BASE / FILES[0]).read_text(encoding="utf-8")
        cls.chapter2 = (BASE / FILES[1]).read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.receipt = RECEIPT.read_text(encoding="utf-8")
        cls.sections = list(SECTION.finditer(cls.reader))

    def test_retained_source_hash_and_owner_limit(self):
        self.assertEqual(blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.data["year"], 2016)
        self.assertIn("historical identity unverified", self.data["limits"])

    def test_selected_2016_first_slot_week_five_seven_events(self):
        expected = [
            (5, 111.68, 93.62, "HOME"),
            (6, 134.70, 117.26, "HOME"),
            (7, 88.98, 167.48, "AWAY"),
        ]
        for week, home, away, winner in expected:
            rows = next(w["matchups"] for w in self.data["weeks"] if w["week"] == week)
            matches = [m for m in rows if m["home_id"] == 1 or m["away_id"] == 1]
            with self.subTest(week=week):
                self.assertEqual(len(matches), 1)
                m = matches[0]
                self.assertEqual((points(m["hp"]), points(m["ap"]), m["winner"]),
                                 (points(home), points(away), winner))
                self.assertEqual(m["home_id"] if winner == "HOME" else m["away_id"], 1)

    def test_chapter_two_score_quotes_in_order(self):
        anchors = ["111.68 to 93.62", "134.70 against the Gunslingers 117.26",
                   "88.98 to 167.48"]
        positions = [self.chapter2.index(x) for x in anchors]
        self.assertEqual(positions, sorted(positions))
        scores = set(re.findall(r"(?<![\d.])\d{2,3}\.\d{2}(?!\d)",
                                self.chapter2.split("---\n\n*Editorial handoff")[0]))
        self.assertEqual(scores, {"111.68", "93.62", "134.70", "117.26", "88.98", "167.48"})

    def test_real_substantial_causal_prose_not_week_coverage(self):
        self.assertGreaterEqual(len(self.chapter2.split()), 4000)
        self.assertEqual([m.group(1) for m in
                          re.finditer(r"(?m)^### ([IVX]+)\. ", self.chapter2)],
                         ["I", "II", "III", "IV", "V"])
        self.assertNotIn("## Week Five", self.chapter2)
        self.assertIn("cart", self.chapter2)
        self.assertIn("canvas", self.chapter2)
        self.assertIn("two exits", self.chapter2)

    def test_pov_and_provisional_world_explicit(self):
        for phrase in ("CHAR-JAKE-KALOPER", "NONCANON", "No archival evidence",
                       "invented fictional proposals", "No new principal POV"):
            self.assertIn(phrase, self.chapter2)
        for banned in ("Edrin", "Edin", "El Niño said", "the child thought",
                       "the driver knew privately"):
            self.assertNotIn(banned, self.chapter2)

    def test_unresolved_causal_objects_not_silently_ended(self):
        for phrase in ("broken latch", "seller", "unpaid", "bowl", "claimant",
                       "roof", "Mara", "inspector", "three nights", "choice"):
            self.assertIn(phrase.lower(), self.chapter2.lower())
        self.assertIn("The person", self.chapter2)
        self.assertIn("private file", self.chapter2)

    def test_reader_exactly_embeds_two_pinned_manuscripts(self):
        self.assertEqual(len(self.sections), 2)
        self.assertEqual([m.group("name") for m in self.sections], FILES)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 2)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 2)
        for m in self.sections:
            with self.subTest(name=m.group("name")):
                name = m.group("name")
                src = (BASE / name).read_text(encoding="utf-8")
                self.assertEqual(blob(BASE / name), KNOWN[name])
                self.assertEqual(m.group("sha"), KNOWN[name])
                self.assertEqual(m.group("body"), src.rstrip())
                self.assertIn("| `" + name + "` | `" + KNOWN[name] + "` |", self.reader)

    def test_reader_length_and_no_false_completion(self):
        self.assertGreaterEqual(len(self.reader.split()), 8300)
        self.assertIn("NONCANON", self.reader)
        self.assertIn("Not the official 2016 Historical Chronicle", self.reader)
        self.assertIn("HOLD", self.reader)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reader)

    def test_qa_receipt_does_not_suppress_historical_drift(self):
        for term in ("THREE_WINS_THEN_LOSS", "NOT PROVIDER-AUTHENTICATED",
                     "omitted", "Umpire", "Founder", "HOLD"):
            self.assertIn(term, self.receipt)

if __name__ == "__main__":
    unittest.main()
