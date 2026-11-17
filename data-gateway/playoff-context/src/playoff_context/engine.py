from __future__ import annotations

from dataclasses import dataclass
from math import erfc, exp, hypot, isfinite, sqrt
from random import Random
from statistics import mean, pstdev
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


class UnsupportedRulesError(ValueError):
    """The requested report needs qualification rules not implemented here."""


class UnresolvedTiebreakError(UnsupportedRulesError):
    """The configured tiebreak did not determine every reported seed."""


@dataclass(frozen=True)
class TeamState:
    team_id: str
    name: str
    wins: int
    losses: int
    ties: int = 0
    points_for: float = 0.0
    scores: Tuple[float, ...] = ()
    points_against: float = 0.0


@dataclass(frozen=True)
class Game:
    week: int
    home_id: str
    away_id: str
    home_projection: Optional[float] = None
    away_projection: Optional[float] = None


@dataclass(frozen=True)
class LeagueRules:
    playoff_teams: int
    regular_season_weeks: int
    tiebreaker: str = "UNKNOWN"
    divisions: Optional[Mapping[str, str]] = None
    qualification_policy: str = "UNKNOWN"


@dataclass(frozen=True)
class Strength:
    mu: float
    sigma: float


Outcome = Tuple[str, str, Optional[str]]


