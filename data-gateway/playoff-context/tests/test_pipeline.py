import copy
import importlib
import unittest
from datetime import datetime, timezone


NOW = datetime(2026, 11, 17, 16, 30, tzinfo=timezone.utc)


def fixture():
    names = {str(i): f'Team {i}' for i in range(1, 5)}
    def game(week, home, away, hp, ap, winner):
        return {'matchupPeriodId': week, 'winner': winner,
                'home': {'teamId': home, 'teamName': names[str(home)], 'totalPoints': hp},
                'away': {'teamId': away, 'teamName': names[str(away)], 'totalPoints': ap}}
    def observation(data):
        return {'captured_at': '2026-11-17T16:00:00Z', 'success': True, 'data': data}
    weeks = []
    rows = [
        [game(1, 1, 2, 100, 90, 'HOME'), game(1, 3, 4, 80, 70, 'HOME')],
        [game(2, 1, 3, 85, 95, 'AWAY'), game(2, 2, 4, 110, 100, 'HOME')],
        [game(3, 1, 4, 0, 0, 'UNDECIDED'), game(3, 2, 3, 0, 0, 'UNDECIDED')],
    ]
    for n, games in enumerate(rows, 1):
        weeks.append({'requested_week': n, **observation({'leagueId': '1417621',
            'seasonYear': 2026, 'matchupPeriod': n, 'matchups': games})})
    standings = [dict(teamId=i, teamName=names[str(i)], wins=w, losses=l, ties=0,
                      pointsFor=pf, pointsAgainst=pa, playoffSeed=i)
                 for i, w, l, pf, pa in [(1, 1, 1, 185, 185), (2, 1, 1, 200, 200),
                                        (3, 2, 0, 175, 155), (4, 0, 2, 170, 190)]]
    capture = {'schema_version': 1, 'provider': 'flaim', 'platform': 'espn',
        'league_id': '1417621', 'season': 2026, 'through_week': 2,
        'league_info': observation({'id': 1417621, 'seasonId': 2026, 'size': 4,
            'teams': [{'teamId': int(k), 'teamName': v} for k, v in names.items()],
            'schedule': {'playoffSeedingRule': 'H2H_RECORD'},
            'scoringSettings': {'matchupTieRule': 'SLOT_POINTS'}}),
        'standings': observation({'leagueId': '1417621', 'seasonYear': 2026, 'standings': standings}),
        'weeks': weeks}
    config = {'league_id': '1417621', 'season': 2026, 'team_count': 4,
        'regular_season_weeks': 3, 'playoff_teams': 2, 'tiebreaker': 'H2H_RECORD',
        'qualification_policy': 'UNKNOWN', 'rule_evidence': ['synthetic test fixture']}
    return capture, config


class PipelineTests(unittest.TestCase):
    def pipeline(self):
        spec = importlib.util.find_spec('playoff_context.pipeline')
        self.assertIsNotNone(spec, 'production snapshot runner is missing')
        return importlib.import_module('playoff_context.pipeline')

    def test_real_arithmetic_and_rule_hold_are_separate(self):
        capture, rules = fixture()
        report = self.pipeline().build_report(capture, rules, now=NOW, simulations=100)
        self.assertEqual(report['input_validation']['completed_matchups'], 4)
        self.assertEqual(report['input_validation']['remaining_matchups'], 2)
        self.assertEqual(report['teams']['2']['all_play'], {'wins': 5, 'losses': 1, 'ties': 0})
        self.assertAlmostEqual(report['teams']['2']['schedule_neutral_wins'], 5/3)
        self.assertAlmostEqual(report['teams']['3']['schedule_luck_wins'], 4/3)
        self.assertEqual(report['forecast']['status'], 'HOLD')
        self.assertIsNone(report['teams']['2']['playoff_probability'])
        self.assertFalse(report['publication_authorized'])

    def test_stale_and_future_dated_observations_fail(self):
        for date in ['2026-11-15T16:00:00Z', '2026-11-17T17:00:00Z']:
            capture, rules = fixture()
            capture['weeks'][0]['captured_at'] = date
            with self.assertRaisesRegex(ValueError, 'STALE|future'):
                self.pipeline().build_report(capture, rules, now=NOW)

    def test_missing_week_undecided_or_wrong_scores_fail(self):
        for mutate in [lambda c: c['weeks'].pop(0),
                       lambda c: c['weeks'][1]['data']['matchups'][0].update(winner='UNDECIDED'),
                       lambda c: c['standings']['data']['standings'][0].update(pointsFor=184)]:
            capture, rules = fixture(); mutate(capture)
            with self.assertRaises(ValueError):
                self.pipeline().build_report(capture, rules, now=NOW)

    def test_wrong_season_duplicate_team_and_unsafe_number_fail(self):
        for mutate in [lambda c: c['weeks'][0]['data'].update(seasonYear=2025),
                       lambda c: c['standings']['data']['standings'][1].update(teamId=1),
                       lambda c: c['weeks'][0]['data']['matchups'][0]['home'].update(totalPoints=float('nan'))]:
            capture, rules = fixture(); mutate(capture)
            with self.assertRaises(ValueError):
                self.pipeline().build_report(capture, rules, now=NOW)

    def test_input_hash_changes_and_no_later_week_leaks(self):
        capture, rules = fixture()
        report = self.pipeline().build_report(capture, rules, now=NOW, simulations=100)
        self.assertEqual(len(report['provenance']['input_sha256']), 64)
        bad = copy.deepcopy(capture); bad['weeks'][2]['data']['matchups'][0]['winner'] = 'HOME'
        with self.assertRaisesRegex(ValueError, 'cutoff|future'):
            self.pipeline().build_report(bad, rules, now=NOW)

    def test_zero_observations_have_positive_uncertainty_and_no_editorial_clearance(self):
        capture, rules = fixture()
        rules.update(qualification_policy='OVERALL', tiebreaker='POINTS_FOR', playoff_teams=1,
                     manual_override_review='NO_EDIT_REPORTED')
        capture['league_info']['data']['schedule']['playoffSeedingRule'] = 'POINTS_FOR'
        capture['league_info']['data']['status'] = {'isPlayoffMatchupEdited': False}
        report = self.pipeline().build_report(capture, rules, now=NOW, simulations=50)
        self.assertEqual(report['teams']['4']['playoff_probability'], 0)
        self.assertIn('monte_carlo_95_interval', report['teams']['4'])
        self.assertGreater(report['teams']['4']['monte_carlo_95_interval'][1], 0)
        self.assertFalse(report['forecast'].get('editorial_probability_eligible', True))

    def test_unbound_validation_cannot_attach_to_report(self):
        capture, rules = fixture()
        module = self.pipeline()
        report = module.build_report(capture, rules, now=NOW, simulations=10)
        with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
            module.attach_validation(report, {'provenance': {'input_sha256':'0'*64}})


if __name__ == '__main__':
    unittest.main()
