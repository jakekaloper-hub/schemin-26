"""NONCANON 2016 Week 3 archival and POV regression.

Technical fixture fidelity does not grant character/Atlas/independent literary
or Umpire acceptance.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W03.md"
PREVIOUS = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W02.md"
PIN_SOURCE = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PIN_PREVIOUS = "a2c179164dc529a34d92479b1c8a93f37acb10dd"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class WeekThree2016DraftChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.story = STORY.read_text(encoding="utf-8")
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.source["weeks"] if w["week"] == 3)

    def test_exact_pinned_archive_sha_and_era(self):
        self.assertEqual(git_blob(SOURCE), PIN_SOURCE)
        self.assertEqual(self.source["year"], 2016)
        self.assertIn("1417621", self.source["source"])

    def test_six_unique_period_three_fixtures(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(sorted(i for row in self.rows for i in (row["home_id"], row["away_id"])), list(range(1, 13)))
        self.assertEqual({row["period"] for row in self.rows}, {3})

    def test_archive_winner_flags_score_consistent(self):
        for row in self.rows:
            with self.subTest(row=row["home"]):
                self.assertEqual(row["winner"], "HOME" if row["hp"] > row["ap"] else "AWAY")

    def test_every_exact_fixture_printed(self):
        for i, row in enumerate(self.rows):
            home, away = row["home"].strip(), row["away"].strip()
            winner = home if row["winner"] == "HOME" else away
            expected = (f"Fixture {chr(65+i)} — verified result: {home} {row['hp']:.2f} — "
                        f"{away} {row['ap']:.2f}. Verified winner: {winner}.")
            with self.subTest(i=i+1):
                self.assertIn(expected, self.story)

    def test_distinct_six_chronicle_scenes_in_source_order(self):
        self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) — ", self.story, re.M),
                         ["I", "II", "III", "IV", "V", "VI"])

    def test_substantial_fiction_not_factsheet_only(self):
        self.assertGreaterEqual(len(self.story.split()), 3800)
        self.assertIn("The flaw in the timber", self.story)
        self.assertIn("The piece that could not be returned", self.story)

    def test_provisional_twelve_owner_only_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.story)
        self.assertIn("PRINCIPAL_CHARACTER", self.story)
        self.assertNotRegex(self.story, r"(?im)^## (Edrin|Edin|Oren)\b")

    def test_no_historical_owner_claim(self):
        self.assertIn("NOT PROVIDER-AUTHENTICATED", self.story)
        self.assertIn("not a historical owner attribution", self.story)
        self.assertIn("independent Character Canon approval", self.story)

    def test_no_second_named_hyena_slot_conflation(self):
        self.assertIn("not the same entry as Austin's Hyena's", self.story)
        self.assertIn("previous year's champion slot", self.story)

    def test_fiction_not_claimed_as_atlas(self):
        self.assertIn("PROPOSED FICTION", self.story)
        self.assertIn("not historical Commonwealth canon", self.story)
        self.assertIn("No physical-world Atlas location", self.story)

    def test_irreversible_causal_consequence(self):
        for marker in ("future share", "provision ledger", "warranty", "conditional approval", "remains unpaid"):
            self.assertIn(marker, self.story)

    def test_previous_week_byte_unchanged(self):
        self.assertEqual(git_blob(PREVIOUS), PIN_PREVIOUS)

    def test_approved_hard_canon_unchanged(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_closed_gates_and_literary_dissent(self):
        for marker in ("NONCANON", "editorial HOLD", "independent Author Council",
                       "Umpire acceptance", "No canon promotion or publication"):
            self.assertIn(marker.lower(), self.story.lower())


if __name__ == "__main__":
    unittest.main()
