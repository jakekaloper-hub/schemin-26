"""Independent fixtures for conditional ESPN H2H regular-season seeding."""

from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import random
import unittest

from playoff_context.seeding import rank_espn


def ledger_records(outcomes):
    """Build consistent test inputs from explicitly specified game results."""
    records = {}
    for home, away, winner in outcomes:
        for team in (home, away):
            records.setdefault(team, [0, 0, 0])
            records[team][2 if winner is None else (0 if winner == team else 1)] += 1
    return {team: tuple(record) for team, record in records.items()}


def equal_record_fixture(main_outcomes, target_wins=5, target_losses=3):
    """Add outsiders without changing H2H results among the main tied teams."""
    outcomes = list(main_outcomes)
    main_records = ledger_records(main_outcomes)
    for team, (wins, losses, ties) in main_records.items():
        assert ties == 0
        assert wins <= target_wins and losses <= target_losses
        outsider = "outsider_" + team
        outcomes.extend((team, outsider, team) for _ in range(target_wins - wins))
        outcomes.extend((team, outsider, outsider) for _ in range(target_losses - losses))
    return outcomes, ledger_records(outcomes)


class TestESPNSeeding(unittest.TestCase):
    def rank(self, outcomes, points=None, against=None, divisions=None, seed=17):
        records = ledger_records(outcomes)
        points = points or {team: 100 for team in records}
        against = against or {team: 100 for team in records}
        return rank_espn(records, points, against, outcomes, divisions or {}, random.Random(seed))

    def test_official_five_team_example(self):
        # ESPN's Aug 18, 2026 example (source in seeding.py) explicitly yields
        # E, C, B, D, A. The Nov 9 article's example table contains a different,
        # internally contradictory set of H2H results, so it is not this fixture.
        main = [
            ("A", "B", "A"), ("A", "C", "C"), ("A", "D", "D"),
            ("A", "E", "E"), ("B", "C", "B"), ("B", "E", "E"),
            ("C", "D", "C"), ("C", "E", "E"), ("D", "E", "D"),
        ]
        outcomes, records = equal_record_fixture(main, 7, 5)
        self.assertTrue(all(records[team] == (7, 5, 0) for team in "ABCDE"))
        divisions = {"A": "one", "B": "one", "E": "one", "C": "two", "D": "two"}
        for team in "ABCDE":
            # Outsiders are in the same division as their only opponent and
            # have losing records, preserving the published division winners.
            divisions["outsider_" + team] = divisions[team]
        pf = {team: 0 for team in records}
        pf.update(A=825, B=918, C=725, D=720, E=920)
        order = rank_espn(records, pf, pf, outcomes, divisions, random.Random(1))
        self.assertEqual(order[:5], ["E", "C", "B", "D", "A"])

    def test_equal_h2h_uses_h2h_before_points(self):
        outcomes, records = equal_record_fixture([
            ("A", "B", "A"), ("A", "C", "A"), ("B", "C", "B"),
        ])
        pf = {team: 0 for team in records}
        pf.update(A=100, B=200, C=900)
        order = rank_espn(records, pf, pf, outcomes, {}, random.Random(2))
        self.assertEqual(order[:3], ["A", "B", "C"])

    def test_unequal_h2h_skips_to_points(self):
        outcomes, records = equal_record_fixture([
            ("A", "B", "A"), ("A", "C", "C"),
        ])
        pf = {team: 0 for team in records}
        pf.update(A=200, B=900, C=100)
        order = rank_espn(records, pf, pf, outcomes, {}, random.Random(3))
        self.assertEqual(order[:3], ["B", "C", "A"])

    def test_equal_h2h_totals_do_not_make_pairings_balanced(self):
        # Every main team has two games within this tied group, but four of
        # its six unordered pairings were never played. A/C's 2-0 records
        # therefore cannot displace the PF leader B for this seed.
        main = [
            ("A", "B", "A"), ("B", "A", "A"),
            ("C", "D", "C"), ("D", "C", "C"),
        ]
        outcomes, records = equal_record_fixture(main)
        self.assertTrue(all(records[team] == (5, 3, 0) for team in "ABCD"))
        self.assertTrue(all(sum(ledger_records(main)[team]) == 2 for team in "ABCD"))
        pf = {team: 0 for team in records}
        pf.update(A=200, B=900, C=100, D=50)
        order = rank_espn(records, pf, pf, outcomes, {}, random.Random(13))
        self.assertEqual(order[:4], ["B", "A", "C", "D"])

    def test_reset_after_each_seed(self):
        outcomes, records = equal_record_fixture([
            ("A", "B", "A"), ("B", "C", "B"), ("C", "A", "C"),
        ])
        pf = {team: 0 for team in records}
        pf.update(A=200, B=300, C=100)
        order = rank_espn(records, pf, pf, outcomes, {}, random.Random(4))
        # B wins the three-way PF tie; restarting gives C the A/C H2H tie.
        self.assertEqual(order[:3], ["B", "C", "A"])

    def test_no_h2h_restart_before_seed_is_awarded(self):
        outcomes, records = equal_record_fixture([
            ("A", "B", "A"), ("A", "C", "A"), ("A", "D", "D"),
            ("B", "C", "B"), ("B", "D", "B"), ("C", "D", "C"),
        ])
        pf = {team: 0 for team in records}
        pf.update(A=100, B=200, C=1000, D=50)
        order = rank_espn(records, pf, pf, outcomes, {}, random.Random(5))
        # A and B are 2-1 in the full tied group. PF resolves their remaining
        # tie for this seed; prematurely restarting on A/B would choose A.
        self.assertEqual(order[0], "B")

    def test_division_berths_override_global_record(self):
        outcomes = [
            ("A", "B", "A"), ("A", "C", "A"), ("A", "D", "A"),
            ("B", "C", "B"), ("B", "D", "B"), ("C", "D", "C"),
        ]
        divisions = {"A": "one", "B": "one", "C": "two", "D": "two"}
        self.assertEqual(self.rank(outcomes, divisions=divisions), ["A", "C", "B", "D"])

    def test_division_winner_uses_same_h2h_waterfall(self):
        outcomes = [
            ("A", "B", "A"), ("A", "C", "A"), ("A", "D", "D"),
            ("B", "C", "B"), ("B", "D", "B"), ("C", "D", "C"),
        ]
        divisions = {"A": "one", "B": "one", "C": "two", "D": "two"}
        self.assertEqual(
            self.rank(outcomes, points={"A": 1, "B": 999, "C": 1, "D": 999}, divisions=divisions),
            ["A", "C", "B", "D"],
        )

    def test_ties_count_half_a_win_with_exact_percentages(self):
        outcomes = [
            ("A", "C", "A"), ("C", "A", "C"),
            ("B", "C", None), ("C", "B", None),
        ]
        self.assertEqual(ledger_records(outcomes), {"A": (1, 1, 0), "C": (1, 1, 2), "B": (0, 0, 2)})
        # All are exactly .500, though their W/L/T representations differ.
        self.assertEqual(self.rank(outcomes, points={"A": 200, "B": 300, "C": 100})[0], "B")

    def test_points_against_prefers_higher_total(self):
        outcomes = [
            ("A", "C", "A"), ("C", "B", "C"),
            ("B", "D", "B"), ("D", "A", "D"),
        ]
        order = self.rank(
            outcomes,
            points={"A": 200, "B": 200, "C": 150, "D": 150},
            against={"A": 180, "B": 220, "C": 150, "D": 150},
        )
        self.assertEqual(order[0], "B")

    def test_division_percentage_precedes_points_against(self):
        outcomes = [("A", "C", "A"), ("A", "X", "X"),
                    ("B", "D", "D"), ("B", "Y", "Y")]
        outcomes += [("A", "FA", "A")] * 3 + [("A", "FA", "FA")] * 3
        outcomes += [("B", "FB", "B")] * 4 + [("B", "FB", "FB")] * 2
        divisions = {"A": "one", "C": "one", "X": "one", "FB": "one",
                     "B": "two", "D": "two", "Y": "two", "FA": "two"}
        records = ledger_records(outcomes)
        pf = {team: 1 for team in records}
        pf.update(A=500, B=500, X=1000, Y=1000)
        pa = {team: 1 for team in records}
        pa.update(A=100, B=900)
        order = rank_espn(records, pf, pa, outcomes, divisions, random.Random(7))
        self.assertLess(order.index("A"), order.index("B"))

    def test_true_residual_tie_uses_supplied_random_generator(self):
        outcomes = [("A", "B", None)]
        records = {"A": (0, 0, 1), "B": (0, 0, 1)}
        points = {"A": Decimal("0.3"), "B": Fraction(3, 10)}
        observed_winners = set()
        for seed in range(12):
            expected = random.Random(seed).choice(["A", "B"])
            order = rank_espn(records, points, points, outcomes, {}, random.Random(seed))
            self.assertEqual(order[0], expected)
            observed_winners.add(order[0])
        self.assertEqual(observed_winners, {"A", "B"})

    def test_inputs_are_not_mutated_and_mapping_order_is_irrelevant(self):
        records = {"A": (0, 0, 1), "B": (0, 0, 1)}
        points = {"A": 1, "B": 1}
        outcomes = [("A", "B", None)]
        inputs = deepcopy((records, points, outcomes))
        first = rank_espn(records, points, points, outcomes, {}, random.Random(9))
        reverse = rank_espn(dict(reversed(list(records.items()))), points, points, outcomes, {}, random.Random(9))
        self.assertEqual(first, reverse)
        self.assertEqual((records, points, outcomes), inputs)

    def test_malformed_or_incomplete_ledger_is_rejected(self):
        records = {"A": (1, 0, 0), "B": (0, 1, 0)}
        points = {"A": 2, "B": 1}
        invalid_ledgers = [
            [], [("A", "B", None)], [("A", "B", "B")],
            [("A", "B", "C")], [("A", "A", "A")],
            [("A", "C", "A")], [("A", "B")], [("A", "B", False)],
            [("A", "B", "A"), ("B", "A", "A")],
        ]
        for ledger in invalid_ledgers:
            with self.subTest(ledger=ledger), self.assertRaises(ValueError):
                rank_espn(records, points, points, ledger, {}, random.Random(10))

    def test_invalid_records_points_or_divisions_are_rejected(self):
        records = {"A": (1, 0, 0), "B": (0, 1, 0)}
        points = {"A": 2, "B": 1}
        outcomes = [("A", "B", "A")]
        cases = [
            ({"A": (True, 0, 0), "B": (0, 1, 0)}, points, {}),
            ({"A": (-1, 0, 0), "B": (0, 1, 0)}, points, {}),
            ({"A": (1.0, 0, 0), "B": (0, 1, 0)}, points, {}),
            (records, {"A": float("nan"), "B": 1}, {}),
            (records, {"A": Decimal("Infinity"), "B": 1}, {}),
            (records, {"A": True, "B": 1}, {}),
            (records, {"A": 2}, {}),
            (records, {"A": 2, "B": 1, "C": 0}, {}),
            (records, points, {"A": "one"}),
            (records, points, {"A": "one", "B": ""}),
        ]
        for test_records, test_points, test_divisions in cases:
            with self.subTest(records=test_records, points=test_points, divisions=test_divisions), self.assertRaises(ValueError):
                rank_espn(test_records, test_points, points, outcomes, test_divisions, random.Random(11))


if __name__ == "__main__":
    unittest.main()
