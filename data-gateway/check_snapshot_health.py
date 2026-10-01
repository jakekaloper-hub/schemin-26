#!/usr/bin/env python3
import json
import os
import pathlib

from refresh_espn_snapshot import refresh_freshness_for_read

LEAGUE_ID = os.getenv("LEAGUE_ID", "1417621")
DEFAULT_PATH = pathlib.Path("data/snapshots") / LEAGUE_ID / "latest.json"
SNAPSHOT_PATH = pathlib.Path(os.getenv("SCHEMIN_SNAPSHOT_PATH", str(DEFAULT_PATH)))
MAX_STALE_SECONDS = float(os.getenv("SCHEMIN_MAX_STALE_SECONDS", "86400"))


def evaluate_snapshot(path=SNAPSHOT_PATH, max_stale_seconds=MAX_STALE_SECONDS, now=None):
    if not path.exists():
        return {
            "state": "RED_UNAVAILABLE",
            "snapshot_path": str(path),
            "reason": "NO_VALIDATED_SNAPSHOT",
        }, 2

    envelope = json.loads(path.read_text())
    hydrated = refresh_freshness_for_read(
        envelope,
        now=now,
        max_stale_seconds=max_stale_seconds,
    )
    meta = hydrated.get("meta", {})
    if meta.get("stale"):
        state = "YELLOW_DEGRADED"
        code = 1
    else:
        state = "GREEN_LIVE"
        code = 0

    return {
        "state": state,
        "snapshot_path": str(path),
        "meta": meta,
    }, code


def main():
    result, code = evaluate_snapshot()
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
