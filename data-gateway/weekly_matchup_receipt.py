#!/usr/bin/env python3
"""Fail-closed bridge for captured Flaim weekly matchup observations.

This accepts only an explicitly provenance-stamped capture produced by an
authorized operator. It does NOT query or authenticate Flaim by itself.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

class WeeklyMatchupError(ValueError):
    pass

def timestamp(value):
    if not isinstance(value, str) or not value.strip():
        raise WeeklyMatchupError("captured_at required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WeeklyMatchupError("invalid captured_at") from exc
    if parsed.tzinfo is None:
        raise WeeklyMatchupError("captured_at must have timezone")
    return parsed.astimezone(timezone.utc)

def normalize(capture, now=None, slo_seconds=3600):
    if capture.get("provider") != "flaim" or capture.get("platform") != "espn":
        raise WeeklyMatchupError("provider/platform mismatch")
    if str(capture.get("league_id")) != "1417621" or capture.get("season_year") != 2026:
        raise WeeklyMatchupError("league/season mismatch")
    week = capture.get("week")
    if type(week) is not int or not 1 <= week <= 18:
        raise WeeklyMatchupError("invalid week")
    rows = capture.get("matchups")
    if not isinstance(rows, list) or len(rows) != 6:
        raise WeeklyMatchupError("six matchups required")
    seen = []
    output = []
    for row in rows:
        if row.get("matchupPeriodId") != week:
            raise WeeklyMatchupError("matchup week mismatch")
        sides = []
        for role in ("home", "away"):
            team = row.get(role)
            if not isinstance(team, dict):
                raise WeeklyMatchupError("missing matchup side")
            tid = team.get("teamId")
            if type(tid) is not int or not 1 <= tid <= 12 or not team.get("teamName"):
                raise WeeklyMatchupError("invalid team identity")
            seen.append(tid)
            sides.append({"team_id": tid, "team_name": team["teamName"],
                "points": team.get("currentPoints"),
                "total_points": team.get("totalPoints")})
        winner = row.get("winner")
        if winner not in ("HOME", "AWAY", "TIE", "UNDECIDED"):
            raise WeeklyMatchupError("unsupported outcome")
        output.append({"home": sides[0], "away": sides[1], "winner": winner})
    if sorted(seen) != list(range(1, 13)):
        raise WeeklyMatchupError("each league team must appear exactly once")
    captured = timestamp(capture.get("captured_at"))
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise WeeklyMatchupError("now must have timezone")
    age = (now.astimezone(timezone.utc) - captured).total_seconds()
    if age < 0:
        raise WeeklyMatchupError("capture timestamp in the future")
    if type(slo_seconds) is not int or slo_seconds <= 0:
        raise WeeklyMatchupError("invalid SLO")
    return {"meta": {"provider": "flaim", "platform": "espn",
        "league_id": 1417621, "season_year": 2026, "week": week,
        "captured_at": captured.isoformat(), "age_seconds": int(age),
        "stale": age > slo_seconds, "freshness_slo_seconds": slo_seconds,
        "authority": "PROVIDER_OBSERVATION_NOT_FACT_LOCK",
        "end_to_end_live_certified": False}, "matchups": output}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("capture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = normalize(json.loads(args.capture.read_text()))
    payload = json.dumps(output, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")
