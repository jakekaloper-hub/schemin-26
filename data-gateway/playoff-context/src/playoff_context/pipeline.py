"""Weekly provider capture -> validated analytics -> optional Memo OS candidates.

This is a read-only, reproducible adapter. Provider finality is not a signed
Schemin Fact Lock, and computed candidates never authorize publication.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from statistics import mean, median

from .engine import Game, LeagueRules, simulate, exact_bounds_status, conditional_leverage
from .normalize import normalize_teams, normalize_future_games, require_final_week
from .editorial import classify_candidates

MODEL_VERSION = 'playoff-context-v1.1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('timezone-aware captured_at required')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timezone-aware captured_at required')
    return parsed.astimezone(timezone.utc)


def finite(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be a finite number')
    return float(value)


def observation(capture, row, now, max_age_seconds):
    if not isinstance(row, dict) or row.get('success') is not True:
        raise ValueError('successful provider observation required')
    captured = timestamp(row.get('captured_at'))
    age = (now - captured).total_seconds()
    if age < 0:
        raise ValueError('observation timestamp is in the future')
    if age > max_age_seconds:
        raise ValueError('STALE_INPUT: capture exceeds freshness SLO; recapture or explicit historical replay')
    data = row.get('data')
    if not isinstance(data, dict):
        raise ValueError('provider data must be an object')
    if str(data.get('leagueId', data.get('id'))) != str(capture['league_id']):
        raise ValueError('provider league mismatch')
    if data.get('seasonYear', data.get('seasonId')) != capture['season']:
        raise ValueError('provider season mismatch')
    return data


def normalize_snapshot(capture, config, *, now=None, max_age_seconds=86400):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now must have a timezone')
    if type(max_age_seconds) is not int or max_age_seconds <= 0:
        raise ValueError('positive freshness SLO required')
    if capture.get('schema_version') != 1 or capture.get('provider') != 'flaim' or capture.get('platform') != 'espn':
        raise ValueError('unsupported provider capture contract')
    for key in ('league_id', 'season'):
        if str(capture.get(key)) != str(config.get(key)):
            raise ValueError(f'config/capture {key} mismatch')
    week, horizon, count, qualifiers = (capture.get('through_week'), config.get('regular_season_weeks'),
                                      config.get('team_count'), config.get('playoff_teams'))
    if any(type(v) is not int for v in (week, horizon, count, qualifiers)):
        raise ValueError('integer cutoff, horizon, team count and qualifiers required')
    if not 1 <= week <= horizon or count < 2 or count % 2 or not 1 <= qualifiers < count:
        raise ValueError('invalid league dimensions')
    info = observation(capture, capture.get('league_info'), now, max_age_seconds)
    standing_data = observation(capture, capture.get('standings'), now, max_age_seconds)
    standings = standing_data.get('standings', [])
    if info.get('size') != count or len(standings) != count:
        raise ValueError('league team count mismatch')
    schedule_settings = info.get('schedule', {})
    for field, expected in (('playoffTeamCount', qualifiers), ('regularSeasonMatchupPeriodCount', horizon)):
        if field in schedule_settings and schedule_settings[field] != expected:
            raise ValueError(f'provider/config structural rule mismatch: {field}')
    ids = {str(t['teamId']) for t in info.get('teams', [])}
    if len(ids) != count or len(info.get('teams', [])) != count:
        raise ValueError('league team identities incomplete or duplicated')
    official_ids = [str(t.get('teamId')) for t in standings]
    if len(set(official_ids)) != count or set(official_ids) != ids:
        raise ValueError('standings team identities incomplete or duplicated')
    names = {str(t['teamId']): t['teamName'].strip() for t in info['teams']}
    raw_weeks = capture.get('weeks')
    if not isinstance(raw_weeks, list) or len(raw_weeks) != horizon:
        raise ValueError('complete season schedule required, including all completed weeks')
    by_week = {}
    for row in raw_weeks:
        n = row.get('requested_week')
        if type(n) is not int or not 1 <= n <= horizon or n in by_week:
            raise ValueError('duplicate/invalid week in provider observations')
        data = observation(capture, row, now, max_age_seconds)
        if data.get('matchupPeriod') != n:
            raise ValueError('requested/provider week mismatch')
        by_week[n] = data
    if set(by_week) != set(range(1, horizon+1)):
        raise ValueError('missing season week')
    scores = {tid: [] for tid in ids}
    recomputed = {tid: {'wins': 0, 'losses': 0, 'ties': 0, 'pf': 0., 'pa': 0.} for tid in ids}
    outcomes, score_weeks = [], []
    tie_rule = info.get('scoringSettings', {}).get('matchupTieRule')
    for n in range(1, week+1):
        data = by_week[n]
        try:
            require_final_week(data, expected_team_ids=ids, expected_week=n, matchup_tie_rule=tie_rule)
        except RuntimeError as exc:
            raise ValueError(str(exc)) from exc
        weekly_scores = {}
        for row in data['matchups']:
            h, a = str(row['home']['teamId']), str(row['away']['teamId'])
            hp, ap = finite(row['home']['totalPoints'], 'home score'), finite(row['away']['totalPoints'], 'away score')
            for tid, pf, pa in ((h, hp, ap), (a, ap, hp)):
                weekly_scores[tid] = pf
                scores[tid].append(pf)
                recomputed[tid]['pf'] += pf
                recomputed[tid]['pa'] += pa
            winner = h if row['winner'] == 'HOME' else a if row['winner'] == 'AWAY' else None
            outcomes.append((h, a, winner))
            if winner is None:
                recomputed[h]['ties'] += 1; recomputed[a]['ties'] += 1
            else:
                recomputed[winner]['wins'] += 1
                recomputed[a if winner == h else h]['losses'] += 1
        score_weeks.append(weekly_scores)
    for row in standings:
        tid = str(row['teamId'])
        if row.get('teamName', '').strip() != names[tid]:
            raise ValueError('standings/league team name mismatch')
        for field in ('wins', 'losses', 'ties'):
            if type(row.get(field)) is not int or row[field] != recomputed[tid][field]:
                raise ValueError(f'standings/history record mismatch: {tid}/{field}')
        for source_key, derived_key in (('pointsFor', 'pf'), ('pointsAgainst', 'pa')):
            if abs(finite(row.get(source_key), source_key) - recomputed[tid][derived_key]) > 0.011:
                raise ValueError(f'standings/history score mismatch: {tid}/{source_key}')
    future_rows = []
    for n in range(week+1, horizon+1):
        for row in by_week[n].get('matchups', []):
            if row.get('winner') != 'UNDECIDED':
                raise ValueError('future results beyond cutoff are not a pregame snapshot')
            for side in ('home', 'away'):
                data = row.get(side, {})
                for field in ('currentPoints', 'totalPoints'):
                    if field in data and finite(data[field], field) != 0:
                        raise ValueError('live future score cannot enter a pregame cutoff model')
                for score in data.get('pointsByScoringPeriod', {}).values():
                    if finite(score, 'future scoring-period points') != 0:
                        raise ValueError('live future score cannot enter a pregame cutoff model')
        future_rows.append({'week': n, **by_week[n]})
    future = normalize_future_games(future_rows, week+1, horizon, expected_team_ids=ids)
    # This version is deliberately historical-score-only. Provider projections
    # retrieved later are neither verified pregame snapshots nor backtest inputs.
    future = [Game(g.week, g.home_id, g.away_id) for g in future]
    teams = normalize_teams(standings, scores)
    rules = LeagueRules(playoff_teams=qualifiers, regular_season_weeks=horizon,
        tiebreaker=config.get('tiebreaker', 'UNKNOWN'), divisions=config.get('divisions'),
        qualification_policy=config.get('qualification_policy', 'UNKNOWN'))
    observed = [capture['league_info']['captured_at'], capture['standings']['captured_at']]
    observed += [r['captured_at'] for r in raw_weeks]
    return {'teams': teams, 'rules': rules, 'future_games': future, 'outcomes': outcomes,
        'score_weeks': score_weeks, 'standings': standings, 'names': names,
        'source_as_of': min(observed, key=timestamp), 'evaluated_at': now.isoformat(),
        'provider_tiebreaker': info.get('schedule', {}).get('playoffSeedingRule'),
        'provider_playoff_edited': info.get('status', {}).get('isPlayoffMatchupEdited')}


def descriptive_metrics(snapshot):
    teams, future, score_weeks = snapshot['teams'], snapshot['future_games'], snapshot['score_weeks']
    official = {str(r['teamId']): r for r in snapshot['standings']}
    out = {}
    for tid, t in sorted(teams.items(), key=lambda item: int(item[0])):
        wins = losses = ties = mw = ml = mt = 0
        for scores in score_weeks:
            for oid, score in scores.items():
                if oid == tid: continue
                wins += scores[tid] > score; losses += scores[tid] < score; ties += scores[tid] == score
            m = median(scores.values())
            mw += scores[tid] > m; ml += scores[tid] < m; mt += scores[tid] == m
        expected = (wins + 0.5*ties)/(len(teams)-1)
        remaining = []
        for game in future:
            if tid in (game.home_id, game.away_id):
                oid = game.away_id if tid == game.home_id else game.home_id
                remaining.append({'week': game.week, 'opponent_id': oid, 'opponent': teams[oid].name,
                                  'home': tid == game.home_id, 'opponent_scoring_average': mean(teams[oid].scores)})
        out[tid] = {'team_id': tid, 'name': t.name, 'class': 'DESCRIPTIVE',
            'wins': t.wins, 'losses': t.losses, 'ties': t.ties,
            'provider_seed': official[tid].get('playoffSeed'),
            'points_for': t.points_for, 'points_against': official[tid]['pointsAgainst'],
            'scoring_average': mean(t.scores), 'last_three_average': mean(t.scores[-3:]),
            'all_play': {'wins': wins, 'losses': losses, 'ties': ties},
            'all_play_win_rate': (wins+0.5*ties)/(wins+losses+ties),
            'weekly_median_record': {'wins': mw, 'losses': ml, 'ties': mt},
            'schedule_neutral_wins': expected, 'schedule_luck_wins': t.wins+0.5*t.ties-expected,
            'remaining_schedule': remaining,
            'remaining_opponent_scoring_average': mean([g['opponent_scoring_average'] for g in remaining]) if remaining else None,
            'playoff_probability': None, 'seed_probability': None,
            'exact_status': {'status': 'UNKNOWN', 'class': 'UNRESOLVED'}}
    return out


def build_report(capture, config, *, now=None, max_age_seconds=86400, simulations=10000,
                 seed=2610, leverage_simulations=2000, include_leverage=False):
    if type(simulations) is not int or simulations <= 0 or type(seed) is not int:
        raise ValueError('positive integer simulations and integer seed required')
    snapshot = normalize_snapshot(capture, config, now=now, max_age_seconds=max_age_seconds)
    teams = descriptive_metrics(snapshot)
    policy = config.get('qualification_policy')
    blocked = []
    if policy not in ('OVERALL', 'DIVISION_WINNERS_PLUS_WILDCARDS'):
        blocked.append('qualification policy not established')
    if not config.get('rule_evidence'):
        blocked.append('rule provenance missing')
    if config.get('tiebreaker') != snapshot['provider_tiebreaker']:
        blocked.append('configured tiebreaker differs from provider')
    if config.get('manual_override_review') != 'NO_EDIT_REPORTED':
        blocked.append('current manual-playoff-edit status not reconciled')
    if snapshot['provider_playoff_edited'] is not False:
        blocked.append('provider playoff edit reported or status unavailable')
    probability, leverage, exact = {}, {}, {}
    if not blocked:
        try:
            probability = simulate(snapshot['teams'], snapshot['future_games'], snapshot['rules'],
                simulations=simulations, seed=seed, completed_outcomes=snapshot['outcomes'])
            exact = exact_bounds_status(snapshot['teams'], snapshot['future_games'], snapshot['rules'])
            if include_leverage and snapshot['future_games']:
                next_week = min(g.week for g in snapshot['future_games'])
                for g in snapshot['future_games']:
                    if g.week == next_week:
                        leverage.update(conditional_leverage(snapshot['teams'], snapshot['future_games'], snapshot['rules'], g,
                            simulations=leverage_simulations, seed=seed, completed_outcomes=snapshot['outcomes']))
        except ValueError as exc:
            blocked.append(str(exc))
            probability, leverage, exact = {}, {}, {}
    for tid in teams:
        if probability:
            p = probability[tid]['playoff_probability']
            teams[tid].update(probability[tid])
            teams[tid]['class'] = 'DERIVED_METRICS'
            teams[tid]['metric_classes'] = {'observed_score_comparisons': 'DESCRIPTIVE',
                'future_qualification_seeds_wins': 'PROBABILISTIC', 'clinch_elimination': 'exact_status.class'}
            teams[tid]['monte_carlo_standard_error_pp'] = 100*math.sqrt(p*(1-p)/simulations)
            z = 1.959963984540054
            denominator = 1 + z*z/simulations
            center = (p+z*z/(2*simulations))/denominator
            radius = z*math.sqrt(p*(1-p)/simulations + z*z/(4*simulations*simulations))/denominator
            teams[tid]['monte_carlo_95_interval'] = [max(0., center-radius), min(1., center+radius)]
            teams[tid]['qualifying_trials'] = round(p*simulations)
        teams[tid]['exact_status'] = exact.get(tid, {'status': 'UNKNOWN', 'class': 'UNRESOLVED'})
        if tid in leverage: teams[tid]['next_game_leverage'] = leverage[tid]
    code_hash = digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(Path(__file__).parent.glob('*.py'))})
    candidates = classify_candidates(probability, exact, leverage)
    return {'schema_version': 1, 'model_version': MODEL_VERSION, 'league_id': str(capture['league_id']),
        'season': capture['season'], 'through_week': capture['through_week'],
        'scope': f"Completed regular-season results through Week {capture['through_week']}",
        'status': 'EDITORIAL_CANDIDATE', 'publication_authorized': False,
        'source_authority': 'FLAIM_ESPN_PROVIDER_OBSERVATION', 'canonical_fact_lock_certified': False,
        'input_validation': {'status': 'PASS', 'provider_result_lock': 'FINAL',
            'completed_matchups': len(snapshot['outcomes']), 'remaining_matchups': len(snapshot['future_games']),
            'records_pf_pa_reconciled': True, 'freshness_slo_seconds': max_age_seconds,
            'source_as_of': snapshot['source_as_of'], 'evaluated_at': snapshot['evaluated_at']},
        'provenance': {'input_sha256': digest(capture), 'rules_sha256': digest(config),
            'model_code_sha256': code_hash, 'seed': seed, 'simulations': simulations if probability else 0,
            'leverage_simulations': leverage_simulations if leverage else 0, 'rule_evidence': config.get('rule_evidence', [])},
        'forecast': {'status': 'CONDITIONAL_MODEL_ESTIMATE' if probability else 'HOLD', 'blockers': blocked,
            'rule_policy': policy, 'tiebreaker': config.get('tiebreaker'),
            'projections_used': False,
            'editorial_probability_eligible': False,
            'editorial_gate': 'HOLD_PENDING_MODEL_VALIDATION_AND_INDEPENDENT_ACCEPTANCE',
            'publication_note': 'Forecast fields are for Analyst review only; the Memo adapter withholds them.',
            'assumptions': ['Recorded division policy and ESPN documented default tie waterfall; no unreported LM override.',
                'Independent team score draws; historical scoring strength; no injury, lineup, roster or NFL bye adjustment.',
                'Regular-season qualification and seed estimates only; no championship probabilities.',
                'Monte Carlo sampling error excludes model/rule uncertainty. This model is not externally calibrated.'],
            'calibration_status': 'NOT_EXTERNALLY_CALIBRATED'},
        'metric_definitions': {'all_play': 'Each completed weekly score compared with the other teams that week; score ties count half.',
            'schedule_neutral_wins': 'Sum of weekly all-play win shares divided by opponents per week.',
            'schedule_luck_wins': 'Actual win equivalents minus schedule-neutral wins; descriptive schedule effect, not skill or causation.',
            'remaining_opponent_scoring_average': 'Mean observed season points per game of future scheduled opponents; backward-looking difficulty proxy.',
            'weekly_median_record': 'Weekly score versus that same week league median; not an additional league matchup.'},
        'teams': teams, 'editorial_candidates': candidates,
        'consumer_authority': {'analytics': 'The Analyst', 'data': 'The Scout / Data Gateway',
            'memo': 'Memo OS / Beat Writer', 'qa': 'Independent Umpire', 'integration': 'GM / Closer'},
        'external_reference': {'name': 'TheFFHub', 'url': 'https://theffhub.com/',
            'role': 'OPTIONAL_REFERENCE_OR_MANUAL_CROSSCHECK', 'vendor_run_performed': False,
            'data_sent_to_vendor': False},
        'required_publication_gates': ['Data Release Steward / canonical Fact Lock',
            'Memo editorial selection', 'Independent production QA']}


def attach_validation(report, diagnostic):
    """Attach only a diagnostic bound to this exact input, rules and model."""
    for name in ('input_sha256', 'rules_sha256', 'model_code_sha256'):
        if diagnostic.get('provenance', {}).get(name) != report['provenance'][name]:
            raise ValueError(f'model diagnostic provenance mismatch: {name}')
    if (diagnostic.get('league_id') != report['league_id']
            or diagnostic.get('season') != report['season']
            or diagnostic.get('capture_through_week') != report['through_week']):
        raise ValueError('model diagnostic scope mismatch')
    aggregate = diagnostic['aggregate']
    forecast = report['forecast']
    forecast['model_diagnostic'] = {'sha256': digest(diagnostic),
        'scope': diagnostic['validation_scope'], 'evaluation_weeks': diagnostic['evaluation_weeks'],
        'aggregate': aggregate,
        'current_seed_order_matches_provider': diagnostic['current_seed_reconciliation']['exact_order_match']}
    forecast['editorial_probability_eligible'] = False
    if aggregate['brier_score'] >= aggregate['constant_half_probability_brier']:
        forecast['editorial_gate'] = 'HOLD_BASELINE_NOT_BEATEN'
    else:
        forecast['editorial_gate'] = 'HOLD_EXTERNAL_CALIBRATION_AND_INDEPENDENT_ACCEPTANCE'
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    parser.add_argument('--rules', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--memo-output', type=Path)
    parser.add_argument('--previs', type=Path)
    parser.add_argument('--validation', type=Path, help='Hash-bound walk-forward diagnostic; cannot self-authorize forecast publication')
    parser.add_argument('--simulations', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=2610)
    parser.add_argument('--include-leverage', action='store_true')
    parser.add_argument('--leverage-simulations', type=int, default=2000)
    parser.add_argument('--as-of', help='Explicit historical replay time; never relabels old data as live')
    args = parser.parse_args()
    report = build_report(json.loads(args.capture.read_text()), json.loads(args.rules.read_text()),
        now=timestamp(args.as_of) if args.as_of else None, simulations=args.simulations, seed=args.seed,
        include_leverage=args.include_leverage, leverage_simulations=args.leverage_simulations)
    report['evaluation_mode'] = 'HISTORICAL_REPLAY' if args.as_of else 'CURRENT_CAPTURE'
    if args.validation:
        attach_validation(report, json.loads(args.validation.read_text()))
    report['provenance']['capture_path'] = str(args.capture)
    report['provenance']['rules_path'] = str(args.rules)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    if args.memo_output:
        adapter = Path(__file__).resolve().parents[4]/'memo-os'/'playoff_context_adapter.py'
        spec = importlib.util.spec_from_file_location('memo_playoff_context', adapter)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        previs = json.loads(args.previs.read_text()) if args.previs else None
        packet = module.build_memo_packet(report, previs=previs,
            now=timestamp(args.as_of) if args.as_of else None)
        args.memo_output.parent.mkdir(parents=True, exist_ok=True)
        args.memo_output.write_text(json.dumps(packet, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    print(json.dumps({'report': str(args.output), 'forecast': report['forecast']['status'],
                      'validated_games': report['input_validation']['completed_matchups'],
                      'memo_packet': str(args.memo_output) if args.memo_output else None}))


if __name__ == '__main__':
    main()
