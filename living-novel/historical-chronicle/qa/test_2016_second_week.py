"""Fail-closed provenance and structure checks for the NONCANON 2016 Week 2 Chronicle.

This checks archival fixture fidelity and negative authorial boundaries, NOT
literary merit, historical human ownership, Atlas approval, or Umpire signoff.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
WEEK = ROOT / "living-novel/historical-chronicle/seasons/2016/weeks/W02.md"
ARCHIVE = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"


class WeekTwo2016DraftChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WEEK.read_text(encoding="utf-8")
        cls.archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        weeks = [week for week in cls.archive["weeks"] if week["week"] == 2]
        assert len(weeks) == 1, "2016 Week 2 source missing or ambiguous"
        cls.fixtures = weeks[0]["matchups"]

    def test_archival_source_era_and_provider(self):
        self.assertEqual(self.archive["year"], 2016)
        self.assertIn("Flaim", self.archive["source"])
        self.assertIn("1417621", self.archive["source"])

    def test_six_fixtures_exactly(self):
        self.assertEqual(len(self.fixtures), 6)
        self.assertEqual({f["period"] for f in self.fixtures}, {2})

    def test_unique_source_slots(self):
        ids = [i for fixture in self.fixtures for i in (fixture["home_id"], fixture["away_id"])]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 12)

    def test_source_result_flags_match_scores(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["home"]):
                self.assertIn(fixture["winner"], {"HOME", "AWAY"})
                expected = "HOME" if fixture["hp"] > fixture["ap"] else "AWAY"
                self.assertEqual(fixture["winner"], expected)

    def test_all_six_exact_result_receipts_present(self):
        for i, f in enumerate(self.fixtures):
            home, away = f["home"].strip(), f["away"].strip()
            winner = home if f["winner"] == "HOME" else away
            expected = (
                f"Fixture {chr(65+i)} — verified result: {home} {f['hp']:.2f} — "
                f"{away} {f['ap']:.2f}. Verified winner: {winner}."
            )
            with self.subTest(fixture=i+1):
                self.assertIn(expected, self.text)

    def test_six_individual_narrative_movements(self):
        movements = re.findall(r"^## (I|II|III|IV|V|VI) — ", self.text, re.M)
        self.assertEqual(movements, ["I", "II", "III", "IV", "V", "VI"])

    def test_substantial_new_literary_text(self):
        self.assertGreaterEqual(len(self.text.split()), 3500)
        self.assertIn("The unnumbered hour", self.text)
        self.assertIn("After the tally", self.text)

    def test_single_named_principal_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER", self.text)
        self.assertIn("PRINCIPAL_CHARACTER", self.text)
        self.assertNotRegex(self.text, r"(?im)^## (Edrin|Edin|Oren)\b")
        self.assertNotRegex(self.text, r"(?im)^\*POV: (?!CHAR-JAKE-KALOPER)")

    def test_owner_binding_not_implicitly_promoted(self):
        self.assertIn("NOT PROVIDER-AUTHENTICATED", self.text)
        self.assertIn("historical owner authentication", self.text)
        self.assertIn("author-room conjecture", self.text)
        self.assertIn("real owner", self.text.lower())

    def test_proposed_geography_not_claimed_as_canon(self):
        self.assertIn("not recovered historical events or approved Atlas geography", self.text)
        self.assertIn("No new Atlas settlement", self.text)
        self.assertIn("fictional", self.text.lower())

    def test_no_prohibited_canon_promotion(self):
        self.assertIn("NONCANON", self.text)
        self.assertIn("independent editorial HOLD", self.text)
        self.assertIn("do not promote to canon", self.text)

    def test_consequences_not_just_recap(self):
        for phrase in ("roof beam", "provision ledger", "unfastened", "unfinished admission tally"):
            self.assertIn(phrase, self.text)

    def test_chronicle_source_path_explicit(self):
        self.assertIn("G01_2016_FULL_WEEKLY_MATCHUPS.json", self.text)
        self.assertIn("weeks[week == 2]", self.text)

    def test_did_not_forecast_future_result_as_character_knowledge(self):
        self.assertNotIn("eventual champion", self.text.lower())
        self.assertNotIn("future finalist", self.text.lower())
        self.assertNotIn("next year's champion", self.text.lower())


if __name__ == "__main__":
    unittest.main()
