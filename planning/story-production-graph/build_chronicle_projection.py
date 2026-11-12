#!/usr/bin/env python3
"""Rebuildable Chronicle projection helpers.

Chronicle projections are read models only. They never promote canon and can
always be deleted/recomputed from accepted event records.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable

def character_timeline(events: Iterable[dict], character_id: str, source_cutoff: str) -> dict:
    rows=[]
    for event in events:
        participant_ids={p["entity_id"] for p in event.get("participants",[])}
        if character_id not in participant_ids:
            continue
        rows.append({
            "event_id":event["event_id"],
            "classification":"FACT" if event["authority"]["evidence_status"]=="VERIFIED" else "NARRATIVE_INTERPRETATION",
            "summary":event_summary(event),
            "provenance":list(event["authority"]["source_receipts"]),
        })
    return {
      "schema_version":"1.0",
      "projection_id":f"CHR-CHAR-{character_id}-{source_cutoff}",
      "projection_type":"CHARACTER_TIMELINE",
      "subject_ids":[character_id],
      "event_ids":[r["event_id"] for r in rows],
      "source_cutoff":source_cutoff,
      "entries":rows,
      "derived_only":True,
      "rebuildable":True,
    }

def relationship_history(events: Iterable[dict], a: str, b: str, source_cutoff: str) -> dict:
    rows=[]
    for event in events:
        participant_ids={p["entity_id"] for p in event.get("participants",[])}
        if {a,b}.issubset(participant_ids):
            rows.append({
              "event_id":event["event_id"],
              "classification":"FACT" if event["authority"]["evidence_status"]=="VERIFIED" else "NARRATIVE_INTERPRETATION",
              "summary":event_summary(event),
              "provenance":list(event["authority"]["source_receipts"]),
            })
    return {
      "schema_version":"1.0","projection_id":f"CHR-REL-{a}-{b}-{source_cutoff}",
      "projection_type":"RELATIONSHIP_HISTORY","subject_ids":[a,b],
      "event_ids":[r["event_id"] for r in rows],"source_cutoff":source_cutoff,
      "entries":rows,"derived_only":True,"rebuildable":True,
    }

def event_summary(event: dict) -> str:
    result=event.get("result") or {}
    winner=result.get("winner")
    hs=result.get("home_score"); as_=result.get("away_score")
    if winner and hs is not None and as_ is not None:
        return f"{winner} won {hs}–{as_} in {event['event_id']}."
    return f"{event['event_type']} recorded as {event['event_id']}."

def index_events_by_location(events: Iterable[dict], scenes: Iterable[dict]) -> dict[str,list[str]]:
    event_for_scene={s["scene_id"]:s["event_id"] for s in scenes}
    out=defaultdict(list)
    for s in scenes:
        loc=s["location"]["location_id"]
        eid=event_for_scene[s["scene_id"]]
        if eid not in out[loc]:
            out[loc].append(eid)
    return dict(out)
