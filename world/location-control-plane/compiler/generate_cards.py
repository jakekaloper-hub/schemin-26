#!/usr/bin/env python3
"""Deterministically compile Phase 2 Homeland/Location cards and registries.

Upstream World Engine/state/reference files remain authoritative.
Use --check in CI and --write only in governed rebuilds.
"""
from __future__ import annotations
import argparse, difflib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
WORLD=ROOT/"world"/"data"
LCP=ROOT/"world"/"location-control-plane"

def load(path): return json.loads(Path(path).read_text())
def dump(obj): return json.dumps(obj,indent=2,ensure_ascii=False)+"\n"
def slug(s): return re.sub(r"(^-|-$)","",re.sub(r"[^A-Z0-9]+","-",str(s).upper()))[:60]

def compile_outputs():
    locations=load(WORLD/"locations.json")["locations"]
    routes=load(WORLD/"routes.json")["routes"]
    zones=load(WORLD/"physical_zones.json")["regions"]
    divisions=load(WORLD/"divisions.json")["divisions"]
    domains=load(WORLD/"owner_domains.json")["domains"]
    state=load(WORLD/"current_world_state.json")
    events=load(WORLD/"world_state_events.json")["events"]
    horizons=load(WORLD/"landmark_visibility.json")["relationships"]
    weather=load(WORLD/"weather_regions.json")["weather_regions"]
    refs=load(LCP/"registries"/"LOCATION_REFERENCE_REGISTRY.json")["locations"]
    zmap={x["id"]:x for x in zones}; dmap={x["id"]:x for x in divisions}
    lmap={x["id"]:x for x in locations}; rmap={x["id"]:x for x in routes}; refmap={x["location_id"]:x for x in refs}
    out={}

    homelands=[]
    for d in domains:
        p=lmap[d["primary_location_id"]]; div=dmap[d["division_id"]]
        h={
          "schema_version":"1.1","compilation_version":"phase2-v1.1",
          "character_id":d["character_id"],"owner":d["owner"],"team":d["team"],"team_id":d["team_id"],
          "division_id":d["division_id"],"division_name":div["name"],"domain_type":d["domain_type"],
          "primary_location_id":d["primary_location_id"],"physical_zone_ids":d["physical_zone_ids"],
          "physical_zone_profiles":[{"id":zmap[i]["id"],"name":zmap[i]["name"],"terrain":zmap[i]["environment"]["terrain"],"climate":zmap[i]["environment"]["climate"],"movement":zmap[i]["environment"]["movement"]} for i in d["physical_zone_ids"]],
          "ontology_class":d["ontology_class"],"canon_guard":d.get("canon_guard",[]),
          "shared_location_ids":d.get("shared_location_ids",[]),"manifestation_modes":d.get("manifestation_modes",[]),
          "primary_landmarks":p.get("persistent_landmarks",[]),"primary_access_route_ids":p.get("access_route_ids",[]),
          "current_world_state":state.get("locations",{}).get(d["primary_location_id"],p.get("current_state",[])),
          "ordinary_population_rule":"Broader same-kind/compatible ordinary population may exist only as permitted by governing ontology." if d["ontology_class"]=="PEOPLED_KIND" else ("Do not infer a same-kind civilization from the principal." if d["ontology_class"]=="SINGULAR_BEING" else "Shared-cohabitation relationship is canonical; do not infer unsupported wider population facts."),
          "division_visual_fingerprint":div.get("visual_fingerprint"),
          "visual_reference_status":"CHARACTER_REFERENCE_RESOLVED_SEPARATELY__LOCATION_REFERENCE_COMPILED_FROM_CENTRAL_REGISTRY",
          "open_questions":p.get("open_questions",[]),
          "generated_from":["world/data/owner_domains.json","world/data/locations.json","world/data/physical_zones.json","world/data/divisions.json","world/data/current_world_state.json","world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json"],
          "authority_note":"Derived card. Regenerate from upstream sources; do not hand-edit."
        }
        path=f"world/location-control-plane/homelands/{h['character_id']}/CARD.json"
        out[path]=dump(h); homelands.append({"character_id":h["character_id"],"path":path,"primary_location_id":h["primary_location_id"]})

    handles=[]
    locreg=[]
    for l in locations:
        z=zmap[l["physical_zone_id"]]; div=dmap.get(l.get("division_id")); rr=refmap[l["id"]]
        owner_ids=list(dict.fromkeys([*(l.get("owner_character_ids") or []),*([l["owner_character_id"]] if l.get("owner_character_id") else [])]))
        access=[]
        for rid in l.get("access_route_ids",[]):
            r=rmap[rid]; via=[*(r.get("via_location_ids") or []),*([r["via_location_id"]] if r.get("via_location_id") else [])]
            access.append({"id":r["id"],"name":r["name"],"route_class":r["route_class"],"from":r["from"],"to":r["to"],"travel_modes":r.get("travel_modes",[]),"constraints":r.get("constraints",[]),"via_location_ids":via})
        local_handles=[]
        for name in l.get("persistent_landmarks",[]):
            h={"handle_id":f"SUB::{l['id']}::{slug(name)}","parent_location_id":l["id"],"name":name,"handle_class":"PERSISTENT_FEATURE_HANDLE","source":"persistent_landmarks","inherits":["physical_zone","division_relationship","current_world_state","route_context"],"canon_effect":"NONE_UNLESS_SEPARATELY_PROMOTED"}
            local_handles.append({k:v for k,v in h.items() if k!="source"}); handles.append(h)
        card={
          "schema_version":"1.1","compilation_version":"phase2-v1.1","location_id":l["id"],"name":l["name"],"canon_status":l["canon_status"],"location_type":l["location_type"],
          "physical_zone":{"id":l["physical_zone_id"],"name":z["name"],"terrain":z["environment"]["terrain"],"climate":z["environment"]["climate"],"movement":z["environment"]["movement"]},
          "division_overlay":{"id":div["id"],"name":div["name"],"food_referent":div["food_referent"],"visual_fingerprint":div["visual_fingerprint"],"anti_drift":div["anti_drift"]} if div else None,
          "owner_character_ids":owner_ids,"shared_location_ids":l.get("shared_location_ids",[]),"division_presence_ids":l.get("division_presence_ids",[]),"abstract_position":l.get("abstract_position"),
          "access_routes":access,"persistent_landmarks":l.get("persistent_landmarks",[]),"addressable_feature_handles":local_handles,
          "base_location_state":l.get("current_state",[]),"current_world_state":state.get("locations",{}).get(l["id"],[]),
          "historical_events":[{"id":e["id"],"week":e["week"],"event_type":e["event_type"],"classification":e["classification"],"entering_state":e["entering_state"],"continuity_out":e["continuity_out"]} for e in events if e.get("location_id")==l["id"]],
          "horizon_constraints":[h for h in horizons if h.get("observer_location_id")==l["id"]],
          "weather_relationships":[{"id":w["id"],"role":"SOURCE_ZONE" if l["physical_zone_id"] in w["source_zone_ids"] else "PROPAGATION_ZONE","effects":w["effects"],"rule":w["rule"]} for w in weather if l["physical_zone_id"] in w["source_zone_ids"] or l["physical_zone_id"] in w["propagation_order"]],
          "visual_dna":{"terrain":z["environment"]["terrain"],"climate":z["environment"]["climate"],"movement":z["environment"]["movement"],"division_materials":div.get("visual_fingerprint",{}).get("materials",[]) if div else [],"division_skyline":div.get("visual_fingerprint",{}).get("skyline",[]) if div else [],"division_roads":div.get("visual_fingerprint",{}).get("roads",[]) if div else [],"division_night":div.get("visual_fingerprint",{}).get("night",[]) if div else [],"landmark_anchors":l.get("persistent_landmarks",[])},
          "reference_status":rr,
          "open_questions":l.get("open_questions",[]),
          "prohibited_inventions":["Do not move location to another physical zone.","Do not convert Division overlay into physical geography.","Do not erase unresolved current world state.","Do not create new permanent landmarks from generated scenery.","Do not infer character body identity from location theme."],
          "source_provenance":l.get("source_provenance",[]),
          "generated_from":["world/data/locations.json","world/data/routes.json","world/data/physical_zones.json","world/data/divisions.json","world/data/current_world_state.json","world/data/world_state_events.json","world/data/landmark_visibility.json","world/data/weather_regions.json","world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json"],
          "authority_note":"Derived card. Regenerate from upstream sources; do not hand-edit."
        }
        path=f"world/location-control-plane/locations/{l['id']}/CARD.json"
        out[path]=dump(card); locreg.append({"location_id":l["id"],"path":path,"canon_status":l["canon_status"]})

    out["world/location-control-plane/registries/HOMELAND_CARD_REGISTRY.json"]=dump({"schema_version":"1.1","count":len(homelands),"cards":homelands})
    out["world/location-control-plane/registries/LOCATION_CARD_REGISTRY.json"]=dump({"schema_version":"1.1","count":len(locreg),"cards":locreg})
    out["world/location-control-plane/registries/PARENT_SUBLOCATION_REGISTRY.json"]=dump({"schema_version":"1.1","rule":"Derived feature handles are not separate active locations.","handles":handles})
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    outputs=compile_outputs(); drift=[]
    for rel,expected in outputs.items():
        p=ROOT/rel; actual=p.read_text() if p.exists() else None
        if actual!=expected:
            drift.append(rel)
            if args.write:
                p.parent.mkdir(parents=True,exist_ok=True); p.write_text(expected)
    if args.write: print(f"wrote {len(drift)} derived files")
    if args.check:
        if drift:
            print("DERIVED_CARD_DRIFT"); [print(x) for x in drift]
            first=drift[0]
            actual=(ROOT/first).read_text().splitlines()
            expected=outputs[first].splitlines()
            print("FIRST_DRIFT_DIFF")
            for line in list(difflib.unified_diff(actual,expected,fromfile=first,tofile=first+" (generated)",lineterm=""))[:120]:
                print(line)
            raise SystemExit(1)
        print(f"derived cards clean: {len(outputs)} files")
    if not args.write and not args.check:
        print(f"would manage {len(outputs)} derived files; drift={len(drift)}")

if __name__=="__main__": main()
