"""Independent regressions for attaching analytics to the correct Memo issue."""
import importlib.util
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'data-gateway'/'playoff-context'/'src'))
sys.path.insert(0, str(ROOT/'data-gateway'/'playoff-context'/'tests'))

from test_pipeline import fixture, NOW
from test_pipeline_independent import ready_fixture
from playoff_context.pipeline import build_report


class MemoPlayoffIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT/'memo-os'/'playoff_context_adapter.py'
        spec = importlib.util.spec_from_file_location('identity_test_memo_adapter', path)
        cls.adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.adapter)

    def report(self, *, league_id='1417621', season=2026):
        capture, rules = fixture()
        capture['league_id'] = rules['league_id'] = league_id
        capture['season'] = rules['season'] = season
        capture['league_info']['data'].update(id=int(league_id), seasonId=season)
        capture['standings']['data'].update(leagueId=league_id, seasonYear=season)
        for week in capture['weeks']:
            week['data'].update(leagueId=league_id, seasonYear=season)
        return build_report(capture, rules, now=NOW, simulations=10)

    def previs(self, issue_id='SCHEMIN-26-W02'):
        return {'issue_id': issue_id, 'final_fact_lock': False,
                'pages': [{'page_id': 'W02-P30', 'body': 'Preserve this issue copy.'}]}

    def packet(self, report, previs):
        return self.adapter.build_memo_packet(report, previs=previs, now=NOW,
                                             bindings={'W02-P30': 'playoff_picture'})

    def test_other_league_report_cannot_bind_to_schemin(self):
        with self.assertRaisesRegex(ValueError, 'league|identity'):
            self.packet(self.report(league_id='9999999'), self.previs())

    def test_other_season_report_cannot_bind_to_current_issue(self):
        with self.assertRaisesRegex(ValueError, 'season|identity'):
            self.packet(self.report(season=2025), self.previs())

    def test_issue_identity_must_agree_even_when_page_prefix_matches(self):
        report = self.report()
        for issue_id in ('SCHEMIN-25-W02', 'SCHEMIN-26-W03'):
            with self.subTest(issue_id=issue_id):
                with self.assertRaisesRegex(ValueError, 'issue|season|week|identity'):
                    self.packet(report, self.previs(issue_id))

    def test_duplicate_page_ids_cannot_silently_select_one_copy(self):
        previs = self.previs()
        previs['pages'].append({'page_id': 'W02-P30', 'body': 'A conflicting second page.'})
        with self.assertRaisesRegex(ValueError, 'duplicate|unique|page'):
            self.packet(self.report(), previs)

    def test_valid_packet_retains_league_and_season_identity(self):
        packet = self.packet(self.report(), self.previs())
        self.assertEqual(packet['league_id'], '1417621')
        self.assertEqual(packet['season'], 2026)
        self.assertEqual(packet['through_week'], 2)
        self.assertEqual(packet['hydrated_previs']['issue_id'], 'SCHEMIN-26-W02')
        self.assertFalse(packet['publication_authorized'])
        self.assertFalse(packet['hydrated_previs']['final_fact_lock'])

    def test_ineligible_forecasts_cannot_leak_through_nested_team_fields(self):
        capture, rules = ready_fixture()
        report = build_report(capture, rules, now=NOW, simulations=100)
        report['forecast']['editorial_probability_eligible'] = False
        report['teams']['1']['future_extension'] = {
            'nested': {'playoff_probability': 0.99},
        }
        report['editorial_candidates'].append({
            'team_id': '1', 'class': 'PROBABILISTIC', 'kind': 'HIGH_LEVERAGE',
            'conditional_win_probability': 75, 'conditional_loss_probability': 25,
            'leverage_delta_pp': 50,
        })
        original = copy.deepcopy(report)
        packet = self.packet(report, self.previs())
        forbidden = {
            'playoff_probability', 'seed_probability', 'division_title_probability',
            'next_game_leverage', 'conditional_win_probability',
            'conditional_loss_probability', 'leverage_delta_pp',
            'expected_final_wins', 'final_wins_p10_p90',
            'playoff_probability_mc_standard_error', 'monte_carlo_standard_error_pp',
            'monte_carlo_95_interval', 'qualifying_trials',
        }

        def inspect(value, path='packet'):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertNotIn(key, forbidden, f'forecast leak at {path}/{key}')
                    inspect(child, f'{path}/{key}')
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    inspect(child, f'{path}/{index}')

        inspect(packet)
        self.assertTrue(all(row['class'] == 'DESCRIPTIVE'
                            for row in packet['teams'].values()))
        self.assertTrue(all(row.get('class') != 'PROBABILISTIC'
                            for row in packet['interpretations']))
        self.assertEqual(packet['teams']['1']['all_play'], original['teams']['1']['all_play'])
        self.assertEqual(report, original, 'the audit report must retain its source values')


if __name__ == '__main__':
    unittest.main()
