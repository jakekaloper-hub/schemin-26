"""Synthetic receipt-consistency checks; no private league fixture or calibration claim."""
import copy
import math
import unittest

from test_model_validation import VALIDATION
from test_pipeline import NOW, fixture
from playoff_context.pipeline import attach_validation, build_report


def diagnostic_pair(*, stronger_predictions=False, seed_mismatch=False, with_sources=False):
    capture, config = fixture()
    config.update(qualification_policy='DIVISION_WINNERS_PLUS_WILDCARDS',
                  divisions={'1': 'X', '2': 'X', '3': 'Y', '4': 'Y'},
                  manual_override_review='NO_EDIT_REPORTED')
    capture['league_info']['data']['status'] = {'isPlayoffMatchupEdited': False}
    provider_order = ['3', '1', '2', '4']
    if stronger_predictions:
        game = capture['weeks'][1]['data']['matchups'][0]
        game['home']['totalPoints'], game['away']['totalPoints'], game['winner'] = 95, 85, 'HOME'
        for team in capture['standings']['data']['standings']:
            if team['teamId'] == 1:
                team.update(wins=2, losses=0, pointsFor=195, pointsAgainst=175)
            elif team['teamId'] == 3:
                team.update(wins=1, losses=1, pointsFor=165, pointsAgainst=165)
        provider_order = ['1', '3', '2', '4']
    if seed_mismatch:
        provider_order[0], provider_order[1] = provider_order[1], provider_order[0]
    for team in capture['standings']['data']['standings']:
        team['playoffSeed'] = provider_order.index(str(team['teamId'])) + 1
    diagnostic = VALIDATION.build_diagnostic(capture, config, start_week=2, end_week=2,
                                            now=NOW, seed=9)
    report = build_report(capture, config, now=NOW, simulations=25, seed=9)
    return (report, diagnostic, capture, config) if with_sources else (report, diagnostic)


