"""Mission 175 Central Basin: read-only, source-backed Memo/Novel scene packets."""
from __future__ import annotations

from world.engine.universe_resolver import UniverseResolver
from world.engine.civilization_consumers import resolve_scene_context

ANCHORS = ("LOC-LEAGUE-CHAMBER", "LOC-LEAGUE-ARCHIVE", "LOC-PITTSYS-BOOK")
LEGS = (("LOC-LEAGUE-ARCHIVE", "LOC-LEAGUE-CHAMBER"), ("LOC-LEAGUE-CHAMBER", "LOC-PITTSYS-BOOK"))


def build_central_basin_pilot() -> dict:
    resolver = UniverseResolver()
    anchors = []
    for loc_id in ANCHORS:
        loc = resolver.loc_by_id.get(loc_id)
        if not loc or loc.get("physical_zone_id") != "REG-CENTRAL-BASIN":
            return {"ok": False, "code": "INVALID_BASIN_ANCHOR", "location_id": loc_id}
        anchors.append({
            "id": loc_id,
            "name": loc["name"],
            "canon_status": loc["canon_status"],
            "landmarks": loc["persistent_landmarks"],
            "source_provenance": loc["source_provenance"],
            "open_questions": loc.get("open_questions", []),
        })
    journeys = []
    for start, end in LEGS:
        route = resolver.how_to_travel(start, end)
        if not route["ok"]:
            return {"ok": False, "code": "UNVERIFIED_ROUTE", "start": start, "end": end}
        journeys.append({"start": start, "end": end, "route": route})
    views = {consumer: resolve_scene_context("LOC-LEAGUE-CHAMBER", consumer)
             for consumer in ("memo", "novel", "atlas", "art_environment")}
    if not all(v["ok"] for v in views.values()):
        return {"ok": False, "code": "CONSUMER_CONTEXT_FAILED"}
    ids = {v["context_id"] for v in views.values()}
    if len(ids) != 1:
        return {"ok": False, "code": "CONSUMER_CONTEXT_DRIFT"}
    shared = {
        "region_id": "REG-CENTRAL-BASIN",
        "context_id": next(iter(ids)),
        "anchors": anchors,
        "verified_route_legs": journeys,
        "ordinary_life": views["memo"]["ordinary_life"],
        "economic_activities": views["memo"]["economic_activities"],
        "provenance": views["memo"]["provenance"],
    }
    memo = {
        "format": "MEMO_SCENE_CONTEXT_DRAFT",
        "world_facts": shared,
        "scene_focus": "Institutional and commercial life around the Chamber, Archive and Book",
        "background": views["memo"]["scene_support"],
        "publication_status": "UNPUBLISHED_INTERPRETIVE_DEMO",
        "restrictions": ["NO_INVENTED_MATCH_RESULT", "NO_NAMED_NPCS", "NO_CANON_PROMOTION"],
    }
    novel = {
        "format": "NOVEL_SCENE_CONTEXT_DRAFT",
        "world_facts": shared,
        "scene_focus": "Ordinary routines and record-keeping continue between League encounters",
        "background": views["novel"]["scene_support"],
        "pov_rule": "TWELVE_OWNER_POV_ONLY; NO_NPC_POV",
        "publication_status": "UNPUBLISHED_INTERPRETIVE_DEMO",
        "restrictions": ["NO_UNVERIFIED_HISTORY", "NO_NAMED_NPCS", "NO_CANON_PROMOTION"],
    }
    return {"ok": True, "shared_world_facts": shared, "memo_packet": memo,
            "novel_packet": novel, "atlas_view": views["atlas"],
            "environment_art_view": views["art_environment"],
            "gate": "SIMULATED_DEVELOPMENT_ONLY"}
