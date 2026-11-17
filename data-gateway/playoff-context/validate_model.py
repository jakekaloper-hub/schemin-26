#!/usr/bin/env python3
"""Reproduce bounded walk-forward diagnostics from a frozen provider capture.

This evaluates matchup win probabilities, not playoff-probability calibration.
Each scored week uses only earlier completed scores. Current-week projections,
future scores, final standings and future rosters never enter the prediction.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from random import Random
from statistics import mean
import sys
from time import perf_counter
from typing import Mapping

_PACKAGE_ROOT = Path(__file__).resolve().parent
if str(_PACKAGE_ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT / 'src'))

from playoff_context.engine import TeamState, estimate_strengths, simulate, win_probability
from playoff_context.normalize import require_final_week
from playoff_context.pipeline import MODEL_VERSION, digest, normalize_snapshot, timestamp
from playoff_context.seeding import ESPN_DEFAULT_RULE_CAVEAT, rank_espn


def walk_forward_predictions(weeks: Mapping[int, dict], team_names: Mapping[str, str], *,
                             start_week: int = 4, end_week: int = 10,
                             matchup_tie_rule: str | None = None) -> list[dict]:
    """Produce expanding-history predictions without reading weeks after cutoff.

    All teams' strengths for a week are frozen before adding any score from that
    week. A tied matchup has no binary winner and is recorded but excluded from
    binary Brier/log-loss aggregates. The actual capture has no such ties.
    """
    if type(start_week) is not int or type(end_week) is not int or not 2 <= start_week <= end_week:
        raise ValueError('integer diagnostic range with 2 <= start_week <= end_week required')
    if not team_names or any(not isinstance(tid, str) or not tid for tid in team_names):
        raise ValueError('nonempty string team ID mapping required')
    if not set(range(1, end_week + 1)).issubset(weeks):
        raise ValueError('all prior and evaluation weeks are required')
    records = {tid: [0, 0, 0] for tid in team_names}
    histories = {tid: [] for tid in team_names}
    points_for = {tid: 0.0 for tid in team_names}
    points_against = {tid: 0.0 for tid in team_names}
    predictions = []
    for week in range(1, end_week + 1):
        data = weeks[week]
        require_final_week(data, expected_team_ids=team_names, expected_week=week,
                           matchup_tie_rule=matchup_tie_rule)
        states = {tid: TeamState(
            tid, name, records[tid][0], records[tid][1], records[tid][2],
            points_for[tid], tuple(histories[tid]), points_against[tid],
        ) for tid, name in team_names.items()}
        # No provider projection is passed, including historical projected scores.
        strengths = estimate_strengths(states) if week >= start_week else None
        for row in sorted(data['matchups'], key=lambda value: (str(value['home']['teamId']),
                                                              str(value['away']['teamId']))):
            home, away = str(row['home']['teamId']), str(row['away']['teamId'])
            hs, as_ = float(row['home']['totalPoints']), float(row['away']['totalPoints'])
            winner = home if row['winner'] == 'HOME' else away if row['winner'] == 'AWAY' else None
            if strengths is not None:
                probability = win_probability(strengths[home], strengths[away])
                observed = 1 if winner == home else 0 if winner == away else None
                clipped = min(1 - 1e-15, max(1e-15, probability))
                brier = (probability - observed) ** 2 if observed is not None else None
                log_loss = (-observed * math.log(clipped) - (1 - observed) * math.log1p(-clipped)
                            if observed is not None else None)
                predictions.append({
                    'week': week, 'home_id': home, 'away_id': away,
                    'home': team_names[home], 'away': team_names[away],
                    'training_first_week': 1, 'training_last_week': week - 1,
                    'training_scores_per_team': {tid: len(states[tid].scores) for tid in sorted(states)},
                    'provider_projections_used': False,
                    'home_strength_mean': strengths[home].mu, 'home_strength_sigma': strengths[home].sigma,
                    'away_strength_mean': strengths[away].mu, 'away_strength_sigma': strengths[away].sigma,
                    'home_win_probability': probability, 'observed_home_win': observed,
                    'actual_home_score': hs, 'actual_away_score': as_,
                    'provider_winner': row['winner'], 'brier': brier, 'log_loss': log_loss,
                    'log_loss_probability_clipped': observed is not None and clipped != probability,
                    'binary_metric_exclusion': 'ACTUAL_TIE' if observed is None else None,
                })
            histories[home].append(hs)
            histories[away].append(as_)
            points_for[home] += hs
            points_for[away] += as_
            points_against[home] += as_
            points_against[away] += hs
            if winner is None:
                records[home][2] += 1
                records[away][2] += 1
            else:
                records[winner][0] += 1
                records[away if winner == home else home][1] += 1
    return predictions


def metric_summary(predictions: list[dict]) -> dict:
    included = [row for row in predictions if row['observed_home_win'] is not None]
    if not included:
        raise ValueError('diagnostic has no binary completed matchups')
    brier = mean(row['brier'] for row in included)
    loss = mean(row['log_loss'] for row in included)
    return {
        'matchup_count': len(predictions), 'binary_pair_count': len(included),
        'tied_matchups_excluded': len(predictions) - len(included),
        'brier_score': brier, 'constant_half_probability_brier': 0.25,
        'brier_difference_vs_half_baseline': brier - 0.25,
        'log_loss_nats': loss, 'constant_half_probability_log_loss_nats': math.log(2),
        'log_loss_difference_vs_half_baseline_nats': loss - math.log(2),
        'log_loss_clipped_predictions': sum(row['log_loss_probability_clipped'] for row in included),
        'lower_is_better': True,
    }


def build_diagnostic(capture: dict, config: dict, *, start_week: int = 4, end_week: int = 10,
                     now: datetime | None = None, max_age_seconds: int = 86400,
                     benchmark_simulations: int = 0, seed: int = 2610) -> dict:
    if type(benchmark_simulations) is not int or benchmark_simulations < 0:
        raise ValueError('benchmark_simulations must be a nonnegative integer')
    if type(seed) is not int:
        raise ValueError('seed must be an integer')
    snapshot = normalize_snapshot(capture, config, now=now, max_age_seconds=max_age_seconds)
    if end_week > capture['through_week']:
        raise ValueError('evaluation cannot extend beyond the validated final-result cutoff')
    weeks = {row['requested_week']: row['data'] for row in capture['weeks']}
    tie_rule = capture['league_info']['data'].get('scoringSettings', {}).get('matchupTieRule')
    predictions = walk_forward_predictions(weeks, snapshot['names'], start_week=start_week,
                                           end_week=end_week, matchup_tie_rule=tie_rule)
    teams = snapshot['teams']
    ranked = rank_espn(
        {tid: (team.wins, team.losses, team.ties) for tid, team in teams.items()},
        {tid: team.points_for for tid, team in teams.items()},
        {tid: team.points_against for tid, team in teams.items()},
        snapshot['outcomes'], snapshot['rules'].divisions, Random(seed),
    )
    standings = snapshot['standings']
    provider_seeds = [row.get('playoffSeed') for row in standings]
    if any(type(value) is not int for value in provider_seeds) or set(provider_seeds) != set(range(1, len(teams) + 1)):
        raise ValueError('provider seeds must be a complete unique ordering')
    provider = [str(row['teamId']) for row in sorted(standings, key=lambda row: row['playoffSeed'])]
    code_files = sorted((_PACKAGE_ROOT / 'src' / 'playoff_context').glob('*.py')) + [Path(__file__)]
    report = {
        'schema_version': 1, 'status': 'DIAGNOSTIC_ONLY_NOT_CALIBRATION_CERTIFICATION',
        'model_version': MODEL_VERSION, 'league_id': str(capture['league_id']), 'season': capture['season'],
        'capture_through_week': capture['through_week'],
        'validation_scope': 'RETROSPECTIVE_WALK_FORWARD_MATCHUP_WIN_PROBABILITIES',
        'evaluation_weeks': {'first': start_week, 'last': end_week},
        'method': {
            'model': 'estimate_strengths plus its matching independent-Normal win_probability',
            'training': 'Expanding completed-score history from Week 1 through the week before each prediction.',
            'weekly_strength_freeze': 'All team strengths are computed before adding any score from that evaluation week.',
            'projections_used': False, 'model_parameters_refit': False,
            'ties': 'Actual matchup ties are recorded but excluded from binary scoring metrics.',
            'brier_definition': 'Mean squared difference between home-win probability and observed binary home result.',
            'log_loss_definition': 'Mean binary negative log likelihood in natural-log units; probabilities clipped only for logs at 1e-15.',
            'baseline': '0.5 win probability in every evaluated matchup.',
        },
        'aggregate': metric_summary(predictions),
        'by_week': {str(week): metric_summary([row for row in predictions if row['week'] == week])
                    for week in range(start_week, end_week + 1)},
        'current_seed_reconciliation': {
            'completed_matchups': len(snapshot['outcomes']), 'through_week': capture['through_week'],
            'model_team_ids_in_seed_order': ranked, 'provider_team_ids_in_seed_order': provider,
            'exact_order_match': ranked == provider,
            'mismatches': [{'seed': index, 'model_team_id': actual, 'provider_team_id': expected}
                           for index, (actual, expected) in enumerate(zip(ranked, provider), start=1)
                           if actual != expected],
            'scope': 'One observed regular-season standings checkpoint; not complete rule validation or an exact clinch proof.',
            'rules_assumption': ESPN_DEFAULT_RULE_CAVEAT,
        },
        'input_validation': {
            'records_pf_pa_reconciled': True, 'completed_matchups': len(snapshot['outcomes']),
            'source_as_of': snapshot['source_as_of'], 'evaluated_at': snapshot['evaluated_at'],
            'freshness_slo_seconds': max_age_seconds,
        },
        'provenance': {
            'input_sha256': digest(capture), 'rules_sha256': digest(config),
            'model_code_sha256': digest({path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                        for path in code_files if path != Path(__file__)}),
            'model_and_diagnostic_code_sha256': digest({path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                                       for path in code_files}),
            'ranking_seed': seed,
        },
        'limitations': [
            'A sparse same-league retrospective sample; repeated teams and related weeks are not independent validation cohorts.',
            'These predictions were reconstructed now, not logged prospectively before the games.',
            'The frozen provider history can include later score corrections; original contemporaneous captures were not reconstructed.',
            'No external validation, calibration certification, hyperparameter optimization or statistical significance claim.',
            'Matchup prediction scores do not establish calibrated playoff or seed probabilities.',
            'No injury, roster, lineup, NFL bye, projection or opponent covariance adjustment.',
            'A matching current seed order validates one observed checkpoint only; unseen future tiebreak configurations may differ.',
        ],
        'predictions': predictions,
        'benchmark': {'performed': False},
        'publication_authorized': False,
        'forecast_editorial_gate': 'HOLD_EXPLORATORY',
    }
    if benchmark_simulations:
        started = perf_counter()
        output = simulate(teams, snapshot['future_games'], snapshot['rules'],
                          simulations=benchmark_simulations, seed=seed,
                          completed_outcomes=snapshot['outcomes'])
        elapsed = perf_counter() - started
        report['benchmark'] = {
            'performed': True, 'simulations': benchmark_simulations, 'seed': seed,
            'elapsed_seconds': elapsed, 'simulations_per_second': benchmark_simulations / elapsed,
            'remaining_matchups_per_trial': len(snapshot['future_games']),
            'sum_playoff_probabilities': sum(row['playoff_probability'] for row in output.values()),
            'expected_qualifying_berths': snapshot['rules'].playoff_teams,
            'output_sha256': digest(output),
            'scope': 'Runtime/invariant diagnostic only; no editorial publication authorization.',
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture', type=Path)
    parser.add_argument('--rules', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--start-week', type=int, default=4)
    parser.add_argument('--end-week', type=int, default=10)
    parser.add_argument('--benchmark-simulations', type=int, default=0)
    parser.add_argument('--seed', type=int, default=2610)
    parser.add_argument('--as-of', help='Explicit historical replay evaluation timestamp; does not relabel old data as live.')
    args = parser.parse_args()
    report = build_diagnostic(
        json.loads(args.capture.read_text()), json.loads(args.rules.read_text()),
        start_week=args.start_week, end_week=args.end_week,
        now=timestamp(args.as_of) if args.as_of else None,
        benchmark_simulations=args.benchmark_simulations, seed=args.seed,
    )
    report['evaluation_mode'] = 'HISTORICAL_REPLAY' if args.as_of else 'CURRENT_CAPTURE'
    report['provenance']['capture_path'] = str(args.capture)
    report['provenance']['rules_path'] = str(args.rules)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    print(json.dumps({'output': str(args.output), 'aggregate': report['aggregate'],
                      'seed_order_matches': report['current_seed_reconciliation']['exact_order_match'],
                      'benchmark': report['benchmark']}))


if __name__ == '__main__':
    main()
