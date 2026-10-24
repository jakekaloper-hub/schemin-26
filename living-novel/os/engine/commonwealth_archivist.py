#!/usr/bin/env python3
"""Read-only, source-backed Commonwealth archivist index; no canon mutations."""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from pathlib import Path

def build(root: Path) -> dict:
    def load(relative):
        return json.loads((root / relative).read_text(encoding="utf-8"))
    locations = load("world/data/locations.json")["locations"]
    events = load("world/data/world_state_events.json")["events"]
    relations = load("world/data/location_relationship_graph.json")["relationships"]
    ids = {x["id"] for x in locations}
    if len(ids) != len(locations):
        raise ValueError("Duplicate location IDs")
    byloc = defaultdict(list)
    findings = []
    for event in events:
        eid = event.get("id")
        loc = event.get("location_id")
        if loc not in ids:
            findings.append({"severity":"FATAL","code":"ORPHAN_EVENT_LOCATION","event_id":eid,"location_id":loc})
            continue
        if not event.get("source_provenance"):
            findings.append({"severity":"FATAL","code":"UNSOURCED_EVENT","event_id":eid})
        byloc[loc].append({
            "id":eid,"week":event.get("week"),"event_type":event.get("event_type"),
            "classification":event.get("classification"),"continuity_out":event.get("continuity_out",[]),
            "source_provenance":event.get("source_provenance",[]),
            "source_record":"world/data/world_state_events.json"
        })
    for relation in relations:
        for endpoint in ("from","to"):
            identifier=relation.get(endpoint,"")
            if identifier.startswith("LOC-") and identifier not in ids:
                findings.append({"severity":"ERROR","code":"ORPHAN_RELATION_LOCATION","location_id":identifier})
    entries = [{
        "id":loc["id"],"name":loc.get("name"),
        "canon_status":loc.get("canon_status"),"owner_character_id":loc.get("owner_character_id"),
        "physical_zone_id":loc.get("physical_zone_id"),
        "source_provenance":loc.get("source_provenance",[]),
        "source_record":"world/data/locations.json",
        "events":sorted(byloc[loc["id"]],key=lambda x:(x["week"] or 0,x["id"])),
        "open_questions":loc.get("open_questions",[]),
    } for loc in sorted(locations,key=lambda x:x["id"])]
    return {"schema_version":"1.0","status":"DERIVED_READ_ONLY",
            "entries":entries,"findings":findings,
            "counts":{"locations":len(locations),"events":len(events),"relations":len(relations)},
            "caution":"Historical league event completeness is NOT verified by this index. No inferred mythology is accepted canon."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    result=build(args.root)
    payload=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    if any(x["severity"]=="FATAL" for x in result["findings"]):
        raise SystemExit(2)
if __name__=="__main__":
    main()
