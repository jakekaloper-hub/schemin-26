"""Adversarial checks for the descriptive-only Memo analytics boundary."""
import copy
from datetime import timedelta
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'data-gateway/playoff-context/src'))
sys.path.insert(0, str(ROOT / 'data-gateway/playoff-context/tests'))

from test_pipeline import NOW
from test_pipeline_independent import ready_fixture
from playoff_context.pipeline import build_report


class MemoPublicationGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            'publication_gate_adapter', ROOT / 'memo-os/playoff_context_adapter.py')
        cls.adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.adapter)

    def report(self):
        capture, rules = ready_fixture()
        return build_report(capture, rules, now=NOW, simulations=20, seed=99)

    def packet(self, report, **kwargs):
        return self.adapter.build_memo_packet(report, now=kwargs.pop('now', NOW), **kwargs)

    def assert_no_predictions(self, value):
        forbidden = {
            'playoff_probability', 'seed_probability', 'division_title_probability',
            'next_game_leverage', 'conditional_win_probability', 'conditional_loss_probability',
            'leverage_delta_pp', 'expected_final_wins', 'final_wins_p10_p90',
        }
        if isinstance(value, dict):
            self.assertFalse(forbidden.intersection(value))
            for child in value.values():
                self.assert_no_predictions(child)
        elif isinstance(value, list):
            for child in value:
                self.assert_no_predictions(child)

    def test_declared_eligibility_cannot_release_held_or_claimed_approved_odds(self):
        for gate in ('HOLD_PENDING_MODEL_VALIDATION_AND_INDEPENDENT_ACCEPTANCE', 'APPROVED'):
            with self.subTest(gate=gate):
                report = self.report()
                report['forecast'].update(editorial_probability_eligible=True, editorial_gate=gate)
                report['editorial_candidates'] = [
                    {'team_id': '1', 'class': 'PROBABILISTIC', 'kind': 'HIGH_LEVERAGE',
                     'conditional_win_probability': 99, 'leverage_delta_pp': 80}]
                original = copy.deepcopy(report)
                packet = self.packet(report)
                self.assert_no_predictions(packet)
                self.assertFalse(packet['forecast']['editorial_probability_eligible'])
                self.assertTrue(packet['forecast']['editorial_gate'].startswith('HOLD_'))
                self.assertEqual(packet['forecast']['status'], 'WITHHELD_FROM_MEMO')
                self.assertEqual(packet['interpretations'], [])
                self.assertFalse(packet['publication_authorized'])
                self.assertEqual(report, original)

    def test_nested_unknown_forecast_content_is_not_descriptive_data(self):
        report = self.report()
        team = report['teams']['1']
        team['all_play']['playoff_probability'] = .99
        team['weekly_median_record']['extension'] = {'seed_probability': {'1': 1}}
        team['remaining_schedule'][0]['playoff_probability'] = .99
        team['exact_status']['conditional_win_probability'] = 99
        report['forecast']['extension'] = {'playoff_probability': .99}
        report['forecast']['model_diagnostic'] = {
            'sha256': 'a' * 64, 'aggregate': {'playoff_probability': .99}}
        report['metric_definitions']['extension'] = {'playoff_probability': .99}
        packet = self.packet(report)
        self.assert_no_predictions(packet)
        self.assertEqual(packet['forecast']['model_diagnostic'], {'sha256': 'a' * 64})
        self.assertEqual(set(packet['teams']['1']['all_play']), {'wins', 'losses', 'ties'})

    def test_unclassified_probabilistic_and_exact_claims_are_withheld(self):
        report = self.report()
        report['teams']['1']['exact_status'] = {
            'status': 'CLINCHED', 'class': 'EXACT', 'proof': 'unaccepted prose'}
        report['editorial_candidates'] = [
            {'team_id': '1', 'kind': 'HIGH_LEVERAGE', 'conditional_win_probability': 99},
            {'team_id': '1', 'class': 'EXACT', 'kind': 'CLINCHED', 'reason': 'unaccepted prose'},
            {'team_id': '1', 'class': 'DESCRIPTIVE', 'kind': 'CLINCHED'},
            {'team_id': '1', 'class': 'DESCRIPTIVE', 'kind': 'SCORING_FORM', 'priority': 20,
             'reason': 'This team has clinched', 'playoff_probability': .99},
        ]
        packet = self.packet(report)
        self.assertEqual(packet['interpretations'], [
            {'team_id': '1', 'class': 'DESCRIPTIVE', 'kind': 'SCORING_FORM', 'priority': 20}])
        exact = packet['teams']['1']['exact_status']
        self.assertEqual((exact['status'], exact['class'], exact['proof']), ('UNKNOWN', 'UNRESOLVED', None))
        self.assert_no_predictions(packet)

    def test_known_descriptive_fields_require_types_not_nested_payloads(self):
        mutations = [
            lambda t: t['all_play'].update(wins={'playoff_probability': .99}),
            lambda t: t['weekly_median_record'].update(ties=True),
            lambda t: t['remaining_schedule'][0].update(opponent_scoring_average={'playoff_probability': .99}),
            lambda t: t.update(scoring_average='99%'),
            lambda t: t.update(all_play_win_rate=2),
        ]
        for mutate in mutations:
            report = self.report()
            mutate(report['teams']['1'])
            with self.subTest(team=report['teams']['1']), self.assertRaises(ValueError):
                self.packet(report)

    def test_declared_freshness_limit_cannot_extend_consumer_limit(self):
        report = self.report()
        report['input_validation']['source_as_of'] = (NOW - timedelta(days=2)).isoformat()
        report['input_validation']['freshness_slo_seconds'] = 10 ** 10
        with self.assertRaisesRegex(ValueError, 'STALE'):
            self.packet(report)

    def test_future_or_pre_source_evaluation_cannot_be_accepted(self):
        for evaluated in (NOW + timedelta(seconds=1), NOW - timedelta(days=1)):
            report = self.report()
            report['input_validation']['evaluated_at'] = evaluated.isoformat()
            with self.subTest(evaluated=evaluated), self.assertRaisesRegex(ValueError, 'evaluation'):
                self.packet(report)

    def test_historical_replay_remains_explicitly_historical(self):
        report = self.report()
        report['evaluation_mode'] = 'HISTORICAL_REPLAY'
        packet = self.packet(report, now=NOW)
        self.assertEqual(packet['evaluation_mode'], 'HISTORICAL_REPLAY')
        self.assertFalse(packet['publication_authorized'])

    def test_valid_pipeline_descriptive_values_are_preserved(self):
        report = self.report()
        packet = self.packet(report)
        for team_id, source in report['teams'].items():
            for field in ('team_id', 'name', 'wins', 'losses', 'ties', 'provider_seed',
                          'points_for', 'points_against', 'scoring_average', 'last_three_average',
                          'all_play', 'all_play_win_rate', 'weekly_median_record',
                          'schedule_neutral_wins', 'schedule_luck_wins', 'remaining_schedule',
                          'remaining_opponent_scoring_average'):
                self.assertEqual(packet['teams'][team_id][field], source[field])
        self.assert_no_predictions(packet)


if __name__ == '__main__':
    unittest.main()
