#!/usr/bin/env python3
"""Validate and normalize Flaim fantasy-league evidence receipts.

Flaim is an authorized read-only provider adapter. It is not the Schemin
source of truth by itself. Schemin validates the captured provider evidence,
preserves provenance/limitations, and recomputes freshness at read time.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_LEAGUE_ID = "1417621"
EXPECTED_SEASON = 2026
EXPECTED_TEAMS = 12


class FlaimContractError(ValueError):
    pass


def _parse_iso(value: str) -> datetime:
    if not value:
        raise FlaimContractError("captured_at missing")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def snapshot_age_seconds(captured_at: str, now: datetime | None = None) -> int:
    captured = _parse_iso(captured_at)
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return max(0, int((current.astimezone(timezone.utc) - captured).total_seconds()))


def validate_capture(data: dict[str, Any]) -> None:
    errors: list[str] = []

    if data.get("provider") != "flaim":
        errors.append("provider must be flaim")
    if data.get("upstream_platform") != "espn":
        errors.append("upstream_platform must be espn")

    league = data.get("league") or {}
    if str(league.get("league_id")) != EXPECTED_LEAGUE_ID:
        errors.append("wrong league id")
    if int(league.get("season", 0)) != EXPECTED_SEASON:
        errors.append("wrong season")
    if int(league.get("team_count", 0)) != EXPECTED_TEAMS:
        errors.append("expected 12 teams")

    teams = league.get("teams") or []
    if len(teams) != EXPECTED_TEAMS:
        errors.append("league teams must contain 12 rows")
    team_ids = [str(t.get("team_id")) for t in teams]
    if len(team_ids) != len(set(team_ids)):
        errors.append("duplicate league team ids")
    if any(not str(t.get("team_name", "")).strip() for t in teams):
        errors.append("empty league team name")

    standings = data.get("standings") or []
    if len(standings) != EXPECTED_TEAMS:
        errors.append("standings must contain 12 rows")
    standing_ids = {str(s.get("team_id")) for s in standings}
    if set(team_ids) != standing_ids:
        errors.append("standings team set does not match league team set")

    matchups = data.get("week4_matchups") or []
    if len(matchups) != 6:
        errors.append("Week 4 must contain exactly 6 matchups")
    matchup_ids: list[str] = []
    for matchup in matchups:
        home = str((matchup.get("home") or {}).get("team_id"))
        away = str((matchup.get("away") or {}).get("team_id"))
        if home == away:
            errors.append("matchup cannot contain same team twice")
        matchup_ids.extend([home, away])
    if sorted(matchup_ids) != sorted(team_ids):
        errors.append("Week 4 matchup team set must contain each team exactly once")

    rosters = data.get("rosters") or []
    if len(rosters) != EXPECTED_TEAMS:
        errors.append("rosters must contain 12 team snapshots")
    roster_ids = {str(r.get("team_id")) for r in rosters}
    if roster_ids != set(team_ids):
        errors.append("roster team set does not match league team set")
    for roster in rosters:
        if (roster.get("snapshot") or {}).get("type") != "current":
            errors.append(f"roster {roster.get('team_id')} is not current snapshot")
        if not roster.get("players"):
            errors.append(f"roster {roster.get('team_id')} has no players")

    transactions = data.get("transactions") or {}
    rows = transactions.get("rows") or []
    if int(transactions.get("count", -1)) != len(rows):
        errors.append("transaction count does not equal row count")
    if transactions.get("source") not in {
        "mTransactions2",
        "mTransactions2_with_activity_trade_details",
        "activity_feed",
    }:
        errors.append("unknown ESPN transaction source")

    _parse_iso(str(data.get("captured_at", "")))

    if errors:
        raise FlaimContractError("; ".join(errors))


def normalize_capture(
    data: dict[str, Any],
    *,
    now: datetime | None = None,
    slo_seconds: int = 3600,
) -> dict[str, Any]:
    validate_capture(data)
    age = snapshot_age_seconds(data["captured_at"], now=now)
    transactions = data["transactions"]

    return {
        "meta": {
            "league_id": int(data["league"]["league_id"]),
            "season": int(data["league"]["season"]),
            "source": "flaim-espn-adapter",
            "captured_at": data["captured_at"],
            "snapshot_age_seconds": age,
            "stale": age > slo_seconds,
            "freshness_slo_seconds": slo_seconds,
            "failure_reason": None,
            "provider_limitations": data.get("limitations", []),
        },
        "league": data["league"],
        "standings": data["standings"],
        "matchups": data["week4_matchups"],
        "rosters": data["rosters"],
        "transactions": {
            **transactions,
            "exact_trade_assets_complete": not bool(
                (transactions.get("limitations") or {}).get(
                    "structured_details_incomplete"
                )
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("capture", type=Path)
    parser.add_argument("--slo-seconds", type=int, default=3600)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.capture.read_text())
    normalized = normalize_capture(data, slo_seconds=args.slo_seconds)
    payload = json.dumps(normalized, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
