#!/usr/bin/env python3
"""Read-only Universe OS V1.2 resolver.

Consumes canonical World/Atlas data. It never mutates canon.
"""
from __future__ import annotations
import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"


def load_json(name: str) -> dict[str, Any]:
    return json.loads((DATA / name).read_text())


class UniverseResolver:
    def __init__(self) -> None:
        self.locations = load_json("locations.json")["locations"]
        self.routes = load_json("routes.json")["routes"]
        self.divisions = load_json("divisions.json")["divisions"]
        self.owner_domains = load_json("owner_domains.json")["domains"]
        self.entities = load_json("entities.json")["entities"]
        self.domain_profiles = load_json("domain_profiles.json")["domains"]
        self.memory = load_json("world_memory.json")["events"]
        self.institutions = load_json("league_institutions.json")["institutions"]
        self.settlements = load_json("settlements.json")["settlements"]
        self.economies = load_json("economies.json")["economies"]
        self.relationships = load_json("location_relationship_graph.json")["relationships"]
        self.loc_by_id = {x["id"]: x for x in self.locations}
        self.route_by_id = {x["id"]: x for x in self.routes}
        self.entity_by_id = {x["entity_id"]: x for x in self.entities}
        self.div_by_id = {x["id"]: x for x in self.divisions}
        self.domain_by_char = {x["character_id"]: x for x in self.owner_domains}
        self.profile_by_char = {x["owner_character_id"]: x for x in self.domain_profiles}

    def _entity(self, value: str) -> dict[str, Any] | None:
        if value in self.entity_by_id:
            return self.entity_by_id[value]
        q = value.lower()
        for e in self.entities:
            if q in {str(e.get("name", "")).lower(), str(e.get("team", "")).lower()}:
                return e
        for d in self.owner_domains:
            if q in {str(d.get("owner", "")).lower(), str(d.get("team", "")).lower()}:
                return self.entity_by_id.get(d["character_id"])
        return None

    def _location(self, value: str) -> dict[str, Any] | None:
        if value in self.loc_by_id:
            return self.loc_by_id[value]
        q = value.lower()
        for loc in self.locations:
            if q == str(loc.get("name", "")).lower():
                return loc
        return None

    def where_is(self, entity: str) -> dict[str, Any]:
        e = self._entity(entity)
        if not e:
            return self._fail("UNKNOWN_ENTITY", entity)
        rel = e.get("location_relationship") or {}
        loc_id = rel.get("home_anchor")
        loc = self.loc_by_id.get(loc_id) if loc_id else None
        return self._ok(
            entity_id=e["entity_id"],
            home_anchor=loc_id,
            location=loc,
            authority=["world/data/entities.json", "world/data/locations.json"],
        )

    def who_lives(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        populations = []
        principals = []
        for p in self.domain_profiles:
            if p.get("home_anchor") == loc["id"]:
                principals.append(p["owner_character_id"])
                populations.extend(p.get("population", p.get("population_context", [])) if isinstance(p.get("population", p.get("population_context", [])), list) else [p.get("population_context")])
        for s in self.settlements:
            if loc["id"] in s.get("anchor_location_ids", []):
                populations.extend(s.get("ordinary_life", []))
        return self._ok(
            location_id=loc["id"],
            principals=principals,
            population_context=[x for x in populations if x],
            authority=["world/data/domain_profiles.json", "world/data/settlements.json"],
        )

    def _graph(self) -> dict[str, list[tuple[str, str]]]:
        g: dict[str, list[tuple[str, str]]] = {}
        def add(a: str, b: str, route_id: str) -> None:
            g.setdefault(a, []).append((b, route_id))
            g.setdefault(b, []).append((a, route_id))
        for r in self.routes:
            chain = [r["from"]]
            if r.get("via_location_id"):
                chain.append(r["via_location_id"])
            chain.extend(r.get("via_location_ids", []))
            chain.append(r["to"])
            for a, b in zip(chain, chain[1:]):
                add(a, b, r["id"])
        return g

    def how_to_travel(self, start: str, end: str) -> dict[str, Any]:
        a = self._location(start)
        b = self._location(end)
        if not a or not b:
            return self._fail("UNKNOWN_LOCATION", f"{start} -> {end}")
        if a["id"] == b["id"]:
            return self._ok(location_path=[a["id"]], route_ids=[])
        g = self._graph()
        q = deque([(a["id"], [a["id"]], [])])
        seen = {a["id"]}
        while q:
            node, path, route_ids = q.popleft()
            for nxt, rid in g.get(node, []):
                if nxt in seen:
                    continue
                npath = path + [nxt]
                nroutes = route_ids + [rid]
                if nxt == b["id"]:
                    return self._ok(location_path=npath, route_ids=nroutes, authority=["world/data/routes.json"])
                seen.add(nxt)
                q.append((nxt, npath, nroutes))
        return self._fail("NO_APPROVED_ROUTE", f"{a['id']} -> {b['id']}")

    def what_happened(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        events = [e for e in self.memory if e.get("location") == loc["id"]]
        return self._ok(location_id=loc["id"], events=events, authority=["world/data/world_memory.json"])

    def what_state(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        return self._ok(location_id=loc["id"], current_state=loc.get("current_state", []), authority=["world/data/locations.json"])

    def what_institutions_near(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        direct = [x for x in self.institutions if x.get("location_id") == loc["id"]]
        same_region = []
        for inst in self.institutions:
            iloc = self.loc_by_id.get(inst.get("location_id"))
            if iloc and iloc.get("physical_zone_id") == loc.get("physical_zone_id") and inst not in direct:
                same_region.append(inst)
        return self._ok(location_id=loc["id"], direct=direct, same_region=same_region, authority=["world/data/league_institutions.json"])

    def what_economy(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        region = loc.get("physical_zone_id")
        rows = [x for x in self.economies if x.get("physical_zone_id") == region]
        return self._ok(location_id=loc["id"], physical_zone_id=region, economy=rows, authority=["world/data/economies.json"])

    def what_division_culture(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        ids = []
        if loc.get("division_id"):
            ids.append(loc["division_id"])
        ids.extend(loc.get("division_presence_ids", []))
        ids = list(dict.fromkeys(ids))
        return self._ok(location_id=loc["id"], divisions=[self.div_by_id[x] for x in ids if x in self.div_by_id], authority=["world/data/divisions.json"])

    def what_can_appear_in_scene(self, location: str) -> dict[str, Any]:
        lives = self.who_lives(location)
        loc = self._location(location)
        if not loc:
            return lives
        return self._ok(
            location_id=loc["id"],
            principal_candidates=lives.get("principals", []),
            ordinary_context=lives.get("population_context", []),
            landmarks=loc.get("persistent_landmarks", []),
            rule="Incidental details do not become named canon.",
        )

    def what_is_forbidden(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        locks = []
        for p in self.domain_profiles:
            if p.get("home_anchor") == loc["id"]:
                locks.extend(p.get("forbidden_drift", []))
        return self._ok(location_id=loc["id"], forbidden=list(dict.fromkeys(locks)))

    def what_changed_after(self, event_id: str) -> dict[str, Any]:
        for e in self.memory:
            if e.get("event_id") == event_id:
                return self._ok(event=e, authority=["world/data/world_memory.json"])
        return self._fail("UNKNOWN_EVENT", event_id)

    def what_region_contains(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        return self._ok(location_id=loc["id"], physical_zone_id=loc.get("physical_zone_id"))

    def what_atlas_layers_contain(self, location: str) -> dict[str, Any]:
        loc = self._location(location)
        if not loc:
            return self._fail("UNKNOWN_LOCATION", location)
        layers = ["PHYSICAL"]
        if loc.get("division_id") or loc.get("division_presence_ids"):
            layers.append("DIVISION")
        if loc.get("owner_character_id") or loc.get("owner_character_ids"):
            layers.append("OWNER_DOMAIN")
        if loc.get("access_route_ids"):
            layers.append("ROADS_TRAVEL")
        if loc.get("current_state"):
            layers.append("WORLD_STATE")
        if "encounter" in str(loc.get("location_type", "")):
            layers.append("ENCOUNTER")
        return self._ok(location_id=loc["id"], atlas_layers=layers)

    @staticmethod
    def _ok(**kwargs: Any) -> dict[str, Any]:
        return {"ok": True, **kwargs}

    @staticmethod
    def _fail(code: str, detail: str) -> dict[str, Any]:
        return {"ok": False, "code": code, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("args", nargs="*")
    ns = parser.parse_args()
    r = UniverseResolver()
    table = {
        "WHERE_IS": r.where_is,
        "WHO_LIVES": r.who_lives,
        "HOW_TO_TRAVEL": r.how_to_travel,
        "WHAT_HAPPENED": r.what_happened,
        "WHAT_STATE": r.what_state,
        "WHAT_INSTITUTIONS_NEAR": r.what_institutions_near,
        "WHAT_ECONOMY": r.what_economy,
        "WHAT_DIVISION_CULTURE": r.what_division_culture,
        "WHAT_CAN_APPEAR_IN_SCENE": r.what_can_appear_in_scene,
        "WHAT_IS_FORBIDDEN": r.what_is_forbidden,
        "WHAT_CHANGED_AFTER": r.what_changed_after,
        "WHAT_REGION_CONTAINS": r.what_region_contains,
        "WHAT_ATLAS_LAYERS_CONTAIN": r.what_atlas_layers_contain,
    }
    fn = table.get(ns.query.upper())
    if not fn:
        print(json.dumps({"ok": False, "code": "UNKNOWN_QUERY"}))
        return 2
    try:
        result = fn(*ns.args)
    except TypeError:
        result = {"ok": False, "code": "BAD_ARGUMENTS"}
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
