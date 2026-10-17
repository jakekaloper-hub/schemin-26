"""Validate sourced ESPN matchup extracts without guessing champions from scores."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

def validate_extract(doc: dict) -> dict:
    rows = doc["rows"]
    coverage = doc["weeks_queried"]
    problems = []
    if doc.get("season") != 2022 or len(coverage) != 17 or any(not x["success"] for x in coverage):
        problems.append("incomplete 2022 week coverage")
    if len(rows) != sum(w["pairings"] for w in coverage):
        problems.append("weekly row count mismatch")
    weeks = {}
    for row in rows:
        w = row["week"]
        weeks.setdefault(w, []).append(row)
        if row.get("home_team_id") is None:
            problems.append(f"week {w} missing home team")
        if row.get("away_team_id") is None:
            if row.get("winner") != "UNDECIDED":
                problems.append(f"week {w} singleton falsely decided")
        elif row.get("winner") in ("HOME", "AWAY"):
            home, away = row.get("home_points"), row.get("away_points")
            if home is None or away is None or (home > away) != (row["winner"] == "HOME"):
                problems.append(f"week {w} winner/points contradiction")
    title_rows = [x for x in rows if x["week"] == 17 and x.get("tier") == "WINNERS_BRACKET"
                  and x.get("home_team_id") is not None and x.get("away_team_id") is not None]
    if len(title_rows) != 1:
        problems.append("not exactly one fully paired week17 winners-bracket result")
    final = title_rows[0] if len(title_rows) == 1 else None
    semifinal = [x for x in rows if x["week"] == 16 and x.get("tier") == "WINNERS_BRACKET"]
    if len(semifinal) != 2:
        problems.append("2022 semifinal pairing count not two")
    finalists = {final.get("home_team_id"), final.get("away_team_id")} if final else set()
    advancing = {m["home_team_id"] if m["winner"] == "HOME" else m.get("away_team_id") for m in semifinal if m.get("winner") in ("HOME", "AWAY")}
    if finalists != advancing:
        problems.append("finalist IDs inconsistent with semifinal winners")
    return {"valid": not problems, "issues": problems, "season": doc.get("season"), "week_count": len(weeks),
            "record_count": len(rows), "singles": sum(1 for x in rows if x.get("away_team_id") is None),
            "title": {"home_team_id": final["home_team_id"], "away_team_id": final["away_team_id"],
                      "score": [final["home_points"], final["away_points"]],
                      "winner_team_id":final["home_team_id"] if final["winner"] == "HOME" else final["away_team_id"]} if final else None,
            "provenance_limits": ["Raw provider payload SHA is absent", "Historical owner identities not source-proven",
                                   "Singleton records are not H2H wins or losses"]}

if __name__ == "__main__":
    p = Path(__file__).resolve().parents[3] / "living-novel/production/full-rewrite-2026/evidence/G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json"
    print(json.dumps(validate_extract(json.loads(p.read_text())), indent=2))
