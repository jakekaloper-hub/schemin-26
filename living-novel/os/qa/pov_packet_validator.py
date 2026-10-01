"""Fail-closed validation for Novel POV packets."""
from __future__ import annotations

def validate_pov_packet(packet: dict) -> list[str]:
    errors=[]
    if not packet.get("character_id"):
        errors.append("MISSING_CHARACTER_ID")
    if not packet.get("story_time_cutoff"):
        errors.append("MISSING_STORY_TIME_CUTOFF")
    if "verified_knowledge" not in packet:
        errors.append("MISSING_VERIFIED_KNOWLEDGE_FIELD")
    if "unknowns" not in packet:
        errors.append("MISSING_UNKNOWNS_FIELD")
    if "prohibited_knowledge" not in packet:
        errors.append("MISSING_PROHIBITED_KNOWLEDGE_FIELD")
    if not packet.get("attention_bias"):
        errors.append("MISSING_ATTENTION_BIAS")
    if packet.get("real_owner_derived") and not packet.get("real_owner_boundary_note"):
        errors.append("MISSING_REAL_OWNER_FIREWALL")
    if packet.get("pov_class")=="PRINCIPAL_CHARACTER" and not packet.get("fictional_interior_range"):
        errors.append("MISSING_FICTIONAL_INTERIOR_RANGE")
    return errors
