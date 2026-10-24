"""Forward-only twelve-owner POV acceptance gate for the Living Novel rewrite.

Historical manuscripts are inputs to revision, never silently promoted.
"""
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"canon/characters/CHARACTER_REGISTRY.yaml"
OLD_POV_NAMES=re.compile(r"\b(?:Edrin(?: Vale)?|Edin|Master Oren)\b",re.IGNORECASE)

def canonical_owner_ids() -> set[str]:
    registry=REGISTRY.read_text(encoding="utf-8")
    section=registry.split("\ncharacters:\n",1)
    if len(section)!=2:
        raise ValueError("canonical character registry missing")
    ids=set(re.findall(r"(?m)^  - \{id: (CHAR-[A-Z-]+), owner:",section[1]))
    if len(ids)!=12:
        raise ValueError(f"expected exactly 12 owner identities, got {len(ids)}")
    return ids

def validate_rewrite_scene(scene:dict) -> list[str]:
    errors=[]
    try:
        owners=canonical_owner_ids()
    except ValueError:
        return ["OWNER_REGISTRY_UNRESOLVED"]
    if scene.get("pov_character_id") not in owners:
        errors.append("NON_OWNER_POV_FORBIDDEN")
    if scene.get("pov_class")!="PRINCIPAL_CHARACTER":
        errors.append("INSTITUTIONAL_OR_WITNESS_POV_FORBIDDEN")
    if not scene.get("source_event_ids"):
        errors.append("VERIFIED_EVENT_PROVENANCE_REQUIRED")
    if not scene.get("world_context_id"):
        errors.append("SHARED_WORLD_CONTEXT_REQUIRED")
    if not scene.get("story_time_cutoff"):
        errors.append("STORY_TIME_CUTOFF_REQUIRED")
    if not scene.get("real_owner_boundary_note"):
        errors.append("REAL_OWNER_FIREWALL_REQUIRED")
    if OLD_POV_NAMES.search(scene.get("manuscript_text","")):
        errors.append("RETIRED_INSTITUTIONAL_CHARACTER_IN_MANUSCRIPT")
    if not scene.get("manuscript_text","").strip():
        errors.append("EMPTY_MANUSCRIPT")
    return errors
