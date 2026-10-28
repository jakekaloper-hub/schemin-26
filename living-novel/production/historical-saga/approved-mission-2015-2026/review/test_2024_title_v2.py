"""Noncanonical 2024 title V2 textual and source-boundary regressions.

These tests do NOT establish independent literary acceptance or owner binding.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "manuscript" / "2024-title"
ORIGINAL = ROOT / "THE_DOOR_AFTER_THE_CROWN_NONCANON.md"
ADDITION = ROOT / "THE_NAMES_NOT_ON_THE_RECEIPT_NONCANON.md"
COMBINED = ROOT / "THE_DOOR_AFTER_THE_CROWN_CAUSAL_READING_CANDIDATE_V2_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_V2.json"


class TestTitleCausalV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = ORIGINAL.read_text(encoding="utf-8")
        cls.addition = ADDITION.read_text(encoding="utf-8")
        cls.combined = COMBINED.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTER.read_text(encoding="utf-8"))

    def test_original_four_scene_bodies_unchanged(self):
        old_body = self.original[self.original.index("## I. The Speech for Tomorrow"):].strip()
        self.assertIn(old_body, self.combined)

    def test_new_scene_body_unchanged_in_assembly(self):
        new_body = self.addition[self.addition.index("Jake loosened the cord"):].strip()
        self.assertIn(new_body, self.combined)

    def test_substantive_growth(self):
        self.assertGreaterEqual(len(self.addition.split()), 2000)
        self.assertGreaterEqual(len(self.combined.split()), 4300)

    def test_exactly_five_development_scenes(self):
        headers = re.findall(r"^## ([IVX]+)\\. ", self.combined, flags=re.M)
        self.assertEqual(headers, ["I", "II", "III", "IV", "V"])
        self.assertEqual(len(self.registry["scenes"]), 5)

    def test_all_pov_entries_are_sole_eligible_principal(self):
        self.assertEqual(self.registry["primary_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual({scene["pov_character_id"] for scene in self.registry["scenes"]}, {"CHAR-JAKE-KALOPER"})
        self.assertNotRegex(self.combined, r"(?m)^## [IVX]+\\. .*\\b(?:Edrin|Oren|El Niño)\\b")

    def test_verified_title_facts_and_boundary(self):
        self.assertIn("187.52", self.combined)
        self.assertIn("161.68", self.combined)
        self.assertEqual(self.registry["historical_source_event"], "HIST-2024-CHAMPIONSHIP-1")
        self.assertEqual(self.registry["historical_owner_binding"], "UNKNOWN")
        self.assertEqual(self.registry["historical_venue"], "PROPOSED_UNAPPROVED")

    def test_no_future_2025_2026_outcome_given_to_character(self):
        story = self.combined[self.combined.index("## I. The Speech for Tomorrow"):]
        self.assertNotRegex(story, r"\\b202[56]\\b")
        self.assertNotRegex(story, r"(?m)^## [IVX]+\\. .*\\b(?:2025|2026)\\b")

    def test_release_fails_closed(self):
        self.assertEqual(self.registry["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertFalse(self.registry["canonical_merge"])
        self.assertFalse(self.registry["independent_editorial_acceptance"])
        self.assertIn("NOT HARD CANON", self.combined)


if __name__ == "__main__":
    unittest.main()
