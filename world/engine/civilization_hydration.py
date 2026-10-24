"""Read-only cross-publication hydration using the existing Universe scene contract.

This is an executable pre-production handoff, not a published Memo or Novel job.
"""
from __future__ import annotations

from world.engine.central_basin_pilot import build_central_basin_pilot


def build_central_basin_hydration() -> dict:
    pilot = build_central_basin_pilot()
    if not pilot["ok"]:
        return pilot
    facts = pilot["shared_world_facts"]
    first_leg = facts["verified_route_legs"][0]
    return {
        "ok": True,
        "contract": "world/contracts/WORLD_NARRATIVE_HYDRATION_CONTRACT_V1.md",
        "LOC_ID": "LOC-LEAGUE-CHAMBER",
        "REGION_ZONE": facts["region_id"],
        "ARRIVAL_ROUTE": first_leg["route"]["route_ids"],
        "ENTERING_WORLD_STATE": "UNKNOWN_AT_WEEK_SPECIFIC_TIME",
        "PRIOR_MEMORY": "UNKNOWN_UNTIL_VERIFIED_EVENT_CONTEXT",
        "ORDINARY_WORLD_LIFE": facts["ordinary_life"],
        "MATERIAL_CONSTRAINTS": facts["economic_activities"],
        "PUBLIC_KNOWLEDGE": "NOT_RESOLVED",
        "POV_KNOWLEDGE": "NOT_RESOLVED",
        "EVENT_DELTA": "NONE_PROPOSED",
        "DEPARTURE_STATE": "UNCHANGED",
        "IMAGE_TELLS": ["existing institutional landmarks", "ordinary background labor"],
        "PROSE_TELLS": ["continuity of civic routines between encounters"],
        "UNKNOWN_FORBIDDEN_INVENTIONS": ["new named NPCs", "invented historical results", "unapproved location IDs"],
        "memo_packet": pilot["memo_packet"],
        "novel_packet": pilot["novel_packet"],
        "publication_eligible": False,
    }
