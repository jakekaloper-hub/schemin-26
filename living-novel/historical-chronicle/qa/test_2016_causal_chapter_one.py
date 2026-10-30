"""Bounded technical regression for 2016 causal-novel Chapter One, NONCANON.

The historical archive verifies fixtures, not real-owner identities, fictional
institutions, historical motives, world geography, or literary acceptance.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
CHAPTER = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/THE_DEBT_BEFORE_THE_DOOR_CHAPTER_01_NONCANON.md"
RECEIPT = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/CHAPTER_01_SOURCE_EDITORIAL_QA_RECEIPT.md"
CANON = ROOT / "living-novel/manuscript"
SOURCE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def decimal(value):
    return f"{Decimal(str(value)):.2f}"

class Test2016CausalChapterOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.prose = CHAPTER.read_text(encoding="utf-8")
        cls.receipt = RECEIPT.read_text(encoding="utf-8")
        cls.first_slot = {}
        for week in cls.data["weeks"]:
            if week["week"] in (1, 2, 3, 4):
                matches = [m for m in week["matchups"] if 1 in (m["home_id"], m["away_id"])]
                assert len(matches) == 1, "archival first-slot fixture cardinality changed"
                cls.first_slot[week["week"]] = matches[0]

    def test_source_is_exact_archived_2016_evidence(self):
        self.assertEqual(git_blob(SOURCE), SOURCE_SHA)
        self.assertEqual(self.data["year"], 2016)
        self.assertEqual(self.data["source"], "Flaim ESPN 1417621")
        self.assertIn("historical identity unverified", self.data["limits"])

    def test_first_four_weeks_sequence_is_three_wins_then_loss(self):
        expected = [
            (1, 95.62, 85.64, "HOME"),
            (2, 85.38, 102.42, "AWAY"),
            (3, 106.8, 163.14, "AWAY"),
            (4, 88.28, 127.52, "AWAY"),
        ]
        for week, home, away, result in expected:
            with self.subTest(week=week):
                m = self.first_slot[week]
                self.assertEqual((decimal(m["hp"]), decimal(m["ap"]), m["winner"]),
                                 (decimal(home), decimal(away), result))
                actual_slot_one_won = ((m["home_id"] == 1 and m["winner"] == "HOME") or
                                       (m["away_id"] == 1 and m["winner"] == "AWAY"))
                self.assertEqual(actual_slot_one_won, week < 4)

    def test_chapter_anchors_selected_weeks_2_3_4_in_order(self):
        anchors = ["102.42 to 85.38", "163.14 over Hook, Line, and Zeeker's 106.80",
                   "88.28 to 127.52"]
        indices = [self.prose.index(s) for s in anchors]
        self.assertEqual(indices, sorted(indices))
        for n in ("Bavid Dabbs", "Hook, Line, and Zeeker",
                  "I'M HERE SO I WON'T GET FINED"):
            self.assertIn(n, self.prose)

    def test_no_unaccounted_numbered_score_in_prose(self):
        body = self.prose.split("---\n\n*Editorial handoff", 1)[0]
        seen = set(re.findall(r"(?<![\d.])\d{2,3}\.\d{2}(?!\d)", body))
        self.assertEqual(seen, {"102.42", "85.38", "163.14", "106.80", "88.28", "127.52"})

    def test_literary_body_is_substantial_and_not_chronicle_week_headings(self):
        self.assertGreaterEqual(len(self.prose.split()), 4000)
        chapters = re.findall(r"(?m)^### ([IVX]+)\. (.+)$", self.prose)
        self.assertEqual([k for k, _ in chapters], ["I", "II", "III", "IV", "V"])
        self.assertEqual(len(chapters), 5)
        self.assertNotIn("## Week Two", self.prose)
        self.assertNotIn("## Week Three", self.prose)

    def test_single_proposed_canonical_principal_pov_and_no_institutional_pov(self):
        for term in ("CHAR-JAKE-KALOPER", "Proposed limited principal POV",
                     "fiction proposal", "historical-identity", "NONCANON"):
            self.assertIn(term, self.prose)
        for banned in ("Edrin", "Edin", "El Niño said", "the seller thought", "Mara wondered"):
            self.assertNotIn(banned, self.prose)

    def test_source_and_geography_firewall(self):
        for term in ("2016 scoring slot belonged to Jake", "historical-identity",
                     "Unnamed settlement", "invented", "Atlas"):
            self.assertIn(term.lower(), self.prose.lower())
        self.assertIn("No approved 2026 hard manuscript is revised", self.prose)

    def test_repair_has_cost_and_unresolved_followthrough(self):
        for term in ("seller", "inspector", "Mara", "beam", "conditional",
                     "pledge", "grain", "empty bowl", "latch", "missing"):
            self.assertIn(term.lower(), self.prose.lower())
        self.assertIn("It is holding", self.prose)

    def test_all_hard_canon_manuscript_blobs_untouched(self):
        self.assertEqual(len(PROTECTED), 4)
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(CANON / name), sha)

    def test_receipt_preserves_source_conflict_not_fake_approval(self):
        for term in ("THREE_WINS_THEN_LOSS", "THE_MEASURE_OF_REPAIR_NONCANON",
                     "NONCANON", "Umpire", "HOLD", "omitted", "Founder"):
            self.assertIn(term, self.receipt)

if __name__ == "__main__":
    unittest.main()
