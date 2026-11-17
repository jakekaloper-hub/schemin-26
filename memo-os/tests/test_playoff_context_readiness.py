"""Synthetic regressions for actual-copy consumption and retained-claim holds."""
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    'tested_playoff_readiness', Path(__file__).resolve().parents[1]/'playoff_context_readiness.py')
READINESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READINESS)
NOW = datetime(2030, 10, 20, 12, 30, tzinfo=timezone.utc)
PAGE = 'W03-P27'


def sync_page(page, packet):
    """Model a producer rebuilding real copy/prompt mirrors from one source."""
    text = READINESS.COPY_MARKER+'\n'+json.dumps(page['draft_copy'], ensure_ascii=False)+'\n\nFACT POLICY\nFINAL'
    page['draft_copy_template'] = copy.deepcopy(page['draft_copy'])
    page['candidate_render_prompt'] = text
    page['illustrated_page_brief'] = {
        'publication_copy': copy.deepcopy(page['draft_copy']),
        'exact_copy_template': copy.deepcopy(page['draft_copy']), 'artist_prompt': text}
    receipt = page['analytics_consumption']
    receipt.update(report_sha256=packet['report_sha256'], source_snapshot=packet['source_snapshot'],
                   copy_sha256=READINESS.digest(page['draft_copy']))
    return {'page_id': page['page_id'], 'publication_copy': copy.deepcopy(page['draft_copy']),
            'prompt': text, 'analytics_consumption': copy.deepcopy(receipt),
            'sports_policy': {'official_winner_decided': True, 'source_capture_scope': 'FINAL_THROUGH_WEEK_3'}}


def fixture():
    packet = {
        'report_sha256': 'a'*64, 'source_snapshot': 'b'*64,
        'source_as_of': '2030-10-20T12:00:00+00:00', 'league_id': '123', 'season': 2030,
        'through_week': 3, 'forecast': {'editorial_probability_eligible': False, 'status': 'WITHHELD_FROM_MEMO'},
        'page_bindings': {PAGE: {'purpose': 'official_standings', 'candidate_only': True}},
        'teams': {
            '1': {'team_id': '1', 'name': 'Team Alpha', 'wins': 2, 'losses': 1, 'ties': 0,
                  'points_for': 321.5, 'provider_seed': 1, 'remaining_schedule': []},
            '2': {'team_id': '2', 'name': 'Team Beta', 'wins': 1, 'losses': 2, 'ties': 0,
                  'points_for': 311.75, 'provider_seed': 2, 'remaining_schedule': []},
        },
    }
    page = {'page_id': PAGE, 'draft_copy': {'body': 'Current scoring totals through three games.', 'rows': [
        {'team': 'Team Alpha', 'record': '2–1', 'seed': 1, 'points_for': '321.50'},
        {'team': 'Team Beta', 'record': '1–2', 'seed': 2, 'points_for': '311.75'},
    ]}, 'analytics_consumption': {'decision': 'ACCEPTED', 'metric_bindings': [
        {'source_pointer': '/teams/1/points_for', 'copy_pointer': '/rows/0/points_for', 'format': 'fixed_2'},
    ]}}
    source = {key: packet[key] for key in ('league_id', 'season', 'through_week', 'source_snapshot',
                                         'report_sha256', 'source_as_of')}
    source['result_lock'] = 'FINAL'
    previs = {'final_fact_lock': True, 'sports_snapshot_utc': packet['source_as_of'],
              'sports_source': source, 'pages': [page]}
    return packet, previs, {PAGE: sync_page(page, packet)}


def claim_receipt(packet, page, claim_type='EXACT'):
    text = page['draft_copy']['body']
    evidence = {'type': 'strict_record_bound', 'team_id': '1', 'berths': 1}
    return {'page_id': PAGE, 'copy_pointer': '/body', 'claim_type': claim_type,
            'disposition': 'ACCEPTED_FOR_EDITORIAL_REVIEW',
            'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'copy_sha256': READINESS.digest(page['draft_copy']),
            'report_sha256': packet['report_sha256'], 'source_snapshot': packet['source_snapshot'],
            'evidence': evidence, 'evidence_sha256': READINESS.digest(evidence)}


