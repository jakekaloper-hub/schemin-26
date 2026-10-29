#!/usr/bin/env python3
"""Compile noncanonical After Dark character continuity packets from existing Schemin truth stores."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
load=lambda p: json.loads((ROOT/p).read_text())
domains=load("world/data/owner_domains.json")["domains"]
locations={x["id"]:x for x in load("world/data/locations.json")["locations"]}
routes={x["id"]:x for x in load("world/data/routes.json")["routes"]}
out=[]
for d in domains:
    loc=locations.get(d["primary_location_id"])
    assert loc is not None, d["character_id"]
    out.append({
      "character_id":d["character_id"],"team_id":d["team_id"],"team_name":d["team"],
      "owner_identity_source":"world/data/owner_domains.json",
      "canonical_home":{"location_id":loc["id"],"name":loc["name"],"zone":loc["physical_zone_id"],"canon_status":loc["canon_status"]},
      "known_location_state":{"source":"world/data/locations.json","states":loc.get("current_state",[]),"open_questions":loc.get("open_questions",[])},
      "last_verified_physical_whereabouts":{"status":"UNKNOWN","note":"Home domain does not establish actual Week 7/8 presence"},
      "travel_to_broadcast_house":{"status":"UNVERIFIED","candidate":"CAND-AFTER-DARK-BROADCAST-HOUSE","home_route_ids":[r for r in loc.get("access_route_ids",[]) if r in routes]},
      "after_dark_knowledge":{"status":"UNVERIFIED","note":"No automatic knowledge of unpublished Memo/Novel scenes"},
      "event_cutoff":"2026-W07", "previous_episode_effects":{"status":"NO_RELEASED_AFTER_DARK_EPISODE"},
      "motivation":{"status":"UNDETERMINED"}, "interview":{"allowed":"NO_IN_PERSON_WITHOUT_ROUTE_AND_TIMELINE"},
      "next_destination":{"status":"UNKNOWN"},
      "macro_thread":{"status":"REQUIRES_WEEKLY_CONTEXT_PACK","source_types":["HISTORICAL_CONTEXT_PACK","WEEKLY_EVENT_CONTEXT_PACK","CHARACTER_CONTEXT_PACK","CONTINUITY_CONTEXT_PACK"]},
      "provenance":["world/data/owner_domains.json","world/data/locations.json","world/data/routes.json"],
      "approval":"NONCANON_DERIVED_DRAFT"
    })
assert len(out)==12 and len({x["character_id"] for x in out})==12
target=ROOT/"productions/after-dark/fixtures/p3c_twelve_character_context.json"
target.write_text(json.dumps({"version":"1.0","status":"DERIVED_NONCANON","as_of":"2026-10-28","characters":out},indent=2)+"\n")
print("compiled",len(out),"character context records",target)
