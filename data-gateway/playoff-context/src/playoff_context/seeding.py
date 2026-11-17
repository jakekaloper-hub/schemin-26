"""Conditional ESPN H2H regular-season seeding, independently implemented.

This module ranks the records supplied by its caller. It does not establish a
league's qualification policy, simulate playoff games, or prove clinching.
An empty ``divisions`` mapping expressly selects a league without divisions;
otherwise every team must have a supplied division. One winner per division is
ranked ahead of the remaining teams. A caller may then select the configured
number of qualifying positions.

The documented H2H-first waterfall is applied to one seed at a time. H2H uses
the entire tied group for that seed and requires the same positive game count
for every pair of teams in that group. Equal per-team totals alone do not
establish that the teams all played each other equally. A tie that remains
after a criterion proceeds to the next criterion; H2H restarts only after a
seed has been awarded.

Official ESPN articles also reserve the League Manager's right to override
seeding. This implementation is conditional on the caller's verified rules,
not a claim that every League Manager league uses this waterfall.
"""

from collections.abc import Mapping, Sequence
from decimal import Decimal
from fractions import Fraction
import math
import random
from typing import TypeAlias


ESPN_DEFAULT_RULE_SOURCES = (
    "https://support.espn.com/hc/en-us/articles/47190901074708-"
    "H2H-Points-League-Playoff-Seeding-Tiebreakers",
    "https://support.espn.com/hc/en-us/articles/360036952471-"
    "Playoff-Seeding-How-Regular-Season-Standings-Tiebreakers-Work",
)
ESPN_DEFAULT_RULE_CAVEAT = (
    "Conditional on verified division winners plus shared berths and ESPN's "
    "documented H2H-first default: H2H only with equal positive game counts "
    "for every tied-team pair, points for, division winning percentage, "
    "points against, then a random tie "
    "decision; the process restarts after each seed. League Manager overrides "
    "may differ. This ranks regular-season seeds, not championship outcomes "
    "or mathematical clinching."
)

Points: TypeAlias = int | float | Decimal | Fraction
Record: TypeAlias = tuple[int, int, int]
Outcome: TypeAlias = tuple[str, str, str | None]


def _winning_percentage(record: Sequence[int]) -> Fraction:
    wins, losses, ties = record
    played = wins + losses + ties
    return Fraction(2 * wins + ties, 2 * played) if played else Fraction(0)


def _exact_points(values: Mapping[str, Points], teams: set[str], name: str):
    if not isinstance(values, Mapping) or set(values) != teams:
        raise ValueError(f"{name} must contain exactly the record team IDs")
    result: dict[str, Fraction] = {}
    for team, value in values.items():
        if isinstance(value, bool) or not isinstance(
            value, (int, float, Decimal, Fraction)
        ):
            raise ValueError(f"{name}[{team!r}] must be a finite number")
        if isinstance(value, float):
            if not math.isfinite(value):
                raise ValueError(f"{name}[{team!r}] must be finite")
            # Preserve the caller's decimal representation instead of creating
            # artificial distinctions from a binary float's full expansion.
            result[team] = Fraction(str(value))
        elif isinstance(value, Decimal):
            if not value.is_finite():
                raise ValueError(f"{name}[{team!r}] must be finite")
            result[team] = Fraction(value)
        else:
            result[team] = Fraction(value)
    return result


