#!/usr/bin/env python3
"""Adversarial, side-effect-free regression tests for the historical Atlas joins."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

MOD = Path(__file__).with_name("postseason_lineage_gates.py")
spec = importlib.util.spec_from_file_location("postseason_lineage_gates", MOD)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class HistoricalSlotIslandHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads(guard.FILE.read_text(encoding="utf-8"))
        cls.island = json.loads(guard.ISLAND.read_text(encoding="utf-8"))

    def data(self):
        return copy.deepcopy(self.matrix), copy.deepcopy(self.island)

    def invalid(self, transform):
        matrix, island = self.data()
        transform(matrix, island)
        with self.assertRaises(ValueError):
            guard.validate(matrix, island)

    def row(self, matrix, slot, season):
        return matrix["slots"][slot - 1]["year_by_year"][season - 2015]

    def test_source_bound_baseline(self):
        self.assertEqual(guard.validate(*self.data())["status"], "PASS_SOURCE_BOUND_NOT_CANON")

    def test_nonqualifier_cannot_be_called_playoff_team(self):
        self.invalid(lambda m, i: self.row(m, 1, 2015).__setitem__("playoff_qualified", True))

    def test_no_fabricated_2015_lineage(self):
        self.invalid(lambda m, i: self.row(m, 1, 2015).__setitem__("historical_owner_person_identity", "JAKE_KALOPER"))

    def test_cannot_backdate_fictional_venue(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024).__setitem__("physical_location_status", "THE_LAST_FIELD"))

    def test_no_2026_champion(self):
        self.invalid(lambda m, i: m.__setitem__("no_2026_finals", False))

    def test_bye_cannot_be_given_to_nonqualifier(self):
        self.invalid(lambda m, i: m["qualification_field_by_season"][6]["bye_slot_ids"].__setitem__(0, 6))

    def test_remove_fixture_partner(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024)["verified_bracket_matchups"].pop())

    def test_changed_match_score_is_rejected(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024)["verified_bracket_matchups"][0].__setitem__("own_score", 0))

    def test_changed_verified_winner_is_rejected(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024)["verified_bracket_matchups"][0].__setitem__("outcome", "LOSS"))

    def test_unverified_venue_staging_cannot_become_verified(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024)["verified_bracket_matchups"][0].__setitem__("fictional_venue_assignment", "FACT"))

    def test_beach_nonqualifier_eligibility_cannot_be_champion(self):
        self.invalid(lambda m, i: self.row(m, 1, 2015).__setitem__("playoff_island_lodging_proposal", "CHAMPION_NOT_BEACH"))

    def test_2015_field_cannot_expand_silently(self):
        self.invalid(lambda m, i: m["qualification_field_by_season"][0]["qualifier_slot_ids"].append(1))

    def test_2015_two_week_round_cannot_become_2026(self):
        self.invalid(lambda m, i: self.row(m, 5, 2015)["verified_bracket_matchups"][0].__setitem__("round", "QF"))

    def test_island_beach_count_must_match_qualifiers(self):
        def change(m, i):
            beach = next(x for x in i["three_depth_records"] if x["id"] == "LOSERS_BEACH")
            beach["layer3"]["historical_beach_years"][0]["opening_nonqualifier_count"] = 7
        self.invalid(change)

    def test_source_fixture_manifest_not_trustable_as_count_only(self):
        self.invalid(lambda m, i: m["full_playoff_source"]["copied_from_fixture_ids"].__setitem__(0, "HIST-POST-FAKE"))

    def test_result_cannot_affect_historical_demolition(self):
        self.invalid(lambda m, i: self.row(m, 1, 2024).__setitem__("domain_evolution_status", "FORTRESS_DESTROYED"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
