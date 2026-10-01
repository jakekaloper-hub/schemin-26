#!/usr/bin/env python3
"""Deterministically compile Universe OS V1.2 world_memory.json from Phase 5 event truth."""
from __future__ import annotations
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"world"/"data"
OUT=DATA/"world_memory.json"

CLASSES=["PERMANENT","RECURRING","HISTORICAL","SEASONAL","TEMPORARY","JOKE_EVENT_ONLY","RUMOR","SUPERSEDED"]

def load(p): return json.loads(Path(p).read_text())
def dump(x): return json.dumps(x,indent=2,ensure_ascii=False)+"\n"

def memory_event(e):
    secondary=[]
    expiry=None
    if e.get("event_type")=="contamination":
        secondary=["TEMPORARY_PHYSICAL_STATE"]
        expiry="explicit cleanup/restoration event for physical residue; history remains"
    return {
      "event_id":e["id"],
      "week":e["week"],
      "era":"2026",
      "source":e.get("source_provenance",[]),
      "participants":[],
      "location":e["location_id"],
      "memory_class":"HISTORICAL",
      "secondary_tags":secondary,
      "physical_effect":e.get("continuity_out",[]),
      "social_effect":[],
      "reputation_effect":[],
      "institutional_effect":[],
      "expiry_condition":expiry,
      "superseded_by":None,
      "current_relevance":True
    }

def compile_memory():
    events=load(DATA/"world_state_events.json")["events"]
    return {"schema_version":"1.0","status":"RELEASE_CANDIDATE","memory_classes":CLASSES,"events":[memory_event(e) for e in events]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--write",action="store_true");ap.add_argument("--check",action="store_true")
    args=ap.parse_args(); expected=dump(compile_memory()); actual=OUT.read_text() if OUT.exists() else None
    if args.write and actual!=expected:
        OUT.write_text(expected); actual=expected
    if args.check:
        if actual!=expected:
            print("WORLD_MEMORY_DRIFT");raise SystemExit(1)
        print(f"world memory clean: {len(compile_memory()['events'])} events")
    if not args.write and not args.check:
        print(expected)

if __name__=="__main__":main()
