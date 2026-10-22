"""Additive Memo OS scene-direction validation and specialist selection.

Advisory only: never mutates canon, approves a raster, or replaces Bullpen Core.
"""
from __future__ import annotations
from typing import Any

SPECIALISTS = {
    "Doug Chiang": ("production_design", "Visual Direction Lead"),
    "Dylan Cole": ("environment_design", "World/Atlas"),
    "Joe Letteri": ("character_vfx", "Visual Direction Lead"),
    "Ngila Dickson": ("costume", "Librarian"),
    "Andy Serkis": ("performance", "Beat Writer"),
    "Rob Alonzo": ("stunt_blocking", "Visual Direction Lead"),
    "James Baxter": ("pose_silhouette", "Visual Direction Lead"),
    "Frank Masi": ("unit_stills", "Visual Direction Lead"),
    "John Knoll": ("vfx_pipeline", "Architect"),
    "Jill Bogdanowicz": ("color_finishing", "Publication Design"),
    "Thelma Schoonmaker": ("editing", "Beat Writer"),
    "Randy Thom": ("sound_motion", "Visual Direction Lead"),
}
ROUTES = {
    "combat": ("performance", "stunt_blocking", "pose_silhouette", "unit_stills", "character_vfx"),
    "dialogue": ("performance", "costume", "unit_stills", "editing"),
    "environment": ("production_design", "environment_design", "unit_stills"),
    "aftermath": ("performance", "pose_silhouette", "unit_stills", "editing"),
    "motion": ("performance", "stunt_blocking", "vfx_pipeline", "sound_motion", "editing"),
}
REQUIRED = (
    "scene_id", "beat_id", "narrative_objective", "intensity", "scene_type",
    "character_intentions", "blocking", "camera", "costume_state",
    "environment", "continuity", "typography_safe", "reference_receipts",
    "director_route",
)
INTENSITY = {"grounded", "epic", "mythic"}
SCENE_TYPES = set(ROUTES)
BLOCKING_KEYS = ("positions", "eyelines", "action_axis", "physical_contact", "silhouette")
CAMERA_KEYS = ("position", "shot_scale", "motivated_light", "decisive_instant", "focal_hierarchy")
ENV_KEYS = ("atlas_location", "foreground", "midground", "background", "visible_landmarks")
CONTINUITY_KEYS = ("entering_state", "exiting_state", "forbidden_mutations")


def select_specialists(scene_type: str) -> list[dict[str, str]]:
    if scene_type not in ROUTES:
        raise ValueError("unknown scene type")
    fields = ROUTES[scene_type]
    return [{"name": n, "domain": d, "sponsor": sponsor, "mode": "PUBLISHED_METHOD_LENS"}
            for n, (d, sponsor) in SPECIALISTS.items() if d in fields]


def validate_scene(packet: dict[str, Any]) -> list[str]:
    errors = []
    for key in REQUIRED:
        if key not in packet:
            errors.append(f"missing {key}")
    if errors:
        return errors
    for key in ("scene_id", "beat_id", "narrative_objective"):
        if not isinstance(packet[key], str) or not packet[key].strip():
            errors.append(f"{key} must be nonempty")
    if packet["intensity"] not in INTENSITY:
        errors.append("invalid intensity")
    if packet["scene_type"] not in SCENE_TYPES:
        errors.append("invalid scene_type")
    for key, subfields in (("blocking", BLOCKING_KEYS), ("camera", CAMERA_KEYS),
                           ("environment", ENV_KEYS), ("continuity", CONTINUITY_KEYS)):
        obj = packet[key]
        if not isinstance(obj, dict):
            errors.append(f"{key} must be an object")
            continue
        for sub in subfields:
            if sub not in obj or obj[sub] is None:
                errors.append(f"missing {key}.{sub}")
    route = packet["director_route"]
    if not isinstance(route, dict) or not route.get("primary") or not isinstance(route.get("counterweight_plan"), dict):
        errors.append("canonical director route and counterweight plan required")
    if not isinstance(packet["character_intentions"], list):
        errors.append("character_intentions must be an array")
    if not isinstance(packet["reference_receipts"], list):
        errors.append("reference_receipts must be an array")
    if not isinstance(packet["typography_safe"], bool) or packet["typography_safe"] is not True:
        errors.append("typography_safe must be true")
    if not isinstance(packet["costume_state"], dict):
        errors.append("costume_state must be an object")
    return errors


def preflight(packet: dict[str, Any]) -> dict[str, Any]:
    errors = validate_scene(packet)
    if errors:
        return {"status": "BLOCK", "errors": errors, "can_render": False}
    if packet["character_intentions"] and not packet["reference_receipts"]:
        return {"status": "HOLD", "errors": ["character reference receipts unavailable"], "can_render": False}
    return {
        "status": "PREVIS_READY",
        "can_render": False,  # Canonical render eligibility is an independent gate.
        "specialists": select_specialists(packet["scene_type"]),
        "scene_id": packet["scene_id"],
        "requires_independent_raster_qa": True,
    }
