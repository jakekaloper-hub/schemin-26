import math
import unittest
from dataclasses import replace
from random import Random
from unittest.mock import patch

from playoff_context import (
    Game, LeagueRules, TeamState, UnsupportedRulesError, UnresolvedTiebreakError,
    conditional_leverage, exact_bounds_status, normalize_future_games,
    normalize_teams, require_final_week, simulate,
)
from playoff_context.engine import Strength, _sample_scores, rank_teams, win_probability


class TestEngineHardening(unittest.TestCase):
    def setUp(self):
        self.teams = {
            'A': TeamState('A', 'A', 1, 1, points_for=200, points_against=190, scores=(90, 110)),
            'B': TeamState('B', 'B', 1, 1, points_for=190, points_against=200, scores=(100, 90)),
        }
        self.rules = LeagueRules(1, 3, 'POINTS_FOR', qualification_policy='OVERALL')
        self.games = [Game(3, 'A', 'B')]

    def test_qualification_and_tiebreak_must_be_explicit(self):
        for rules in (LeagueRules(1, 3), replace(self.rules, tiebreaker='H2H_RECORD'),
                      replace(self.rules, qualification_policy='DIVISION_WINNERS_PLUS_WILDCARDS')):
            with self.subTest(rules=rules), self.assertRaises(UnsupportedRulesError):
                simulate(self.teams, self.games, rules, 1)
        with self.assertRaises(UnsupportedRulesError):
            rank_teams({'A': (1, 1, 0), 'B': (1, 1, 0)}, {'A': 200, 'B': 190}, LeagueRules(1, 2))

    def test_team_id_does_not_resolve_a_sporting_tie(self):
        with self.assertRaises(UnresolvedTiebreakError):
            rank_teams({'A': (1, 1, 0), 'B': (1, 1, 0)}, {'A': 200, 'B': 200}, self.rules)

    def test_record_points_prevent_false_exact_claims_with_ties(self):
        # Realizable schedule: A-C/B-D, A-D/B-C, A-D/B-C, A-C/B-D.
        # A wins weeks 1/3; B ties weeks 1/2/3 and wins week 4.
        teams = {
            'A': TeamState('A', 'A', 2, 2, 0),
            'B': TeamState('B', 'B', 1, 0, 3),
            'C': TeamState('C', 'C', 1, 1, 2),
            'D': TeamState('D', 'D', 1, 2, 1),
        }
        status = exact_bounds_status(teams, [], replace(self.rules, regular_season_weeks=4))
        self.assertEqual(status['B']['status'], 'CLINCHED')
        self.assertEqual(status['A']['status'], 'ELIMINATED')
        self.assertEqual(status['B']['class'], 'EXACT')

    def test_division_bounds_make_no_exact_claim(self):
        rules = replace(self.rules, qualification_policy='DIVISION_WINNERS_PLUS_WILDCARDS',
                        tiebreaker='H2H_RECORD', divisions={'A': 'X', 'B': 'X'})
        result = exact_bounds_status(self.teams, self.games, rules)
        self.assertTrue(all(row['status'] == 'UNKNOWN' and row['class'] == 'UNRESOLVED'
                            and row['proof'] is None for row in result.values()))

    def test_unknown_bounds_do_not_claim_exact_alive(self):
        result = exact_bounds_status(self.teams, self.games, self.rules)
        self.assertTrue(all(row['status'] == 'UNKNOWN' and row['class'] == 'UNRESOLVED'
                            for row in result.values()))

    def test_bad_counts_nonfinite_data_and_invalid_parameters_rejected(self):
        for n in (0, -1, True, 1.5):
            with self.subTest(n=n), self.assertRaises(ValueError):
                simulate(self.teams, self.games, self.rules, n)
        for seed in (True, '7', 2.5):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                simulate(self.teams, self.games, self.rules, 1, seed)
        for field, value in (('wins', 1.5), ('ties', -1), ('points_for', math.nan),
                             ('points_against', math.inf), ('scores', (90, math.nan))):
            broken = {**self.teams, 'A': replace(self.teams['A'], **{field: value})}
            with self.subTest(field=field), self.assertRaises(ValueError):
                simulate(broken, self.games, self.rules, 1)
        for rules in (replace(self.rules, playoff_teams=0), replace(self.rules, playoff_teams=3),
                      replace(self.rules, regular_season_weeks=True)):
            with self.subTest(rules=rules), self.assertRaises(ValueError):
                simulate(self.teams, self.games, rules, 1)

    def test_missing_duplicate_self_unknown_and_post_horizon_games_rejected(self):
        for games in ([], self.games * 2, [Game(3, 'A', 'A')], [Game(3, 'A', 'Z')],
                      [Game(4, 'A', 'B')], [Game(2, 'A', 'B')],
                      [Game(3, 'A', 'B', math.nan)], [Game(3, 'A', 'B', -1)]):
            with self.subTest(games=games), self.assertRaises(ValueError):
                simulate(self.teams, games, self.rules, 1)

    def test_forcing_rejects_missing_game_and_unknown_winner(self):
        for forced in ({(2, 'A', 'B'): 'A'}, {(3, 'A', 'B'): 'Z'}):
            with self.subTest(forced=forced), self.assertRaises(ValueError):
                simulate(self.teams, self.games, self.rules, 1, forced_results=forced)
        with self.assertRaises(ValueError):
            conditional_leverage(self.teams, self.games, self.rules, Game(2, 'A', 'B'), 1)

    def test_results_follow_scores_and_share_the_same_points(self):
        seen = []
        original = rank_teams
        def capture(records, points_for, rules):
            seen.append((records, points_for))
            return original(records, points_for, rules)
        with patch('playoff_context.engine._sample_scores', return_value=(5.0, 10.0)), \
                patch('playoff_context.engine.rank_teams', side_effect=capture):
            simulate(self.teams, self.games, self.rules, 1)
        records, points = seen[0]
        self.assertEqual(records, {'A': (1, 2, 0), 'B': (2, 1, 0)})
        self.assertEqual(points, {'A': 205.0, 'B': 200.0})

    def test_conditional_scores_are_correctly_ordered_even_for_rare_upsets(self):
        home, away = Strength(500.0, 12.0), Strength(1.0, 12.0)
        for forced_home in (False, True):
            for seed in range(10):
                hs, as_ = _sample_scores(home, away, Random(seed), forced_home)
                self.assertEqual(hs > as_, forced_home)
                self.assertNotEqual(hs, as_)

    def test_forced_draws_preserve_the_conditional_normal_distribution(self):
        rng = Random(31)
        scores = [_sample_scores(Strength(0, 1), Strength(0, 1), rng, True)
                  for _ in range(6000)]
        # For independent standard Normals conditioned on H>A, E[H]=1/sqrt(pi).
        self.assertAlmostEqual(sum(h for h, _ in scores) / len(scores), 1 / math.sqrt(math.pi), delta=.06)
        self.assertAlmostEqual(sum(a for _, a in scores) / len(scores), -1 / math.sqrt(math.pi), delta=.06)

    def test_h2h_mode_requires_the_full_historical_ledger(self):
        rules = replace(self.rules, qualification_policy='DIVISION_WINNERS_PLUS_WILDCARDS',
                        tiebreaker='H2H_RECORD', divisions={'A': 'X', 'B': 'X'})
        for ledger in ((), [('A', 'B', 'A')], [('A', 'B', 'Z')], [None]):
            with self.subTest(ledger=ledger), self.assertRaises(ValueError):
                simulate(self.teams, self.games, rules, 1, completed_outcomes=ledger)
        valid = [('A', 'B', 'A'), ('A', 'B', 'B')]
        result = simulate(self.teams, self.games, rules, 5, completed_outcomes=valid)
        self.assertEqual(sum(row['division_title_probability'] for row in result.values()), 1)
        self.assertTrue(all('CONDITIONAL_ON_DOCUMENTED_ESPN_DEFAULT' in row['rules_assumption']
                            for row in result.values()))

    def test_h2h_receives_coherent_pf_pa_and_completed_plus_simulated_results(self):
        from playoff_context.seeding import rank_espn
        rules = replace(self.rules, qualification_policy='DIVISION_WINNERS_PLUS_WILDCARDS',
                        tiebreaker='H2H_RECORD', divisions={'A': 'X', 'B': 'X'})
        ledger = [('A', 'B', 'A'), ('A', 'B', 'B')]
        seen = []
        def capture(records, pf, pa, outcomes, divisions, rng):
            seen.append((records, pf, pa, outcomes))
            return rank_espn(records, pf, pa, outcomes, divisions, rng)
        with patch('playoff_context.engine._sample_scores', return_value=(5.0, 10.0)), \
                patch('playoff_context.seeding.rank_espn', side_effect=capture):
            simulate(self.teams, self.games, rules, 1, completed_outcomes=ledger)
        records, pf, pa, outcomes = seen[0]
        self.assertEqual(records, {'A': (1, 2, 0), 'B': (2, 1, 0)})
        self.assertEqual(pf, {'A': 205.0, 'B': 200.0})
        self.assertEqual(pa, {'A': 200.0, 'B': 205.0})
        self.assertEqual(outcomes, ledger + [('A', 'B', 'B')])

    def test_common_random_stream_preserves_all_unforced_games(self):
        teams = {tid: TeamState(tid, tid, 0, 0) for tid in 'ABCD'}
        games = [Game(1, 'A', 'B'), Game(1, 'C', 'D'), Game(2, 'A', 'C'), Game(2, 'B', 'D')]
        rules = LeagueRules(2, 2, 'POINTS_FOR', qualification_policy='OVERALL')
        traces = []
        for winner in ('A', 'B'):
            trace = []
            def capture(home, away, rng, forced_home=None):
                scores = _sample_scores(home, away, rng, forced_home)
                trace.append(scores)
                return scores
            with patch('playoff_context.engine._sample_scores', side_effect=capture):
                simulate(teams, games, rules, 3, 77, {(1, 'A', 'B'): winner})
            traces.append(trace)
        for index in range(len(traces[0])):
            if index % len(games):
                self.assertEqual(traces[0][index], traces[1][index])

    def test_leverage_is_signed_and_uses_same_seed(self):
        first = {'A': {'playoff_probability': .4}, 'B': {'playoff_probability': .6}}
        second = {'A': {'playoff_probability': .5}, 'B': {'playoff_probability': .5}}
        with patch('playoff_context.engine.simulate', side_effect=[first, second]) as mocked:
            result = conditional_leverage(self.teams, self.games, self.rules, self.games[0], 10, 91)
        self.assertAlmostEqual(result['A']['leverage_delta_pp'], -10)
        self.assertEqual(mocked.call_args_list[0].args[4], mocked.call_args_list[1].args[4])

    def test_probability_and_seed_totals_are_conserved(self):
        result = simulate(self.teams, self.games, self.rules, 400, 7)
        self.assertAlmostEqual(sum(row['playoff_probability'] for row in result.values()), 1)
        for row in result.values():
            self.assertEqual(row['class'], 'PROBABILISTIC')
            self.assertAlmostEqual(sum(row['seed_probability'].values()), 1)
        self.assertAlmostEqual(sum(row['expected_final_wins'] for row in result.values()), 3)

    def test_normal_win_probability_matches_sampling_distribution(self):
        self.assertEqual(win_probability(Strength(100, 20), Strength(100, 20)), .5)
        self.assertGreater(win_probability(Strength(140, 20), Strength(100, 20)), .9)