def _integer(value: object, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _finite(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    try:
        out = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{label} must be a finite number") from exc
    if not isfinite(out):
        raise ValueError(f"{label} must be a finite number")
    return out


def _require_supported_rules(rules: LeagueRules, *, for_probability: bool) -> None:
    if rules.qualification_policy == "OVERALL":
        if not for_probability or rules.tiebreaker == "POINTS_FOR":
            return
    if (rules.qualification_policy == "DIVISION_WINNERS_PLUS_WILDCARDS"
            and rules.tiebreaker == "H2H_RECORD" and rules.divisions):
        if rules.playoff_teams < len(set(rules.divisions.values())):
            raise ValueError("playoff berths cannot be fewer than automatic division berths")
        return
    raise UnsupportedRulesError(
        "RULES_HOLD: explicitly verified qualification and tiebreak rules are required; "
        "supported forecast modes are OVERALL/POINTS_FOR and "
        "DIVISION_WINNERS_PLUS_WILDCARDS/H2H_RECORD (documented ESPN defaults)"
    )


def _validate_inputs(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules) -> int:
    """Validate a complete equal-length season without team byes.

    Freshness, provider identity and final-result locks belong to the snapshot
    runner; direct calls here cannot establish publication eligibility.
    """
    if not isinstance(rules, LeagueRules):
        raise ValueError("rules must be an explicit LeagueRules object")
    if not isinstance(future_games, Sequence) or isinstance(future_games, (str, bytes)):
        raise ValueError("future_games must be a sequence of Game objects")
    if not isinstance(teams, Mapping) or len(teams) < 2 or len(teams) % 2:
        raise ValueError("teams must contain an even number of at least two teams")
    _integer(rules.playoff_teams, "playoff_teams", 1)
    _integer(rules.regular_season_weeks, "regular_season_weeks", 1)
    if rules.playoff_teams > len(teams):
        raise ValueError("playoff_teams cannot exceed team count")
    completed = set()
    for tid, team in teams.items():
        if not isinstance(team, TeamState):
            raise ValueError("teams must map IDs to TeamState objects")
        if not isinstance(tid, str) or not tid.strip() or team.team_id != tid:
            raise ValueError("team mapping keys must match nonempty string team IDs")
        if not isinstance(team.name, str) or not team.name.strip():
            raise ValueError(f"team {tid} requires a nonempty name")
        for field in ("wins", "losses", "ties"):
            _integer(getattr(team, field), f"team {tid} {field}")
        n = team.wins + team.losses + team.ties
        completed.add(n)
        _finite(team.points_for, f"team {tid} points_for")
        _finite(team.points_against, f"team {tid} points_against")
        if len(team.scores) > n:
            raise ValueError(f"team {tid} has more completed scores than recorded games")
        for score in team.scores:
            _finite(score, f"team {tid} completed score")
    if len(completed) != 1:
        raise ValueError("all teams must have the same number of completed games")
    completed_week = completed.pop()
    if completed_week > rules.regular_season_weeks:
        raise ValueError("completed records exceed regular-season horizon")
    if sum(t.wins for t in teams.values()) != sum(t.losses for t in teams.values()):
        raise ValueError("league completed wins must equal completed losses")
    if sum(t.ties for t in teams.values()) % 2:
        raise ValueError("league tie counts must occur in pairs")
    if rules.divisions is not None:
        if set(rules.divisions) != set(teams):
            raise ValueError("division mapping must cover every team exactly once")
        if any(not isinstance(v, str) or not v.strip() for v in rules.divisions.values()):
            raise ValueError("division labels must be nonempty strings")
    participants: Dict[int, set[str]] = {}
    for game in future_games:
        if not isinstance(game, Game):
            raise ValueError("future_games must contain Game objects")
        _integer(game.week, "game week", 1)
        if not completed_week < game.week <= rules.regular_season_weeks:
            raise ValueError("future game is outside the remaining regular-season horizon")
        if game.home_id not in teams or game.away_id not in teams:
            raise ValueError("future game contains an unknown team")
        if game.home_id == game.away_id:
            raise ValueError("a team cannot play itself")
        seen = participants.setdefault(game.week, set())
        if game.home_id in seen or game.away_id in seen:
            raise ValueError("duplicate fixture or repeated team in a future week")
        seen.update((game.home_id, game.away_id))
        for projection in (game.home_projection, game.away_projection):
            if projection is not None and _finite(projection, "projection") <= 0:
                raise ValueError("provided projections must be positive")
    if set(participants) != set(range(completed_week + 1, rules.regular_season_weeks + 1)):
        raise ValueError("future schedule must cover every remaining regular-season week")
    if any(ids != set(teams) for ids in participants.values()):
        raise ValueError("each remaining week must contain every team exactly once")
    return completed_week


def _validate_ledger(teams: Mapping[str, TeamState], outcomes: Sequence[Outcome]) -> None:
    if not isinstance(outcomes, Sequence) or isinstance(outcomes, (str, bytes)):
        raise ValueError("completed outcomes must be a sequence of matchup results")
    records = {tid: [0, 0, 0] for tid in teams}
    for outcome in outcomes:
        if not isinstance(outcome, (tuple, list)) or len(outcome) != 3:
            raise ValueError("completed outcomes must be (home_id, away_id, winner_id_or_None)")
        home, away, winner = outcome
        if home not in teams or away not in teams or home == away:
            raise ValueError("completed outcome must contain two distinct known teams")
        if winner is None:
            records[home][2] += 1
            records[away][2] += 1
        elif winner in (home, away):
            loser = away if winner == home else home
            records[winner][0] += 1
            records[loser][1] += 1
        else:
            raise ValueError("completed winner must be one of the matchup participants")
    for tid, team in teams.items():
        if tuple(records[tid]) != (team.wins, team.losses, team.ties):
            raise ValueError("completed outcome ledger does not reproduce initial W/L/T records")


def _blend_mean(scores: Sequence[float], projection: Optional[float], league_mean: float) -> float:
    if scores:
        season, recent = mean(scores), mean(scores[-3:])
        w_data = min(0.80, 0.35 + 0.10 * len(scores))
        observed = 0.60 * season + 0.40 * recent
        prior = projection if projection is not None else league_mean
        return w_data * observed + (1.0 - w_data) * prior
    return projection if projection is not None else league_mean


def estimate_strengths(teams: Mapping[str, TeamState], next_projection: Optional[Mapping[str, float]] = None,
                       min_sigma: float = 12.0) -> Dict[str, Strength]:
    if _finite(min_sigma, "min_sigma") <= 0:
        raise ValueError("min_sigma must be positive")
    all_scores = [s for t in teams.values() for s in t.scores]
    for score in all_scores:
        _finite(score, "completed score")
    for tid, projection in (next_projection or {}).items():
        if tid not in teams or _finite(projection, "projection") <= 0:
            raise ValueError("projections must be positive and reference known teams")
    league_mean = mean(all_scores) if all_scores else 130.0
    league_sigma = pstdev(all_scores) if len(all_scores) > 1 else 22.0
    out = {}
    for team_id, team in teams.items():
        mu = _blend_mean(team.scores, (next_projection or {}).get(team_id), league_mean)
        sigma = max(min_sigma, pstdev(team.scores) if len(team.scores) > 1 else league_sigma)
        if len(team.scores) < 5:
            sigma = 0.5 * sigma + 0.5 * max(min_sigma, league_sigma)
        _finite(mu, "estimated mean")
        _finite(sigma, "estimated standard deviation")
        out[team_id] = Strength(mu=mu, sigma=sigma)
    return out


def win_probability(a: Strength, b: Strength) -> float:
    """Win probability under the independent Normal scores used by simulation."""
    for strength in (a, b):
        _finite(strength.mu, "strength mean")
        if _finite(strength.sigma, "strength standard deviation") <= 0:
            raise ValueError("strength standard deviation must be positive")
    scale = hypot(a.sigma, b.sigma)
    _finite(scale, "combined standard deviation")
    return 0.5 * erfc((b.mu - a.mu) / (scale * sqrt(2.0)))


def rank_teams(records: Mapping[str, Tuple[int, int, int]], points_for: Mapping[str, float],
               rules: LeagueRules) -> List[str]:
    """Overall/points-for seeds only; team ID is never a sporting tiebreak."""
    if rules.qualification_policy != "OVERALL" or rules.tiebreaker != "POINTS_FOR":
        raise UnsupportedRulesError("RULES_HOLD: rank_teams supports only explicit OVERALL/POINTS_FOR")
    if not records or set(records) != set(points_for):
        raise ValueError("records and points_for must cover the same nonempty team set")
    keys = {}
    for tid, record in records.items():
        if len(record) != 3:
            raise ValueError("records must contain wins, losses and ties")
        for value in record:
            _integer(value, "record value")
        wins, losses, ties = record
        games = wins + losses + ties
        keys[tid] = ((wins + 0.5 * ties) / games if games else 0.0,
                     _finite(points_for[tid], "points_for"))
    ranking = sorted(records, key=keys.__getitem__, reverse=True)
    if any(keys[a] == keys[b] for a, b in zip(ranking, ranking[1:])):
        raise UnresolvedTiebreakError("RULES_HOLD: tied record and points require a verified additional tiebreak")
    return ranking


def _standard_normal_above(threshold: float, rng: Random) -> float:
    """Draw Z | Z > threshold, using exponential rejection for rare tails."""
    _finite(threshold, "conditional threshold")
    if threshold <= 0:
        while True:
            z = rng.gauss(0.0, 1.0)
            if z > threshold:
                return z
    rate = 0.5 * threshold + 0.5 * hypot(threshold, 2.0)
    while True:
        z = threshold + rng.expovariate(rate)
        if rng.random() <= exp(-0.5 * (z - rate) ** 2):
            return z


def _sample_scores(home: Strength, away: Strength, rng: Random,
                   forced_home: Optional[bool] = None) -> Tuple[float, float]:
    if forced_home is None:
        hs, as_ = rng.gauss(home.mu, home.sigma), rng.gauss(away.mu, away.sigma)
        return _finite(hs, "sampled home score"), _finite(as_, "sampled away score")
    sd = _finite(hypot(home.sigma, away.sigma), "combined standard deviation")
    difference_mean = home.mu - away.mu
    _finite(difference_mean, "conditional mean difference")
    if forced_home:
        z = _standard_normal_above(-difference_mean / sd, rng)
    else:
        z = -_standard_normal_above(difference_mean / sd, rng)
    difference = difference_mean + sd * z
    conditional_home_mean = home.mu + (home.sigma / sd) ** 2 * (difference - difference_mean)
    conditional_home_sigma = (home.sigma / sd) * away.sigma
    hs = rng.gauss(conditional_home_mean, conditional_home_sigma)
    as_ = hs - difference
    if not isfinite(hs) or not isfinite(as_) or (hs > as_) != forced_home or hs == as_:
        raise ValueError("forced score draw exceeded numerical precision")
    return hs, as_


def simulate(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules,
             simulations: int = 50000, seed: int = 2604,
             forced_results: Optional[Mapping[Tuple[int, str, str], str]] = None, *,
             completed_outcomes: Sequence[Outcome] = ()) -> Dict[str, dict]:
    """Replay a complete schedule with score-coherent outcomes and shared RNG.

    Each trial/game has an independent stream; forcing one game cannot move other
    games onto unrelated draws. Conditional runs use the same master seed.
    The ESPN mode is conditional on its documented default seeding waterfall;
    league-manager overrides require separate evidence and are not modeled here.
    Independent Normal scores are a modeling assumption, not provider facts.
    """
    _integer(simulations, "simulations", 1)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    _validate_inputs(teams, future_games, rules)
    _require_supported_rules(rules, for_probability=True)
    espn_mode = rules.qualification_policy == "DIVISION_WINNERS_PLUS_WILDCARDS"
    if espn_mode or completed_outcomes:
        _validate_ledger(teams, completed_outcomes)
    if espn_mode:
        from .seeding import rank_espn
    games = sorted(future_games, key=lambda g: (g.week, g.home_id, g.away_id))
    keys = {(g.week, g.home_id, g.away_id) for g in games}
    forced_results = forced_results or {}
    for key, winner in forced_results.items():
        if key not in keys:
            raise ValueError("forced result references a game absent from the future schedule")
        if winner not in key[1:]:
            raise ValueError("forced winner must be a participant in the referenced game")
    strengths = []
    for game in games:
        projections = {tid: projection for tid, projection in (
            (game.home_id, game.home_projection), (game.away_id, game.away_projection)
        ) if projection is not None}
        by_team = estimate_strengths(teams, projections)
        strengths.append((by_team[game.home_id], by_team[game.away_id]))
    rng = Random(seed)
    playoff_count = {tid: 0 for tid in teams}
    seed_count = {tid: [0] * (len(teams) + 1) for tid in teams}
    division_count = {tid: 0 for tid in teams}
    final_wins = {tid: [] for tid in teams}
    for _ in range(simulations):
        rec = {tid: [t.wins, t.losses, t.ties] for tid, t in teams.items()}
        pf = {tid: t.points_for for tid, t in teams.items()}
        pa = {tid: t.points_against for tid, t in teams.items()}
        ledger = list(completed_outcomes)
        for game, (home_strength, away_strength) in zip(games, strengths):
            forced = forced_results.get((game.week, game.home_id, game.away_id))
            forced_home = None if forced is None else forced == game.home_id
            hs, as_ = _sample_scores(home_strength, away_strength, Random(rng.getrandbits(128)), forced_home)
            pf[game.home_id] += hs
            pf[game.away_id] += as_
            pa[game.home_id] += as_
            pa[game.away_id] += hs
            if hs > as_:
                rec[game.home_id][0] += 1
                rec[game.away_id][1] += 1
                winner = game.home_id
            elif hs < as_:
                rec[game.away_id][0] += 1
                rec[game.home_id][1] += 1
                winner = game.away_id
            else:
                rec[game.home_id][2] += 1
                rec[game.away_id][2] += 1
                winner = None
            ledger.append((game.home_id, game.away_id, winner))
        ranking_rng = Random(rng.getrandbits(128))
        final_records = {k: tuple(v) for k, v in rec.items()}
        if espn_mode:
            ranking = rank_espn(final_records, pf, pa, ledger, rules.divisions, ranking_rng)
        else:
            ranking = rank_teams(final_records, pf, rules)
        for idx, tid in enumerate(ranking, start=1):
            seed_count[tid][idx] += 1
            if idx <= rules.playoff_teams:
                playoff_count[tid] += 1
            if espn_mode and idx <= len(set(rules.divisions.values())):
                division_count[tid] += 1
            final_wins[tid].append(rec[tid][0])
    result = {}
    for tid in teams:
        wins = sorted(final_wins[tid])
        probability = playoff_count[tid] / simulations
        result[tid] = {
            "class": "PROBABILISTIC",
            "playoff_probability": probability,
            "playoff_probability_mc_standard_error": sqrt(probability * (1 - probability) / simulations),
            "seed_probability": {str(i): seed_count[tid][i] / simulations
                                 for i in range(1, len(teams) + 1) if seed_count[tid][i]},
            "expected_final_wins": mean(final_wins[tid]),
            "final_wins_p10_p90": [wins[int(0.10 * (len(wins) - 1))], wins[int(0.90 * (len(wins) - 1))]],
            "qualification_policy": rules.qualification_policy,
            "tiebreaker": rules.tiebreaker,
        }
        if espn_mode:
            result[tid]["division_title_probability"] = division_count[tid] / simulations
            result[tid]["rules_assumption"] = "CONDITIONAL_ON_DOCUMENTED_ESPN_DEFAULT_SEEDING; NO_MANAGER_OVERRIDE_MODELED"
    return result


def remaining_games_by_team(future_games: Sequence[Game]) -> Dict[str, int]:
    rem = {}
    for game in future_games:
        rem[game.home_id] = rem.get(game.home_id, 0) + 1
        rem[game.away_id] = rem.get(game.away_id, 0) + 1
    return rem


def exact_bounds_status(teams: Mapping[str, TeamState], future_games: Sequence[Game],
                        rules: LeagueRules) -> Dict[str, dict]:
    _validate_inputs(teams, future_games, rules)
    unknown = {
        "status": "UNKNOWN", "class": "UNRESOLVED", "proof": None,
        "note": "Bounds prove neither a berth nor elimination; no exact ALIVE claim is made.",
    }
    if rules.qualification_policy != "OVERALL":
        return {tid: {**unknown, "note": "Exact division/tiebreak solver not implemented; no exact qualification claim."}
                for tid in teams}
    rem = remaining_games_by_team(future_games)
    minimum = {tid: 2 * team.wins + team.ties for tid, team in teams.items()}
    maximum = {tid: minimum[tid] + 2 * rem.get(tid, 0) for tid in teams}
    out = {}
    for tid in teams:
        guaranteed_above = sum(minimum[other] > maximum[tid] for other in teams if other != tid)
        possible_at_or_above = sum(maximum[other] >= minimum[tid] for other in teams if other != tid)
        if guaranteed_above >= rules.playoff_teams:
            out[tid] = {"status": "ELIMINATED", "class": "EXACT", "proof": "strict_record_point_bounds"}
        elif possible_at_or_above < rules.playoff_teams:
            out[tid] = {"status": "CLINCHED", "class": "EXACT", "proof": "strict_record_point_bounds"}
        else:
            out[tid] = dict(unknown)
    return out


def conditional_leverage(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules,
                         current_game: Game, simulations: int = 20000, seed: int = 2604, *,
                         completed_outcomes: Sequence[Outcome] = ()) -> Dict[str, dict]:
    key = (current_game.week, current_game.home_id, current_game.away_id)
    if key not in {(g.week, g.home_id, g.away_id) for g in future_games}:
        raise ValueError("conditioned game must occur in the supplied future schedule")
    win_home = simulate(teams, future_games, rules, simulations, seed, {key: current_game.home_id},
                        completed_outcomes=completed_outcomes)
    win_away = simulate(teams, future_games, rules, simulations, seed, {key: current_game.away_id},
                        completed_outcomes=completed_outcomes)
    out = {}
    for tid, win_result, loss_result in (
        (current_game.home_id, win_home, win_away), (current_game.away_id, win_away, win_home)
    ):
        pw, pl = win_result[tid]["playoff_probability"], loss_result[tid]["playoff_probability"]
        out[tid] = {
            "class": "PROBABILISTIC", "conditional_win_probability": pw,
            "conditional_loss_probability": pl, "leverage_delta_pp": (pw - pl) * 100.0,
        }
        if rules.qualification_policy == "DIVISION_WINNERS_PLUS_WILDCARDS":
            out[tid]["rules_assumption"] = "CONDITIONAL_ON_DOCUMENTED_ESPN_DEFAULT_SEEDING; NO_MANAGER_OVERRIDE_MODELED"
    return out
