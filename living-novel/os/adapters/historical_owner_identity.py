"""Period-scoped owner evidence; historical ESPN slot/name never proves owner identity."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
def season_slot_evidence(year):
    if not isinstance(year,int) or year not in range(2015,2027): raise ValueError("invalid season")
    if year==2026:
        owner=json.loads((ROOT/"world/data/owner_domains.json").read_text())
        return [{"season":year,"team_id":d["team_id"],"team_name":d["team"],
          "owner":d["owner"],"character_id":d["character_id"],
          "identity_status":"VERIFIED_CURRENT_SEASON_CANON",
          "source":"world/data/owner_domains.json"} for d in owner["domains"]]
    if year==2022:
        doc=json.loads((BASE/"G01_2022_FLAIM_WEEK_BY_WEEK_MATCHUP_EXTRACT.json").read_text())
        rows=doc["rows"]
        # This archive is a matchup extract, not a proof of historical human ownership.
        slots={int(i) for row in rows for i in [row.get("home_team_id"),row.get("away_team_id")] if i is not None}
        return [{"season":year,"team_id":id,"owner":None,"character_id":None,
            "identity_status":"UNKNOWN_HISTORICAL_OWNER","source":"living-novel/history/OWNER_LINEAGE.md"} for id in sorted(slots)]
    doc=json.loads((BASE/f"G01_{year}_FULL_WEEKLY_MATCHUPS.json").read_text())
    vals={}
    for w in doc["weeks"]:
        for g in w["matchups"]:
            for side in ("home","away"):
                id=g.get(f"{side}_id")
                if id is not None:vals[int(id)]=g.get(side)
    # Historical names without ID, especially 2017, cannot be guessed into slot joins.
    return [{"season":year,"team_id":id,"team_name":name,"owner":None,"character_id":None,
            "identity_status":"UNKNOWN_HISTORICAL_OWNER","source":f"living-novel/production/full-rewrite-2026/evidence/G01_{year}_FULL_WEEKLY_MATCHUPS.json"} for id,name in sorted(vals.items())]
