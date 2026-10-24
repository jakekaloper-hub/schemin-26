#!/usr/bin/env python3
"""Compile a renderer-safe Visual World Packet V2 for an active LOC-*."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"world"/"data"

def load(name:str)->dict[str,Any]:
    return json.loads((DATA/name).read_text())

def build_packet(location_id:str)->dict[str,Any]:
    locations=load("locations.json")["locations"]
    routes=load("routes.json")["routes"]
    memory=load("world_memory.json")["events"]
    institutions=load("league_institutions.json")["institutions"]
    domains=load("domain_profiles.json")["domains"]
    # Positive anatomy/identity requirements have independent character-canon
    # semantics and MUST NOT be inverted into renderer negative instructions.
    owner_domains=load("owner_domains.json")["domains"]
    settlements=load("settlements.json")["settlements"]

    loc=next((x for x in locations if x["id"]==location_id),None)
    if loc is None:
        raise ValueError(f"unknown active location: {location_id}")

    route_ids=list(loc.get("access_route_ids",[]))
    for r in routes:
        if r.get("from")==location_id or r.get("to")==location_id or r.get("via_location_id")==location_id or location_id in r.get("via_location_ids",[]):
            if r["id"] not in route_ids:
                route_ids.append(r["id"])

    events=[e for e in memory if e.get("location")==location_id]
    inst=[i for i in institutions if i.get("location_id")==location_id]
    domain=next((d for d in domains if d.get("home_anchor")==location_id),{})
    canonical_character_id=loc.get("owner_character_id")
    owner_record=next((d for d in owner_domains if d["character_id"]==canonical_character_id),{})
    canon_guards=owner_record.get("canon_guard",[])
    visual_domain_rules=domain.get("forbidden_drift",[])
    # A descriptor such as ONE_BODY_THREE_SERPENT_HEADS is a positive lock.
    # Only explicitly negative NO_* rules may be sent as visual negative locks.
    # Institutional constraints are still carried separately in 'domain'.
    body_locks=list(dict.fromkeys(g for g in canon_guards if not g.startswith("NO_")))
    negative_locks=list(dict.fromkeys(
        g for g in [*canon_guards,*visual_domain_rules] if g.startswith("NO_")
    ))
    ordinary=[]
    for s in settlements:
        if location_id in s.get("anchor_location_ids",[]):
            ordinary.extend(s.get("ordinary_life",[]))

    owners=[]
    if loc.get("owner_character_id"):
        owners.append(loc["owner_character_id"])
    owners.extend(loc.get("owner_character_ids",[]))
    owners=list(dict.fromkeys(owners))

    divisions=[]
    if loc.get("division_id"):
        divisions.append(loc["division_id"])
    divisions.extend(loc.get("division_presence_ids",[]))
    divisions=list(dict.fromkeys(divisions))

    # Derive environmental context from the same Universe source used by Memo/Novel.
    from world.engine.civilization_consumers import resolve_scene_context
    civilization = resolve_scene_context(location_id, "art_environment")
    if not civilization.get("ok"):
        raise ValueError(f"unresolved civilization context for {location_id}: {civilization.get('code', civilization.get('error'))}")
    if civilization.get("character_rendering_allowed") is not False:
        raise ValueError("civilization context cannot authorize character rendering")

    return {
      "civilization_context": civilization,
      "schema_version":"2.0",
      "world":{
        "location_id":location_id,
        "physical_zone":loc.get("physical_zone_id"),
        "world_state":loc.get("current_state",[]),
        "history":events,
        "institutions":inst,
        "ordinary_inhabitants":ordinary,
        "weather":None
      },
      "atlas":{
        "civil_context":loc.get("location_type"),
        "division_presence":divisions,
        "owner_domain":domain.get("domain_id"),
        "arrival_routes":route_ids,
        "water_relationship":"DERIVE_FROM_ACTIVE_ATLAS",
        "elevation_relationship":"DERIVE_FROM_ACTIVE_ATLAS",
        "camera_direction":None,
        "foreground_terrain":None,
        "midground":None,
        "background_topography":None,
        "visible_landmarks":loc.get("persistent_landmarks",[]),
        "forbidden_landmarks":[],
        "historical_overlays":[e["event_id"] for e in events]
      },
      "domain":domain,
      "character":{
        "principal_character_ids":owners,
        "reference_status":"CHARACTER_REFERENCE_GATE_SEPARATE" if owners else "NO_PRINCIPAL_REQUIRED",
        "body_locks":body_locks,
        "negative_locks":negative_locks
      },
      "memory":{
        "events":events,
        "prohibited_literalization":["generated scenery does not create canon"]
      },
      "typography":{
        "exact_location_name":loc["name"],
        "generated_text_allowed":False,
        "approved_labels":[loc["name"]]
      }
    }

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("location_id")
    ap.add_argument("--output")
    ns=ap.parse_args()
    packet=build_packet(ns.location_id)
    out=json.dumps(packet,indent=2)
    if ns.output:
        Path(ns.output).write_text(out+"\n")
    else:
        print(out)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
