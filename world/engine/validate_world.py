#!/usr/bin/env python3
"""Schemin World Engine V1 validation.

Pure-stdlib validator for topology, identity linkage, continuity references,
and selected anti-drift invariants. Abstract coordinates are non-metric.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"


def load_json(name: str) -> dict[str, Any]:
    with (DATA / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def load_repo_json(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as f:
        return json.load(f)


def point_in_bounds(point: list[float], bounds: list[float]) -> bool:
    x, y = point
    xmin, ymin, xmax, ymax = bounds
    return xmin <= x <= xmax and ymin <= y <= ymax


def validate_payloads(
    physical: dict[str, Any],
    divisions: dict[str, Any],
    locations: dict[str, Any],
    domains: dict[str, Any],
    routes: dict[str, Any],
    state_events: dict[str, Any],
    current_state: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    regions = physical.get("regions", [])
    region_by_id = {r["id"]: r for r in regions}
    if len(region_by_id) != len(regions):
        errors.append("duplicate physical region id")

    # Adjacency should be symmetric.
    for region in regions:
        rid = region["id"]
        for neighbor in region.get("adjacent_region_ids", []):
            if neighbor not in region_by_id:
                errors.append(f"{rid} references missing adjacent region {neighbor}")
                continue
            if rid not in region_by_id[neighbor].get("adjacent_region_ids", []):
                errors.append(f"adjacency not symmetric: {rid} <-> {neighbor}")

    divs = divisions.get("divisions", [])
    div_by_id = {d["id"]: d for d in divs}
    if set(div_by_id) != {"DIV-BURGERS", "DIV-WINGS", "DIV-PIZZA"}:
        errors.append("division ids must be exactly Burgers/Wings/Pizza")

    wings = div_by_id.get("DIV-WINGS", {})
    if wings.get("food_referent") != "chicken_wings":
        errors.append("Wings semantic lock violated: must be chicken_wings")

    team_ids: list[int] = []
    for div in divs:
        members = div.get("member_team_ids_2026", [])
        if len(members) != 4:
            errors.append(f"{div.get('id')} must have four 2026 members")
        team_ids.extend(members)
        for zid in div.get("physical_zone_ids", []):
            if zid not in region_by_id:
                errors.append(f"{div.get('id')} references missing physical zone {zid}")
    if sorted(team_ids) != list(range(1, 13)):
        errors.append("2026 division membership must cover team ids 1..12 exactly once")

    locs = locations.get("locations", [])
    loc_by_id = {l["id"]: l for l in locs}
    if len(loc_by_id) != len(locs):
        errors.append("duplicate location id")

    for loc in locs:
        lid = loc["id"]
        zid = loc.get("physical_zone_id")
        did = loc.get("division_id")
        if zid is not None and zid not in region_by_id:
            errors.append(f"{lid} references missing physical zone {zid}")
        if did is not None and did not in div_by_id:
            errors.append(f"{lid} references missing division {did}")
        pos = loc.get("abstract_position")
        if pos is not None and zid in region_by_id:
            bounds = region_by_id[zid].get("abstract_bounds")
            if bounds and not point_in_bounds(pos, bounds):
                errors.append(f"{lid} abstract position is outside assigned physical zone")

    route_list = routes.get("routes", [])
    route_by_id = {r["id"]: r for r in route_list}
    if len(route_by_id) != len(route_list):
        errors.append("duplicate route id")

    for route in route_list:
        for endpoint_key in ("from", "to"):
            endpoint = route.get(endpoint_key)
            if endpoint not in loc_by_id:
                errors.append(f"{route.get('id')} has missing endpoint {endpoint}")

    for loc in locs:
        for route_id in loc.get("access_route_ids", []):
            if route_id not in route_by_id:
                errors.append(f"{loc['id']} references missing route {route_id}")

    domain_list = domains.get("domains", [])
    if len(domain_list) != 12:
        errors.append("owner domain register must contain 12 domains")
    if sorted(d.get("team_id") for d in domain_list) != list(range(1, 13)):
        errors.append("owner domains must cover team ids 1..12 exactly once")

    seen_chars: set[str] = set()
    for domain in domain_list:
        char = domain.get("character_id")
        if char in seen_chars:
            errors.append(f"duplicate owner domain character {char}")
        seen_chars.add(char)
        did = domain.get("division_id")
        if did not in div_by_id:
            errors.append(f"{char} references missing division {did}")
        primary = domain.get("primary_location_id")
        if primary not in loc_by_id:
            errors.append(f"{char} references missing primary location {primary}")
            continue
        ploc = loc_by_id[primary]
        if ploc.get("owner_character_id") != char:
            errors.append(f"{char} primary location owner mismatch")
        if ploc.get("division_id") != did:
            errors.append(f"{char} primary location division mismatch")

    by_char = {d["character_id"]: d for d in domain_list}
    wilson = by_char.get("CHAR-WILSON-LOOK", {})
    if "ARSENAL_GORILLA_WARRIOR" not in wilson.get("canon_guard", []):
        errors.append("Wilson Look current gorilla lock missing")
    if "NO_CENTAUR_ANATOMY" not in wilson.get("canon_guard", []):
        errors.append("Wilson Look retired-centaur negative lock missing")

    pitts = by_char.get("CHAR-PHILLIP-PITTS", {})
    if "ONE_BODY_THREE_SERPENT_HEADS" not in pitts.get("canon_guard", []):
        errors.append("Phillip Pitts three-head body lock missing")

    jake = by_char.get("CHAR-JAKE-KALOPER", {})
    if "NO_CHAMPIONSHIP_BELT" not in jake.get("canon_guard", []):
        errors.append("Jake no-belt hard lock missing")

    events = state_events.get("events", [])
    event_ids = set()
    for event in events:
        eid = event.get("id")
        if eid in event_ids:
            errors.append(f"duplicate state event {eid}")
        event_ids.add(eid)
        lid = event.get("location_id")
        if lid not in loc_by_id:
            errors.append(f"{eid} references missing location {lid}")
        if not event.get("source_provenance"):
            errors.append(f"{eid} missing provenance")

    for lid in current_state.get("locations", {}):
        if lid not in loc_by_id:
            errors.append(f"current world state references missing location {lid}")

    return errors


EXPECTED_DIVISION_MEMBERS = {
    "DIV-BURGERS": {1, 5, 6, 10},
    "DIV-WINGS": {2, 3, 7, 12},
    "DIV-PIZZA": {4, 8, 9, 11},
}

EXPECTED_ONTOLOGY = {
    "PEOPLED_KIND": {
        "CHAR-JAKE-KALOPER",
        "CHAR-WILSON-LOOK",
        "CHAR-KEVIN-ZEEK",
        "CHAR-JORDAN-HOLLINGSHEAD",
        "CHAR-BOBBY-MITCHELL",
        "CHAR-BEN-WHIPPLE",
    },
    "SINGULAR_BEING": {
        "CHAR-AUSTIN-BYARS",
        "CHAR-ZACH-WILSON",
        "CHAR-MANNING-WELTY",
        "CHAR-DAVID-BABB",
    },
    "SHARED_COHABITATION": {
        "CHAR-PHILLIP-PITTS",
        "CHAR-BRANDON-PRYOR",
    },
}


def route_chain(route: dict[str, Any]) -> list[str]:
    via = route.get("via_location_ids", [])
    if not via and route.get("via_location_id"):
        via = [route["via_location_id"]]
    return [route.get("from"), *via, route.get("to")]


def build_location_graph(routes: dict[str, Any]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for route in routes.get("routes", []):
        chain = [x for x in route_chain(route) if x]
        for a, b in zip(chain, chain[1:]):
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)
    return graph


def path_exists(graph: dict[str, set[str]], start: str, goal: str) -> bool:
    if start == goal:
        return True
    if start not in graph or goal not in graph:
        return False
    seen = {start}
    queue = [start]
    while queue:
        node = queue.pop(0)
        for nxt in graph.get(node, set()):
            if nxt == goal:
                return True
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def validate_universe_extensions(
    divisions: dict[str, Any],
    locations: dict[str, Any],
    domains: dict[str, Any],
    routes: dict[str, Any],
    ontology: dict[str, Any],
    venue_policy: dict[str, Any],
    novel_travel_graph: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    div_by_id = {d["id"]: d for d in divisions.get("divisions", [])}
    for did, expected in EXPECTED_DIVISION_MEMBERS.items():
        actual = set(div_by_id.get(did, {}).get("member_team_ids_2026", []))
        if actual != expected:
            errors.append(f"{did} membership mismatch: expected {sorted(expected)}, got {sorted(actual)}")

    team_to_division = {
        team_id: did
        for did, members in EXPECTED_DIVISION_MEMBERS.items()
        for team_id in members
    }

    loc_by_id = {l["id"]: l for l in locations.get("locations", [])}
    route_by_id = {r["id"]: r for r in routes.get("routes", [])}

    # Every location-declared route must actually touch that location, either
    # as endpoint or an explicit via stop.
    for loc in locations.get("locations", []):
        lid = loc["id"]
        for rid in loc.get("access_route_ids", []):
            route = route_by_id.get(rid)
            if route is None:
                continue
            if lid not in route_chain(route):
                errors.append(f"{lid} claims access route {rid} but route does not touch location")

    # Via stops must resolve.
    for route in routes.get("routes", []):
        for lid in route_chain(route):
            if lid and lid not in loc_by_id:
                errors.append(f"{route.get('id')} references missing route-chain location {lid}")

    domains_by_team = {d.get("team_id"): d for d in domains.get("domains", [])}
    for team_id, expected_division in team_to_division.items():
        domain = domains_by_team.get(team_id)
        if domain and domain.get("division_id") != expected_division:
            errors.append(f"team {team_id} owner-domain division mismatch: expected {expected_division}")

    # Ontology classes must be mutually exclusive and cover all Twelve.
    classes = ontology.get("classes", {})
    seen: set[str] = set()
    for class_name, expected in EXPECTED_ONTOLOGY.items():
        actual = set(classes.get(class_name, []))
        if actual != expected:
            errors.append(f"{class_name} ontology mismatch")
        overlap = seen & actual
        if overlap:
            errors.append(f"ontology overlap: {sorted(overlap)}")
        seen |= actual
    if len(seen) != 12:
        errors.append("inhabitant ontology must classify exactly 12 principal characters")

    el_nino = ontology.get("el_nino", {})
    modes = set(el_nino.get("manifestation_modes", []))
    if not {"EMBODIED", "ATMOSPHERIC_MANIFESTATION"}.issubset(modes):
        errors.append("El Niño dual manifestation law missing")

    shared = ontology.get("shared_cohabitation", {})
    if set(shared.get("members", [])) != EXPECTED_ONTOLOGY["SHARED_COHABITATION"]:
        errors.append("TDS/Chili shared-cohabitation membership mismatch")
    shared_lid = shared.get("geography_anchor")
    if shared_lid not in loc_by_id:
        errors.append("TDS/Chili shared-cohabitation location missing")
    else:
        presence = set(loc_by_id[shared_lid].get("division_presence_ids", []))
        if presence != {"DIV-BURGERS", "DIV-WINGS"}:
            errors.append("TDS/Chili shared march must carry Burgers + Wings presence")

    # Venue policy.
    home_venues = venue_policy.get("home_venues", {})
    if set(home_venues) != {str(i) for i in range(1, 13)}:
        errors.append("Encounter venue policy must define home venue for team ids 1..12")
    for team_id_str, lid in home_venues.items():
        if lid not in loc_by_id:
            errors.append(f"home venue {lid} for team {team_id_str} is missing")
            continue
        expected_division = team_to_division[int(team_id_str)]
        if loc_by_id[lid].get("division_id") != expected_division:
            errors.append(f"home venue {lid} division mismatch for team {team_id_str}")

    for event_name in ("GAME_OF_THE_WEEK", "PLAYOFF", "CHAMPIONSHIP"):
        rule = venue_policy.get("event_rules", {}).get(event_name, {})
        if rule.get("venue_mode") != "NEUTRAL_DEFAULT":
            errors.append(f"{event_name} must default to neutral venue")

    neutral_pool = venue_policy.get("neutral_pool", [])
    if not neutral_pool:
        errors.append("neutral venue pool cannot be empty")
    for lid in neutral_pool:
        if lid not in loc_by_id:
            errors.append(f"neutral venue {lid} missing")
        elif loc_by_id[lid].get("division_id") is not None:
            errors.append(f"default neutral venue {lid} must not belong to a division")

    graph = build_location_graph(routes)
    for home_lid in home_venues.values():
        if neutral_pool and not any(path_exists(graph, home_lid, neutral) for neutral in neutral_pool):
            errors.append(f"home venue {home_lid} has no approved route to neutral network")

    # Living Novel graph must be hydrated from World Engine rather than remain
    # the old zero-edge seed.
    if novel_travel_graph.get("status") == "SEED_NOT_FULL_MAP":
        errors.append("Living Novel travel graph still marked SEED_NOT_FULL_MAP")
    if not novel_travel_graph.get("edges"):
        errors.append("Living Novel travel graph has zero approved edges")

    return errors

def validate_repo() -> list[str]:
    physical = load_json("physical_zones.json")
    divisions = load_json("divisions.json")
    locations = load_json("locations.json")
    domains = load_json("owner_domains.json")
    routes = load_json("routes.json")
    state_events = load_json("world_state_events.json")
    current_state = load_json("current_world_state.json")
    ontology = load_json("inhabitant_ontology.json")
    venue_policy = load_json("encounter_venue_policy.json")
    novel_travel_graph = load_repo_json("living-novel/os/geography/world_travel_graph_v1.json")

    errors = validate_payloads(
        physical,
        divisions,
        locations,
        domains,
        routes,
        state_events,
        current_state,
    )
    errors += validate_universe_extensions(
        divisions,
        locations,
        domains,
        routes,
        ontology,
        venue_policy,
        novel_travel_graph,
    )
    return errors


if __name__ == "__main__":
    errs = validate_repo()
    if errs:
        for err in errs:
            print(f"FAIL: {err}")
        raise SystemExit(1)
    print("PASS: Schemin World Engine V1 machine data validation")