def rank_espn(
    records: Mapping[str, Record],
    points_for: Mapping[str, Points],
    points_against: Mapping[str, Points],
    completed_outcomes: Sequence[Outcome],
    divisions: Mapping[str, str],
    rng: random.Random,
) -> list[str]:
    """Return all team IDs in conditional ESPN regular-season seed order.

    ``completed_outcomes`` must contain the complete result ledger represented
    by ``records``, including simulated results when ranking a simulated
    season. Each entry is ``(home_id, away_id, winner_id)``; ``None`` means an
    actual tied game, never a missing or undecided result. Repeated pairings
    are valid rematches. Ledger W/L/T totals must exactly match every record.

    ``divisions`` is either an explicit empty mapping for no divisions or a
    complete mapping of team ID to nonempty division ID. An incomplete mapping
    is rejected. No implicit qualification policy or tiebreaker is inferred.

    Records and winning percentages use integer/rational arithmetic. Points
    must be finite; negative scores are allowed. The ledger has no score or
    game-ID fields, so callers remain responsible for score provenance and
    unique game identities. Only ``rng`` may be mutated, and only if a residual
    tie needs a random decision. All other inputs are left unchanged.

    Raises ``ValueError`` for malformed or inconsistent ranking inputs.
    """
    if not isinstance(records, Mapping) or not records:
        raise ValueError("records must be a nonempty mapping")
    teams = set(records)
    if any(not isinstance(team, str) or not team for team in teams):
        raise ValueError("team IDs must be nonempty strings")
    for team, record in records.items():
        if (
            not isinstance(record, (tuple, list))
            or len(record) != 3
            or any(type(count) is not int or count < 0 for count in record)
        ):
            raise ValueError(f"record for {team!r} must be nonnegative integer W/L/T")
    pf = _exact_points(points_for, teams, "points_for")
    pa = _exact_points(points_against, teams, "points_against")
    if not isinstance(divisions, Mapping):
        raise ValueError("divisions must be an explicit mapping")
    if divisions and set(divisions) != teams:
        raise ValueError("divisions must be empty or contain every record team ID")
    if any(not isinstance(division, str) or not division for division in divisions.values()):
        raise ValueError("division IDs must be nonempty strings")
    if not isinstance(rng, random.Random):
        raise ValueError("rng must be an explicit random.Random instance")
    if not isinstance(completed_outcomes, Sequence) or isinstance(
        completed_outcomes, (str, bytes)
    ):
        raise ValueError("completed_outcomes must be a sequence of game results")

    counted = {team: [0, 0, 0] for team in teams}
    division_records = {team: [0, 0, 0] for team in teams}
    # Each directed pair stores [games played, twice wins plus ties].
    pair_records = {team: {} for team in teams}
    for index, outcome in enumerate(completed_outcomes):
        if not isinstance(outcome, (tuple, list)) or len(outcome) != 3:
            raise ValueError(f"ledger entry {index} must be (home, away, winner)")
        home, away, winner = outcome
        if (
            not isinstance(home, str)
            or not isinstance(away, str)
            or home not in teams
            or away not in teams
            or home == away
        ):
            raise ValueError(f"ledger entry {index} requires two different known teams")
        if winner is not None and (
            not isinstance(winner, str) or winner not in (home, away)
        ):
            raise ValueError(f"ledger entry {index} has an invalid winner")
        same_division = bool(divisions) and divisions[home] == divisions[away]
        for team, opponent in ((home, away), (away, home)):
            result_index = 2 if winner is None else (0 if winner == team else 1)
            counted[team][result_index] += 1
            if same_division:
                division_records[team][result_index] += 1
            pair = pair_records[team].setdefault(opponent, [0, 0])
            pair[0] += 1
            pair[1] += 1 if winner is None else (2 if winner == team else 0)

    for team in sorted(teams):
        if tuple(counted[team]) != tuple(records[team]):
            raise ValueError(
                f"ledger/record mismatch for {team}: ledger {tuple(counted[team])}, "
                f"record {tuple(records[team])}"
            )

    percentages = {team: _winning_percentage(records[team]) for team in teams}
    division_percentages = {
        team: _winning_percentage(division_records[team]) for team in teams
    }

    def best_by(candidates: list[str], values: Mapping[str, Fraction]) -> list[str]:
        best = max(values[team] for team in candidates)
        return [team for team in candidates if values[team] == best]

    def select_seed(pool: Sequence[str]) -> str:
        candidates = best_by(sorted(pool), percentages)
        if len(candidates) == 1:
            return candidates[0]

        # ESPN's condition is that all tied teams played each other equally.
        # Include unplayed pairs as zero: identical aggregate game totals can
        # otherwise incorrectly admit disconnected or unbalanced schedules.
        pair_counts = {
            pair_records[team].get(opponent, (0, 0))[0]
            for index, team in enumerate(candidates)
            for opponent in candidates[index + 1:]
        }
        if len(pair_counts) == 1 and 0 not in pair_counts:
            h2h_results = {}
            for team in candidates:
                played = earned = 0
                for opponent in candidates:
                    pair = pair_records[team].get(opponent)
                    if pair is not None:
                        played += pair[0]
                        earned += pair[1]
                h2h_results[team] = Fraction(earned, 2 * played)
            candidates = best_by(candidates, h2h_results)
        # Keep the surviving leaders and advance the waterfall. Do not
        # recompute H2H against a smaller group while selecting this seed.
        for values in (pf, division_percentages, pa):
            if len(candidates) == 1:
                return candidates[0]
            candidates = best_by(candidates, values)
        return candidates[0] if len(candidates) == 1 else rng.choice(candidates)

    def seed_pool(pool: Sequence[str]) -> list[str]:
        remaining = list(pool)
        ordered = []
        while remaining:
            selected = select_seed(remaining)
            ordered.append(selected)
            remaining.remove(selected)
        return ordered

    if not divisions:
        return seed_pool(sorted(teams))

    division_pools: dict[str, list[str]] = {}
    for team in sorted(teams):
        division_pools.setdefault(divisions[team], []).append(team)
    champions = [select_seed(division_pools[division]) for division in sorted(division_pools)]
    other_teams = sorted(teams.difference(champions))
    return seed_pool(champions) + seed_pool(other_teams)
