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


def validate_repo() -> list[str]:
    return validate_payloads(
        load_json("physical_zones.json"),
        load_json("divisions.json"),
        load_json("locations.json"),
        load_json("owner_domains.json"),
        load_json("routes.json"),
        load_json("world_state_events.json"),
        load_json("current_world_state.json"),
    )


if __name__ == "__main__":
    errs = validate_repo()
    if errs:
        for err in errs:
            print(f"FAIL: {err}")
        raise SystemExit(1)
    print("PASS: Schemin World Engine V1 machine data validation")
