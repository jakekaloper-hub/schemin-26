#!/usr/bin/env python3
"""Derive Atlas presentation data without changing or promoting world canon."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
data=ROOT/"world/data"
def load(name):
    return json.loads((data/(name+".json")).read_text(encoding="utf-8"))
locations=load("locations")["locations"]
routes=load("routes")["routes"]
events=load("world_state_events")["events"]
state=load("current_world_state")
ids={x["id"] for x in locations}
assert len(ids)==len(locations)
assert all(isinstance(x.get("abstract_position"),list) and len(x["abstract_position"])==2 for x in locations)
assert all(r["from"] in ids and r["to"] in ids for r in routes)
assert all(e["location_id"] in ids for e in events)
payload={"schema_version":1,"coordinate_space":load("locations").get("coordinate_space"),"state_as_of":state.get("as_of"),
"notices":["Abstract positions are non-metric: no geographic distances or travel times should be inferred.","Historical interpretation is distinguished from world canon.","Current world state may lag more recent weekly storytelling."],
"locations":[{"id":x["id"],"name":x["name"],"position":x["abstract_position"],"zone":x.get("physical_zone_id"),"division":x.get("division_id"),"owner":x.get("owner_character_id"),"canon_status":x.get("canon_status"),"current_state":state.get("locations",{}).get(x["id"],[])} for x in locations],
"routes":[{"id":r["id"],"name":r["name"],"from":r["from"],"to":r["to"],"class":r.get("route_class"),"canon_status":r.get("canon_status"),"travel_modes":r.get("travel_modes",[])} for r in routes],
"events":[{"id":e["id"],"week":e["week"],"location_id":e["location_id"],"type":e["event_type"],"classification":e["classification"],"continuity_out":e.get("continuity_out",[])} for e in events],
"provenance":["world/data/locations.json","world/data/routes.json","world/data/world_state_events.json","world/data/current_world_state.json"]}
(ROOT/"docs/visual/atlas-data.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ATLAS GENERATED",len(locations),"locations",len(routes),"routes",len(events),"events")
