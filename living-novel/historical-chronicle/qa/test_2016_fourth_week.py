"""Noncanonical 2016 Week 4 six-fixture manuscript/source and protected-canon checks.

This technical suite is NOT an independent literary, historical identity,
Atlas, Umpire or Founder acceptance.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
STORY = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W04.md"
W02 = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W02.md"
W03 = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W03.md"
ARCHIVE_BLOB = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
W02_BLOB = "a2c179164dc529a34d92479b1c8a93f37acb10dd"
W03_BLOB = "f515d2e46486f599906fd43cb98232585427ba0c"
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class WeekFour2016DraftChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = STORY.read_text(encoding="utf-8")
        cls.archive = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.rows = next(w["matchups"] for w in cls.archive["weeks"] if w["week"] == 4)

    def test_01_year_and_archive_blob_pinned(self):
        self.assertEqual(self.archive["year"], 2016)
        self.assertIn("1417621", self.archive["source"])
        self.assertEqual(git_blob(SOURCE), ARCHIVE_BLOB)

    def test_02_exactly_six_unique_scoring_slot_pairs(self):
        self.assertEqual(len(self.rows), 6)
        self.assertEqual(sorted(slot for r in self.rows for slot in (r["home_id"], r["away_id"])), list(range(1, 13)))

    def test_03_all_matchup_periods_are_four(self):
        self.assertEqual({r["period"] for r in self.rows}, {4})

    def test_04_winner_flags_agree_with_scores(self):
        for r in self.rows:
            with self.subTest(home=r["home"]):
                self.assertEqual(r["winner"], "HOME" if r["hp"] > r["ap"] else "AWAY")

    def test_05_every_fixture_has_exact_source_text(self):
        for i, r in enumerate(self.rows):
            home, away = r["home"].strip(), r["away"].strip()
            winner = home if r["winner"] == "HOME" else away
            statement = (f"Fixture {chr(65 + i)} — verified result: {home} {r['hp']:.2f} — "
                         f"{away} {r['ap']:.2f}. Verified winner: {winner}.")
            with self.subTest(fixture=i + 1):
                self.assertIn(statement, self.text)

    def test_06_six_distinct_dramatic_sections_in_fixture_order(self):
        self.assertEqual(re.findall(r"^## (I|II|III|IV|V|VI) — ", self.text, flags=re.M),
                         ["I", "II", "III", "IV", "V", "VI"])

    def test_07_substantial_prose_not_stub_or_results_list(self):
        self.assertGreaterEqual(len(self.text.split()), 4500)
        for marker in ("A count made before breakfast", "What remained on the shelf",
                       "The portion with his name", "The sack left in the rain"):
            self.assertIn(marker, self.text)

    def test_08_exclusive_canonical_owner_pov_candidate_only(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.text)
        self.assertIn("PRINCIPAL_CHARACTER", self.text)
        self.assertNotRegex(self.text, r"(?im)^## (Edrin|Edin|Oren)\b")
        self.assertIn("only interior viewpoint", self.text)

    def test_09_no_historical_owner_or_atlas_authentication(self):
        for marker in ("NOT PROVIDER-AUTHENTICATED", "PROPOSED FICTION",
                       "not historical Commonwealth canon", "HOLD"):
            self.assertIn(marker.lower(), self.text.lower())

    def test_10_separate_similar_historical_hyena_slots(self):
        self.assertIn("The Real Austin's Hyenas (slot 12)", self.text)
        self.assertIn("Austin's Hyena's (slot 8)", self.text)
        self.assertIn("separate entries in the archive", self.text)

    def test_11_material_causal_cost_not_trivial_win_loss_recap(self):
        for marker in ("invoice", "witnessed", "remains unpaid", "crack-seal",
                       "quarantined", "provision portion", "unclaimed"):
            self.assertIn(marker, self.text)

    def test_12_prior_two_drafts_byte_identical(self):
        self.assertEqual(git_blob(W02), W02_BLOB)
        self.assertEqual(git_blob(W03), W03_BLOB)

    def test_13_all_four_hard_canon_blobs_preserved(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT / "living-novel/manuscript" / name), sha)

    def test_14_no_auto_promotion_and_independent_review_hold(self):
        for marker in ("NONCANON", "independent Author Council",
                       "independent Umpire acceptance", "No canon promotion or publication"):
            self.assertIn(marker.lower(), self.text.lower())

    def test_15_causal_handoff_preserves_real_world_source_firewall(self):
        for marker in ("Proposed-fiction continuity handoff",
                       "No historical human/owner identity",
                       "Fictional preceding state", "Historical slot 1"):
            self.assertIn(marker, self.text)


if __name__ == "__main__":
    unittest.main()
