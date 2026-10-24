#!/usr/bin/env python3
"""Preview existing Schemin route topology without inventing metric or venue canon.

Source of truth remains World Engine V1.1 world/data/*.json. This is a VIEW.
There is no geodesic length, elevation, speed, duration, new LOC or road.
"""
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "world" / "data"
REFERENCE_REGISTRY = ROOT / "world" / "location-control-plane" / "registries" / "LOCATION_REFERENCE_REGISTRY.json"

def load(filename: str) -> dict[str, Any]:
    return json.loads((DATA / filename).read_text(encoding="utf-8"))

def route_chain(route: dict[str, Any]) -> list[str]:
    via = route.get("via_location_ids") or []
    if not via and route.get("via_location_id"):
        via = [route["via_location_id"]]
    return [route["from"], *via, route["to"]]

def build_graph(locations: list[dict[str, Any]], routes: list[dict[str, Any]]) -> dict[str, list[tuple[str, str]]]:
    graph: dict[str, list[tuple[str, str]]] = {loc["id"]: [] for loc in locations}
    for route in routes:
        chain = route_chain(route)
        for a, b in zip(chain, chain[1:]):
            if a not in graph or b not in graph:
                raise ValueError(f"invalid route {route['id']}: missing active endpoint")
            graph[a].append((b, route["id"]))
            graph[b].append((a, route["id"]))
    return graph

def read_only_preview(start: str, goal: str, *,
                      locations: list[dict[str, Any]] | None = None,
                      routes: list[dict[str, Any]] | None = None,
                      references: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    locs = locations if locations is not None else load("locations.json")["locations"]
    edges = routes if routes is not None else load("routes.json")["routes"]
    refs = references if references is not None else json.loads(REFERENCE_REGISTRY.read_text())["locations"]
    loc_by = {loc["id"]: loc for loc in locs}
    if start not in loc_by or goal not in loc_by:
        return {"ok": False, "code": "UNKNOWN_OR_EDITORIAL_LOCATION",
                "start": start, "goal": goal, "canon_mutation_allowed": False}
    graph = build_graph(locs, edges)
    seen = {start}
    queue = deque([start])
    parents: dict[str, tuple[str, str]] = {}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor, route_id in graph[current]:
            if neighbor not in seen:
                parents[neighbor] = (current, route_id)
                seen.add(neighbor)
                queue.append(neighbor)
    if goal not in seen:
        return {"ok": False, "code": "NO_ESTABLISHED_ROUTE",
                "start": start, "goal": goal, "canon_mutation_allowed": False}
    hops: list[dict[str, str]] = []
    node = goal
    while node != start:
        previous, route_id = parents[node]
        hops.append({"from": previous, "to": node, "route_id": route_id})
        node = previous
    hops.reverse()
    ref_by = {ref["location_id"]: ref for ref in refs}
    loc = loc_by[start]
    ref = ref_by.get(start, {})
    return {
        "ok": True,
        "status": "TOPOLOGICAL_PREVIEW_ONLY",
        "origin_location_id": start,
        "destination_location_id": goal,
        "physical_zone_id": loc["physical_zone_id"],
        "known_landmarks": list(loc.get("persistent_landmarks", [])),
        "hops": hops,
        "hop_count": len(hops),
        "measurement_space": "schemin-local-v1 abstract/non-metric",
        "distance_m": None,
        "duration_minutes": None,
        "parcel_area_m2": None,
        "building_footprints": [],
        "approved_structural_reference_uris": list(ref.get("approved_structural_reference_uris", [])),
        "approved_cinematic_reference_uris": list(ref.get("approved_cinematic_reference_uris", [])),
        "cinematic_render_status": "HOLD_PENDING_APPROVED_ENVIRONMENT_AND_CHARACTER_REFERENCES",
        "canon_mutation_allowed": False,
        "note": "A hop is a graph connection, not a measured distance or an approved all-weather journey.",
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origin")
    parser.add_argument("destination")
    args = parser.parse_args()
    packet = read_only_preview(args.origin, args.destination)
    print(json.dumps(packet, indent=2, ensure_ascii=False))
    return 0 if packet["ok"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
