from __future__ import annotations

from math import isfinite
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from .engine import Game, TeamState


_WEEK_KEYS = ("week", "matchupWeek", "matchupPeriod", "matchupPeriodId")


def _integer(value: object, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{label} must be a finite number") from exc
    if not isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def _id(value: object) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)) or not str(value).strip():
        raise ValueError("team ID must be a nonempty string or integer")
    return str(value)


def _team_id(side: Mapping[str, Any]) -> str:
    ids = [_id(side[key]) for key in ("teamId", "team_id") if key in side]
    if not ids or len(set(ids)) != 1:
        raise ValueError("teamId/team_id is missing or conflicting")
    return ids[0]


def _week(value: Mapping[str, Any], *, required: bool = True) -> int | None:
    weeks = [_integer(value[key], "week", 1) for key in _WEEK_KEYS if key in value]
    if not weeks:
        if required:
            raise ValueError("week metadata is missing")
        return None
    if len(set(weeks)) != 1:
        raise ValueError("week metadata is conflicting")
    return weeks[0]


def _expected_ids(values: Iterable[str] | None) -> set[str] | None:
    if values is None:
        return None
    ids = [_id(value) for value in values]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("expected team IDs must be nonempty and unique")
    return set(ids)


def require_final_week(
    matchups: Mapping[str, Any], *, expected_team_ids: Iterable[str] | None = None,
    expected_week: int | None = None, matchup_tie_rule: str | None = None,
) -> None:
    """Fail closed unless every supplied matchup has a coherent final result.

    Expected IDs/week bind this guard to the full requested league cutoff. With
    explicit SLOT_POINTS, a provider HOME/AWAY winner may have equal total points
    because the provider's position tiebreak decides that matchup. This does not
    implement or infer the position tiebreak from an equal-score observation.
    """
    try:
        expected = _expected_ids(expected_team_ids)
        if expected_week is not None:
            _integer(expected_week, "expected_week", 1)
        if matchup_tie_rule not in (None, "SLOT_POINTS"):
            raise ValueError("unsupported matchup tie rule")
        rows = matchups.get("matchups")
        if not isinstance(rows, list) or not rows:
            raise ValueError("a nonempty matchup list is required")
        top_week = _week(matchups, required=False)
        if expected_week is not None and top_week is not None and top_week != expected_week:
            raise ValueError("snapshot week does not match required final week")
        seen: set[str] = set()
        observed_weeks: set[int] = set()
        for row in rows:
            if not isinstance(row, Mapping):
                raise ValueError("matchup rows must be objects")
            winner = row.get("winner")
            if winner not in {"HOME", "AWAY", "TIE"}:
                raise ValueError("matchup winner must be HOME, AWAY or TIE; undecided/missing states cannot lock")
            row_week = _week(row, required=False)
            if row_week is not None and top_week is not None and row_week != top_week:
                raise ValueError("matchup and snapshot weeks conflict")
            week = row_week if row_week is not None else top_week
            if week is not None:
                observed_weeks.add(week)
            if expected_week is not None and week != expected_week:
                raise ValueError("matchup week is missing or does not match required final week")
            home, away = row.get("home"), row.get("away")
            if not isinstance(home, Mapping) or not isinstance(away, Mapping):
                raise ValueError("both home and away sides are required")
            home_id, away_id = _team_id(home), _team_id(away)
            if home_id == away_id or home_id in seen or away_id in seen:
                raise ValueError("each team must occur in exactly one final matchup")
            seen.update((home_id, away_id))
            hs = _number(home.get("totalPoints"), "final home totalPoints")
            as_ = _number(away.get("totalPoints"), "final away totalPoints")
            if hs == as_:
                if winner != "TIE" and matchup_tie_rule != "SLOT_POINTS":
                    raise ValueError("equal scores require TIE or an explicit supported provider tiebreak")
            elif (winner == "HOME" and hs < as_) or (winner == "AWAY" and as_ < hs) or winner == "TIE":
                raise ValueError("final winner disagrees with final scores")
        if len(observed_weeks) > 1:
            raise ValueError("a final-week lock cannot mix multiple weeks")
        if expected is not None and seen != expected:
            raise ValueError("final matchups must contain every expected team exactly once")
    except (ValueError, TypeError, AttributeError) as exc:
        raise RuntimeError(f"RESULT_LOCK_REQUIRED: {exc}") from exc


