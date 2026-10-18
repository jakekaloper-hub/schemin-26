"""Compare archived season-specific roster snapshots without inventing transactions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/"living-novel/production/full-rewrite-2026/evidence"

def build(season: int):
    if season not in range(2018,2026):
        raise ValueError("Only 2018–2025 snapshots source-backed")
    teams=[]
    for segment in (("1_3","4_6","7_9","10_12") if season == 2018 else ("1_6","7_12")):
        doc=json.loads((BASE/f"G01_{season}_ROSTER_SLOTS_{segment}{'' if season == 2018 else '_W1_W14'}.json").read_text())
        for entry in doc["teams"]:
            a,b=entry["snapshots"]
            left={str(p["id"]):p for p in a["players"]}
            right={str(p["id"]):p for p in b["players"]}
            teams.append({"historical_team_id":entry["id"],"week1_name":a.get("team",a.get("name")),
              "week14_name":b.get("team",b.get("name")),
              "week1_count":len(left),"week14_count":len(right),
              "appeared_ids":sorted(right.keys()-left.keys()),
              "departed_ids":sorted(left.keys()-right.keys()),
              "retained_count":len(left.keys()&right.keys()),
              "transaction_type":"UNKNOWN_UNVERIFIED",
              "season_division":"UNKNOWN_UNLESS_SEASON_SOURCE_PROVIDED"})
    return {"season":season,"source":"Flaim ESPN historical weekly roster snapshots",
      "provenance":"season-scoped provider team IDs, not verified actual human owner identity",
      "teams":sorted(teams,key=lambda t:t["historical_team_id"])}
if __name__=="__main__":
    import sys
    print(json.dumps(build(int(sys.argv[1]) if len(sys.argv)>1 else 2025),indent=2))
