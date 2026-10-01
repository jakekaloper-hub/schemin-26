#!/usr/bin/env python3
"""Universe OS V1.2 / Atlas Control Plane acceptance suite."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DATA=ROOT/"world"/"data"

def load(name):
    return json.loads((DATA/name).read_text())

def check(cond,msg):
    if not cond:
        raise AssertionError(msg)

def main():
    locations=load("locations.json")["locations"]
    routes=load("routes.json")["routes"]
    divisions=load("divisions.json")["divisions"]
    owners=load("owner_domains.json")["domains"]
    entities=load("entities.json")["entities"]
    domains=load("domain_profiles.json")["domains"]
    memory=load("world_memory.json")["events"]
    institutions=load("league_institutions.json")["institutions"]
    settlements=load("settlements.json")["settlements"]
    rel=load("location_relationship_graph.json")["relationships"]

    loc_ids={x["id"] for x in locations}
    route_ids={x["id"] for x in routes}
    char_ids={x["character_id"] for x in owners}
    ent_ids={x["entity_id"] for x in entities}

    check(len(owners)==12,"expected 12 owner domains")
    check(len(char_ids)==12,"owner character IDs must be unique")
    check(len(domains)==12,"expected 12 V2 domain profiles")
    check(all(x["home_anchor"] in loc_ids for x in domains),"every domain home anchor must resolve")

    dmap={x["id"]:x for x in divisions}
    check(set(dmap)=={"DIV-BURGERS","DIV-WINGS","DIV-PIZZA"},"division IDs drifted")
    check(all(len(x["member_team_ids_2026"])==4 for x in divisions),"division membership must be 4/4/4")
    check(dmap["DIV-WINGS"].get("food_referent")=="chicken_wings","Wings semantic drift")
    check(dmap["DIV-WINGS"].get("cultural_layer_v2",{}).get("food_identity")=="chicken_wings","Wings V2 culture missing")

    check("COMM-JEDI-ORDER" in ent_ids,"Jedi community entity missing")
    jedi=next(x for x in entities if x["entity_id"]=="COMM-JEDI-ORDER")
    check("CHAR-JAKE-KALOPER" in jedi.get("related_entities",[]),"ObiWan/Jedi coexistence not linked")

    shared=next((x for x in locations if x["id"]=="LOC-TDS-CHILI-SHARED-MARCH"),None)
    check(shared is not None,"shared march missing")
    check(set(shared.get("division_presence_ids",[]))=={"DIV-BURGERS","DIV-WINGS"},"shared march division coexistence drift")

    for o in owners:
        loc=next(x for x in locations if x["id"]==o["primary_location_id"])
        touch=set(loc.get("access_route_ids",[]))
        touch.update(r["id"] for r in routes if r.get("from")==loc["id"] or r.get("to")==loc["id"] or r.get("via_location_id")==loc["id"] or loc["id"] in r.get("via_location_ids",[]))
        check(touch,"owner home anchor lacks approved route context")
        check(touch.issubset(route_ids),"unknown route reference")

    neutral=[x for x in locations if x.get("location_type") in {"neutral_encounter_ground","neutral_institution","league_institution"}]
    for loc in neutral:
        touch=[r for r in routes if r.get("from")==loc["id"] or r.get("to")==loc["id"] or r.get("via_location_id")==loc["id"] or loc["id"] in r.get("via_location_ids",[])]
        check(touch,f"neutral location not reachable: {loc['id']}")

    check(all(e.get("location") in loc_ids for e in memory if e.get("location")),"memory references unknown location")
    check(all(i.get("location_id") in loc_ids for i in institutions),"institution references unknown location")
    check(all(a in loc_ids for s in settlements for a in s.get("anchor_location_ids",[])),"settlement context references unknown anchor")

    within={x["from"] for x in rel if x["type"]=="WITHIN"}
    check(loc_ids.issubset(within),"every active location must resolve to a physical region")

    # Existing Atlas phases must remain active/reachable.
    for path in [
        ROOT/"world"/"atlas"/"phase-1"/"_INDEX.md",
        ROOT/"world"/"location-control-plane"/"_INDEX.md",
        ROOT/"world"/"environment-references"/"_INDEX.md",
        ROOT/"world"/"atlas"/"interactive"/"_INDEX.md",
        ROOT/"world"/"evolution"/"_INDEX.md",
    ]:
        check(path.exists(),f"missing Atlas subsystem: {path}")

    # Query resolver smoke.
    from world.engine.universe_resolver import UniverseResolver
    from world.production.build_visual_world_packet import build_packet
    r=UniverseResolver()
    check(r.where_is("CHAR-JAKE-KALOPER").get("ok"),"ObiWan WHERE_IS failed")
    check(r.who_lives("LOC-TRADE-JEDI-MOUNTAIN-BASE").get("ok"),"ObiWan WHO_LIVES failed")
    check(r.what_division_culture("LOC-TDS-CHILI-SHARED-MARCH").get("ok"),"shared march culture query failed")\n\n    for loc_id in ["LOC-TRADE-JEDI-MOUNTAIN-BASE","LOC-MUD-DOGS-SWAMP","LOC-COUNTRY-CLUB-JACKSON","LOC-LLC-STORM-CITY","LOC-TDS-CHILI-SHARED-MARCH","LOC-COMPACT-NEUTRAL-GROUNDS"]:\n        packet=build_packet(loc_id)\n        check(packet["world"]["location_id"]==loc_id,f"visual packet mismatch: {loc_id}")\n        check(packet["atlas"]["arrival_routes"],f"visual packet lacks arrival route: {loc_id}")

    print("UNIVERSE OS V1.2 ACCEPTANCE: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