class PlayoffReadinessTests(unittest.TestCase):
    def audit(self, packet, previs, requests, **kwargs):
        return READINESS.audit_memo_readiness(packet, previs=previs, render_requests=requests,
                                             now=kwargs.pop('now', NOW), **kwargs)

    def codes(self, result):
        return {issue['code'] for issue in result['issues']}

    def test_real_consumption_checks_can_pass_without_granting_release(self):
        packet, previs, requests = fixture()
        before = copy.deepcopy((packet, previs, requests))
        result = self.audit(packet, previs, requests)
        self.assertEqual(result['issues'], [])
        self.assertTrue(result['consumption_witnessed'])
        self.assertFalse(result['copy_change_required'])
        for field in ('publication_authorized', 'canonical_fact_lock_certified', 'artwork_reviewed',
                      'external_director_approval_claimed'):
            self.assertFalse(result[field])
        self.assertEqual((packet, previs, requests), before)

    def test_reference_attachment_and_fresh_packet_do_not_refresh_old_copy(self):
        packet, previs, requests = fixture()
        packet['copy_change_required'] = False
        previs['final_fact_lock'] = False
        previs['sports_snapshot_utc'] = '2030-10-19T12:00:00+00:00'
        previs.pop('sports_source')
        previs['creative_revision'] = {'sports_status': 'All outcomes UNDECIDED; current-leads-hold.'}
        page = previs['pages'][0]
        page.pop('analytics_consumption')
        page['analytics_context'] = {'report_sha256': packet['report_sha256'], 'editorial_selection': 'PENDING'}
        result = self.audit(packet, previs, None)
        self.assertEqual(result['status'], 'HOLD')
        self.assertTrue(result['copy_change_required'])
        self.assertFalse(result['consumption_witnessed'])
        self.assertTrue({'PREVIS_NOT_FACT_LOCKED', 'PROVISIONAL_SPORTS_STATE', 'PREVIS_SNAPSHOT_NOT_RECONCILED',
                         'SOURCE_RECONCILIATION_NOT_WITNESSED', 'PAGE_CONSUMPTION_NOT_WITNESSED',
                         'RENDER_CONSUMPTION_NOT_WITNESSED'} <= self.codes(result))

    def test_source_freshness_is_rechecked_when_actual_consumer_runs(self):
        for review_time in [NOW+timedelta(days=2), NOW-timedelta(hours=1)]:
            with self.subTest(now=review_time):
                result = self.audit(*fixture(), now=review_time)
                self.assertIn('STALE_OR_FUTURE_ANALYTICS_SOURCE', self.codes(result))

    def test_updated_hashes_cannot_make_old_standings_values_correct(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['rows'][0].update(points_for='200.00', record='1–1', seed=2)
        requests[PAGE] = sync_page(page, packet)
        result = self.audit(packet, previs, requests)
        self.assertIn('STANDINGS_VALUE_DIFFERS_FROM_SOURCE', self.codes(result))
        self.assertIn('COPY_VALUE_DIFFERS_FROM_SOURCE', self.codes(result))
        comparison = next(x for x in result['compared_values'] if x['copy_pointer'] == '/rows/0/points_for')
        self.assertEqual((comparison['incoming'], comparison['copy_value']), ('321.50', '200.00'))

    def test_internal_team_id_cannot_mask_a_different_printed_name(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['rows'][0].update(team_id='1', team='Team Beta')
        requests[PAGE] = sync_page(page, packet)
        self.assertIn('STANDINGS_DISPLAY_NAME_MISMATCH', self.codes(self.audit(packet, previs, requests)))

    def test_bound_copy_and_source_hashes_must_match(self):
        for field in ['report_sha256', 'source_snapshot', 'copy_sha256']:
            packet, previs, requests = fixture()
            previs['pages'][0]['analytics_consumption'][field] = 'c'*64
            result = self.audit(packet, previs, requests)
            self.assertIn('CONSUMPTION_HASH_MISMATCH', self.codes(result))

    def test_correct_copy_outside_prompt_does_not_hide_stale_prompt_text(self):
        packet, previs, requests = fixture()
        stale = copy.deepcopy(previs['pages'][0]['draft_copy'])
        stale['body'] = 'Older printed copy.'
        text = READINESS.COPY_MARKER+'\n'+json.dumps(stale)
        requests[PAGE]['prompt'] = text
        previs['pages'][0]['candidate_render_prompt'] = text
        previs['pages'][0]['illustrated_page_brief']['artist_prompt'] = text
        self.assertIn('PROMPT_PUBLICATION_COPY_MISMATCH', self.codes(self.audit(packet, previs, requests)))

    def test_stale_nested_mirror_and_provisional_render_policy_hold(self):
        packet, previs, requests = fixture()
        previs['pages'][0]['illustrated_page_brief']['publication_copy']['body'] = 'Old body.'
        requests[PAGE]['sports_policy'] = {'official_winner_decided': False, 'source_capture_scope': 'CURRENT_PROVISIONAL_PRE_MNF'}
        codes = self.codes(self.audit(packet, previs, requests))
        self.assertIn('PREVIS_COPY_MIRROR_MISMATCH', codes)
        self.assertIn('RENDER_SPORTS_STILL_PROVISIONAL', codes)

    def test_future_week_page_cannot_claim_current_consumption(self):
        packet, previs, requests = fixture()
        previs['pages'][0]['page_id'] = 'W04-P27'
        codes = self.codes(self.audit(packet, previs, requests))
        self.assertIn('PAGE_WEEK_MISMATCH', codes)
        self.assertIn('BOUND_PAGE_ABSENT', codes)

    def test_retained_conditional_exact_claim_is_not_cleared_by_receipt_flags(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['body'] = 'If the current leads hold, another loss eliminates Team Beta.'
        requests[PAGE] = sync_page(page, packet)
        result = self.audit(packet, previs, requests, accepted_claims=[claim_receipt(packet, page)])
        self.assertIn('UNACCEPTED_EXACT_CLAIM', self.codes(result))

    def test_all_teams_and_no_clinches_are_exact_claims_too(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['body'] = 'All twelve teams still have a route and none has clinched.'
        requests[PAGE] = sync_page(page, packet)
        self.assertIn('UNACCEPTED_EXACT_CLAIM', self.codes(self.audit(packet, previs, requests)))

    def test_held_probability_prose_cannot_be_overridden_by_acceptance(self):
        for forged_eligibility in (False, True):
            packet, previs, requests = fixture()
            packet['forecast'].update(editorial_probability_eligible=forged_eligibility, editorial_gate='HOLD')
            page = previs['pages'][0]
            page['draft_copy']['body'] = 'Team Alpha has a 90% playoff chance.'
            requests[PAGE] = sync_page(page, packet)
            result = self.audit(packet, previs, requests, accepted_claims=[claim_receipt(packet, page, 'PROBABILISTIC')],
                                claim_verifier=lambda *a, **k: True)
            self.assertIn('HELD_FORECAST_IN_VISIBLE_COPY', self.codes(result))

    def test_percent_words_and_structured_probability_keys_stay_held(self):
        for update in [
            {'body': 'Team Alpha has a 90 percent chance to reach the postseason.'},
            {'playoff_odds': {'Team Alpha': '90%'}},
            {'playoff_odds': {'Team Alpha': 0.9}},
        ]:
            with self.subTest(update=update):
                packet, previs, requests = fixture()
                page = previs['pages'][0]
                page['draft_copy'].update(update)
                requests[PAGE] = sync_page(page, packet)
                self.assertIn('HELD_FORECAST_IN_VISIBLE_COPY', self.codes(self.audit(packet, previs, requests)))

    def test_extra_printed_claims_outside_exact_copy_are_not_silently_accepted(self):
        for extra in ['Team Alpha has a 90% playoff chance.', 'Team Beta is eliminated.']:
            with self.subTest(extra=extra):
                packet, previs, requests = fixture()
                page = previs['pages'][0]
                prompt = page['candidate_render_prompt']+'\nREQUIRED PRINTED FOOTNOTE: '+extra
                page['candidate_render_prompt'] = page['illustrated_page_brief']['artist_prompt'] = prompt
                requests[PAGE]['prompt'] = prompt
                self.assertIn('OUTSIDE_COPY_CLAIM_REVIEW_REQUIRED', self.codes(self.audit(packet, previs, requests)))

    def test_standalone_prompt_prohibitions_are_not_treated_as_forecasts(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        prompt = page['candidate_render_prompt']+'\nNever print playoff odds or elimination claims.'
        page['candidate_render_prompt'] = page['illustrated_page_brief']['artist_prompt'] = prompt
        requests[PAGE]['prompt'] = prompt
        self.assertEqual(self.audit(packet, previs, requests)['issues'], [])

    def test_explicit_proof_verifier_must_recompute_a_bound_claim(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['body'] = 'Team Alpha has clinched the single qualification place.'
        requests[PAGE] = sync_page(page, packet)
        receipt = claim_receipt(packet, page)

        def strict_bound(receipt, *, packet, **_):
            team_id = receipt['evidence']['team_id']
            own_minimum = packet['teams'][team_id]['wins']
            other_maximum = max(t['wins']+len(t['remaining_schedule']) for key, t in packet['teams'].items() if key != team_id)
            return receipt['evidence']['berths'] == 1 and own_minimum > other_maximum

        result = self.audit(packet, previs, requests, accepted_claims=[receipt], claim_verifier=strict_bound)
        self.assertNotIn('UNACCEPTED_EXACT_CLAIM', self.codes(result))
        packet['teams']['2']['remaining_schedule'] = [{'week': 4}]
        result = self.audit(packet, previs, requests, accepted_claims=[receipt], claim_verifier=strict_bound)
        self.assertIn('UNACCEPTED_EXACT_CLAIM', self.codes(result))

    def test_historical_or_prohibitory_prompt_context_is_advisory(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        prompt = (page['candidate_render_prompt']
                  + '\nHistorical reference: eliminated in the previous semifinal.'
                  + '\nForbidden mutations: invented playoff probabilities.')
        page['candidate_render_prompt'] = page['illustrated_page_brief']['artist_prompt'] = prompt
        requests[PAGE]['prompt'] = prompt
        result = self.audit(packet, previs, requests)
        self.assertEqual(result['issues'], [])
        self.assertEqual(len(result['review_notes']), 2)
        self.assertFalse(result['publication_authorized'])

    def test_no_material_candidate_is_explicit_and_preserves_optional_analytics(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['analytics_consumption'].update(decision='NO_MATERIAL_CANDIDATE', metric_bindings=[])
        requests[PAGE] = sync_page(page, packet)
        self.assertEqual(self.audit(packet, previs, requests)['issues'], [])

    def test_selected_scope_does_not_weaken_default_full_copy_review(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['body'] = 'Team Alpha has clinched the single qualification place.'
        requests[PAGE] = sync_page(page, packet)
        self.assertIn('UNACCEPTED_EXACT_CLAIM', self.codes(self.audit(packet, previs, requests)))
        selected = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
        self.assertEqual(selected['issues'], [])
        self.assertEqual(selected['claim_screening_scope'], 'SELECTED_ANALYTICS_COPY_POINTERS')

    def test_selected_identity_text_cannot_smuggle_forecast_or_exact_claims(self):
        for text, code in [('Team Alpha has clinched.', 'UNACCEPTED_EXACT_CLAIM'),
                           ('90 percent playoff chance', 'HELD_FORECAST_IN_VISIBLE_COPY')]:
            with self.subTest(text=text):
                packet, previs, requests = fixture()
                packet['page_bindings'][PAGE]['purpose'] = 'scoring_form'
                packet['teams']['1']['name'] = text
                page = previs['pages'][0]
                page['draft_copy']['selected_value'] = text
                page['analytics_consumption']['metric_bindings'] = [{
                    'source_pointer': '/teams/1/name', 'copy_pointer': '/selected_value'}]
                requests[PAGE] = sync_page(page, packet)
                result = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
                self.assertIn(code, self.codes(result))

    def test_known_structured_forecasts_are_held_in_full_review(self):
        for field in ('seed_probability', 'division_title_probability'):
            with self.subTest(field=field):
                packet, previs, requests = fixture()
                page = previs['pages'][0]
                page['draft_copy'][field] = {'1': .9}
                requests[PAGE] = sync_page(page, packet)
                self.assertIn('HELD_FORECAST_IN_VISIBLE_COPY', self.codes(self.audit(packet, previs, requests)))

    def test_selected_source_types_and_nested_record_shape_are_enforced(self):
        for field, value in [('scoring_average', True),
                             ('all_play', {'wins': 1, 'losses': 0, 'ties': 0, 'playoff_probability': .9})]:
            with self.subTest(field=field):
                packet, previs, requests = fixture()
                packet['teams']['1'][field] = value
                page = previs['pages'][0]
                page['draft_copy']['selected_value'] = value
                page['analytics_consumption']['metric_bindings'] = [{
                    'source_pointer': '/teams/1/' + field, 'copy_pointer': '/selected_value'}]
                requests[PAGE] = sync_page(page, packet)
                result = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
                self.assertIn('INVALID_METRIC_BINDING', self.codes(result))

    def test_json_boolean_cannot_stand_in_for_a_numeric_seed(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        page['draft_copy']['rows'][0]['seed'] = True
        page['analytics_consumption']['metric_bindings'] = [{
            'source_pointer': '/teams/1/provider_seed', 'copy_pointer': '/rows/0/seed'}]
        requests[PAGE] = sync_page(page, packet)
        codes = self.codes(self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS'))
        self.assertIn('STANDINGS_VALUE_DIFFERS_FROM_SOURCE', codes)
        self.assertIn('COPY_VALUE_DIFFERS_FROM_SOURCE', codes)

    def test_selected_scope_leaves_native_prompt_claim_review_explicit(self):
        packet, previs, requests = fixture()
        page = previs['pages'][0]
        prompt = page['candidate_render_prompt'] + '\nPRINT FOOTNOTE: Team Alpha has clinched.'
        page['candidate_render_prompt'] = page['illustrated_page_brief']['artist_prompt'] = prompt
        requests[PAGE]['prompt'] = prompt
        self.assertIn('OUTSIDE_COPY_CLAIM_REVIEW_REQUIRED', self.codes(self.audit(packet, previs, requests)))
        selected = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
        self.assertEqual(selected['issues'], [])
        self.assertEqual(len(selected['review_notes']), 1)
        self.assertIn('unselected prompt instructions are not evaluated', selected['scope'])

    def test_archived_revision_prose_is_not_current_selected_source_authority(self):
        packet, previs, requests = fixture()
        previs['creative_revision'] = {'sports_status': 'Archived pre-MNF pass: outcomes UNDECIDED.'}
        self.assertIn('PROVISIONAL_SPORTS_STATE', self.codes(self.audit(packet, previs, requests)))
        selected = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
        self.assertEqual(selected['issues'], [])
        self.assertEqual(selected['review_notes'][0]['code'], 'LEGACY_SPORTS_REVISION_CONTEXT')
        requests[PAGE]['sports_policy']['official_winner_decided'] = False
        self.assertIn('RENDER_SPORTS_STILL_PROVISIONAL', self.codes(
            self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')))

    def test_noncanonical_copy_pointers_cannot_evade_selected_claim_screening(self):
        for pointer, draft in [('/selected~2value', {'selected~2value': 'Team Alpha has clinched.'}),
                               ('/selected/00', {'selected': ['Team Alpha has clinched.']})]:
            with self.subTest(pointer=pointer):
                packet, previs, requests = fixture()
                packet['page_bindings'][PAGE]['purpose'] = 'scoring_form'
                packet['teams']['1']['name'] = 'Team Alpha has clinched.'
                page = previs['pages'][0]
                page['draft_copy'].update(draft)
                page['analytics_consumption']['metric_bindings'] = [{
                    'source_pointer': '/teams/1/name', 'copy_pointer': pointer}]
                requests[PAGE] = sync_page(page, packet)
                result = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
                self.assertIn('INVALID_METRIC_BINDING', self.codes(result))

    def test_valid_escaped_copy_keys_still_receive_selected_claim_screening(self):
        packet, previs, requests = fixture()
        packet['page_bindings'][PAGE]['purpose'] = 'scoring_form'
        packet['teams']['1']['name'] = 'Team Alpha has clinched.'
        page = previs['pages'][0]
        page['draft_copy']['selected/value~'] = packet['teams']['1']['name']
        page['analytics_consumption']['metric_bindings'] = [{
            'source_pointer': '/teams/1/name', 'copy_pointer': '/selected~1value~0'}]
        requests[PAGE] = sync_page(page, packet)
        result = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
        self.assertNotIn('INVALID_METRIC_BINDING', self.codes(result))
        self.assertIn('UNACCEPTED_EXACT_CLAIM', self.codes(result))

    def test_source_receipt_identity_types_must_match_the_accepted_packet(self):
        for key in ('season', 'through_week'):
            with self.subTest(key=key):
                packet, previs, requests = fixture()
                previs['sports_source'][key] = float(previs['sports_source'][key])
                result = self.audit(packet, previs, requests, audit_scope='SELECTED_ANALYTICS')
                self.assertIn('PREVIS_SOURCE_MISMATCH', self.codes(result))

    def test_known_purpose_label_cannot_disable_existing_standings_row_checks(self):
        for scope in ('FULL_ISSUE', 'SELECTED_ANALYTICS'):
            with self.subTest(scope=scope):
                packet, previs, requests = fixture()
                packet['page_bindings'][PAGE]['purpose'] = 'scoring_form'
                page = previs['pages'][0]
                page['draft_copy']['rows'][1]['points_for'] = '999.99'
                requests[PAGE] = sync_page(page, packet)
                result = self.audit(packet, previs, requests, audit_scope=scope)
                self.assertIn('STANDINGS_VALUE_DIFFERS_FROM_SOURCE', self.codes(result))

    def test_scoring_form_row_shape_does_not_imply_official_standings(self):
        for scope in ('FULL_ISSUE', 'SELECTED_ANALYTICS'):
            with self.subTest(scope=scope):
                packet, previs, requests = fixture()
                packet['page_bindings'][PAGE]['purpose'] = 'scoring_form'
                page = previs['pages'][0]
                page['draft_copy']['rows'] = [{'rank': 1, 'team': 'Team Alpha', 'index': 99.0}]
                page['analytics_consumption'].update(decision='NO_MATERIAL_CANDIDATE', metric_bindings=[])
                requests[PAGE] = sync_page(page, packet)
                self.assertEqual(self.audit(packet, previs, requests, audit_scope=scope)['issues'], [])


if __name__ == '__main__':
    unittest.main()
