#!/usr/bin/env python3
import json
import os
import pathlib
import time
import urllib.request
from datetime import datetime, timezone

LEAGUE_ID = os.getenv("LEAGUE_ID", "1417621")
SEASON = os.getenv("SEASON", "2026")
BASE = (
    "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/"
    f"seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
)
URL = BASE + "?view=mTeam&view=mRoster&view=mMatchup&view=mSettings&view=mStatus"


def validate(data):
    if str(data.get("id")) != LEAGUE_ID:
        raise ValueError("wrong league id")
    if len(data.get("teams", [])) != 12:
        raise ValueError("expected 12 teams")
    for key in ("schedule", "settings", "status"):
        if key not in data:
            raise ValueError(key + " missing")


def build_envelope(data, fetched_at):
    return {
        "meta": {
            "league_id": int(LEAGUE_ID),
            "season": int(SEASON),
            "source": "espn-lm-api-reads",
            "fetched_at": fetched_at,
            "snapshot_age_seconds": 0,
            "stale": False,
            "failure_reason": None,
        },
        "data": data,
    }


def write_snapshot(envelope, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / "latest.json.tmp"
    tmp.write_text(json.dumps(envelope, separators=(",", ":")))
    tmp.replace(out_dir / "latest.json")
    (out_dir / "manifest.json").write_text(json.dumps(envelope["meta"], indent=2))


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
            validate(data)
            now = datetime.now(timezone.utc).isoformat()
            envelope = build_envelope(data, now)
            write_snapshot(envelope, out_dir)
            print("Validated ESPN snapshot", now)
            return 0
        except Exception as exc:
            last = str(exc)
            print("attempt failed:", last)
            if attempt < 3:
                time.sleep(2**attempt)
    raise SystemExit("ESPN refresh failed: " + str(last))


if __name__ == "__main__":
    raise SystemExit(main())
