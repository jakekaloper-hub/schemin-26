#!/usr/bin/env python3
"""Validate the Schemin Atlas Publication Convergence Contract V1."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "world" / "atlas" / "integration" / "ATLAS_PUBLICATION_CONVERGENCE_CONTRACT_V1.json"

REQUIRED_SYSTEMS = {
    "league_truth",
    "character_canon",
    "world_engine",
    "location_control_plane",
    "memo_os",
    "novel_os",
    "visual_grounding",
    "interactive_atlas",
    "world_evolution",
    "publication_release",
}

REQUIRED_HANDOFFS = {
    ("location_control_plane", "memo_os"),
    ("location_control_plane", "novel_os"),
    ("location_control_plane", "visual_grounding"),
    ("memo_os", "world_evolution"),
    ("novel_os", "world_evolution"),
}


def load_contract() -> dict:
    with CONTRACT.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_contract(payload: dict) -> list[str]:
    errors: list[str] = []

    principles = payload.get("binding_principles", {})
    if principles.get("division_spatial_model") != "NONEXCLUSIVE_OVERLAY":
        errors.append("division model must remain NONEXCLUSIVE_OVERLAY")
    if principles.get("world_determines_image") is not True:
        errors.append("world_determines_image must be true")
    if principles.get("image_can_mutate_world") is not False:
        errors.append("image_can_mutate_world must be false")
    if principles.get("candidate_firewall") is not True:
        errors.append("candidate firewall must be enabled")
    if principles.get("mercer_private_leakage_allowed") is not False:
        errors.append("Mercer-private leakage must be prohibited")

    systems = payload.get("systems", [])
    system_ids = {s.get("id") for s in systems}
    if system_ids != REQUIRED_SYSTEMS:
        errors.append(
            f"system coverage mismatch: expected {sorted(REQUIRED_SYSTEMS)}, got {sorted(x for x in system_ids if x)}"
        )

    for system in systems:
        sid = system.get("id", "<unknown>")
        refs = system.get("authority_refs", [])
        if not refs:
            errors.append(f"{sid} has no authority_refs")
        for ref in refs:
            if not (ROOT / ref).exists():
                errors.append(f"{sid} references missing authority file {ref}")
        if not system.get("must_not_write"):
            errors.append(f"{sid} must declare authority exclusions")

    handoffs = payload.get("handoffs", [])
    seen_handoffs = {(h.get("from"), h.get("to")) for h in handoffs}
    for handoff in REQUIRED_HANDOFFS:
        if handoff not in seen_handoffs:
            errors.append(f"missing required handoff {handoff[0]} -> {handoff[1]}")

    for h in handoffs:
        if h.get("from") not in REQUIRED_SYSTEMS:
            errors.append(f"handoff has unknown source {h.get('from')}")
        if h.get("to") not in REQUIRED_SYSTEMS:
            errors.append(f"handoff has unknown target {h.get('to')}")
        if not h.get("artifact") or not h.get("rule"):
            errors.append(f"handoff {h.get('from')} -> {h.get('to')} missing artifact/rule")

    counterweights = payload.get("live_counterweight_evidence", [])
    if len(counterweights) < 3:
        errors.append("at least three live counterweight evidence records are required")
    for item in counterweights:
        if item.get("decision_changed") is not True:
            errors.append(f"{item.get('id')} does not prove a changed decision")
        if not item.get("counterweights"):
            errors.append(f"{item.get('id')} missing counterweights")
        for ref in item.get("evidence_refs", []):
            if not (ROOT / ref).exists():
                errors.append(f"{item.get('id')} references missing evidence {ref}")

    return errors


def validate_repo() -> list[str]:
    return validate_contract(load_contract())


if __name__ == "__main__":
    errors = validate_repo()
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        raise SystemExit(1)
    print("PASS: Atlas Publication Convergence Contract V1")
