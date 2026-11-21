#!/usr/bin/env python3
"""Setup Man + Umpire: real selective-invalidation mutation exercise.

Mutates a COPY of the adapted Week 9 graph in memory. Source files are never
changed. Demonstrates that RESULT, CHARACTER, and LOCATION changes have distinct
impact sets.
"""
from __future__ import annotations
import json
from adapt_week9_matchups import compile_week9
from adapt_week9_scenes import compile_scenes
from build_compiler_manifest import build_manifest
from dependency_invalidation import impacted_nodes

def exercise():
    week=compile_week9(False)
    scenes=compile_scenes()
    manifest=build_manifest(week["events"],scenes,"week9-hold")
    first=week["events"][0]
    eid=first["event_id"]
    char=next(p["entity_id"] for p in first["participants"] if p["entity_type"]=="CHARACTER")
    loc=next(p["entity_id"] for p in first["participants"] if p["entity_type"]=="LOCATION")
    edges=manifest["invalidation"]["dependency_edges"]

    result=set(impacted_nodes(edges,[f"{eid}::RESULT"]))
    base=set(impacted_nodes(edges,[f"{eid}::BASE"]))
    character=set(impacted_nodes(edges,[f"CHAR::{char}"]))
    location=set(impacted_nodes(edges,[f"LOC::{loc}"]))

    first_scenes={s["scene_id"] for s in scenes if s["event_id"]==eid}
    result_sensitive={s["scene_id"] for s in scenes if s["event_id"]==eid and f"{eid}::RESULT" in s["dependencies"]}
    base_only=first_scenes-result_sensitive

    assertions={
      "result_hits_result_scenes":result_sensitive.issubset(result),
      "result_spares_base_only_scenes":base_only.isdisjoint(result),
      "base_hits_all_matchup_scenes":first_scenes.issubset(base),
      "character_hits_depicting_scenes":all((s["scene_id"] in character) for s in scenes if any(c["character_id"]==char for c in s["cast"])),
      "location_hits_location_scenes":all((s["scene_id"] in location) for s in scenes if s["location"]["location_id"]==loc),
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    return {
      "state":"SELECTIVE_INVALIDATION_PASS",
      "event_id":eid,
      "character_id":char,
      "location_id":loc,
      "counts":{
        "all_matchup_scenes":len(first_scenes),
        "result_sensitive_scenes":len(result_sensitive),
        "result_impacted_nodes":len(result),
        "base_impacted_nodes":len(base),
        "character_impacted_nodes":len(character),
        "location_impacted_nodes":len(location),
      },
      "assertions":assertions,
    }

if __name__=="__main__":
    print(json.dumps(exercise(),indent=2))
