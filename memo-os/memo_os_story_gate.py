"""Fail-closed creative-story gate for new publication-candidate scene packets.

This supplements structural checks; it does not authorize a renderer or replace the Umpire.
Existing historical/legacy packets are unchanged unless publication_candidate=True.
"""
from __future__ import annotations

REQUIRED = (
    "verified_week_event", "source_receipt", "causal_action", "visible_consequence",
    "atlas_dependency", "character_relationship", "camera_decisive_instant",
    "non_reusable_league_detail", "independent_editorial_review",
)
REJECTED_GRAMMARS = {"static_ensemble_portrait", "generic_council_lineup", "decorative_character_rollcall"}


def validate_story_gate(packet: dict) -> list[str]:
    if packet.get("publication_candidate") is not True:
        return []
    story = packet.get("story_first")
    if not isinstance(story, dict):
        return ["publication candidate missing story_first evidence"]
    errors = []
    for key in REQUIRED:
        val = story.get(key)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"missing story_first.{key}")
    if story.get("visual_grammar") in REJECTED_GRAMMARS:
        errors.append("rejected generic visual grammar")
    if story.get("most_principals_acting") is not True:
        errors.append("principals lack consequential action")
    if story.get("atlas_necessary") is not True:
        errors.append("atlas is a replaceable backdrop")
    if story.get("independent_editorial_verdict") != "PASS":
        errors.append("independent editorial acceptance missing")
    if story.get("source_fact_classification") not in {"VERIFIED_FACT", "COMMISSIONER_SUPPLIED_FACT"}:
        errors.append("no supported current-week fact anchor")
    return errors
