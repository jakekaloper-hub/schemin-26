#!/usr/bin/env python3
"""Compare complete normalized transaction rows; never certify provider facts."""
import argparse
import hashlib
import json
from pathlib import Path


def decode(raw):
    def invalid(value):
        raise ValueError('non-finite JSON value')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    value = json.loads(raw, parse_constant=invalid, object_pairs_hook=unique)
    canonical(value)  # Also rejects exponent overflow such as 1e309.
    if not isinstance(value, dict):
        raise ValueError('snapshot must be an object')
    batch = value.get('week7_transactions')
    if not isinstance(batch, dict) or not isinstance(batch.get('transactions'), list):
        raise ValueError('full transaction rows required; summary counts are insufficient')
    rows = batch['transactions']
    window = batch.get('window')
    if not isinstance(window, dict):
        raise ValueError('transaction window required')
    if (type(batch.get('count')) is not int or batch['count'] != len(rows)
            or type(window.get('returned_rows')) is not int or window['returned_rows'] != len(rows)
            or batch.get('truncated') is not False
            or type(batch.get('dropped_invalid_timestamp_count')) is not int
            or batch['dropped_invalid_timestamp_count'] != 0):
        raise ValueError('incomplete or inconsistent transaction batch')
    identity = {}
    for field in ('platform', 'sport', 'league_id', 'season_year', 'source'):
        v = batch.get(field)
        if not isinstance(v, (str, int)) or isinstance(v, bool) or v == '':
            raise ValueError('missing transaction scope: ' + field)
        identity[field] = v
    identity['window'] = {k: v for k, v in window.items() if k != 'returned_rows'}
    if not window.get('mode') or not window.get('unit') or not window.get('weeks'):
        raise ValueError('missing transaction period scope')
    indexed = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('transaction row must be an object')
        key = row.get('transaction_id')
        if not isinstance(key, str) or not key.strip() or key in indexed:
            raise ValueError('missing or duplicate transaction_id')
        if (type(row.get('timestamp')) is not int or row['timestamp'] <= 0
                or not isinstance(row.get('status'), str) or not row['status']):
            raise ValueError('transaction timestamp/status required')
        indexed[key] = row
    return identity, indexed


def canonical(value):
    # JSON spelling retains boolean/numeric distinctions hidden by Python ==.
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def compare(before_raw, after_raw):
    result = {'status': 'DIAGNOSTIC_HOLD', 'fact_lock': False,
              'provider_authenticity_verified': False, 'freshness_accepted': False,
              'before_sha256': hashlib.sha256(before_raw).hexdigest(),
              'after_sha256': hashlib.sha256(after_raw).hexdigest()}
    try:
        before_scope, before = decode(before_raw)
        after_scope, after = decode(after_raw)
        if canonical(before_scope) != canonical(after_scope):
            raise ValueError('transaction scopes/windows differ')
    except (ValueError, UnicodeError) as exc:
        result['errors'] = [str(exc)]
        return result
    added = sorted(after.keys() - before.keys())
    removed = sorted(before.keys() - after.keys())
    changed = sorted(k for k in before.keys() & after.keys()
                     if canonical(before[k]) != canonical(after[k]))
    result.update(status='ROW_COMPARISON_COMPLETE_NOT_APPROVED', errors=[],
                  before_count=len(before), after_count=len(after),
                  added_rows=[after[k] for k in added], removed_rows=[before[k] for k in removed],
                  changed_rows=[{'transaction_id': k, 'before': before[k], 'after': after[k]} for k in changed],
                  unchanged_count=len(before.keys() & after.keys()) - len(changed))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before')
    parser.add_argument('after')
    parser.add_argument('output')
    args = parser.parse_args()
    output = Path(args.output)
    if output.resolve() in (Path(args.before).resolve(), Path(args.after).resolve()):
        parser.error('output must not overwrite input snapshots')
    try:
        result = compare(Path(args.before).read_bytes(), Path(args.after).read_bytes())
    except OSError as exc:
        result = {'status': 'DIAGNOSTIC_HOLD', 'errors': [str(exc)], 'fact_lock': False}
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    return 0 if result['status'] == 'ROW_COMPARISON_COMPLETE_NOT_APPROVED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
