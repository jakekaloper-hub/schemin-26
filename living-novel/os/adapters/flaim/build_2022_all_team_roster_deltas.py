"""Read-only roster-delta synthesis from archived 2022 team snapshots."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/"living-novel/production/full-rewrite-2026/evidence"
def build():
 teams=[]
 for segment in ("1_6","7_12"):
  doc=json.loads((BASE/f"G01_2022_ROSTER_SLOTS_{segment}_W1_W14.json").read_text())
  for t in doc["teams"]:
   a,b=t["snapshots"]
   before={str(p["id"]):p for p in a["players"]}
   after={str(p["id"]):p for p in b["players"]}
   teams.append({"historical_team_id":t["id"],"team_name_week1":a["name"],
                 "week1_count":len(before),"week14_count":len(after),
                 "arrivals_observed":[after[k]["name"] for k in sorted(after.keys()-before.keys())],
                 "departures_observed":[before[k]["name"] for k in sorted(before.keys()-after.keys())],
                 "lineup_slot_changes":[{"name":before[k]["name"],"from":before[k]["slot"],"to":after[k]["slot"]}
                    for k in sorted(before.keys()&after.keys()) if before[k]["slot"]!=after[k]["slot"]],
                 "transaction_cause":"UNKNOWN"})
 return {"season":2022,"source":"Flaim ESPN historical roster week 1 versus week 14",
         "statement":"Observed differences, NOT proven trades, waivers, injuries, or motives",
         "teams":sorted(teams,key=lambda t:t["historical_team_id"])}
if __name__=="__main__":print(json.dumps(build(),indent=2,ensure_ascii=False))