class TestNormalizationHardening(unittest.TestCase):
    def setUp(self):
        self.row = {'winner': 'HOME', 'home': {'teamId': 'A', 'totalPoints': 110},
                    'away': {'teamId': 'B', 'totalPoints': 100}}
        self.payload = {'week': 3, 'matchups': [self.row]}

    def lock(self, payload, **kwargs):
        return require_final_week(payload, expected_team_ids=['A', 'B'], expected_week=3, **kwargs)

    def test_result_lock_fails_closed_on_incomplete_and_unfinalized_payloads(self):
        for payload in ({}, {'matchups': []}, {'week': 3, 'matchups': [{}]},
                        {'week': 3, 'matchups': [{**self.row, 'winner': None}]},
                        {'week': 3, 'matchups': [{**self.row, 'winner': 'IN_PROGRESS'}]},
                        {'week': 3, 'matchups': [{**self.row, 'winner': 'UNDECIDED'}]},
                        {'matchups': [self.row]}, {'week': 4, 'matchups': [self.row]}):
            with self.subTest(payload=payload), self.assertRaises(RuntimeError):
                self.lock(payload)

    def test_result_lock_checks_scores_participants_and_coverage(self):
        self.lock(self.payload)
        for row in ({**self.row, 'winner': 'AWAY'},
                    {**self.row, 'away': {'teamId': 'B', 'totalPoints': math.nan}},
                    {**self.row, 'away': {'teamId': 'A', 'totalPoints': 100}},
                    {**self.row, 'away': {'teamId': 'C', 'totalPoints': 100}},
                    {**self.row, 'home': {'teamId': 'A'}}):
            with self.subTest(row=row), self.assertRaises(RuntimeError):
                self.lock({'week': 3, 'matchups': [row]})
        with self.assertRaises(RuntimeError):
            self.lock({'week': 3, 'matchups': [self.row, self.row]})

    def test_slot_points_allows_only_explicit_provider_tie_resolution(self):
        row = {**self.row, 'away': {'teamId': 'B', 'totalPoints': 110}}
        payload = {'week': 3, 'matchups': [row]}
        with self.assertRaises(RuntimeError):
            self.lock(payload)
        self.lock(payload, matchup_tie_rule='SLOT_POINTS')
        row['winner'] = 'AWAY'
        self.lock(payload, matchup_tie_rule='SLOT_POINTS')
        row['winner'] = 'UNDECIDED'
        with self.assertRaises(RuntimeError):
            self.lock(payload, matchup_tie_rule='SLOT_POINTS')

    def test_standings_never_default_missing_records_or_overwrite_ids(self):
        row = {'teamId': 'A', 'wins': 1, 'losses': 1, 'ties': 0, 'pointsFor': 200}
        self.assertEqual(normalize_teams([row], {'A': [90, 110]})['A'].wins, 1)
        for rows in ([row, row], [{'teamId': 'A'}], [{**row, 'wins': 1.8}],
                     [{**row, 'pointsFor': math.inf}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                normalize_teams(rows, {})

    def test_future_schedule_does_not_silently_drop_missing_sides_or_weeks(self):
        weeks = [{'week': 3, 'matchups': [self.row]}]
        result = normalize_future_games(weeks, 3, 3, expected_team_ids=['A', 'B'])
        self.assertEqual(result, [Game(3, 'A', 'B')])
        cases = ([], [{'matchups': [self.row]}], [{'week': 3, 'matchups': []}],
                 [{'week': 3, 'matchups': [{'home': {'teamId': 'A'}, 'away': {}}]}],
                 [{'week': 3, 'matchups': [self.row, self.row]}], weeks * 2,
                 [{'week': 3, 'matchups': [{**self.row, 'home': {'teamId': 'A', 'totalProjectedPoints': math.nan}}]}])
        for broken in cases:
            with self.subTest(weeks=broken), self.assertRaises(ValueError):
                normalize_future_games(broken, 3, 3, expected_team_ids=['A', 'B'])
        self.assertEqual(normalize_future_games([], 4, 3), [])


if __name__ == '__main__':
    unittest.main()
