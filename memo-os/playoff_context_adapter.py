"""Consume derived league analytics without overwriting Memo copy or release state."""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
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
MAX_MEMO_SOURCE_AGE_SECONDS = 86400
DESCRIPTIVE_CANDIDATE_KINDS = {
    'ALL_PLAY', 'WEEKLY_MEDIAN', 'SCHEDULE_LUCK', 'SCORING_FORM',
    'REMAINING_SCHEDULE',
}
DESCRIPTIVE_DEFINITION_KEYS = {
    'all_play', 'weekly_median_record', 'schedule_neutral_wins',
    'schedule_luck_wins', 'remaining_opponent_scoring_average',
}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string')
    return value


def _number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be a finite number')
    return value


def _count(value, label, *, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{label} must be an integer >= {minimum}')
    return value


def _strings(value, label):
    if not isinstance(value, list):
        raise ValueError(f'{label} must be a list of strings')
    return [_text(item, label) for item in value]


def _record(value, label):
    if not isinstance(value, dict):
        raise ValueError(f'{label} must be a W/L/T record')
    return {key: _count(value.get(key), f'{label}.{key}') for key in ('wins', 'losses', 'ties')}


def _descriptive_team(team_id, value):
    """Rebuild known schemas; no unknown nested member crosses the boundary."""
    if not isinstance(value, dict) or value.get('team_id') != team_id:
        raise ValueError('team identity must agree with its report key')
    row = {'team_id': _text(team_id, 'team_id'), 'name': _text(value.get('name'), 'name'),
           'class': 'DESCRIPTIVE'}
    for key in ('wins', 'losses', 'ties'):
        row[key] = _count(value.get(key), key)
    seed = value.get('provider_seed')
    row['provider_seed'] = None if seed is None else _count(seed, 'provider_seed', minimum=1)
    for key in ('points_for', 'points_against', 'scoring_average', 'last_three_average',
                'all_play_win_rate', 'schedule_neutral_wins', 'schedule_luck_wins'):
        row[key] = _number(value.get(key), key)
    if not 0 <= row['all_play_win_rate'] <= 1 or row['schedule_neutral_wins'] < 0:
        raise ValueError('invalid descriptive win rate or schedule-neutral wins')
    for key in ('all_play', 'weekly_median_record'):
        row[key] = _record(value.get(key), key)
    average = value.get('remaining_opponent_scoring_average')
    row['remaining_opponent_scoring_average'] = (
        None if average is None else _number(average, 'remaining_opponent_scoring_average'))
    schedule = value.get('remaining_schedule')
    if not isinstance(schedule, list):
        raise ValueError('remaining_schedule must be a list')
    row['remaining_schedule'] = []
    for game in schedule:
        if not isinstance(game, dict) or type(game.get('home')) is not bool:
            raise ValueError('remaining_schedule requires typed descriptive games')
        row['remaining_schedule'].append({
            'week': _count(game.get('week'), 'remaining_schedule.week', minimum=1),
            'opponent_id': _text(game.get('opponent_id'), 'remaining_schedule.opponent_id'),
            'opponent': _text(game.get('opponent'), 'remaining_schedule.opponent'),
            'home': game['home'],
            'opponent_scoring_average': _number(game.get('opponent_scoring_average'),
                                               'remaining_schedule.opponent_scoring_average'),
        })
    # The Analyst report retains proofs. This consumer has no independent
    # proof-acceptance contract, so an EXACT label/prose cannot release a claim.
    row['exact_status'] = {
        'status': 'UNKNOWN', 'class': 'UNRESOLVED', 'proof': None,
        'note': 'Exact qualification claims require an independently accepted proof; this consumer has no proof-acceptance gate.',
    }
    return row


def _descriptive_candidates(values, teams):
    if not isinstance(values, list):
        raise ValueError('editorial_candidates must be a list')
    candidates = []
    for value in values:
        if (not isinstance(value, dict) or value.get('class') != 'DESCRIPTIVE'
                or not isinstance(value.get('kind'), str)
                or not isinstance(value.get('team_id'), str)
                or value.get('kind') not in DESCRIPTIVE_CANDIDATE_KINDS
                or value.get('team_id') not in teams):
            continue
        priority = value.get('priority', 0)
        if type(priority) is not int or not 0 <= priority <= 100:
            continue
        # Candidate kinds refer to the typed team metrics above. Arbitrary
        # prose, numeric predictions and extension objects are not a contract.
        candidates.append({'team_id': value['team_id'], 'class': 'DESCRIPTIVE',
                           'kind': value['kind'], 'priority': priority})
    return candidates


def _descriptive_forecast(value):
    if not isinstance(value, dict):
        raise ValueError('forecast must be an object')
    gate = value.get('editorial_gate')
    if not isinstance(gate, str) or not gate.startswith('HOLD_'):
        gate = 'HOLD_NO_FORECAST_APPROVAL_MECHANISM'
    result = {
        'status': 'HOLD' if value.get('status') == 'HOLD' else 'WITHHELD_FROM_MEMO',
        'editorial_probability_eligible': False,
        'editorial_gate': gate,
        'blockers': _strings(value.get('blockers'), 'forecast.blockers'),
        'assumptions': _strings(value.get('assumptions'), 'forecast.assumptions'),
        'calibration_status': 'NOT_EXTERNALLY_CALIBRATED',
        'publication_note': 'Model probabilities and exact qualification claims remain in the Analyst report; this Memo consumer has no approval mechanism for them.',
    }
    for key in ('rule_policy', 'tiebreaker'):
        item = value.get(key)
        result[key] = None if item is None else _text(item, f'forecast.{key}')
    if type(value.get('projections_used')) is not bool:
        raise ValueError('forecast.projections_used must be boolean')
    result['projections_used'] = value['projections_used']
    diagnostic = value.get('model_diagnostic')
    if diagnostic is not None:
        if (not isinstance(diagnostic, dict) or not isinstance(diagnostic.get('sha256'), str)
                or not re.fullmatch(r'[0-9a-f]{64}', diagnostic['sha256'])):
            raise ValueError('model diagnostic reference must contain a SHA-256 digest')
        # Keep a review reference, not arbitrary diagnostic payload/claims.
        result['model_diagnostic'] = {'sha256': diagnostic['sha256']}
    return result


def _aware_time(value, label):
    parsed = datetime.fromisoformat(_text(value, label).replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError(f'{label} must have timezone')
    return parsed


def build_memo_packet(report, *, previs=None, bindings=None, render_requests=None, now=None,
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
    source_time = _aware_time(checked.get('source_as_of'), 'source timestamp')
    evaluated = _aware_time(checked.get('evaluated_at'), 'evaluation timestamp')
    if evaluated > now or evaluated < source_time:
        raise ValueError('future evaluation timestamp or evaluation predates source')
    declared_slo = _count(checked.get('freshness_slo_seconds'), 'freshness SLO', minimum=1)
    age = (now-source_time).total_seconds()
    if age < 0 or age > min(declared_slo, MAX_MEMO_SOURCE_AGE_SECONDS):
        raise ValueError('STALE_INPUT or future source timestamp')
    evaluation_mode = report.get('evaluation_mode', 'CURRENT_CAPTURE')
    if evaluation_mode not in ('CURRENT_CAPTURE', 'HISTORICAL_REPLAY'):
        raise ValueError('unsupported evaluation mode')
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
    forecast = _descriptive_forecast(report['forecast'])
    if not isinstance(report.get('teams'), dict):
        raise ValueError('teams must be an object')
    teams = {tid: _descriptive_team(tid, row) for tid, row in report['teams'].items()}
    definitions = report.get('metric_definitions')
    if not isinstance(definitions, dict):
        raise ValueError('metric_definitions must be an object')
    definitions = {key: _text(value, f'metric_definitions.{key}')
                   for key, value in definitions.items() if key in DESCRIPTIVE_DEFINITION_KEYS}
    packet = {
        'schema_version': 1, 'run_id': run_id, 'assignment_id': run_id+'-memo',
        'from': 'The Analyst / Data Gateway derived analytics', 'to': 'Memo OS / Beat Writer',
        'artifact': 'weekly-playoff-context-candidates', 'artifact_version': report['model_version'],
        'status': 'EDITORIAL_CANDIDATE', 'ack_state': 'NOT_REQUESTED',
        'source_authority': report['source_authority'],
        'source_snapshot': report['provenance']['input_sha256'],
        'report_sha256': source_sha, 'source_as_of': checked['source_as_of'],
        'evaluation_mode': evaluation_mode,
        'league_id': str(report['league_id']),
        'season': report['season'], 'through_week': week, 'scope': report['scope'],
        'publication_authorized': False, 'canonical_fact_lock_certified': False,
        'verified_facts': ['Complete provider-final results through the specified week.',
            'Every team record and PF/PA reconciled against completed matchup history.'],
        'interpretations': _descriptive_candidates(report['editorial_candidates'], teams),
        'assumptions': copy.deepcopy(forecast['assumptions']),
        'unavailable': copy.deepcopy(forecast['blockers']),
        'unresolved': _strings(report['required_publication_gates'], 'required_publication_gates'),
        'confidence': 'Descriptive arithmetic verified; model probabilities and exact qualification claims withheld.',
        'qa_already_performed': ['Provider shape, cutoff, freshness, schedule coverage, record/PF/PA reconciliation.'],
        'prohibited_inferences': PROHIBITED,
        'dependencies': report['provenance'],
        'next_required_action': 'Select material findings; reconcile canonical Fact Lock; independently review numbers and copy.',
        'next_gate': 'Memo OS editorial and independent publication QA',
        'forecast': forecast,
        'metric_definitions': definitions,
        'teams': teams, 'page_bindings': {},
        'copy_change_required': True,
    }
    # No forecast/proof approval mechanism is implemented in this consumer.
    # The declared eligibility boolean cannot override descriptive-only output.
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
    # A candidate attachment is not evidence that operative copy or render
    # requests consumed the accepted source. Inspect the actual inputs and
    # keep their unresolved source/selection/mirror work visible to the caller.
    spec = importlib.util.spec_from_file_location('memo_playoff_readiness',
        Path(__file__).with_name('playoff_context_readiness.py'))
    readiness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(readiness)
    packet['production_readiness'] = readiness.audit_memo_readiness(
        packet, previs=packet.get('hydrated_previs'), render_requests=render_requests, now=now)
    packet['copy_change_required'] = packet['production_readiness']['copy_change_required']
    if previs is not None:
        packet['hydrated_previs']['derived_analytics']['production_readiness'] = packet['production_readiness']['status']
        packet['hydrated_previs']['derived_analytics']['consumption_witnessed'] = packet['production_readiness']['consumption_witnessed']
    return packet
