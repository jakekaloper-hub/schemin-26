"""Regression fixtures for Commissioner Creative DNA structural contracts.

No fixture represents a real league result, approved render, or publication.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_creative_dna import validate_packet, validate_registry  # noqa: E402


def fixture():
    rows = [
        {
            "rank": i, "prior_rank": i, "movement": 0,
            "team_id": f"synthetic-owner-{i:02}",
            "record": {"wins": 3, "losses": 2},
            "commentary": f"Test rationale for ranking {i}",
            "portrait_asset_ref": f"approved-matchup/portrait-{i:02}",
            "portrait_source": "same_issue_accepted_matchup_crop",
        }
        for i in range(1, 13)
    ]
    def page(page_id, pattern, data):
        return {
            "page_id": page_id, "creative_dna_patterns": [pattern],
            "creative_dna": {pattern: data},
            "image_tells": "Meaningful action", "prose_tells": "Character motivation",
            "data_tells": "Evidence and outcome",
        }
    return {
        "issue_id": "TEST-NOT-RELEASED",
        "pages": [
            page("TEST-OPEN", "opening_drive", {
                "weekly_thesis": "Underdogs change the world",
                "narrative_text": "Verified football events reshape the fictional geography.",
                "world_event_callouts": [
                    {"event_ref": "test-result-a", "world_consequence": "Bridge damaged", "location_ref": "world/bridge"},
                    {"event_ref": "test-result-b", "world_consequence": "Hall reopened", "location_ref": "world/hall"},
                ],
                "fact_evidence_refs": ["test-fact-lock"],
                "world_atlas_ref": "test-atlas", "entry_world_state_ref": "test-world-state",
            }),
            page("TEST-RANKS", "power_rankings", {
                "ranking_rows": rows, "fact_lock_ref": "test-fact-lock",
                "previous_published_rankings_ref": "test-prior-rankings",
            }),
            page("TEST-STORY", "cinematic_sequence", {
                "sequence_beats": ["Challenge", "Reversal"],
                "narrative_text": "The challenger arrives at a known place.",
                "fantasy_causality_ref": "test-week-events",
                "world_atlas_ref": "test-hill", "text_treatment": "integrated",
            }),
            page("TEST-RESULT", "matchup_progression_receipt", {
                "scene_asset_refs": ["test-scene-1", "test-scene-2"],
                "accepted_character_assets": {
                    "synthetic-owner-01": "accepted/portrait-01",
                    "synthetic-owner-02": "accepted/portrait-02",
                },
                "result": {
                    "home": {"team_id": "synthetic-owner-01", "score": 150.50,
                             "record": {"wins": 3, "losses": 2}, "portrait_asset_ref": "accepted/portrait-01"},
                    "away": {"team_id": "synthetic-owner-02", "score": 140.25,
                             "record": {"wins": 2, "losses": 3}, "portrait_asset_ref": "accepted/portrait-02"},
                    "margin": 10.25,
                },
                "fact_lock_ref": "test-final-fact-lock",
            }),
        ],
    }


class CreativeDNAContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "COMMISSIONER_CREATIVE_DNA_V1.json").read_text(encoding="utf-8"))

    def check_defect(self, mutant, phrase):
        failures = validate_packet(mutant, self.registry)
        self.assertTrue(any(phrase in error for error in failures), failures)

    def test_exact_four_approved_patterns(self):
        self.assertEqual(validate_registry(self.registry), [])

    def test_valid_synthetic_packet(self):
        self.assertEqual(validate_packet(fixture(), self.registry), [])

    def test_missing_world_opening_without_exception(self):
        obj = fixture()
        obj["pages"] = [p for p in obj["pages"] if p["page_id"] != "TEST-OPEN"]
        self.check_defect(obj, "required module opening_drive")

    def test_explicit_omission_is_traceable(self):
        obj = fixture()
        obj["pages"] = [p for p in obj["pages"] if p["page_id"] != "TEST-OPEN"]
        obj["explicit_module_omission_reasons"] = {"opening_drive": "Editorial exception for special issue"}
        self.assertEqual(validate_packet(obj, self.registry), [])

    def test_missing_twelve_ranked_owners(self):
        obj = fixture()
        obj["pages"][1]["creative_dna"]["power_rankings"]["ranking_rows"].pop()
        self.check_defect(obj, "exactly 12")

    def test_wrong_ranking_movement(self):
        obj = fixture()
        obj["pages"][1]["creative_dna"]["power_rankings"]["ranking_rows"][0]["movement"] = 4
        self.check_defect(obj, "movement not equal")

    def test_duplicate_ranking_owner(self):
        obj = fixture()
        obj["pages"][1]["creative_dna"]["power_rankings"]["ranking_rows"][1]["team_id"] = "synthetic-owner-01"
        self.check_defect(obj, "missing/duplicate stable team_id")

    def test_rankings_portrait_not_independently_generated(self):
        obj = fixture()
        obj["pages"][1]["creative_dna"]["power_rankings"]["ranking_rows"][0]["portrait_source"] = "fresh_generated_portrait"
        self.check_defect(obj, "portrait source not approved")

    def test_result_portraits_match_accepted_wave(self):
        obj = fixture()
        obj["pages"][3]["creative_dna"]["matchup_progression_receipt"]["result"]["home"]["portrait_asset_ref"] = "incorrect/face"
        self.check_defect(obj, "portrait is not from accepted matchup wave")

    def test_score_margin_is_deterministic(self):
        obj = fixture()
        obj["pages"][3]["creative_dna"]["matchup_progression_receipt"]["result"]["margin"] = 34.0
        self.check_defect(obj, "margin does not match")

    def test_cinematic_prose_requires_fantasy_cause(self):
        obj = fixture()
        obj["pages"][2]["creative_dna"]["cinematic_sequence"]["fantasy_causality_ref"] = ""
        self.check_defect(obj, "fantasy_causality_ref")

    def test_opening_callout_requires_world_location(self):
        obj = fixture()
        obj["pages"][0]["creative_dna"]["opening_drive"]["world_event_callouts"][0]["location_ref"] = ""
        self.check_defect(obj, "callout not linked")

    def test_image_prose_data_roles_are_explicit(self):
        obj = fixture()
        obj["pages"][0]["data_tells"] = ""
        self.check_defect(obj, "missing data_tells")

    def test_historical_page_cannot_override_character_canon(self):
        obj = copy.deepcopy(self.registry)
        obj["reuse_policy"]["historical_pages"] = "CHARACTER_IDENTITY_AUTHORITY"
        self.assertTrue(any("historical reference images" in e for e in validate_registry(obj)))


if __name__ == "__main__":
    unittest.main()
