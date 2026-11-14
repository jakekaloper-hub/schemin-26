import copy
import unittest
from validate_transaction_lineage import inspect_window

PENDING = {
    'type': 'waiver', 'status': 'pending', 'team_ids': ['1'],
    'espn_event_id': {'kind': 'string', 'value': 'pending-1'},
    'claim_outcome': {'status': 'complete', 'outcome_event_id': {'kind': 'string', 'value': 'terminal-1'}},
}
TERMINAL = {
    'type': 'waiver', 'status': 'complete', 'team_ids': ['1'],
    'espn_event_id': {'kind': 'string', 'value': 'terminal-1'},
    'espn_related_event_id': {'kind': 'string', 'value': 'pending-1'},
}

class TypedWaiverLineage(unittest.TestCase):
    def setUp(self):
        self.w = {'source': 'mTransactions2', 'transactions': [copy.deepcopy(PENDING), copy.deepcopy(TERMINAL)],
                  'count': 2, 'truncated': False, 'limitations': {}, 'dropped_invalid_timestamp_count': 0}

    def test_resolved_pending_is_historical_not_live(self):
        errors, summary = inspect_window(self.w)
        self.assertEqual(errors, [])
        self.assertEqual(summary, {'historical_pending_resolved_complete': 1})

    def test_unknown_outcome_never_becomes_active_waiver(self):
        self.w['transactions'][0]['claim_outcome'] = {'status': 'unknown'}
        self.w['transactions'].pop(); self.w['count'] = 1
        errors, summary = inspect_window(self.w)
        self.assertEqual(errors, [])
        self.assertEqual(summary, {'historical_pending_unresolved': 1})

    def test_malformed_claim_object_fails_closed(self):
        self.w['transactions'][0]['claim_outcome'] = 'complete'
        self.assertTrue(any('INVALID_CLAIM_OUTCOME' in e for e in inspect_window(self.w)[0]))

    def test_missing_terminal_fails_closed(self):
        self.w['transactions'].pop(); self.w['count'] = 1
        self.assertTrue(any('TARGET_NOT_PRESENT' in e for e in inspect_window(self.w)[0]))

    def test_tampered_outcome_status_fails_closed(self):
        self.w['transactions'][0]['claim_outcome']['status'] = 'failed'
        self.assertTrue(any('STATUS_CONFLICT' in e for e in inspect_window(self.w)[0]))

    def test_reversed_event_reference_fails_closed(self):
        self.w['transactions'][1]['espn_related_event_id'] = {'kind': 'string', 'value': 'someone-else'}
        self.assertTrue(any('REVERSE_LINK_MISSING' in e for e in inspect_window(self.w)[0]))

    def test_team_mismatch_fails_closed(self):
        self.w['transactions'][1]['team_ids'] = ['2']
        self.assertTrue(any('TEAM_MISMATCH' in e for e in inspect_window(self.w)[0]))

    def test_event_ids_are_typed_and_unique(self):
        self.w['transactions'][1]['espn_event_id'] = {'kind': 'string', 'value': 'pending-1'}
        self.assertTrue(any('DUPLICATE' in e for e in inspect_window(self.w)[0]))

    def test_count_mismatch_fails_closed(self):
        self.w['count'] = 3
        self.assertIn('TRANSACTION_COUNT_MISMATCH', inspect_window(self.w)[0])

    def test_activity_feed_not_authoritative(self):
        self.w['source'] = 'activity_feed'
        self.assertIn('STRUCTURED_SOURCE_NOT_VERIFIED', inspect_window(self.w)[0])

    def test_truncation_fails_closed(self):
        self.w['truncated'] = True
        self.assertIn('TRANSACTION_WINDOW_TRUNCATED', inspect_window(self.w)[0])

    def test_omitted_rows_fail_closed(self):
        self.w['limitations']['omitted_unrecognized_rows'] = 1
        self.assertIn('TRANSACTION_ROWS_OMITTED:omitted_unrecognized_rows', inspect_window(self.w)[0])

    def test_number_string_ids_do_not_conflate(self):
        self.w['transactions'][1]['espn_event_id'] = {'kind': 'number', 'value': 'pending-1'}
        self.assertFalse(any('DUPLICATE' in e for e in inspect_window(self.w)[0]))

if __name__ == '__main__':
    unittest.main()
