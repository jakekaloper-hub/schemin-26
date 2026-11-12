#!/usr/bin/env python3
"""Minimal stdlib validator for Story Production Graph V1 candidate.

This does not replace JSON Schema validation or any Schemin authority gate.
It verifies cross-object identity, fail-closed publication invariants, projection
derivation, and dependency reachability on the Week 9 conformance fixture.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "planning/story-production-graph/fixtures/week9_minimal.json"

def load():
    return json.loads(FIXTURE.read_text())

def downstream(edges, changed):
    out = set()
    frontier = [changed]
    while frontier:
        node = frontier.pop()
        for edge in edges:
            if edge["upstream"] == node and edge["downstream"] not in out:
                out.add(edge["downstream"])
                frontier.append(edge["downstream"])
    return out

def validate(data):
    errors = []
    event = data["event"]
    scene = data["scene"]
    chron = data["chronicle"]
    compiler = data["compiler"]

    if scene["event_id"] != event["event_id"]:
        errors.append("SCENE_EVENT_MISMATCH")
    if chron["event_ids"] != [event["event_id"]]:
        errors.append("CHRONICLE_EVENT_MISMATCH")
    if event["authority"]["canon_status"] == "ACCEPTED" and event["authority"]["evidence_status"] != "VERIFIED":
        errors.append("ACCEPTED_EVENT_WITHOUT_VERIFIED_EVIDENCE")
    if chron.get("derived_only") is not True or chron.get("rebuildable") is not True:
        errors.append("CHRONICLE_NOT_DERIVED")
    pub = compiler["publication"]
    if pub.get("authority_mutation_allowed") is not False or pub.get("auto_publish_allowed") is not False:
        errors.append("COMPILER_AUTHORITY_ESCALATION")
    if scene["qa"]["publication_state"] == "ACCEPTED" and not scene["qa"]["required_gates"]:
        errors.append("SCENE_ACCEPTED_WITHOUT_GATES")

    edges = compiler["invalidation"]["dependency_edges"]
    impacted = downstream(edges, event["event_id"]+"::RESULT")
    required = {"SCN-W09-M01-LAST-PUTT", "JOB-W09-M01-PNG", "JOB-W09-M01-MOTION"}
    if not required.issubset(impacted):
        errors.append("INVALIDATION_GRAPH_INCOMPLETE")

    scene_chars = {x["character_id"] for x in scene["cast"]}
    event_chars = {x["entity_id"] for x in event["participants"] if x["entity_type"] == "CHARACTER"}
    if not scene_chars.issubset(event_chars):
        errors.append("SCENE_CAST_NOT_EVENT_BOUND")

    return sorted(set(errors))

if __name__ == "__main__":
    data = load()
    errors = validate(data)
    assert not errors, errors
    impacted = sorted(downstream(data["compiler"]["invalidation"]["dependency_edges"], data["event"]["event_id"]))
    print(json.dumps({
        "state": "STRUCTURAL_CANDIDATE_PASS_NOT_RELEASE_ACCEPTANCE",
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "event_id": data["event"]["event_id"],
        "scene_id": data["scene"]["scene_id"],
        "chronicle_projection": data["chronicle"]["projection_id"],
        "impacted_if_event_changes": impacted
    }, indent=2))
