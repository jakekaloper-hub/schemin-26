#!/usr/bin/env python3
"""Executable enforcement for:
One World Model. One Spatial Control Plane. Many Views. No Forked Geography.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str):
    return json.loads((ROOT / path).read_text())

def check(cond: bool, msg: str):
    if not cond:
        raise AssertionError(msg)

def main() -> int:
    locations = load("world/data/locations.json")["locations"]
    routes = load("world/data/routes.json")["routes"]
    zones = load("world/data/physical_zones.json")["regions"]
    state = load("world/data/current_world_state.json")
    candidates = load("world/data/atlas_location_candidates.json")["candidates"]
    travel = load("living-novel/os/geography/world_travel_graph_v1.json")
    card_registry = load("world/location-control-plane/registries/LOCATION_CARD_REGISTRY.json")
    atlas_layers = load("world/data/atlas_layers.json")

    loc_by = {x["id"]: x for x in locations}
    loc_ids = set(loc_by)
    route_ids = {x["id"] for x in routes}
    zone_ids = {x["id"] for x in zones}
    cand_ids = {x["id"] for x in candidates}

    check(len(loc_ids) == len(locations), "duplicate active LOC identity")
    check(not (loc_ids & cand_ids), "candidate ID collides with active LOC identity")
    check(all(x.get("physical_zone_id") in zone_ids for x in locations), "active LOC references unknown physical region")
    check(set(state.get("locations", {})).issubset(loc_ids), "current world state references noncanonical LOC")

    # Derived travel graph must declare the canonical authority and preserve identity.
    auth = travel.get("authority", "")
    check("world/data/locations.json" in auth and "world/data/routes.json" in auth, "travel graph lost upstream authority declaration")
    check(set(travel.get("nodes", {})) == loc_ids, "derived travel graph node set forked from active LOC store")
    for edge in travel.get("edges", []):
        check(edge.get("from") in loc_ids and edge.get("to") in loc_ids, "travel graph edge references unknown LOC")
        check(edge.get("route_id") in route_ids, "travel graph references unknown ROUTE")

    # Location Cards are derived and must be one-for-one with canonical active locations.
    cards = card_registry.get("cards", [])
    card_ids = {x.get("location_id") for x in cards}
    check(card_ids == loc_ids, "Location Card registry forked from active location identities")

    for item in cards:
        card = load(item["path"])
        lid = item["location_id"]
        check(card.get("location_id") == lid, f"card identity mismatch: {lid}")
        check(card.get("physical_zone_id") == loc_by[lid].get("physical_zone_id"), f"derived physical zone fork: {lid}")

    # Active Atlas layers must source canonical stores; candidate layer must remain editorial-only.
    layers = {x["id"]: x for x in atlas_layers.get("layers", [])}
    check("world/data/physical_zones.json" in layers["LAYER-PHYSICAL"]["source"], "physical Atlas no longer sourced from canonical regions")
    check("world/data/routes.json" in layers["LAYER-ROUTES"]["source"], "route Atlas no longer sourced from canonical routes")
    check(layers["LAYER-CANDIDATES"].get("authority") == "EDITORIAL_ONLY_NOT_ACTIVE_GEOGRAPHY", "candidate firewall lost")

    # Interactive Atlas must remain a view that reads canonical stores.
    builder = (ROOT / "world/atlas/interactive/build_interactive_atlas.py").read_text()
    for required in ["physical_zones.json", "locations.json", "routes.json", "divisions.json", "current_world_state.json"]:
        check(required in builder, f"interactive Atlas no longer consumes {required}")
    for forbidden in ["locations.json).write", "routes.json).write", "current_world_state.json).write"]:
        check(forbidden not in builder, "interactive Atlas appears to write upstream world authority")

    # Governance artifacts must exist.
    for path in [
        "world/governance/WORLD_DATA_OWNERSHIP_MATRIX_V1.md",
        "world/governance/CANONICAL_WORLD_ID_CONTRACT_V1.md",
        "world/governance/DERIVED_WORLD_DATA_CONTRACT_V1.md",
        "world/evolution/WORLD_MUTATION_FANOUT_CONTRACT_V2.md",
        "world/qa/ONE_WORLD_MODEL_ANTI_FORK_AUDIT_V1.md",
        "world/qa/ATLAS_CONTROL_PLANE_CONSOLIDATION_REPORT_V1.md",
    ]:
        check((ROOT / path).exists(), f"missing architecture control: {path}")

    print("ONE WORLD MODEL CONTRACT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
