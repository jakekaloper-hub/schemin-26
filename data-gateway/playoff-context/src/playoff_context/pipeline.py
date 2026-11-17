"""Weekly provider capture -> validated analytics -> optional Memo OS candidates.

This is a read-only, reproducible adapter. Provider finality is not a signed
Schemin Fact Lock, and computed candidates never authorize publication.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from statistics import mean, median

from .engine import Game, LeagueRules, Strength, simulate, exact_bounds_status, conditional_leverage, win_probability
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


def _diagnostic_metrics(summary, rows):
    """Recompute the reported score, baseline and sample size from checked rows."""
    if not isinstance(summary, dict):
        raise ValueError('diagnostic metric summary must be an object')
    included = [row for row in rows if row['observed_home_win'] is not None]
    if not included:
        raise ValueError('diagnostic requires binary evaluated matchups')
    brier = mean(row['brier'] for row in included)
    loss = mean(row['log_loss'] for row in included)
    expected = {
        'matchup_count': len(rows), 'binary_pair_count': len(included),
        'tied_matchups_excluded': len(rows) - len(included),
        'brier_score': brier, 'constant_half_probability_brier': 0.25,
        'brier_difference_vs_half_baseline': brier - 0.25,
        'log_loss_nats': loss, 'constant_half_probability_log_loss_nats': math.log(2),
        'log_loss_difference_vs_half_baseline_nats': loss - math.log(2),
        'log_loss_clipped_predictions': sum(row['log_loss_probability_clipped'] for row in included),
    }
    for name, value in expected.items():
        actual = summary.get(name)
        if type(value) is int:
            if type(actual) is not int or actual != value:
                raise ValueError(f'diagnostic sample count mismatch: {name}')
        elif not math.isclose(finite(actual, name), value, rel_tol=1e-10, abs_tol=1e-12):
            raise ValueError(f'diagnostic metric mismatch: {name}')
    if summary.get('lower_is_better') is not True:
        raise ValueError('diagnostic scoring direction mismatch')


def _check_diagnostic(report, diagnostic):
    """Validate receipt consistency, without treating hashes as an attestation."""
    if not isinstance(diagnostic, dict) or not isinstance(diagnostic.get('provenance'), dict):
        raise ValueError('model diagnostic provenance mismatch: receipt or provenance missing')
    provenance = diagnostic['provenance']
    for name in ('input_sha256', 'rules_sha256', 'model_code_sha256'):
        if provenance.get(name) != report['provenance'][name]:
            raise ValueError(f'model diagnostic provenance mismatch: {name}')
    if (type(diagnostic.get('schema_version')) is not int or diagnostic['schema_version'] != 1
            or diagnostic.get('model_version') != report['model_version']
            or diagnostic.get('model_version') != MODEL_VERSION
            or diagnostic.get('status') != 'DIAGNOSTIC_ONLY_NOT_CALIBRATION_CERTIFICATION'
            or diagnostic.get('validation_scope') != 'RETROSPECTIVE_WALK_FORWARD_MATCHUP_WIN_PROBABILITIES'
            or diagnostic.get('publication_authorized') is not False
            or diagnostic.get('forecast_editorial_gate') != 'HOLD_EXPLORATORY'):
        raise ValueError('unsupported diagnostic schema, model, status or validation scope')
    if (diagnostic.get('league_id') != report['league_id']
            or type(diagnostic.get('season')) is not int or diagnostic['season'] != report['season']
            or type(diagnostic.get('capture_through_week')) is not int
            or diagnostic['capture_through_week'] != report['through_week']):
        raise ValueError('model diagnostic scope mismatch')
    method = diagnostic.get('method', {})
    if (method.get('projections_used') is not False or method.get('model_parameters_refit') is not False):
        raise ValueError('diagnostic method differs from the fixed historical-score model')

    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(Path(__file__).parent.glob('*.py'))}
    if provenance['model_code_sha256'] != digest(sources):
        raise ValueError('model diagnostic does not describe the current model code')
    evaluator = Path(__file__).resolve().parents[2] / 'validate_model.py'
    evaluator_hash = digest({**sources, evaluator.name: hashlib.sha256(evaluator.read_bytes()).hexdigest()})
    if provenance.get('model_and_diagnostic_code_sha256') != evaluator_hash:
        raise ValueError('model diagnostic evaluator code hash mismatch')
    if type(provenance.get('ranking_seed')) is not int or provenance['ranking_seed'] != report['provenance']['seed']:
        raise ValueError('diagnostic ranking seed mismatch')

    checked, source = diagnostic.get('input_validation', {}), report['input_validation']
    if (checked.get('records_pf_pa_reconciled') is not True
            or type(checked.get('completed_matchups')) is not int
            or checked['completed_matchups'] != source['completed_matchups']
            or type(checked.get('freshness_slo_seconds')) is not int
            or checked['freshness_slo_seconds'] != source['freshness_slo_seconds']):
        raise ValueError('diagnostic source validation mismatch')
    source_time = timestamp(checked.get('source_as_of'))
    evaluated = timestamp(checked.get('evaluated_at'))
    report_evaluated = timestamp(source.get('evaluated_at'))
    if (source_time != timestamp(source.get('source_as_of')) or not source_time <= evaluated <= report_evaluated
            or (evaluated-source_time).total_seconds() > checked['freshness_slo_seconds']):
        raise ValueError('diagnostic source or evaluation chronology mismatch')
    mode = diagnostic.get('evaluation_mode', 'CURRENT_CAPTURE')
    if mode not in ('CURRENT_CAPTURE', 'HISTORICAL_REPLAY') or mode != report.get('evaluation_mode', 'CURRENT_CAPTURE'):
        raise ValueError('diagnostic evaluation mode mismatch')

    ids = set(report['teams'])
    if len(ids) < 2 or len(ids) % 2:
        raise ValueError('diagnostic requires an even complete team set')
    window = diagnostic.get('evaluation_weeks', {})
    first, last = window.get('first'), window.get('last')
    if type(first) is not int or type(last) is not int or not 2 <= first <= last <= report['through_week']:
        raise ValueError('diagnostic evaluation window is outside completed history')
    predictions = diagnostic.get('predictions')
    if not isinstance(predictions, list) or len(predictions) != (last-first+1) * (len(ids)//2):
        raise ValueError('diagnostic prediction count does not cover the evaluation window')
    by_week = {week: [] for week in range(first, last+1)}
    participants = {week: set() for week in by_week}
    for row in predictions:
        if not isinstance(row, dict) or type(row.get('week')) is not int or row['week'] not in by_week:
            raise ValueError('diagnostic prediction week is invalid')
        week = row['week']
        home, away = row.get('home_id'), row.get('away_id')
        if (home not in ids or away not in ids or home == away
                or home in participants[week] or away in participants[week]):
            raise ValueError('diagnostic matchup coverage is incomplete or duplicated')
        participants[week].update((home, away))
        training = row.get('training_scores_per_team', {})
        if (type(row.get('training_first_week')) is not int or row['training_first_week'] != 1
                or type(row.get('training_last_week')) is not int or row['training_last_week'] != week-1
                or set(training) != ids or any(type(v) is not int or v != week-1 for v in training.values())
                or row.get('provider_projections_used') is not False):
            raise ValueError('diagnostic prediction includes an invalid training cutoff')
        probability = finite(row.get('home_win_probability'), 'diagnostic probability')
        if not 0 <= probability <= 1:
            raise ValueError('diagnostic probability must be between zero and one')
        strengths = [Strength(finite(row.get(side+'_strength_mean'), 'diagnostic mean'),
                              finite(row.get(side+'_strength_sigma'), 'diagnostic deviation'))
                     for side in ('home', 'away')]
        if not math.isclose(probability, win_probability(*strengths), rel_tol=1e-10, abs_tol=1e-12):
            raise ValueError('diagnostic probability disagrees with recorded scoring strengths')
        hs, aws = finite(row.get('actual_home_score'), 'diagnostic home score'), finite(row.get('actual_away_score'), 'diagnostic away score')
        winner = row.get('provider_winner')
        outcome = row.get('observed_home_win')
        if (winner not in ('HOME', 'AWAY', 'TIE')
                or (winner == 'HOME' and hs < aws) or (winner == 'AWAY' and aws < hs)
                or (winner == 'TIE' and hs != aws)):
            raise ValueError('diagnostic observed result contradicts recorded scores')
        if winner == 'TIE':
            if (outcome is not None or row.get('brier') is not None or row.get('log_loss') is not None
                    or row.get('binary_metric_exclusion') != 'ACTUAL_TIE'
                    or row.get('log_loss_probability_clipped') is not False):
                raise ValueError('diagnostic tied result must be excluded from binary metrics')
        else:
            expected_outcome = int(winner == 'HOME')
            if type(outcome) is not int or outcome != expected_outcome or row.get('binary_metric_exclusion') is not None:
                raise ValueError('diagnostic binary result mismatch')
            clipped = min(1-1e-15, max(1e-15, probability))
            expected_brier = (probability-outcome)**2
            expected_loss = -outcome*math.log(clipped)-(1-outcome)*math.log1p(-clipped)
            if (not math.isclose(finite(row.get('brier'), 'diagnostic Brier score'), expected_brier, rel_tol=1e-10, abs_tol=1e-12)
                    or not math.isclose(finite(row.get('log_loss'), 'diagnostic log loss'), expected_loss, rel_tol=1e-10, abs_tol=1e-12)
                    or row.get('log_loss_probability_clipped') is not (clipped != probability)):
                raise ValueError('diagnostic per-matchup scoring mismatch')
        by_week[week].append(row)
    if any(seen != ids for seen in participants.values()):
        raise ValueError('diagnostic weekly team coverage mismatch')
    weekly = diagnostic.get('by_week', {})
    if set(weekly) != {str(week) for week in by_week}:
        raise ValueError('diagnostic weekly summaries do not cover the evaluation window')
    _diagnostic_metrics(diagnostic.get('aggregate'), predictions)
    for week, rows in by_week.items():
        _diagnostic_metrics(weekly[str(week)], rows)

    seeds = diagnostic.get('current_seed_reconciliation', {})
    if (type(seeds.get('through_week')) is not int or seeds['through_week'] != report['through_week']
            or type(seeds.get('completed_matchups')) is not int or seeds['completed_matchups'] != source['completed_matchups']
            or source['completed_matchups'] != report['through_week'] * (len(ids)//2)):
        raise ValueError('diagnostic seed reconciliation scope mismatch')
    observed_seeds = [team.get('provider_seed') for team in report['teams'].values()]
    if any(type(value) is not int for value in observed_seeds) or set(observed_seeds) != set(range(1, len(ids)+1)):
        raise ValueError('report provider seed ordering is incomplete')
    provider = sorted(ids, key=lambda tid: report['teams'][tid]['provider_seed'])
    modeled = seeds.get('model_team_ids_in_seed_order')
    if (not isinstance(modeled, list) or len(modeled) != len(ids) or set(modeled) != ids
            or seeds.get('provider_team_ids_in_seed_order') != provider):
        raise ValueError('diagnostic seed ordering does not cover the report teams/provider order')
    mismatches = [{'seed': index, 'model_team_id': actual, 'provider_team_id': expected}
                  for index, (actual, expected) in enumerate(zip(modeled, provider), 1) if actual != expected]
    if seeds.get('exact_order_match') is not (modeled == provider) or seeds.get('mismatches') != mismatches:
        raise ValueError('diagnostic seed mismatch claim disagrees with its recorded orderings')


def _replay_diagnostic_source(report, diagnostic, capture, config):
    """Reproduce the small diagnostic from the supplied frozen source, offline."""
    if capture is None and config is None:
        return {'status': 'NOT_PERFORMED'}
    if capture is None or config is None:
        raise ValueError('diagnostic source replay requires both capture and config')
    for value, name in ((capture, 'input_sha256'), (config, 'rules_sha256')):
        if digest(value) != report['provenance'][name]:
            raise ValueError(f'diagnostic source replay provenance mismatch: {name}')
    evaluator_path = Path(__file__).resolve().parents[2] / 'validate_model.py'
    spec = importlib.util.spec_from_file_location('_playoff_diagnostic_source_replay', evaluator_path)
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    expected = evaluator.build_diagnostic(
        capture, config,
        start_week=diagnostic['evaluation_weeks']['first'],
        end_week=diagnostic['evaluation_weeks']['last'],
        now=timestamp(diagnostic['input_validation']['evaluated_at']),
        max_age_seconds=report['input_validation']['freshness_slo_seconds'],
        seed=report['provenance']['seed'],
    )
    predictions_hash = digest(expected['predictions'])
    if digest(diagnostic['predictions']) != predictions_hash:
        raise ValueError('diagnostic predictions disagree with frozen-source replay')
    if digest(diagnostic['current_seed_reconciliation']) != digest(expected['current_seed_reconciliation']):
        raise ValueError('diagnostic seed reconciliation disagrees with frozen-source replay')
    return {'status': 'PASS', 'predictions_sha256': predictions_hash,
            'scope': 'Offline replay of the bound frozen source; not external calibration or publication approval.'}


def attach_validation(report, diagnostic, *, capture=None, config=None):
    """Attach a checked diagnostic, with optional offline frozen-source replay.

    Self-consistency and matching asserted hashes do not prove that predictions
    were generated from the captured history. A baseline comparison becomes
    evidence only after source replay; an attachment without the source remains
    HOLD_DIAGNOSTIC_SOURCE_NOT_REPLAYED. Neither path authorizes forecasts.
    """
    try:
        _check_diagnostic(report, diagnostic)
        replay = _replay_diagnostic_source(report, diagnostic, capture, config)
    except (KeyError, TypeError, AttributeError, OverflowError) as exc:
        raise ValueError(f'malformed model diagnostic: {exc}') from exc
    aggregate = diagnostic['aggregate']
    seeds_match = diagnostic['current_seed_reconciliation']['exact_order_match']
    forecast = report['forecast']
    forecast['model_diagnostic'] = {'sha256': digest(diagnostic),
        'acceptance': ('SOURCE_REPLAYED_NOT_CALIBRATION_CERTIFIED' if replay['status'] == 'PASS'
                       else 'INTERNAL_CONSISTENCY_ONLY_SOURCE_NOT_REPLAYED'),
        'source_replay': replay,
        'scope': diagnostic['validation_scope'], 'evaluation_weeks': copy.deepcopy(diagnostic['evaluation_weeks']),
        'aggregate': copy.deepcopy(aggregate), 'current_seed_order_matches_provider': seeds_match}
    forecast['editorial_probability_eligible'] = False
    if replay['status'] != 'PASS':
        forecast['editorial_gate'] = 'HOLD_DIAGNOSTIC_SOURCE_NOT_REPLAYED'
    elif not seeds_match:
        forecast['editorial_gate'] = 'HOLD_SEED_RECONCILIATION_MISMATCH'
    elif (aggregate['brier_score'] >= 0.25 or aggregate['log_loss_nats'] >= math.log(2)):
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
    parser.add_argument('--render-inputs', type=Path,
                        help='Existing render-inputs directory; checks actual request.json consumers without changing them')
    parser.add_argument('--validation', type=Path, help='Hash-bound walk-forward diagnostic; cannot self-authorize forecast publication')
    parser.add_argument('--simulations', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=2610)
    parser.add_argument('--include-leverage', action='store_true')
    parser.add_argument('--leverage-simulations', type=int, default=2000)
    parser.add_argument('--as-of', help='Explicit historical replay time; never relabels old data as live')
    args = parser.parse_args()
    if args.render_inputs and (not args.previs or not args.memo_output):
        parser.error('--render-inputs requires --previs and --memo-output')
    capture = json.loads(args.capture.read_text())
    config = json.loads(args.rules.read_text())
    report = build_report(capture, config,
        now=timestamp(args.as_of) if args.as_of else None, simulations=args.simulations, seed=args.seed,
        include_leverage=args.include_leverage, leverage_simulations=args.leverage_simulations)
    report['evaluation_mode'] = 'HISTORICAL_REPLAY' if args.as_of else 'CURRENT_CAPTURE'
    if args.validation:
        attach_validation(report, json.loads(args.validation.read_text()), capture=capture, config=config)
    report['provenance']['capture_path'] = str(args.capture)
    report['provenance']['rules_path'] = str(args.rules)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    if args.memo_output:
        adapter = Path(__file__).resolve().parents[4]/'memo-os'/'playoff_context_adapter.py'
        spec = importlib.util.spec_from_file_location('memo_playoff_context', adapter)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        previs = json.loads(args.previs.read_text()) if args.previs else None
        render_requests = None
        if args.render_inputs:
            if not args.render_inputs.is_dir():
                parser.error('--render-inputs must be an existing directory')
            render_requests = {}
            for path in sorted(args.render_inputs.glob('*/request.json')):
                request = json.loads(path.read_text())
                page_id = request.get('page_id')
                if page_id != path.parent.name or page_id in render_requests:
                    parser.error('render request page identity is missing, duplicated or mismatched')
                render_requests[page_id] = request
        packet = module.build_memo_packet(report, previs=previs,
            render_requests=render_requests, now=timestamp(args.as_of) if args.as_of else None)
        args.memo_output.parent.mkdir(parents=True, exist_ok=True)
        args.memo_output.write_text(json.dumps(packet, indent=2, ensure_ascii=False, allow_nan=False)+'\n')
    print(json.dumps({'report': str(args.output), 'forecast': report['forecast']['status'],
                      'validated_games': report['input_validation']['completed_matchups'],
                      'memo_packet': str(args.memo_output) if args.memo_output else None,
                      'production_readiness': packet['production_readiness']['status'] if args.memo_output else 'NOT_EVALUATED'}))


if __name__ == '__main__':
    main()
