"""Consume derived league analytics without overwriting Memo copy or release state."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
import re

WEEK_10_BINDINGS = {
    'W10-P27': 'official_standings',
    'W10-P28': 'division_context',
    'W10-P29': 'scoring_form',
    'W10-P30': 'playoff_picture',
    'W10-P31': 'next_week_preview',
    'W10-P35': 'gotw_stakes',
}
PROHIBITED = [
    'No simulated 0%/100% clinch or elimination claim.',
    'No championship odds inferred from regular-season qualification.',
    'No model rank substituted for official provider seed or editorial power ranking.',
    'No schedule-luck metric used to assert real owner motives or skill.',
    'No old leaders-hold scenario promoted to final results without rerun.',
    'No automatic GOTW selection, character/canon mutation or publication approval.',
]
DESCRIPTIVE_FIELDS = {
    'team_id', 'name', 'wins', 'losses', 'ties', 'provider_seed',
    'points_for', 'points_against', 'scoring_average', 'last_three_average',
    'all_play', 'all_play_win_rate', 'weekly_median_record',
    'schedule_neutral_wins', 'schedule_luck_wins', 'remaining_schedule',
    'remaining_opponent_scoring_average', 'exact_status',
}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def build_memo_packet(report, *, previs=None, bindings=None, now=None,
                      expected_league_id='1417621', expected_season=2026):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('timezone-aware time required')
    if str(report.get('league_id')) != str(expected_league_id):
        raise ValueError('report/consumer league mismatch')
    if report.get('season') != expected_season:
        raise ValueError('report/consumer season mismatch')
    checked = report.get('input_validation', {})
    if checked.get('status') != 'PASS' or checked.get('provider_result_lock') != 'FINAL':
        raise ValueError('accepted complete final provider observation required')
    source_time = datetime.fromisoformat(checked['source_as_of'].replace('Z', '+00:00'))
    if source_time.tzinfo is None:
        raise ValueError('source timestamp must have timezone')
    age = (now-source_time).total_seconds()
    if age < 0 or age > checked['freshness_slo_seconds']:
        raise ValueError('STALE_INPUT or future source timestamp')
    for name in ('input_sha256', 'rules_sha256', 'model_code_sha256'):
        value = report.get('provenance', {}).get(name)
        if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('complete source/model provenance required')
    week = report['through_week']
    prefix = f'W{week:02d}-'
    bindings = bindings if bindings is not None else WEEK_10_BINDINGS if week == 10 else {}
    if any(not page_id.startswith(prefix) for page_id in bindings):
        raise ValueError('analytics and consumer page week mismatch')
    source_sha = _digest(report)
    run_id = f"playoff-context-{report['season']}-w{week:02d}-{source_sha[:12]}"
    packet = {
        'schema_version': 1, 'run_id': run_id, 'assignment_id': run_id+'-memo',
        'from': 'The Analyst / Data Gateway derived analytics', 'to': 'Memo OS / Beat Writer',
        'artifact': 'weekly-playoff-context-candidates', 'artifact_version': report['model_version'],
        'status': 'EDITORIAL_CANDIDATE', 'ack_state': 'NOT_REQUESTED',
        'source_authority': report['source_authority'],
        'source_snapshot': report['provenance']['input_sha256'],
        'report_sha256': source_sha, 'source_as_of': checked['source_as_of'],
        'evaluation_mode': report.get('evaluation_mode', 'CURRENT_CAPTURE'),
        'league_id': str(report['league_id']),
        'season': report['season'], 'through_week': week, 'scope': report['scope'],
        'publication_authorized': False, 'canonical_fact_lock_certified': False,
        'verified_facts': ['Complete provider-final results through the specified week.',
            'Every team record and PF/PA reconciled against completed matchup history.'],
        'interpretations': report['editorial_candidates'],
        'assumptions': report['forecast']['assumptions'],
        'unavailable': report['forecast']['blockers'],
        'unresolved': report['required_publication_gates'],
        'confidence': 'Arithmetic verified; forecasts conditional on recorded rules and model assumptions.',
        'qa_already_performed': ['Provider shape, cutoff, freshness, schedule coverage, record/PF/PA reconciliation.'],
        'prohibited_inferences': PROHIBITED,
        'dependencies': report['provenance'],
        'next_required_action': 'Select material findings; reconcile canonical Fact Lock; independently review numbers and copy.',
        'next_gate': 'Memo OS editorial and independent publication QA',
        'forecast': copy.deepcopy(report['forecast']),
        'metric_definitions': copy.deepcopy(report['metric_definitions']),
        'teams': copy.deepcopy(report['teams']), 'page_bindings': {},
        'copy_change_required': False,
    }
    # An exploratory model must not quietly become publishable through a page
    # attachment. Allowlist descriptive fields, including unknown future keys.
    if report['forecast'].get('editorial_probability_eligible') is not True:
        for tid, team in packet['teams'].items():
            packet['teams'][tid] = {k: v for k, v in team.items() if k in DESCRIPTIVE_FIELDS}
            packet['teams'][tid]['class'] = 'DESCRIPTIVE'
        packet['interpretations'] = [c for c in packet['interpretations'] if c.get('class') != 'PROBABILISTIC']
        if packet['forecast']['status'] != 'HOLD':
            packet['forecast']['status'] = 'WITHHELD_FROM_MEMO'
    for page_id, purpose in bindings.items():
        packet['page_bindings'][page_id] = {
            'purpose': purpose, 'run_id': run_id, 'report_sha256': source_sha,
            'candidate_only': True, 'forecast_status': packet['forecast']['status'],
            'official_standings_unchanged': True,
            'editorial_selection': 'PENDING',
        }
    if previs is not None:
        hydrated = copy.deepcopy(previs)
        issue_id = str(hydrated.get('issue_id', '')).upper()
        years = re.findall(r'(?<!\d)20\d{2}(?!\d)', issue_id)
        short_years = re.findall(r'SCHEMIN[-_ ](\d{2})(?!\d)', issue_id)
        issue_weeks = re.findall(r'W(\d{1,2})(?!\d)', issue_id)
        if (any(int(y) != expected_season for y in years)
                or any(int(y) != expected_season % 100 for y in short_years)
                or hydrated.get('season', expected_season) != expected_season
                or any(int(w) != week for w in issue_weeks)
                or hydrated.get('week', week) != week):
            raise ValueError('issue identity season/week mismatch')
        rows = hydrated.get('pages', [])
        if not isinstance(rows, list) or any(not isinstance(p, dict) or not isinstance(p.get('page_id'), str) for p in rows):
            raise ValueError('valid issue page identities required')
        pages = {p['page_id']: p for p in rows}
        if len(pages) != len(rows):
            raise ValueError('duplicate page IDs in issue previs')
        if any(not page_id.startswith(prefix) for page_id in pages):
            raise ValueError('issue page week mismatch')
        if set(bindings)-set(pages):
            raise ValueError('consumer page absent from the supplied issue previs')
        for page_id, binding in packet['page_bindings'].items():
            pages[page_id]['analytics_context'] = copy.deepcopy(binding)
        hydrated['derived_analytics'] = {'run_id': run_id, 'report_sha256': source_sha,
            'through_week': week, 'source_as_of': checked['source_as_of'],
            'status': 'EDITORIAL_CANDIDATE', 'publication_authorized': False}
        packet['hydrated_previs'] = hydrated
        packet['previs_source_sha256'] = _digest(previs)
    return packet
