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

    # Existing lineage-only visual resolver: no conditioning source promotion.
    # The World Packet now actually carries owner physical/visual constraints,
    # while publication and provider binding stay explicitly blocked.
    from canon.characters.runtime.reference_authority import resolve_approved_lineup_presentation
    visual = resolve_approved_lineup_presentation(owners) if owners else None
    if visual and visual.get("state") != "COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE":
        raise ValueError(f"Character visual canon unresolved for {location_id}: {visual.get('reason')}")
    if visual:
        known = {d["owner_character_id"]: d for d in domains}
        for subject in visual["subjects"]:
            cid = subject["character_id"]
            domain = known.get(cid)
            anchor = subject["spatial_anchor"]
            physics = subject["physical_constraints"]
            if (domain is None
                or anchor.get("home_location_id") != domain.get("home_anchor")
                or not physics.get("anatomy_constraints")
                or not subject["presentation"].get("negative_rules")):
                raise ValueError(f"Character physical/spatial canon mismatch: {cid}")
    physical = {v["character_id"]: v["physical_constraints"] for v in visual["subjects"]} if visual else {}
    negatives = {v["character_id"]: v["presentation"]["negative_rules"] for v in visual["subjects"]} if visual else {}

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
        "body_locks":physical,
        "negative_locks":domain.get("forbidden_drift",[]),
        "owner_specific_negative_locks":negatives,
        "visual_authority":visual,
        "source_binding_state":"UNPROVEN_RENDERER_HOLD",
        "generation_eligible":False
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
