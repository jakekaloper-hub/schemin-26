#!/usr/bin/env python3
"""Source-contract QA for The Road to Seven. No graphic or model-calibration approval.

Run from the repository checkout:
  python3 productions/road-to-seven-2026/tools/verify_source_coverage.py
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
FOLIOS = BASE / "folios"
EVIDENCE = BASE / "evidence"
ISSUES = []


def test(condition, label):
    if not condition:
        ISSUES.append(label)


def load_json(name):
    path = EVIDENCE / name
    test(path.is_file(), "Missing evidence " + name)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run():
    live = load_json("FFHUB_LIVE_W11_2026-11-18_SUMMARY.json")
    forks = load_json("FFHUB_FUTURE_FORKS_2026-11-18.json")
    lineup_path = REPO / "canon/characters/APPROVED_LINEUP_2026_10_18.json"
    test(lineup_path.is_file(), "Approved character lineup JSON not in checkout")
    canon = json.loads(lineup_path.read_text(encoding="utf-8")) if lineup_path.is_file() else {}
    ids = {x["character_id"] for x in canon.get("individuals", [])}
    test(len(ids) == 12, "Expected exactly 12 approved characters")

    players = (EVIDENCE / "FLAIM_CURRENT_ROSTERS_2026-11-18.md").read_text(encoding="utf-8")
    games = (EVIDENCE / "FLAIM_W12_W14_PROVISIONAL_PROJECTIONS.md").read_text(encoding="utf-8")
    market = (EVIDENCE / "NFL_WEEK11_NEWS_AND_MARKET_CONTEXT_2026-11-18.md").read_text(encoding="utf-8")

    test(len(re.findall(r"^## .+ — ESPN team ID \d+$", players, re.M)) == 12,
         "Flaim roster snapshot must contain twelve teams")
    test(len(re.findall(r"^\| (?:Bench|IR|QB|RB|WR|WR/TE|TE|FLEX|D/ST|K|OP|WR/RB|RB/WR) \|", players, re.M)) >= 210,
         "Flaim snapshot does not have complete roster player rows")
    test(len(re.findall(r"^## Week (12|13|14)$", games, re.M)) == 3,
         "Must have 3 future-week projections")
    test(len(re.findall(r"^\| .+ vs .+ \| [0-9.]+ \| [0-9.]+ \| -?[0-9.]+ \|$", games, re.M)) == 18,
         "Must have 18 future-week matchup projections")
    test(market.count("|") >= 100 and "cbssports.com" in market and "2026" in market,
         "Market context missing dated source table")
    teams = live.get("teams", [])
    test(len(teams) == 12 and len({x.get("team") for x in teams}) == 12, "Live Week11 summary not twelve distinct teams")
    test(live.get("source_site", "").startswith("https://theffhub.com/PlayoffTool"), "Missing FFHub source")
    test(len(live.get("sweeps", [])) == 4 and live.get("captured_runs") == 16,
         "Week11 source lacks 12 single-game plus four winout scenarios")
    test(len(forks.get("cases", [])) == 10 and forks.get("run_count") == 20,
         "Week12-14 source lacks 20 conditional results")
    for case in forks.get("cases", []):
        for side in ("a", "b"):
            values = case.get("full_league_" + side, {})
            test(len(values) == 12, "Bad team coverage: " + str(case.get("tag")))
            test(abs(sum(values.values()) - 700) < 0.10, "Bad seven-berth mass: " + str(case.get("tag")))
        test(case.get("week") in (12, 13, 14), "Unexpected future week")

    all_chars = []
    count = 0
    for i in range(1, 8):
        p = FOLIOS / ("RT7-P%02d" % i) / "PAGE_PACKET.md"
        test(p.exists(), "Missing folio " + p.as_posix())
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        count += 1
        chars = set(re.findall(r"CHAR-[A-Z0-9-]+", t)) & ids
        if i == 1:
            test(not chars and "Cover — News" in t, "Cover contains characters or lacks source update")
        else:
            test(len(chars) == 2, "Folio %02d missing two canonical characters" % i)
            all_chars.extend(chars)
            test("Live FFHub revalidation" in t and "Extended production intelligence" in t,
                 "Folio %02d missing live and roster future evidence" % i)
            test("approved crop" in t.lower(), "Folio %02d lacks visual ref binding" % i)
    test(count == 7, "Not exactly seven folios")
    test(len(all_chars) == len(set(all_chars)) == 12, "Twelve character appearances must each be unique")

    print(json.dumps({
        "source_qa": "PASS" if not ISSUES else "FAIL",
        "errors": ISSUES,
        "folio_count": count,
        "canonical_characters": len(set(all_chars)),
        "week11_teams": len(teams),
        "week11_conditional_runs": live.get("captured_runs"),
        "future_conditional_runs": forks.get("run_count"),
        "week12_14_projection_matchups": 18,
        "scope": "SOURCE-CONSISTENCY ONLY — no new live refresh, exact model calibration, pixels, or independent Umpire signoff",
        "independent_visual_gate": "NOT_RUN",
        "final_pngs": "NOT_GENERATED"
    }, indent=2))
    return 0 if not ISSUES else 1


if __name__ == "__main__":
    sys.exit(run())
