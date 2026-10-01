#!/usr/bin/env python3
"""Universe OS V1.2 file-native resolver.

Read-only production query layer over governed Universe/Atlas data.
It never mutates world state and never invents missing facts.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"


def _load(name: str) -> dict[str, Any]:
    with (DATA / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def _index(items: list[dict[str, Any]], key: str = "id") -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items}


def _route_chain(route: dict[str, Any]) -> list[str]:
    via = route.get("via_location_ids", [])
    if not via and route.get("via_location_id"):
        via = [route["via_location_id"]]
    return [x for x in [route.get("from"), *via, route.get("to")] if x]


class UniverseResolver:
    def __init__(self) -> None:
        self.locations = _index(_load("locations.json")["locations"])
        self.routes = _index(_load("routes.json")["routes"])
        self.domains = {d["character_id"]: d for d in _load("owner_domains.json")["domains"]}
        self.divisions = _index(_load("divisions.json")["divisions"])
        self.regions = _index(_load("physical_zones.json")["regions"])
        self.ontology = _load("inhabitant_ontology.json")
        self.venue_policy = _load("encounter_venue_policy.json")
        self.current_state = _load("current_world_state.json")
        self.world_events = _load("world_state_events.json")
        self.atlas_layers = _load("atlas_layers.json")
        self.entities_v2 = _index(_load("entities_v2.json")["entities"], "entity_id")
        self.domain_profiles_v2 = {d["owner_character_id"]: d for d in _load("domain_profiles_v2.json")["domains"]}
        self.relationship_graph = _load("location_relationship_graph_v2.json")
        self.world_memory = _load("world_memory_v1.json")
        self.institutions = _load("league_institutions_v1.json")
        self.settlements = _load("settlements_v1.json")
        self.economies = _load("economies_v1.json")
        self.divisions_v2 = _index(_load("divisions_v2.json")["divisions"])
        self._adj = self._build_route_adjacency()

    def _build_route_adjacency(self) -> dict[str, list[tuple[str, str]]]:
        graph: dict[str, list[tuple[str, str]]] = {}
        for rid, route in self.routes.items():
            chain = _route_chain(route)
            for a, b in zip(chain, chain[1:]):
                graph.setdefault(a, []).append((b, rid))
                graph.setdefault(b, []).append((a, rid))
        return graph

    def where_is(self, character_id: str) -> dict[str, Any]:
        domain = self.domains.get(character_id)
        if not domain:
            raise KeyError(character_id)
        loc = self.locations[domain["primary_location_id"]]
        return {
            "character_id": character_id,
            "location_id": loc["id"],
            "location_name": loc["name"],
            "physical_zone_id": loc["physical_zone_id"],
            "division_id": domain["division_id"],
            "atlas_layers": ["LAYER-PHYSICAL", "LAYER-DIVISIONS", "LAYER-OWNER-DOMAINS", "LAYER-ROUTES"],
            "current_state": self.current_state.get("locations", {}).get(loc["id"], loc.get("current_state", [])),
        }

    def who_lives(self, location_id: str) -> dict[str, Any]:
        if location_id not in self.locations:
            raise KeyError(location_id)
        owner = self.locations[location_id].get("owner_character_id")
        settlement = next((s for s in self.settlements["settlements"] if s["anchor_location_id"] == location_id), None)
        result: dict[str, Any] = {
            "location_id": location_id,
            "principal_owner_character_id": owner,
            "population_status": settlement.get("population_note") if settlement else "UNRESOLVED",
            "confidence": settlement.get("canon_confidence") if settlement else {"status": "UNKNOWN"},
        }
        if owner == "CHAR-JAKE-KALOPER":
            result["communities"] = ["ORDER-JEDI", "non-Jedi humans"]
        if owner in {"CHAR-AUSTIN-BYARS", "CHAR-ZACH-WILSON", "CHAR-MANNING-WELTY", "CHAR-DAVID-BABB"}:
            result["singular_principal"] = True
        return result

    def what_kind(self, entity_id: str) -> dict[str, Any]:
        entity = self.entities_v2.get(entity_id)
        if not entity:
            raise KeyError(entity_id)
        return {
            "entity_id": entity_id,
            "entity_type": entity["entity_type"],
            "ontology_class": entity.get("ontology_class"),
            "current_status": entity["current_status"],
            "canon_guard": entity.get("canon_guard", []),
        }

    def routes_touching(self, location_id: str) -> list[str]:
        if location_id not in self.locations:
            raise KeyError(location_id)
        return sorted({rid for rid, r in self.routes.items() if location_id in _route_chain(r)})

    def how_to_travel(self, start: str, goal: str) -> dict[str, Any]:
        if start not in self.locations or goal not in self.locations:
            raise KeyError("unknown location")
        if start == goal:
            return {"locations": [start], "routes": []}
        queue = deque([start])
        prev: dict[str, tuple[str, str] | None] = {start: None}
        while queue:
            cur = queue.popleft()
            for nxt, rid in self._adj.get(cur, []):
                if nxt in prev:
                    continue
                prev[nxt] = (cur, rid)
                if nxt == goal:
                    queue.clear()
                    break
                queue.append(nxt)
        if goal not in prev:
            raise ValueError(f"NO_APPROVED_ROUTE:{start}->{goal}")
        locs = [goal]
        route_ids: list[str] = []
        cur = goal
        while prev[cur] is not None:
            parent, rid = prev[cur]
            route_ids.append(rid)
            locs.append(parent)
            cur = parent
        return {"locations": list(reversed(locs)), "routes": list(reversed(route_ids))}

    def what_happened(self, location_id: str) -> list[dict[str, Any]]:
        return [m for m in self.world_memory["memories"] if m.get("location_id") == location_id]

    def what_state(self, location_id: str) -> list[str]:
        if location_id not in self.locations:
            raise KeyError(location_id)
        return self.current_state.get("locations", {}).get(location_id, self.locations[location_id].get("current_state", []))

    def institutions_near(self, location_id: str) -> list[dict[str, Any]]:
        return [i for i in self.institutions["institutions"] if i["location_id"] == location_id]

    def division_culture(self, division_id: str) -> dict[str, Any]:
        d = self.divisions_v2.get(division_id)
        if not d:
            raise KeyError(division_id)
        return {
            "division_id": division_id,
            "food_referent": d["food_referent"],
            "culture_v2": d.get("culture_v2", {}),
            "border_rule": d.get("border_rule"),
        }

    def region_contains(self, location_id: str) -> str:
        if location_id not in self.locations:
            raise KeyError(location_id)
        return self.locations[location_id]["physical_zone_id"]

    def atlas_layers_for(self, location_id: str) -> list[str]:
        if location_id not in self.locations:
            raise KeyError(location_id)
        layers = ["LAYER-PHYSICAL", "LAYER-ROUTES"]
        loc = self.locations[location_id]
        if loc.get("division_id") is not None or loc.get("division_presence_ids"):
            layers.append("LAYER-DIVISIONS")
        if loc.get("owner_character_id") is not None:
            layers.append("LAYER-OWNER-DOMAINS")
        if location_id in self.current_state.get("locations", {}):
            layers.append("LAYER-WORLD-STATE")
        return layers

    def neutral_site_reachable_by(self, start_a: str, start_b: str) -> list[str]:
        reachable: list[str] = []
        for neutral in self.venue_policy.get("neutral_pool", []):
            try:
                self.how_to_travel(start_a, neutral)
                self.how_to_travel(start_b, neutral)
            except (KeyError, ValueError):
                continue
            reachable.append(neutral)
        return reachable

    def forbidden(self, character_id: str) -> list[str]:
        domain = self.domains.get(character_id)
        if not domain:
            raise KeyError(character_id)
        locks = list(domain.get("canon_guard", []))
        locks.extend(["NO_RENDERER_CREATED_CANON", "OWNER_DOMAIN_IS_NOT_SOVEREIGN_COUNTRY"])
        if character_id == "CHAR-JAKE-KALOPER":
            locks.extend(["DO_NOT_MAKE_OBIWAN_ONLY_JEDI", "DO_NOT_CLONE_OBIWAN_IDENTITY_ON_OTHER_JEDI"])
        return sorted(set(locks))


def main() -> None:
    resolver = UniverseResolver()
    print(json.dumps({
        "status": "PASS",
        "obiwan": resolver.where_is("CHAR-JAKE-KALOPER"),
        "obiwan_population": resolver.who_lives("LOC-TRADE-JEDI-MOUNTAIN-BASE"),
        "shared_march_layers": resolver.atlas_layers_for("LOC-TDS-CHILI-SHARED-MARCH"),
    }, indent=2))


if __name__ == "__main__":
    main()
