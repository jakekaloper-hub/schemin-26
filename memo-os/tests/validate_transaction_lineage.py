"""V5.1 source-semantic preflight for bounded ESPN transaction evidence.

This module never determines roster ownership, source completeness outside the
returned window, authenticated Steward acceptance, or publication readiness.
Historical pending waiver rows are immutable history, not a live queue.
"""
from collections import Counter

TERMINAL = frozenset({'complete', 'failed', 'canceled'})


def typed_id(value):
    if not isinstance(value, dict):
        return None
    if value.get('kind') not in ('string', 'number'):
        return None
    raw = value.get('value')
    if not isinstance(raw, str) or not raw:
        return None
    return f"{value['kind']}:{raw}"


def inspect_window(window):
    """Return actionable errors and *historical* claim status counters.

    No caller may promote these results to canonical Fact Lock without the
    independent Data Release Steward's authenticated provenance acceptance.
    """
    errors = []
    summary = Counter()
    if not isinstance(window, dict):
        return ['transaction window must be an object'], {}
    source = window.get('source')
    if source not in ('mTransactions2', 'mTransactions2_with_activity_trade_details'):
        errors.append('STRUCTURED_SOURCE_NOT_VERIFIED')
    limitations = window.get('limitations') or {}
    if window.get('truncated') or limitations.get('possibly_truncated'):
        errors.append('TRANSACTION_WINDOW_TRUNCATED')
    for field in ('omitted_unrecognized_rows', 'omitted_unscoped_rows', 'omitted_conflicting_rows'):
        if limitations.get(field, 0):
            errors.append('TRANSACTION_ROWS_OMITTED:' + field)
    if window.get('dropped_invalid_timestamp_count', 0):
        errors.append('INVALID_TIMESTAMP_ROWS_OMITTED')
    rows = window.get('transactions')
    if not isinstance(rows, list):
        errors.append('TRANSACTIONS_NOT_AN_ARRAY')
        return errors, dict(summary)
    if window.get('count') != len(rows):
        errors.append('TRANSACTION_COUNT_MISMATCH')
    index = {}
    for row in rows:
        if not isinstance(row, dict):
            errors.append('MALFORMED_TRANSACTION_ROW')
            continue
        key = typed_id(row.get('espn_event_id'))
        if not key:
            errors.append('UNTYPED_PROVIDER_EVENT_ID')
            continue
        if key in index:
            errors.append('DUPLICATE_PROVIDER_EVENT_ID:' + key)
        index[key] = row
    for row in rows:
        if not isinstance(row, dict) or row.get('status') != 'pending':
            continue
        key = typed_id(row.get('espn_event_id'))
        if row.get('type') != 'waiver':
            summary['other_historical_pending'] += 1
            continue
        outcome = row.get('claim_outcome')
        if outcome is None:
            summary['historical_pending_unresolved'] += 1
            continue
        if not isinstance(outcome, dict):
            errors.append('INVALID_CLAIM_OUTCOME:' + str(key))
            continue
        if outcome.get('status') == 'unknown':
            summary['historical_pending_unresolved'] += 1
            continue
        if outcome.get('status') not in TERMINAL:
            errors.append('INVALID_CLAIM_OUTCOME:' + str(key))
            continue
        outcome_key = typed_id(outcome.get('outcome_event_id'))
        if not outcome_key:
            errors.append('CLAIM_OUTCOME_MISSING_TYPED_ID:' + str(key))
            continue
        terminal = index.get(outcome_key)
        if terminal is None:
            errors.append('CLAIM_OUTCOME_TARGET_NOT_PRESENT:' + str(key))
            continue
        if terminal.get('status') != outcome['status']:
            errors.append('CLAIM_OUTCOME_STATUS_CONFLICT:' + str(key))
            continue
        if typed_id(terminal.get('espn_related_event_id')) != key:
            errors.append('CLAIM_OUTCOME_REVERSE_LINK_MISSING:' + str(key))
            continue
        pending_teams = {str(t) for t in row.get('team_ids', [])}
        outcome_teams = {str(t) for t in terminal.get('team_ids', [])}
        if not pending_teams or not pending_teams.intersection(outcome_teams):
            errors.append('CLAIM_OUTCOME_TEAM_MISMATCH:' + str(key))
            continue
        summary['historical_pending_resolved_' + outcome['status']] += 1
    return errors, dict(summary)
