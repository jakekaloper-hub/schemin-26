#!/usr/bin/env python3
"""Build source-bounded twelve-owner After Dark editorial docket. NOT a canon state update."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/"productions/after-dark/fixtures/p3c_twelve_character_context.json"
data=json.loads(source.read_text())
cards=[]
for c in sorted(data["characters"],key=lambda x:x["team_id"]):
    series=c["historical_franchise_team_id_record"]["seasons"]
    prev,cur=series[-2:]
    best=max(series[:-1],key=lambda x:(x["wins"]/(x["wins"]+x["losses"] or 1),x["wins"]))
    trend="IMPROVING" if cur["wins"]/(cur["wins"]+cur["losses"])>prev["wins"]/(prev["wins"]+prev["losses"]) else "DECLINING" if cur["wins"]/(cur["wins"]+cur["losses"])<prev["wins"]/(prev["wins"]+prev["losses"]) else "LEVEL"
    cards.append({"character_id":c["character_id"],"team_id":c["team_id"],"team":c["team_name"],"home":c["canonical_home"]["name"],"historical_high":{"year":best["season_year"],"record":f'{best["wins"]}-{best["losses"]}',"team_name_then":best["team_name"]},"previous_season":{"year":prev["season_year"],"record":f'{prev["wins"]}-{prev["losses"]}'},"current_through_week_7":{"year":cur["season_year"],"record":f'{cur["wins"]}-{cur["losses"]}'},"winning_percentage_direction":trend,"editorial_tension":f'How did the franchise move from {prev["wins"]}-{prev["losses"]} last season to {cur["wins"]}-{cur["losses"]} through Week 7, against its {best["season_year"]} high of {best["wins"]}-{best["losses"]}?',"guest_appearance":"HOLD_ROUTE_AND_STORY_TIME","current_physical_whereabouts":"UNKNOWN","provenance":["p3c_twelve_character_context.json","p3c_historical_standings_2015_2026.json"],"canon_status":"DERIVED_EDITORIAL_ONLY"})
assert len(cards)==12
out=ROOT/"productions/after-dark/fixtures/p3c_twelve_story_docket.json"
out.write_text(json.dumps({"status":"DERIVED_EDITORIAL_ONLY","as_of":"2026-10-28","note":"Past and current ESPN team-ID records do not independently prove owner tenure or current real-world movements.","cards":cards},indent=2)+"\n")
print("Generated",len(cards),"twelve-team story cards")
