import copy
import json
from pathlib import Path
import unittest
from compare_transaction_snapshots import compare

SOURCE = Path(__file__).with_name('WEEK_7_PROVIDER_NORMALIZED_EVIDENCE_2026-10-23.json')


class TransactionComparisonTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads(SOURCE.read_text())

    def run_compare(self, before, after):
        return compare(json.dumps(before).encode(), json.dumps(after).encode())

    def test_actual_capture_self_comparison_is_not_approval(self):
        r = self.run_compare(self.snapshot, self.snapshot)
        self.assertEqual(r['unchanged_count'], 33)
        self.assertEqual(r['changed_rows'], [])
        self.assertFalse(r['fact_lock'])
        self.assertFalse(r['provider_authenticity_verified'])

    def test_same_count_can_have_addition_removal_and_status_change(self):
        after = copy.deepcopy(self.snapshot)
        rows = after['week7_transactions']['transactions']
        removed = rows[0]['transaction_id']
        rows[0]['transaction_id'] = 'synthetic-new-id'
        rows[1]['status'] = 'synthetic-changed-status'
        r = self.run_compare(self.snapshot, after)
        self.assertEqual(r['added_rows'][0]['transaction_id'], 'synthetic-new-id')
        self.assertEqual(r['removed_rows'][0]['transaction_id'], removed)
        self.assertEqual(len(r['changed_rows']), 1)

    def test_reordering_does_not_create_transactions(self):
        after = copy.deepcopy(self.snapshot)
        after['week7_transactions']['transactions'].reverse()
        self.assertEqual(self.run_compare(self.snapshot, after)['unchanged_count'], 33)

    def test_summary_cannot_stand_in_for_rows(self):
        self.assertEqual(self.run_compare(self.snapshot['baseline'], self.snapshot)['status'], 'DIAGNOSTIC_HOLD')

    def test_incomplete_and_malformed_batches_hold(self):
        mutations = [lambda b: b.update(count=29), lambda b: b.update(truncated=True),
                     lambda b: b.update(dropped_invalid_timestamp_count=1),
                     lambda b: b['window'].update(returned_rows=True),
                     lambda b: b['transactions'].append(b['transactions'][0]),
                     lambda b: b['transactions'][0].update(transaction_id=[]),
                     lambda b: b['transactions'][0].update(timestamp=True)]
        for mutate in mutations:
            after = copy.deepcopy(self.snapshot)
            mutate(after['week7_transactions'])
            self.assertEqual(self.run_compare(self.snapshot, after)['status'], 'DIAGNOSTIC_HOLD')

    def test_scope_mismatch_holds(self):
        after = copy.deepcopy(self.snapshot)
        after['week7_transactions']['league_id'] = 'other-league'
        self.assertEqual(self.run_compare(self.snapshot, after)['status'], 'DIAGNOSTIC_HOLD')

    def test_provider_limits_and_unstable_generated_ids_hold(self):
        mutations = [lambda b: b.update(source='activity_feed'),
                     lambda b: b.update(limitations={'omitted_unrecognized_rows': 1}),
                     lambda b: b.update(limitations={'possibly_truncated': True}),
                     lambda b: b.update(limitations={'possibly_truncated': None}),
                     lambda b: b['transactions'][0].update(transaction_id='mtx-generated')]
        for mutate in mutations:
            after = copy.deepcopy(self.snapshot)
            mutate(after['week7_transactions'])
            self.assertEqual(self.run_compare(self.snapshot, after)['status'], 'DIAGNOSTIC_HOLD')

    def test_invalid_json_is_structured_hold(self):
        for raw in (b'null', b'[]', b'{', b'{"value": NaN}'):
            self.assertEqual(compare(raw, SOURCE.read_bytes())['status'], 'DIAGNOSTIC_HOLD')

    def test_nested_numeric_boolean_changes_are_not_hidden(self):
        before = copy.deepcopy(self.snapshot)
        after = copy.deepcopy(self.snapshot)
        before['week7_transactions']['transactions'][0]['nested'] = {'v': [1]}
        after['week7_transactions']['transactions'][0]['nested'] = {'v': [True]}
        self.assertEqual(len(self.run_compare(before, after)['changed_rows']), 1)
        before['week7_transactions']['window']['requested_week'] = 1
        after['week7_transactions']['window']['requested_week'] = True
        self.assertEqual(self.run_compare(before, after)['status'], 'DIAGNOSTIC_HOLD')

    def test_duplicate_keys_and_overflow_are_rejected(self):
        raw = SOURCE.read_bytes()
        duplicate = b'{"week7_transactions":null,' + raw.lstrip()[1:]
        overflow = raw.replace(b'"faab_bid": 0', b'"faab_bid": 1e309', 1)
        self.assertNotEqual(raw, overflow)
        for bad in (duplicate, overflow):
            self.assertEqual(compare(bad, raw)['status'], 'DIAGNOSTIC_HOLD')


if __name__ == '__main__':
    unittest.main()
