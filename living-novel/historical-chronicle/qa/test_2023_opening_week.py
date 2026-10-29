"""Source-bound regression for 2023 Chronicle Week 1 (NONCANON).

Checks public ESPN/Flaim archive transcription and manuscript safeguards.
Passing is NOT an independent author, Umpire, Atlas or Founder approval.
"""
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
CHRONICLE = ROOT / "living-novel/historical-chronicle/seasons/2023"
SCORE_FILE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
PROLOGUE = CHRONICLE / "PROLOGUE.md"
W01 = CHRONICLE / "weeks/W01.md"
SOURCE_BLOB = "ded119cde5c660f87f197f269b8d6ddd2a11316a"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def printed_amount(x):
    return f"{Decimal(str(x)):.2f}"


def outcome(row):
    hp, ap = Decimal(str(row["hp"])), Decimal(str(row["ap"]))
    return "home" if hp > ap else "away" if ap > hp else "tie"


class Test2023OpeningWeek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = PROLOGUE.read_text(encoding="utf8")
        cls.text = W01.read_text(encoding="utf8")
        cls.evidence = json.loads(SCORE_FILE.read_text(encoding="utf8"))
        cls.week = next(x for x in cls.evidence["weeks"] if x["week"] == 1)
        cls.parts = re.split(r"(?m)^## [IVX]+\\. [^\\n]+\\n", cls.text)
        cls.headings = re.findall(r"(?m)^## ([IVX]+)\\. (.+)$", cls.text)

    def test_source_identity_and_six_unique_matches(self):
        self.assertEqual(git_blob(SCORE_FILE), SOURCE_BLOB)
        self.assertEqual(self.evidence["year"], 2023)
        self.assertEqual(len(self.week["matchups"]), 6)
        ids = [p for r in self.week["matchups"] for p in (r["home_id"], r["away_id"])]
        self.assertEqual(len(set(ids)), 12)
        self.assertEqual(len(ids), 12)

    def test_protected_main_manuscripts_unchanged(self):
        for name, expected in PROTECTED.items():
            with self.subTest(path=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), expected)

    def test_prologue_is_actual_fiction_not_a_packet(self):
        self.assertGreaterEqual(len(self.p.split()), 1000)
        self.assertIn("There were five more to find.", self.p)
        self.assertIn("PROPOSED FICTION", self.p)
        self.assertIn("CHAR-JAKE-KALOPER", self.p)

    def test_six_fully_written_separate_scene_passages(self):
        self.assertEqual([x[0] for x in self.headings], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.parts), 7)
        self.assertGreaterEqual(len(self.text.split()), 3300)
        for i, scene in enumerate(self.parts[1:], 1):
            with self.subTest(scene=i):
                self.assertGreaterEqual(len(scene.split()), 350)

    def test_every_score_home_away_result_and_margin(self):
        for i, r in enumerate(self.week["matchups"], 1):
            with self.subTest(slot=(r["home_id"], r["away_id"])):
                scene = self.parts[i]
                self.assertIn(f'{r["home"].strip()} (home), {printed_amount(r["hp"])}', scene)
                self.assertIn(f'{r["away"].strip()} (away), {printed_amount(r["ap"])}', scene)
                margin = abs(Decimal(str(r["hp"]))-Decimal(str(r["ap"])))
                self.assertIn(f'Margin **{margin:.2f}**', scene)
                self.assertEqual(r["winner"], "HOME" if outcome(r) == "home" else "AWAY")
        self.assertEqual(self.week["matchups"][1]["away_id"], 1)

    def test_no_unlicensed_pov_or_owner_history(self):
        self.assertNotRegex(self.text + self.p, r"\\b(?:Edrin|Edin|Master Oren)\\b")
        self.assertIn("not verified identities of their human owners", self.p)
        self.assertIn("not verified historical human-owner binding", self.text)
        self.assertIn("El Niño is treated as a storm-name/banner", self.text)
        self.assertNotIn("2023 champion was", self.text)
        self.assertIn("HISTORICAL ATLAS HOLD", self.text)
        self.assertIn("NONCANON", self.p + self.text)

    def test_chronicle_vs_causal_chapter_boundary(self):
        self.assertIn("do not treat this chronicle as a substitute", self.text)
        self.assertIn("The Fourth Address", self.text)
        self.assertIn("Opening-week state:", self.text)


if __name__ == "__main__":
    unittest.main()
