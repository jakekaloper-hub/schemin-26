"""Current visual-reference authority router.

This layer runs before mount/binding checks. It prevents a stale composite,
generated convenience image, friendly filename, or legacy packet from being
treated as current primary identity authority.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_REGISTRY=ROOT/"reference_sources_v1.json"
AUTHORITY_REGISTRY=ROOT/"VISUAL_REFERENCE_AUTHORITY_V1.json"

def load_source_registry(path=SOURCE_REGISTRY):
    return json.loads(Path(path).read_text())

def load_authority_registry(path=AUTHORITY_REGISTRY):
    return json.loads(Path(path).read_text())

def expected_source(character_id, source_registry=None):
    doc=source_registry or load_source_registry()
    entries=doc.get("entries",[])
    matches=[x for x in entries if x.get("character_id")==character_id]
    if len(matches)!=1:
        return None
    item=matches[0]
    if item.get("approval_state")!="APPROVED":
        return None
    return item

def validate_reference_candidate(character_id,candidate,source_registry=None,authority_registry=None):
    """Return a fail-closed authority verdict for a proposed renderer input.

    candidate must describe the actual input bytes, not merely a filename:
      sha256, asset_id, source_kind, filename.
    """
    expected=expected_source(character_id,source_registry)
    if not expected:
        return {"state":"GENERATION_BLOCKED","reason":"ACTIVE_SOURCE_NOT_RESOLVED"}

    if not isinstance(candidate,dict):
        return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_CANDIDATE_METADATA_REQUIRED"}

    sha=candidate.get("sha256")
    if not sha or len(sha)!=64:
        return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_SOURCE_HASH_REQUIRED"}

    authority=authority_registry or load_authority_registry()
    asset_id=candidate.get("asset_id")
    for q in authority.get("known_non_authoritative_renderer_assets",[]):
        if asset_id and asset_id==q.get("asset_id"):
            return {
                "state":"GENERATION_BLOCKED",
                "reason":"QUARANTINED_OR_DERIVED_ASSET",
                "quarantine_state":q.get("state"),
            }

    master=authority.get("master_lineup",{})
    if candidate.get("asset_id")==master.get("creative_claw_asset_id") or candidate.get("filename")==master.get("name"):
        if character_id in {x.get("character_id") for x in master.get("stale_for",[])}:
            return {"state":"GENERATION_BLOCKED","reason":"MASTER_LINEUP_STALE_FOR_CHARACTER"}
        return {"state":"GENERATION_BLOCKED","reason":"MASTER_LINEUP_NOT_PRODUCTION_AUTHORITY"}

    if candidate.get("source_kind") in {"GENERATED","DERIVED","COMPOSITE","PREVIEW"}:
        return {"state":"GENERATION_BLOCKED","reason":"DERIVED_REFERENCE_CANNOT_SEED_PRODUCTION"}

    if sha.lower()!=expected.get("expected_sha256","").lower():
        return {
            "state":"GENERATION_BLOCKED",
            "reason":"REFERENCE_SOURCE_HASH_MISMATCH",
            "expected_sha256":expected.get("expected_sha256"),
            "observed_sha256":sha,
        }

    return {
        "state":"REFERENCE_AUTHORITY_RESOLVED",
        "character_id":character_id,
        "source_filename":expected.get("source_filename"),
        "expected_sha256":expected.get("expected_sha256"),
        "render_quality":expected.get("render_quality"),
        "active_version":expected.get("active_version"),
    }

def request_authority_state(character_ids,candidates,source_registry=None,authority_registry=None):
    if set(character_ids)!=set(candidates):
        return {"state":"GENERATION_BLOCKED","reason":"REFERENCE_CANDIDATE_SET_MISMATCH","results":[]}
    results=[
        validate_reference_candidate(cid,candidates[cid],source_registry,authority_registry)
        for cid in character_ids
    ]
    return {
        "state":"REFERENCE_AUTHORITY_RESOLVED" if all(x.get("state")=="REFERENCE_AUTHORITY_RESOLVED" for x in results) else "GENERATION_BLOCKED",
        "results":results,
    }
