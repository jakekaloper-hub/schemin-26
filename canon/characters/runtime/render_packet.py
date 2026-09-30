"""Deterministic minimal character context builder.
Normal production receives active CCCP fields only; historical/superseded material is never accepted as appearance authority.
"""
from dataclasses import dataclass
from typing import Tuple, Mapping, Any

@dataclass(frozen=True)
class CharacterRenderPacket:
    character_id: str
    active_identity: str
    canon_version: str
    primary_asset: Any
    immutable_visual_dna: Tuple[str,...]
    continuity_state: Mapping[str,str]
    negative_locks: Tuple[str,...]
    scene_variables: Mapping[str,str]
    historical_context_included: bool=False

def build_character_render_packet(*, character_id, active_identity, canon_version, primary_asset, immutable_visual_dna, continuity_state=None, negative_locks=(), scene_variables=None, authority_class="CANONICAL_ACTIVE", historical_context=None):
    if authority_class!="CANONICAL_ACTIVE":
        return {"state":"GENERATION_BLOCKED","reason":"NON_ACTIVE_IDENTITY_AUTHORITY"}
    if primary_asset is None:
        return {"state":"GENERATION_BLOCKED","reason":"PRIMARY_ASSET_REQUIRED"}
    if historical_context:
        # History may inform narrative context but cannot mutate identity fields.
        forbidden={"active_identity","primary_asset","immutable_visual_dna","negative_locks","character_id"}
        if forbidden.intersection(historical_context):
            return {"state":"GENERATION_BLOCKED","reason":"HISTORICAL_CONTEXT_IDENTITY_OVERRIDE"}
    return {"state":"PACKET_COMPILED","packet":CharacterRenderPacket(
        character_id=character_id,active_identity=active_identity,canon_version=canon_version,
        primary_asset=primary_asset,immutable_visual_dna=tuple(immutable_visual_dna),
        continuity_state=dict(continuity_state or {}),negative_locks=tuple(negative_locks),
        scene_variables=dict(scene_variables or {}),historical_context_included=bool(historical_context))}
