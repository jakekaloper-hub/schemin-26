#!/usr/bin/env python3
import copy
import json
import os
import pathlib
import time
import urllib.request
from datetime import datetime, timezone

LEAGUE_ID = os.getenv("LEAGUE_ID", "1417621")
SEASON = os.getenv("SEASON", "2026")
EXPECTED_TEAMS = 12
BASE = (
    "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/"
    f"seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
)
URL = BASE + "?view=mTeam&view=mRoster&view=mMatchup&view=mSettings&view=mStatus"


def _parse_timestamp(value):
    if not value:
        raise ValueError("fetched_at missing")
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _coerce_now(now=None):
    if now is None:
        return datetime.now(timezone.utc)
    return _parse_timestamp(now)


def compute_snapshot_age_seconds(fetched_at, now=None):
    fetched = _parse_timestamp(fetched_at)
    current = _coerce_now(now)
    return max(0.0, (current - fetched).total_seconds())


def configured_roster_capacity(data):
    settings = data.get("settings") or {}
    roster_settings = settings.get("rosterSettings") or settings.get("roster") or {}
    counts = roster_settings.get("lineupSlotCounts")
    if not isinstance(counts, dict) or not counts:
        raise ValueError("settings.rosterSettings.lineupSlotCounts missing")
    try:
        capacity = sum(int(value) for value in counts.values())
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid lineup slot counts") from exc
    if capacity <= 0:
        raise ValueError("configured roster capacity must be positive")
    return capacity


def validate(data):
    if str(data.get("id")) != LEAGUE_ID:
        raise ValueError("wrong league id")
    teams = data.get("teams")
    if not isinstance(teams, list) or len(teams) != EXPECTED_TEAMS:
        raise ValueError(f"expected {EXPECTED_TEAMS} teams")
    schedule = data.get("schedule")
    if not isinstance(schedule, list) or not schedule:
        raise ValueError("schedule missing or empty")
    if not isinstance(data.get("settings"), dict):
        raise ValueError("settings missing or invalid")
    if not isinstance(data.get("status"), dict):
        raise ValueError("status missing or invalid")

    team_ids = [str(team.get("id")) for team in teams]
    if any(team_id in ("None", "") for team_id in team_ids):
        raise ValueError("team id missing")
    if len(set(team_ids)) != EXPECTED_TEAMS:
        raise ValueError("duplicate team ids")

    capacity = configured_roster_capacity(data)
    roster_counts = []
    for team in teams:
        roster = team.get("roster")
        entries = roster.get("entries") if isinstance(roster, dict) else None
        if not isinstance(entries, list):
            raise ValueError(f"team {team.get('id', '?')} roster entries missing")
        count = len(entries)
        if count <= 0:
            raise ValueError(f"team {team.get('id', '?')} roster empty")
        if count > capacity:
            raise ValueError(
                f"team {team.get('id', '?')} roster exceeds configured capacity "
                f"({count}>{capacity})"
            )
        roster_counts.append(count)

    return {
        "team_count": EXPECTED_TEAMS,
        "configured_roster_capacity": capacity,
        "roster_entry_counts": roster_counts,
    }


def build_envelope(data, fetched_at, validation=None):
    return {
        "meta": {
            "league_id": int(LEAGUE_ID),
            "season": int(SEASON),
            "source": "espn-lm-api-reads",
            "fetched_at": fetched_at,
            "last_refresh_attempt_at": fetched_at,
            "snapshot_age_seconds": 0,
            "stale": False,
            "failure_reason": None,
            "validation": validation or {},
        },
        "data": data,
    }


def refresh_freshness_for_read(envelope, now=None, max_stale_seconds=None):
    hydrated = copy.deepcopy(envelope)
    meta = hydrated.setdefault("meta", {})
    age = compute_snapshot_age_seconds(meta.get("fetched_at"), now=now)
    stored_age = meta.get("snapshot_age_seconds")
    if isinstance(stored_age, (int, float)):
        age = max(age, float(stored_age))
    meta["snapshot_age_seconds"] = age

    if max_stale_seconds is not None and age > float(max_stale_seconds):
        meta["stale"] = True
        if not meta.get("failure_reason"):
            meta["failure_reason"] = "SNAPSHOT_AGE_EXCEEDED_SLO"
    return hydrated


def _atomic_write_text(path, text):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def write_snapshot(envelope, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(out_dir / "latest.json", json.dumps(envelope, separators=(",", ":")))
    _atomic_write_text(out_dir / "manifest.json", json.dumps(envelope["meta"], indent=2))


def mark_last_good_stale(out_dir, failure_reason, now=None):
    latest = out_dir / "latest.json"
    if not latest.exists():
        return False

    envelope = json.loads(latest.read_text())
    current = _coerce_now(now)
    hydrated = refresh_freshness_for_read(envelope, now=current)
    meta = hydrated.setdefault("meta", {})
    meta["stale"] = True
    meta["failure_reason"] = str(failure_reason)
    meta["last_refresh_attempt_at"] = current.isoformat()
    write_snapshot(hydrated, out_dir)
    return True


def main():
    out_dir = pathlib.Path("data/snapshots") / LEAGUE_ID
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                URL,
                headers={
                    "User-Agent": "Schemin26DataGateway/1.0",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.load(response)
            validation = validate(data)
            now = datetime.now(timezone.utc).isoformat()
            envelope = build_envelope(data, now, validation=validation)
            write_snapshot(envelope, out_dir)
            print("Validated ESPN snapshot", now)
            return 0
        except Exception as exc:
            last = str(exc)
            print("attempt failed:", last)
            if attempt < 3:
                time.sleep(2**attempt)

    marked = mark_last_good_stale(out_dir, last)
    if marked:
        print("Marked last-known-good snapshot stale:", last)
    raise SystemExit("ESPN refresh failed: " + str(last))


if __name__ == "__main__":
    raise SystemExit(main())
