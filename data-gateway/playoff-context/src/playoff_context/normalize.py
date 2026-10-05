from __future__ import annotations
from typing import Any, Dict, List, Mapping, Sequence
from .engine import Game, TeamState

def require_final_week(matchups: Mapping[str, Any]) -> None:
    undecided = [m for m in matchups.get("matchups", []) if m.get("winner") == "UNDECIDED"]
    if undecided:
        raise RuntimeError("RESULT_LOCK_REQUIRED: current week contains UNDECIDED matchup(s)")

def normalize_teams(standings: Sequence[Mapping[str, Any]], completed_scores: Mapping[str, Sequence[float]]) -> Dict[str, TeamState]:
    out: Dict[str, TeamState] = {}
    for row in standings:
        tid = str(row["teamId"])
        out[tid] = TeamState(
            team_id=tid,
            name=str(row.get("teamName", tid)).strip(),
            wins=int(row.get("wins", 0)),
            losses=int(row.get("losses", 0)),
            ties=int(row.get("ties", 0)),
            points_for=float(row.get("pointsFor", 0.0)),
            scores=tuple(float(x) for x in completed_scores.get(tid, ())),
        )
    return out

def normalize_future_games(weeks: Sequence[Mapping[str, Any]], from_week: int, through_week: int) -> List[Game]:
    games: List[Game] = []
    for w in weeks:
        week = int(w.get("week") or w.get("matchupWeek") or w.get("matchupPeriod") or 0)
        if not (from_week <= week <= through_week):
            continue
        for m in w.get("matchups", []):
            home, away = m.get("home") or {}, m.get("away") or {}
            if "teamId" not in home or "teamId" not in away:
                continue
            games.append(Game(
                week=week,
                home_id=str(home["teamId"]),
                away_id=str(away["teamId"]),
                home_projection=_projection(home),
                away_projection=_projection(away),
            ))
    return games

def _projection(side: Mapping[str, Any]) -> float | None:
    v = side.get("totalProjectedPoints")
    if v is None:
        return None
    v = float(v)
    return v if v > 0 else None
