#!/usr/bin/env python3
"""Derive all-12 Week 7/8 editorial context from dated provisional Memo intake."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
load=lambda p:json.loads((ROOT/p).read_text())
base=load("productions/after-dark/fixtures/p3c_twelve_story_docket.json")
e=load("memo-os/week-7/WEEK_7_PROVIDER_NORMALIZED_EVIDENCE_2026-10-27.json")
assert e["validation_status"]=="PRELIMINARY_NOT_INDEPENDENTLY_PASSED"
cards=[]
for card in base["cards"]:
 t=card["team_id"]
 def matchup(key):
  for m in e[key]["matchups"]:
   h,a=m["home"],m["away"]
   if t in (h["teamId"],a["teamId"]):
    own=h if h["teamId"]==t else a
    opp=a if own is h else h
    return {"opponent_id":opp["teamId"],"opponent_name":opp["teamName"].strip(),"home_away":"HOME" if own is h else "AWAY","own_points":own["totalPoints"],"opponent_points":opp["totalPoints"],"result":"WIN" if (m["winner"]=="HOME" and own is h) or (m["winner"]=="AWAY" and own is a) else "LOSS" if m["winner"]!="UNDECIDED" else "UNDECIDED"}
  raise ValueError(t)
 card={**card,"week7_reported":matchup("w7_matchups"),"week8_preview":matchup("week8_schedule_preview"),
 "intelligence_class":"PROVISIONAL_PROVIDER_NORMALIZED_NOT_FACT_LOCK",
 "novel_continuity":{"approval":"UNRESOLVED","note":"Approved Novel manuscript anchor and effective cutoff require direct canonical resolution. No fictional character movements inferred."},
 "last_known_week7_location":"UNKNOWN",
 "week8_story_hypothesis":"PENDING_AUTHORIZED_WRITERS_ROOM",
 "additional_sources":["memo-os/week-7/WEEK_7_PROVIDER_NORMALIZED_EVIDENCE_2026-10-27.json"]}
 cards.append(card)
assert len(cards)==12 and {c["team_id"] for c in cards}==set(range(1,13))
out=ROOT/"productions/after-dark/fixtures/p3c_week7_week8_editorial_cards.json"
out.write_text(json.dumps({"status":"PROVISIONAL_NOT_FACT_LOCKED","as_of":"2026-10-27","cards":cards},indent=2)+"\n")
print("Enriched",len(cards),"Week7/8 cards; no canon approvals")
