#!/usr/bin/env python3
"""Adapt existing Week 9 matchup authority into Story Production Graph objects.

This is a read-only adapter. It does not rewrite Week 9 source files and it does
not promote provisional sports evidence. If the Sports Desk packet remains on
HOLD, emitted events remain PROVISIONAL/BRANCHABLE even when scores are present.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WEEK=ROOT/"memo-os/week-9"
CARDS=WEEK/"WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json"
SPORTS=WEEK/"WEEK_9_FINAL_SPORTS_DESK_EVIDENCE_2026-11-10.json"

def load():
    return json.loads(CARDS.read_text()), json.loads(SPORTS.read_text())

def pair_key(home_id, away_id):
    return f"{home_id}:{away_id}"

def sports_index(sports):
    return {m["pair"]:m for m in sports["matchups"]}

def event_from(card, sports, release_accepted=False):
    sm=sports_index(sports)[pair_key(card["home"]["teamId"],card["away"]["teamId"])]
    verified=bool(sports.get("validations",{}).get("starter_sum_matches_week9_summary"))
    source_hold=sports.get("data_release_status")!="RELEASED"
    evidence_status="VERIFIED" if verified and not source_hold and release_accepted else "PROVISIONAL"
    canon_status="ACCEPTED" if evidence_status=="VERIFIED" else "BRANCHABLE"
    winner_side=sm["winner"]
    winner=sm["home"]["teamName"] if winner_side=="HOME" else sm["away"]["teamName"]
    branch="HOME_WIN" if winner_side=="HOME" else "AWAY_WIN"
    return {
      "schema_version":"1.0",
      "event_id":f"EVT-W09-{card['id']}",
      "event_type":"MATCHUP",
      "league_time":{"season":2026,"week":9,"occurred_at":None},
      "authority":{
        "evidence_status":evidence_status,
        "source_receipts":[
          "memo-os/week-9/WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json",
          "memo-os/week-9/WEEK_9_FINAL_SPORTS_DESK_EVIDENCE_2026-11-10.json"
        ],
        "canon_status":canon_status,
      },
      "participants":[
        {"entity_type":"CHARACTER","entity_id":card["home"]["characterId"]},
        {"entity_type":"CHARACTER","entity_id":card["away"]["characterId"]},
        {"entity_type":"LOCATION","entity_id":card["venue_parent"]},
      ],
      "result":{
        "home_team_id":sm["home"]["teamId"],"home_name":sm["home"]["teamName"],"home_score":sm["home"]["points"],
        "away_team_id":sm["away"]["teamId"],"away_name":sm["away"]["teamName"],"away_score":sm["away"]["points"],
        "winner_side":winner_side,"winner":winner,"selected_branch":branch,
      },
      "state":{
        "branch_state":branch if canon_status!="ACCEPTED" else "SETTLED",
        "knowledge_cutoff":"2026-W09-sports-desk-2026-11-10",
        "world_writeback_allowed":False,
      },
      "dependencies":[card["id"],card["reference_binding_file"],sports["run_id"]],
      "notes":[
        f"Sports Desk source_status={sports.get('source_status')}",
        f"Sports Desk data_release_status={sports.get('data_release_status')}",
        "Score/result may be represented while authority remains branchable; no canon promotion is implied."
      ],
    }

def encounter_from(card,event):
    seq=card["written_storyboard_sequence"]
    scene_ids=[]
    for page_id in seq["active_reading_pages"]:
        scene_ids.append(f"SCN-{card['id']}-{page_id}")
    return {
      "schema_version":"1.0",
      "encounter_id":f"ENC-{card['id']}",
      "event_id":event["event_id"],
      "authority":{
        "source_receipts":[
          "memo-os/week-9/WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json",
          card["reference_binding_file"]
        ],
        "world_authority":"World Engine/Atlas active authority at build time",
        "character_authority":"active Character Canon authority at build time",
      },
      "participants":[card["home"]["characterId"],card["away"]["characterId"]],
      "location":{"location_id":card["venue_parent"],"entering_state_receipt":card["reference_binding_file"]},
      "persistent_scene_anchors":list(seq["persistent_scene_anchors"]),
      "shared_conditions":{},
      "scene_ids":scene_ids,
      "branch_policy":{"supports_outcome_branches":True,"settled_branch":event["result"]["selected_branch"]},
      "notes":[seq["ground_plan"],seq["emotional_spine"]],
    }

def compile_week9(release_accepted=False):
    cards,sports=load()
    events=[];encounters=[]
    for card in cards["cards"]:
        ev=event_from(card,sports,release_accepted=release_accepted)
        events.append(ev)
        encounters.append(encounter_from(card,ev))
    return {
      "source":{
        "cards":str(CARDS.relative_to(ROOT)),
        "sports":str(SPORTS.relative_to(ROOT)),
        "sports_data_release_status":sports.get("data_release_status"),
      },
      "events":events,
      "encounters":encounters,
    }

if __name__=="__main__":
    print(json.dumps(compile_week9(release_accepted=False),indent=2,ensure_ascii=False))
