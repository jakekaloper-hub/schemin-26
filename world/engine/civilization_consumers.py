"""Read-only scene-context projections for existing Memo, Novel, Atlas and Art contracts.

These are callable adapters; they do not yet alter production renderers.
"""
from __future__ import annotations

from world.engine.universe_resolver import UniverseResolver

CONSUMERS = {"memo", "novel", "atlas", "art_environment"}


def resolve_scene_context(location_id: str, consumer: str) -> dict:
    if consumer not in CONSUMERS:
        return {"ok": False, "code": "UNKNOWN_CONSUMER"}
    resolver = UniverseResolver()
    result = resolver.what_civilization_context(location_id)
    if not result["ok"]:
        return result
    context = result["civilization_context"]
    scene = resolver.what_can_appear_in_scene(location_id)
    if not scene["ok"]:
        return scene
    base = {
        "ok": True,
        "consumer": consumer,
        "location_id": result["location_id"],
        "region_id": context["region_id"],
        "context_id": context["settlement_context_id"],
        "ordinary_life": context["ordinary_life"],
        "economic_activities": context["economic_activities"],
        "provenance": context["provenance"],
        "authority": "READ_ONLY_INTERPRETIVE_CONTEXT",
        "prohibitions": context["restrictions"],
    }
    if consumer == "memo":
        base["scene_support"] = {"landmarks": scene["landmarks"], "background": context["ordinary_life"]}
    elif consumer == "novel":
        base["scene_support"] = {"ambient_population": scene["ordinary_context"], "institutions": context["institutions"]}
    elif consumer == "atlas":
        base["scene_support"] = {"existing_anchors": context["anchor_locations"], "transport": context["transport"]}
    else:
        base["scene_support"] = {"terrain": context["terrain"], "climate": context["climate"], "background": context["ordinary_life"]}
        base["character_rendering_allowed"] = False
    return base
