#!/usr/bin/env python3
"""Verify the retained Schemin '26 FFHub packet; does not re-simulate odds or certify exact tiebreak solver."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def validate(path, league=1417621, season=2026, week=10):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    err = []
    def check(ok, note):
        if not ok:
            err.append(note)
    check(data.get("schema_version") == "schemin.playoff_scenario_packet.v1", "Schema differs")
    check(data.get("league_id") == league, "League ID differs")
    check(data.get("season") == season, "Season differs")
    check(data.get("through_week") == week, "Completed week differs")
    povs = data.get("team_povs", [])
    names = {v["team"] for v in povs}
    check(len(povs) == len(names) == 12, "Not exactly 12 distinct team POVs")
    check(len(data.get("finalized_standings", [])) == 12, "Standings do not contain 12 teams")
    check(len(data.get("completed_game_ledger", [])) == 6 * week, "Completed game ledger count differs")
    vendor = data.get("vendor_experiment", {})
    runs = vendor.get("runs", [])
    check(len(runs) == vendor.get("scenario_count", -9) + 2, "Missing runs or baselines")
    check(bool(runs) and runs[0].get("name") == "baseline" and runs[-1].get("name") == "baseline_restored",
          "Baseline bookends not preserved")
    for run in runs:
        title = run.get("name", "unnamed")
        totals = run.get("totals", {})
        check(set(totals) == names, title + ": missing or extra teams")
        check(abs(sum(totals.values()) - 700) <= 0.03, title + ": seven-berth mass differs")
        lines = run.get("table", "").splitlines()
        check(len(lines) == 13, title + ": not 12 table rows")
        for line in lines[1:]:
            cells = line.split("\t")
            if len(cells) != 14:
                err.append(title + ": invalid row width")
                continue
            name = cells[0]
            if name not in totals:
                err.append(title + ": unknown name " + name)
                continue
            try:
                seed_odds = [float(v) for v in cells[1:13]]
                total = float(cells[13])
            except ValueError:
                err.append(title + ": nonnumeric row " + name)
                continue
            check(abs(sum(seed_odds) - 100) < 0.06, title + ": seed distribution differs for " + name)
            check(abs(sum(seed_odds[:7]) - total) < 0.06, title + ": playoff total differs for " + name)
            check(abs(total - totals[name]) < 0.021, title + ": table and run totals disagree for " + name)
    if runs:
        for pov in povs:
            name = pov["team"]
            wins = [r for r in runs if len(r.get("fixedResults", [])) == 1
                    and r["fixedResults"][0].get("week") == week + 1
                    and r["fixedResults"][0].get("winner") == name]
            losses = [r for r in runs if len(r.get("fixedResults", [])) == 1
                      and r["fixedResults"][0].get("week") == week + 1
                      and r["fixedResults"][0].get("loser") == name]
            if len(wins) != 1 or len(losses) != 1:
                err.append(name + ": missing unique Week 11 win/loss experiments")
                continue
            for key, expected in [
                ("baseline_pct", runs[0]["totals"][name]),
                ("if_w11_win_pct", wins[0]["totals"][name]),
                ("if_w11_loss_pct", losses[0]["totals"][name]),
            ]:
                check(abs(pov[key] - expected) < 0.011, name + ": POV differs for " + key)
            check(abs((pov["if_w11_win_pct"] - pov["if_w11_loss_pct"])
                      - pov["win_loss_swing_percentage_points"]) < 0.011,
                  name + ": swing arithmetic differs")
            check(pov["mathematically_alive"] and not pov["mathematically_clinched"],
                  name + ": unexpected exact-status assertion")
        check(len(data.get("exact_evidence", {}).get("w11_loss_survival", {})) == 11,
              "Missing Week 11 loss-survival witnesses")
    drift = max((abs(runs[-1]["totals"][n] - runs[0]["totals"][n])
                 for n in names), default=0) if runs else 0
    return {
        "passed": not err, "errors": err, "sha256": hashlib.sha256(raw).hexdigest(),
        "team_count": len(names), "run_count": len(runs),
        "named_scenarios": vendor.get("scenario_count"),
        "restored_baseline_max_abs_pp": round(drift, 2),
        "scope": "Historical evidence consistency only; not a live FFHub rerun or exact tiebreak proof",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", help="Local path to private Schemin FFHub JSON")
    parser.add_argument("--league", type=int, default=1417621)
    parser.add_argument("--season", type=int, default=2026)
    parser.add_argument("--through-week", type=int, default=10)
    args = parser.parse_args()
    try:
        result = validate(args.packet, args.league, args.season, args.through_week)
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        result = {"passed": False, "errors": [str(exc)]}
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
