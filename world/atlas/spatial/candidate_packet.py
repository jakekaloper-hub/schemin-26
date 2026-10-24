"""Derived, explicitly noncanonical spatial packets for existing Central Basin consumers."""
from __future__ import annotations
from world.atlas.spatial.candidate_validation import load_candidate, validate_candidate
from world.engine.central_basin_pilot import build_central_basin_pilot


def build_candidate_spatial_packet(date: str = "2026-10-21") -> dict:
    data = load_candidate()
    failures = validate_candidate(data)
    if failures:
        return {"ok": False, "code": "INVALID_SPATIAL_CANDIDATE", "errors": failures}
    matches = [s for s in data["scenarios"] if s["date"] == date]
    if len(matches) != 1:
        return {"ok": False, "code": "UNMODELED_SCENARIO_DATE", "date": date}
    baseline = build_central_basin_pilot()
    if not baseline["ok"]:
        return {"ok": False, "code": "SOURCE_PILOT_FAILED", "source": baseline}
    known = {item["id"] for item in baseline["shared_world_facts"]["anchors"]}
    candidate = {item["location_id"] for item in data["anchors"]}
    if known != candidate:
        return {"ok": False, "code": "CANON_ANCHOR_PARITY_FAILURE"}
    shared = {
        "context_id": baseline["shared_world_facts"]["context_id"],
        "region_id": baseline["shared_world_facts"]["region_id"],
        "canonical_anchor_ids": sorted(known),
        "candidate_coordinate_reference": data["coordinate_reference"],
        "candidate_location_geometry": data["anchors"] + data["route_intermediates"],
        "candidate_route_geometry": data["paths"],
        "scenario": matches[0],
        "geometry_status": "SYNTHETIC_UNAPPROVED",
        "canonical_world_mutation": False,
    }
    return {"ok": True, "shared_candidate_spatial_context": shared,
            "memo": {"context_id": shared["context_id"], "spatial": shared},
            "novel": {"context_id": shared["context_id"], "spatial": shared},
            "atlas": {"context_id": shared["context_id"], "spatial": shared},
            "art_environment": {"context_id": shared["context_id"], "spatial": shared,
                                "approved_cinematic_reference": False},
            "publication_status": "UNPUBLISHED_TEST_ONLY"}
