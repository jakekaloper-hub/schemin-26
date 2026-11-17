"""Independent failure cases for provider/config boundaries and cutoff integrity."""
import copy
import unittest

from test_pipeline import fixture, NOW
from playoff_context.pipeline import build_report


def ready_fixture():
    """A small valid overall/PF league isolates adapter behavior from ESPN seeding."""
    capture, rules = fixture()
    rules.update(
        qualification_policy='OVERALL',
        tiebreaker='POINTS_FOR',
        manual_override_review='NO_EDIT_REPORTED',
    )
    info = capture['league_info']['data']
    info['status'] = {'isPlayoffMatchupEdited': False}
    info['schedule'].update(
        playoffSeedingRule='POINTS_FOR',
        playoffTeamCount=2,
        regularSeasonMatchupPeriodCount=3,
    )
    return capture, rules


class IndependentPipelineTests(unittest.TestCase):
    def run_report(self, capture, rules):
        return build_report(capture, rules, now=NOW, simulations=250, seed=410)

    def assert_no_forecast(self, capture, rules):
        """Contradictory inputs may reject or retain descriptive-only output."""
        try:
            report = self.run_report(capture, rules)
        except ValueError:
            return
        self.assertEqual(report['forecast']['status'], 'HOLD')
        self.assertTrue(report['forecast']['blockers'])
        self.assertTrue(all(row['playoff_probability'] is None
                            for row in report['teams'].values()))
        self.assertTrue(all(row['exact_status']['status'] == 'UNKNOWN'
                            for row in report['teams'].values()))
        self.assertFalse(report['publication_authorized'])

    def test_valid_provider_baseline_can_reach_candidate_state(self):
        capture, rules = ready_fixture()
        report = self.run_report(capture, rules)
        self.assertEqual(report['forecast']['status'], 'CONDITIONAL_MODEL_ESTIMATE')
        self.assertAlmostEqual(sum(row['playoff_probability']
                                   for row in report['teams'].values()), 2)
        self.assertFalse(report['publication_authorized'])

    def test_config_cannot_overrule_provider_manual_edit(self):
        capture, rules = ready_fixture()
        capture['league_info']['data']['status']['isPlayoffMatchupEdited'] = True
        self.assert_no_forecast(capture, rules)

    def test_missing_manual_edit_observation_is_not_negative_evidence(self):
        capture, rules = ready_fixture()
        capture['league_info']['data'].pop('status')
        self.assert_no_forecast(capture, rules)

    def test_provider_berth_count_must_match_configuration(self):
        capture, rules = ready_fixture()
        capture['league_info']['data']['schedule']['playoffTeamCount'] = 3
        self.assert_no_forecast(capture, rules)

    def test_provider_regular_season_horizon_must_match_configuration(self):
        capture, rules = ready_fixture()
        capture['league_info']['data']['schedule']['regularSeasonMatchupPeriodCount'] = 4
        self.assert_no_forecast(capture, rules)

    def test_undecided_is_not_sufficient_to_prove_future_games_unstarted(self):
        for field, value in (
            ('currentPoints', 22.4),
            ('totalPoints', 22.4),
            ('pointsByScoringPeriod', {'3': 22.4}),
            ('currentPoints', -2.0),
        ):
            with self.subTest(field=field, value=value):
                capture, rules = ready_fixture()
                capture['weeks'][2]['data']['matchups'][0]['home'][field] = value
                with self.assertRaises(ValueError):
                    self.run_report(capture, rules)

    def test_zero_score_future_observations_remain_usable(self):
        capture, rules = ready_fixture()
        for game in capture['weeks'][2]['data']['matchups']:
            for side in ('home', 'away'):
                game[side].update(currentPoints=0.0, pointsByScoringPeriod={'3': 0.0})
        report = self.run_report(capture, rules)
        self.assertEqual(report['forecast']['status'], 'CONDITIONAL_MODEL_ESTIMATE')

    def test_default_historical_model_does_not_consume_hidden_projection_prior(self):
        low, rules = ready_fixture()
        high = copy.deepcopy(low)
        low['weeks'][2]['data']['matchups'][0]['home']['totalProjectedPoints'] = 1
        high['weeks'][2]['data']['matchups'][0]['home']['totalProjectedPoints'] = 500
        low_report = self.run_report(low, rules)
        high_report = self.run_report(high, rules)
        self.assertEqual(low_report['forecast']['status'], 'CONDITIONAL_MODEL_ESTIMATE')
        self.assertEqual(high_report['forecast']['status'], 'CONDITIONAL_MODEL_ESTIMATE')
        for team_id in low_report['teams']:
            for field in ('playoff_probability', 'seed_probability', 'expected_final_wins'):
                self.assertEqual(low_report['teams'][team_id][field],
                                 high_report['teams'][team_id][field])
        self.assertIs(low_report['forecast']['projections_used'], False)
        self.assertIs(high_report['forecast']['projections_used'], False)
        self.assertNotEqual(low_report['provenance']['input_sha256'],
                            high_report['provenance']['input_sha256'])

    def test_result_lock_failure_has_pipeline_validation_exception(self):
        capture, rules = ready_fixture()
        capture['weeks'][1]['data']['matchups'][0]['winner'] = 'UNDECIDED'
        with self.assertRaisesRegex(ValueError, 'RESULT_LOCK_REQUIRED'):
            self.run_report(capture, rules)


if __name__ == '__main__':
    unittest.main()