class DiagnosticAcceptanceTests(unittest.TestCase):
    def assert_rejected_without_mutating_report(self, report, diagnostic, **source):
        original = copy.deepcopy(report)
        with self.assertRaises(ValueError):
            attach_validation(report, diagnostic, **source)
        self.assertEqual(report, original)

    def test_genuine_receipt_keeps_underperforming_model_held(self):
        report, diagnostic, capture, config = diagnostic_pair(with_sources=True)
        self.assertGreater(diagnostic['aggregate']['brier_score'], .25)
        self.assertEqual(diagnostic['aggregate']['matchup_count'], 2)
        attach_validation(report, diagnostic, capture=capture, config=config)
        self.assertEqual(report['forecast']['editorial_gate'], 'HOLD_BASELINE_NOT_BEATEN')
        self.assertEqual(report['forecast']['model_diagnostic']['source_replay']['status'], 'PASS')
        self.assertFalse(report['forecast']['editorial_probability_eligible'])
        self.assertFalse(report['publication_authorized'])

    def test_better_retrospective_sample_does_not_authorize_forecast(self):
        report, diagnostic, capture, config = diagnostic_pair(stronger_predictions=True, with_sources=True)
        self.assertLess(diagnostic['aggregate']['brier_score'], .25)
        self.assertLess(diagnostic['aggregate']['log_loss_nats'], math.log(2))
        attach_validation(report, diagnostic, capture=capture, config=config)
        self.assertEqual(report['forecast']['editorial_gate'], 'HOLD_EXTERNAL_CALIBRATION_AND_INDEPENDENT_ACCEPTANCE')
        self.assertFalse(report['forecast']['editorial_probability_eligible'])

    def test_hash_matching_forged_receipt_is_not_evidence_of_baseline_improvement(self):
        report, diagnostic = diagnostic_pair()
        diagnostic.update(status='REJECTED', model_version='foreign-model',
                          validation_scope='PLAYOFF_CALIBRATION_CERTIFIED',
                          evaluation_weeks={'first': 88, 'last': 99})
        diagnostic['aggregate'].update(brier_score=-7, constant_half_probability_brier=999)
        diagnostic['input_validation']['evaluated_at'] = '2030-01-01T00:00:00Z'
        diagnostic['provenance']['model_and_diagnostic_code_sha256'] = '0' * 64
        self.assert_rejected_without_mutating_report(report, diagnostic)

    def test_scores_are_recomputed_instead_of_trusting_claimed_aggregate(self):
        for corrupt in (
            lambda d: d['aggregate'].update(brier_score=-7),
            lambda d: d['aggregate'].update(constant_half_probability_brier=999),
            lambda d: d['aggregate'].update(log_loss_nats=-1),
            lambda d: d['aggregate'].update(binary_pair_count=42),
            lambda d: d['predictions'][0].update(home_win_probability=float('nan')),
            lambda d: d['predictions'][0].update(brier=0, log_loss=0),
            lambda d: d['by_week']['2'].update(brier_score=0),
        ):
            with self.subTest(corrupt=corrupt):
                report, diagnostic = diagnostic_pair()
                corrupt(diagnostic)
                self.assert_rejected_without_mutating_report(report, diagnostic)

    def test_current_evaluator_and_source_chronology_must_match(self):
        for corrupt in (
            lambda d: d['provenance'].update(model_and_diagnostic_code_sha256='0' * 64),
            lambda d: d['provenance'].update(ranking_seed=10),
            lambda d: d.update(model_version='foreign-model'),
            lambda d: d.update(status='REJECTED'),
            lambda d: d.update(validation_scope='PLAYOFF_CALIBRATION_CERTIFIED'),
            lambda d: d['input_validation'].update(evaluated_at='2030-01-01T00:00:00Z'),
            lambda d: d['input_validation'].update(source_as_of='2026-11-17T15:59:59Z'),
            lambda d: d.update(evaluation_mode='HISTORICAL_REPLAY'),
        ):
            with self.subTest(corrupt=corrupt):
                report, diagnostic = diagnostic_pair()
                corrupt(diagnostic)
                self.assert_rejected_without_mutating_report(report, diagnostic)

    def test_future_training_or_incomplete_evaluation_sample_is_rejected(self):
        for corrupt in (
            lambda d: d.update(evaluation_weeks={'first': 88, 'last': 99}),
            lambda d: d['predictions'].pop(),
            lambda d: d['predictions'].__setitem__(1, copy.deepcopy(d['predictions'][0])),
            lambda d: d['predictions'][0].update(training_last_week=2),
            lambda d: d['predictions'][0]['training_scores_per_team'].update({'1': 2}),
        ):
            with self.subTest(corrupt=corrupt):
                report, diagnostic = diagnostic_pair()
                corrupt(diagnostic)
                self.assert_rejected_without_mutating_report(report, diagnostic)

    def test_honest_seed_mismatch_overrides_favorable_prediction_metric(self):
        report, diagnostic, capture, config = diagnostic_pair(
            stronger_predictions=True, seed_mismatch=True, with_sources=True)
        seeds = diagnostic['current_seed_reconciliation']
        self.assertFalse(seeds['exact_order_match'])
        attach_validation(report, diagnostic, capture=capture, config=config)
        self.assertEqual(report['forecast']['editorial_gate'], 'HOLD_SEED_RECONCILIATION_MISMATCH')
        self.assertFalse(report['forecast']['editorial_probability_eligible'])
        seeds['exact_order_match'] = True
        self.assert_rejected_without_mutating_report(report, diagnostic)

    def test_without_source_replay_a_better_claim_remains_unverified(self):
        report, diagnostic = diagnostic_pair(stronger_predictions=True)
        attach_validation(report, diagnostic)
        self.assertEqual(report['forecast']['editorial_gate'], 'HOLD_DIAGNOSTIC_SOURCE_NOT_REPLAYED')
        self.assertEqual(report['forecast']['model_diagnostic']['source_replay']['status'], 'NOT_PERFORMED')
        self.assertFalse(report['forecast']['editorial_probability_eligible'])

    def test_outcome_fitted_strengths_cannot_impersonate_a_replayed_model(self):
        report, diagnostic, capture, config = diagnostic_pair(with_sources=True)
        for row in diagnostic['predictions']:
            observed = row['observed_home_win']
            row.update(home_strength_mean=10000 if observed else 0,
                       away_strength_mean=0 if observed else 10000,
                       home_strength_sigma=1, away_strength_sigma=1,
                       home_win_probability=float(observed), brier=0.0,
                       log_loss_probability_clipped=True)
            clipped = min(1-1e-15, max(1e-15, float(observed)))
            row['log_loss'] = -observed*math.log(clipped)-(1-observed)*math.log1p(-clipped)
        diagnostic['aggregate'] = VALIDATION.metric_summary(diagnostic['predictions'])
        diagnostic['by_week']['2'] = VALIDATION.metric_summary(diagnostic['predictions'])
        self.assertEqual(diagnostic['aggregate']['brier_score'], 0)
        # A mathematically consistent forged summary is not accepted as evidence
        # of improvement even when the frozen source was omitted by the caller.
        unverified = copy.deepcopy(report)
        attach_validation(unverified, diagnostic)
        self.assertEqual(unverified['forecast']['editorial_gate'], 'HOLD_DIAGNOSTIC_SOURCE_NOT_REPLAYED')
        # Supplying the matching original source exposes the outcome fitting.
        self.assert_rejected_without_mutating_report(report, diagnostic, capture=capture, config=config)

    def test_replay_requires_both_original_source_objects(self):
        report, diagnostic, capture, config = diagnostic_pair(with_sources=True)
        self.assert_rejected_without_mutating_report(report, diagnostic, capture=capture)
        changed = copy.deepcopy(capture)
        changed['weeks'][0]['data']['matchups'][0]['home']['totalPoints'] += 1
        self.assert_rejected_without_mutating_report(report, diagnostic, capture=changed, config=config)

    def test_attached_summary_cannot_change_by_mutating_the_input_receipt(self):
        report, diagnostic = diagnostic_pair()
        attach_validation(report, diagnostic)
        attached = copy.deepcopy(report['forecast']['model_diagnostic'])
        diagnostic['aggregate']['brier_score'] = -7
        diagnostic['evaluation_weeks']['last'] = 99
        self.assertEqual(report['forecast']['model_diagnostic'], attached)


if __name__ == '__main__':
    unittest.main()
