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

    for conflict in authority.get("source_visual_conflicts", []):
        if (
            conflict.get("character_id") == character_id
            and conflict.get("state") == "ACTIVE_CANON_VISUAL_CONFLICT_HOLD"
            and sha.lower() == conflict.get("affected_expected_sha256", "").lower()
        ):
            return {
                "state": "GENERATION_BLOCKED",
                "reason": "ACTIVE_VISUAL_CANON_CONFLICT",
                "character_id": character_id,
                "review_gate": conflict["state"],
                "source_sha256": sha,
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


def resolve_approved_lineup_presentation(character_ids, repository_root=None):
    """Return current Commissioner-approved appearance evidence, not a render permit.

    This is deliberately independent of PRIMARY source-image SHA approvals and
    native provider-mount capability. It fails closed on missing/mismatched
    original lineup bytes, owner crop bytes, owner ID or owner-specific deltas.
    """
    import hashlib

    def file_sha(p):
        with p.open("rb") as handle:
            return hashlib.file_digest(handle, "sha256").hexdigest()

    root = Path(repository_root) if repository_root is not None else ROOT.parents[1]
    master_path = root / "canon/characters/APPROVED_LINEUP_2026_10_18.json"
    if not master_path.is_file():
        return {"state": "GENERATION_BLOCKED", "reason": "CURRENT_APPROVED_LINEUP_UNAVAILABLE"}
    master = json.loads(master_path.read_text())
    members = {x["character_id"]: x for x in master.get("individuals", [])}
    if (not isinstance(character_ids, list) or not character_ids
            or any(not isinstance(x, str) for x in character_ids)
            or len(character_ids) != len(set(character_ids))
            or len(members) != 12 or not set(character_ids).issubset(members)):
        return {"state": "GENERATION_BLOCKED", "reason": "LINEUP_CHARACTER_SET_INVALID"}
    image_path = root / master["stored_repository_path"]
    if not image_path.is_file() or file_sha(image_path) != master["sha256"]:
        return {"state": "GENERATION_BLOCKED", "reason": "LINEUP_APPROVED_MASTER_SHA256_FAILED"}
    hmb = master.get("supporting_hmb_correction", {})
    if "CHAR-AUSTIN-BYARS" in character_ids:
        hp = root / hmb.get("path", "")
        if not hp.is_file() or file_sha(hp) != hmb.get("sha256"):
            return {"state": "GENERATION_BLOCKED", "reason": "HMB_CORRECTION_EVIDENCE_MISSING"}
    subjects = []
    for cid in character_ids:
        entry = members[cid]
        crop_path = root / entry["crop"]
        delta_path = root / entry["appearance_delta"]
        if not crop_path.is_file() or file_sha(crop_path) != entry["crop_sha256"]:
            return {"state": "GENERATION_BLOCKED", "reason": "LINEUP_OWNER_CROP_SHA256_FAILED", "character_id": cid}
        if not delta_path.is_file():
            return {"state": "GENERATION_BLOCKED", "reason": "LINEUP_OWNER_DELTA_MISSING", "character_id": cid}
        delta = json.loads(delta_path.read_text())
        if (delta.get("character_id") != cid
                or delta.get("lineup_parent_sha256") != master["sha256"]
                or delta.get("derived_crop_sha256") != entry["crop_sha256"]
                or delta.get("primary_source_supersession_approved") is not False):
            return {"state": "GENERATION_BLOCKED", "reason": "LINEUP_OWNER_DELTA_PROVENANCE_FAILED", "character_id": cid}
        subjects.append({
            "character_id": cid,
            "presentation": delta["approved_visual_assertions"],
            "physical_constraints": delta["physical_engine_delta"],
            "spatial_anchor": delta["spatial_anchor"],
            "crop_path": entry["crop"],
            "crop_sha256": entry["crop_sha256"],
            "not_authorized_as_primary_photo": True,
        })
    return {
        "state": "COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE",
        "master_lineup_sha256": master["sha256"],
        "requested_character_ids": list(character_ids),
        "subjects": subjects,
        "image_generation_eligible": False,
        "C1_visual_QA_passed": False,
        "T15": "HOLD",
        "T16": "HOLD",
        "next_gate": "Existing PRIMARY source and native binding controls plus actual generated-image identity QA",
    }
