#!/usr/bin/env python3
"""Character Director + Librarian lane: full Chronicle derived views."""
from __future__ import annotations
from collections import defaultdict

def _entry(event,summary,classification=None):
    if classification is None:
        classification="FACT" if event["authority"]["evidence_status"]=="VERIFIED" else "NARRATIVE_INTERPRETATION"
    return {
      "event_id":event["event_id"],
      "classification":classification,
      "summary":summary,
      "provenance":list(event["authority"]["source_receipts"]),
    }

def character_timelines(events,source_cutoff):
    chars=defaultdict(list)
    for e in events:
        for p in e["participants"]:
            if p["entity_type"]=="CHARACTER":
                chars[p["entity_id"]].append(_entry(e,f"{p['entity_id']} participated in {e['event_id']}."))
    return {
      cid:{
        "schema_version":"1.0","projection_id":f"CHR-CHAR-{cid}-{source_cutoff}",
        "projection_type":"CHARACTER_TIMELINE","subject_ids":[cid],
        "event_ids":[x["event_id"] for x in rows],"source_cutoff":source_cutoff,
        "entries":rows,"derived_only":True,"rebuildable":True,
      } for cid,rows in chars.items()
    }

def relationship_histories(events,source_cutoff):
    rel=defaultdict(list)
    for e in events:
        chars=sorted(p["entity_id"] for p in e["participants"] if p["entity_type"]=="CHARACTER")
        if len(chars)<2: continue
        for i,a in enumerate(chars):
            for b in chars[i+1:]:
                rel[(a,b)].append(_entry(e,f"{a} and {b} share {e['event_id']}."))
    return {
      f"{a}::{b}":{
        "schema_version":"1.0","projection_id":f"CHR-REL-{a}-{b}-{source_cutoff}",
        "projection_type":"RELATIONSHIP_HISTORY","subject_ids":[a,b],
        "event_ids":[x["event_id"] for x in rows],"source_cutoff":source_cutoff,
        "entries":rows,"derived_only":True,"rebuildable":True,
      } for (a,b),rows in rel.items()
    }

def place_memory(events,scenes,source_cutoff):
    event_by_id={e["event_id"]:e for e in events}
    loc_events=defaultdict(set)
    for s in scenes:
        loc_events[s["location"]["location_id"]].add(s["event_id"])
    out={}
    for loc,eids in loc_events.items():
        rows=[]
        for eid in sorted(eids):
            e=event_by_id[eid]
            rows.append(_entry(e,f"{eid} is represented at {loc}."))
        out[loc]={
          "schema_version":"1.0","projection_id":f"CHR-PLACE-{loc}-{source_cutoff}",
          "projection_type":"PLACE_MEMORY","subject_ids":[loc],
          "event_ids":sorted(eids),"source_cutoff":source_cutoff,
          "entries":rows,"derived_only":True,"rebuildable":True,
        }
    return out

def artifact_custody(events,source_cutoff):
    custody=defaultdict(list)
    for e in events:
        for p in e["participants"]:
            if p["entity_type"]=="ARTIFACT":
                custody[p["entity_id"]].append(_entry(e,f"{p['entity_id']} participates in {e['event_id']}."))
    return {
      aid:{
        "schema_version":"1.0","projection_id":f"CHR-ART-{aid}-{source_cutoff}",
        "projection_type":"ARTIFACT_CUSTODY","subject_ids":[aid],
        "event_ids":[x["event_id"] for x in rows],"source_cutoff":source_cutoff,
        "entries":rows,"derived_only":True,"rebuildable":True,
      } for aid,rows in custody.items()
    }