def normalize_teams(
    standings: Sequence[Mapping[str, Any]], completed_scores: Mapping[str, Sequence[float]],
) -> Dict[str, TeamState]:
    if not standings:
        raise ValueError("standings must not be empty")
    out: Dict[str, TeamState] = {}
    for row in standings:
        tid = _team_id(row)
        if tid in out:
            raise ValueError("duplicate standings team ID")
        required = ("wins", "losses", "ties", "pointsFor")
        if any(field not in row for field in required):
            raise ValueError("standings require explicit wins/losses/ties/pointsFor")
        wins, losses, ties = (_integer(row[field], field) for field in ("wins", "losses", "ties"))
        scores = tuple(_number(value, "completed score") for value in completed_scores.get(tid, ()))
        if len(scores) > wins + losses + ties:
            raise ValueError("score history is longer than completed records")
        name = row.get("teamName", row.get("team_name", tid))
        if not isinstance(name, str) or not name.strip():
            raise ValueError("team name must be a nonempty string")
        out[tid] = TeamState(
            team_id=tid, name=name.strip(), wins=wins, losses=losses, ties=ties,
            points_for=_number(row["pointsFor"], "pointsFor"), scores=scores,
            points_against=_number(row.get("pointsAgainst", 0.0), "pointsAgainst"),
        )
    if set(completed_scores) - set(out):
        raise ValueError("score history includes an unknown team")
    return out


def normalize_future_games(
    weeks: Sequence[Mapping[str, Any]], from_week: int, through_week: int, *,
    expected_team_ids: Iterable[str] | None = None,
) -> List[Game]:
    _integer(from_week, "from_week", 1)
    _integer(through_week, "through_week", 1)
    expected = _expected_ids(expected_team_ids)
    if from_week == through_week + 1:
        return []
    if from_week > through_week:
        raise ValueError("future week range is invalid")
    games: List[Game] = []
    seen_weeks: set[int] = set()
    for raw_week in weeks:
        week = _week(raw_week)
        if not from_week <= week <= through_week:
            continue
        if week in seen_weeks:
            raise ValueError("duplicate future-week container")
        seen_weeks.add(week)
        rows = raw_week.get("matchups")
        if not isinstance(rows, list) or not rows:
            raise ValueError("future week requires a nonempty matchup list")
        seen: set[str] = set()
        for row in rows:
            row_week = _week(row, required=False)
            if row_week is not None and row_week != week:
                raise ValueError("future matchup week conflicts with its container")
            home, away = row.get("home"), row.get("away")
            if not isinstance(home, Mapping) or not isinstance(away, Mapping):
                raise ValueError("future matchup requires both participants")
            home_id, away_id = _team_id(home), _team_id(away)
            if home_id == away_id or home_id in seen or away_id in seen:
                raise ValueError("future team cannot repeat or play itself in one week")
            seen.update((home_id, away_id))
            games.append(Game(week, home_id, away_id, _projection(home), _projection(away)))
        if expected is not None and seen != expected:
            raise ValueError("each future week must contain every expected team exactly once")
    if seen_weeks != set(range(from_week, through_week + 1)):
        raise ValueError("future schedule is missing a required week")
    return sorted(games, key=lambda game: (game.week, game.home_id, game.away_id))


def _projection(side: Mapping[str, Any]) -> float | None:
    value = side.get("totalProjectedPoints")
    if value is None:
        return None
    value = _number(value, "totalProjectedPoints")
    if value < 0:
        raise ValueError("totalProjectedPoints cannot be negative")
    return value if value > 0 else None
