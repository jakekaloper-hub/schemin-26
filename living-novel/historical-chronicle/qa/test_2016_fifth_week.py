"""NONCANON 2016 Week 5 archival-fixture, POV, and continuity regression.

Automated correctness is not author acceptance or historical-owner proof.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W05.md"
PRIOR = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W04.md"
SOURCE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PRIOR_BLOB = "c04700fe674489a5e0aac8f73ce4ddae9ba564eb"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class WeekFive2016DraftChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prose = STORY.read_text(encoding="utf-8")
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.source["weeks"] if w["week"] == 5)

    def test_01_archive_byte_identity_and_year(self):
        self.assertEqual(git_blob(SOURCE), SOURCE_BLOB)
        self.assertEqual(self.source["year"], 2016)
        self.assertIn("1417621", self.source["source"])

    def test_02_six_distinct_2016_week5_fixtures(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual({x["period"] for x in self.rows}, {5})
        self.assertEqual(sorted(z for x in self.rows for z in (x["home_id"], x["away_id"])), list(range(1, 13)))

    def test_03_every_verified_winner_is_mathematically_consistent(self):
        for r in self.rows:
            with self.subTest(team=r["home"]):
                self.assertEqual(r["winner"], "HOME" if r["hp"] > r["ap"] else "AWAY")

    def test_04_all_six_full_fixture_lines_match_archive(self):
        for i, r in enumerate(self.rows):
            home, away = r["home"].strip(), r["away"].strip()
            winner = home if r["winner"] == "HOME" else away
            expected = (f"Fixture {chr(65+i)} — verified result: {home} {r['hp']:.2f} — "
                        f"{away} {r['ap']:.2f}. Verified winner: {winner}.")
            with self.subTest(fixture=i+1):
                self.assertIn(expected, self.prose)

    def test_05_all_six_reported_margins_match_arithmetic(self):
        for r in self.rows:
            margin = f"{abs(r['hp']-r['ap']):.2f}"
            with self.subTest(home=r["home"]):
                self.assertIn(margin, self.prose)

    def test_06_six_narrative_movements_without_omission(self):
        self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) — ", self.prose, re.M),
                         ["I", "II", "III", "IV", "V", "VI"])

    def test_07_literary_substance_and_open_ending(self):
        self.assertGreaterEqual(len(self.prose.split()), 5000)
        for marker in ("The bowl with a person's mark", "A place left in the margin",
                       "The road wasn't", "A place left"):
            self.assertIn(marker, self.prose)

    def test_08_only_twelve_owner_proposed_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.prose)
        self.assertIn("PRINCIPAL_CHARACTER", self.prose)
        self.assertIn("sole interior viewpoint", self.prose)
        self.assertNotRegex(self.prose, r"(?im)^## (Edrin|Edin|Oren)\b")

    def test_09_no_historical_owner_binding_asserted(self):
        self.assertIn("NOT PROVIDER-AUTHENTICATED", self.prose)
        self.assertIn("not a fresh authenticated upstream snapshot", self.prose)
        self.assertIn("real-owner biography", self.prose)

    def test_10_two_hyena_slot_names_are_not_conflated(self):
        self.assertIn("slot 12 belonged to The Real Austin's Hyenas", self.prose)
        self.assertIn("slot 8 was Austin's Hyena's", self.prose)
        self.assertIn("different archived team IDs", self.prose)

    def test_11_fictional_material_consequences_persist(self):
        for token in ("unissued", "seller's invoice", "witnessed", "conditional",
                      "labor credits", "unclaimed", "Fiction-only continuity handoff"):
            self.assertIn(token.lower(), self.prose.lower())

    def test_12_previous_week_blob_is_immutable(self):
        self.assertEqual(git_blob(PRIOR), PRIOR_BLOB)

    def test_13_protected_hard_canon_unchanged(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_14_noncanonical_atlas_and_release_gates_remain_closed(self):
        for token in ("PROPOSED FICTION", "historical Commonwealth canon",
                      "Atlas", "Umpire", "No canon promotion or publication"):
            self.assertIn(token.lower(), self.prose.lower())

    def test_15_no_auto_future_season_assertions(self):
        self.assertIn("no subsequent scores, trades, playoff outcomes", self.prose)
        self.assertIn("human owner", self.prose)
        self.assertIn("not historical Commonwealth canon", self.prose.lower())


if __name__ == "__main__":
    unittest.main()
