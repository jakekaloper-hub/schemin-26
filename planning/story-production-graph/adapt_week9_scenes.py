#!/usr/bin/env python3
"""Beat Writer + Architect lane: adapt Week 9 storyboard beats into Scene V1 objects.

Read-only translation. Existing Week 9 cards remain source authority.
No scene emitted here may promote fact, character, world or publication state.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WEEK=ROOT/"memo-os/week-9"
CARDS=WEEK/"WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json"

ROLE_BY_INDEX={0:"SETUP",1:"ESCALATION",2:"RESOLUTION",3:"EPILOGUE"}

def load_cards():
    return json.loads(CARDS.read_text())

def page_groups(card):
    groups=defaultdict(list)
    for beat in card["written_storyboard_sequence"]["beats"]:
        groups[beat["page_id"]].append(beat)
    return groups

def ordered_pages(card):
    active=card["written_storyboard_sequence"].get("active_reading_pages",[])
    groups=page_groups(card)
    return [p for p in active if p in groups] + [p for p in groups if p not in active]

def scene_role(page_index, page_count):
    if page_index == 0: return "SETUP"
    if page_index == page_count-1: return "RESOLUTION"
    if page_index == 1: return "ESCALATION"
    return "TURN"

def branch_for_beats(beats):
    branches={b["branch"] for b in beats}
    if branches=={"COMMON"}: return "COMMON"
    if "HOME_WIN" in branches and "AWAY_WIN" in branches: return "COMMON"
    if len(branches)==1: return next(iter(branches))
    return "COMMON"

def scene_from(card,page_id,beats,index,total):
    seq=card["written_storyboard_sequence"]
    actions=[b["pose_and_physical_action"] for b in beats]
    changes=[b["what_changes"] for b in beats]
    transitions=[b["transition"] for b in beats]
    views=[b.get("shot","") for b in beats if b.get("shot")]
    branch=branch_for_beats(beats)
    role=scene_role(index,total)
    event_id=f"EVT-W09-{card['id']}"
    deps=[
      f"{event_id}::BASE",
      card["id"], page_id,
      "memo-os/week-9/WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json",
      f"CHAR::{card['home']['characterId']}",
      f"CHAR::{card['away']['characterId']}",
      f"LOC::{card['venue_parent']}",
    ]
    if role=="RESOLUTION" or any(b["branch"] in {"HOME_WIN","AWAY_WIN"} for b in beats):
        deps.append(f"{event_id}::RESULT")
    return {
      "schema_version":"1.0",
      "scene_id":f"SCN-{card['id']}-{page_id}",
      "event_id":event_id,
      "encounter_id":f"ENC-{card['id']}",
      "scene_role":role,
      "branch":branch,
      "authority":{
        "character_authority":"active Character Canon authority at build time",
        "world_authority":"World Engine/Atlas active authority at build time",
        "source_receipts":[
          "memo-os/week-9/WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json",
          card["reference_binding_file"]
        ],
      },
      "cast":[
        {"character_id":card["home"]["characterId"],"role":"PRIMARY","reference_receipts":[]},
        {"character_id":card["away"]["characterId"],"role":"PRIMARY","reference_receipts":[]},
      ],
      "location":{
        "location_id":card["venue_parent"],
        "entering_state_receipt":card["reference_binding_file"],
        "persistent_anchors":list(seq["persistent_scene_anchors"]),
      },
      "continuity":{
        "in":[seq["ground_plan"]] if index==0 else [f"prior scene in {card['id']}"],
        "out":changes+transitions,
      },
      "narrative":{
        "objective":card["story_engine"]["mechanism"],
        "emotional_objective":seq["emotional_spine"],
        "action_beats":actions,
        "dialogue":[],
      },
      "visual":{
        "camera":" | ".join(views),
        "blocking":actions,
        "foreground":[],
        "midground":[],
        "background":list(seq["persistent_scene_anchors"]),
        "lighting":"",
        "weather":"",
        "time_of_day":"",
      },
      "state_delta":{
        "persistent":[],
        "ephemeral":changes,
      },
      "dependencies":deps,
      "outputs":["PNG","MOTION","WEB","NOVEL_CONTEXT"],
      "qa":{
        "required_gates":["FACT","CHARACTER","WORLD","COMPOSITION","PUBLICATION"],
        "publication_state":"PLANNED",
        "revision":1,
      },
      "source_mapping":{
        "source_beat_ids":[b["beat_id"] for b in beats],
        "source_classifications":sorted({b["classification"] for b in beats}),
        "branch_variants":sorted({b["branch"] for b in beats}),
      }
    }

def compile_scenes():
    data=load_cards()
    out=[]
    for card in data["cards"]:
        pages=ordered_pages(card)
        groups=page_groups(card)
        for i,pid in enumerate(pages):
            out.append(scene_from(card,pid,groups[pid],i,len(pages)))
    return out

if __name__=="__main__":
    print(json.dumps({"scenes":compile_scenes()},indent=2,ensure_ascii=False))
