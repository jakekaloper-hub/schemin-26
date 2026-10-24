#!/usr/bin/env python3
"""Read-only, non-canonical civilization context derived from existing Universe data."""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
SOURCES = (
    "world/data/physical_zones.json",
    "world/data/settlements.json",
    "world/data/economies.json",
    "world/data/locations.json",
)


def _load(filename: str, key: str) -> list[dict]:
    return json.loads((DATA / filename).read_text(encoding="utf-8"))[key]


def resolve_civilization_context(region_id: str) -> dict:
    """Return one region's approved-source ambient context, never a canon mutation."""
    regions = _load("physical_zones.json", "regions")
    settlements = _load("settlements.json", "settlements")
    economies = _load("economies.json", "economies")
    locations = _load("locations.json", "locations")
    by_region = {r["id"]: r for r in regions}
    if region_id not in by_region:
        return {"ok": False, "error": "UNKNOWN_REGION", "region_id": region_id}
    settlement_matches = [s for s in settlements if s["physical_zone_id"] == region_id]
    economy_matches = [e for e in economies if e["physical_zone_id"] == region_id]
    if len(settlement_matches) != 1 or len(economy_matches) != 1:
        return {"ok": False, "error": "INCOMPLETE_REGION_CONTEXT", "region_id": region_id}
    s, e, r = settlement_matches[0], economy_matches[0], by_region[region_id]
    loc_by_id = {loc["id"]: loc for loc in locations}
    anchors = []
    for loc_id in s["anchor_location_ids"]:
        loc = loc_by_id.get(loc_id)
        if loc is None or loc["physical_zone_id"] != region_id:
            return {"ok": False, "error": "INVALID_LOCATION_ANCHOR", "region_id": region_id}
        anchors.append({"id": loc_id, "name": loc["name"]})
    return {
        "ok": True,
        "status": "READ_ONLY_INTERPRETIVE_CONTEXT",
        "region_id": region_id,
        "region_name": r["name"],
        "terrain": list(r["environment"]["terrain"]),
        "climate": list(r["environment"]["climate"]),
        "movement": list(r["environment"]["movement"]),
        "settlement_context_id": s["id"],
        "anchor_locations": anchors,
        "placement_reasons": list(s["placement_reasons"]),
        "ordinary_life": list(s["ordinary_life"]),
        "transport": list(s["transport"]),
        "food_supply": list(s["food_supply"]),
        "institutions": list(s["institutions"]),
        "economic_activities": list(e["activities"]),
        "confidence": s["canon_confidence"],
        "consumer_permissions": ["MEMO_CONTEXT", "NOVEL_CONTEXT", "ATLAS_READ_ONLY", "ART_ENVIRONMENT_ONLY"],
        "provenance": list(SOURCES),
        "restrictions": ["NO_NAMED_NPCS", "NO_NEW_LOCATION_IDS", "NO_CHARACTER_AUTHORITY", "NO_WORLD_STATE_MUTATION"],
    }
