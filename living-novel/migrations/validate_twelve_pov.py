#!/usr/bin/env python3
"""Fail-closed Twelve-principal scene manifest validator (migration candidate).

This validates structured scene metadata, not prose interiority or canonical approval.
Usage: python living-novel/migrations/validate_twelve_pov.py REGISTRY.json SCENES.json
"""
import json
import sys
from pathlib import Path


def validate(registry, scenes):
    errors = []
    if not isinstance(registry, dict):
        return ["registry must be an object"]
    principals = registry.get("principals")
    if not isinstance(principals, list) or len(principals) != 12:
        return ["registry must contain exactly twelve principals"]
    ids = [p.get("id") for p in principals if isinstance(p, dict)]
    if len(ids) != 12 or any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != 12:
        return ["principal ids must be twelve distinct nonempty strings"]
    allowed = set(ids)
    if registry.get("status") != "MIGRATION_CANDIDATE_NOT_CANON":
        errors.append("registry status differs from current candidate contract")
    if not isinstance(scenes, list):
        return ["scene manifest must be a JSON list"]
    seen = set()
    for i, scene in enumerate(scenes):
        prefix = f"scene[{i}]"
        if not isinstance(scene, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        sid = scene.get("scene_id")
        if not isinstance(sid, str) or not sid.strip() or sid in seen:
            errors.append(f"{prefix}: missing or duplicate scene_id")
        seen.add(sid)
        pov = scene.get("principal_pov_id")
        if not isinstance(pov, str) or pov not in allowed:
            errors.append(f"{prefix}: invalid principal_pov_id {pov!r}")
        if not isinstance(scene.get("story_time"), str) or not scene["story_time"].strip():
            errors.append(f"{prefix}: missing story_time")
        if pov == "el_nino":
            approved = registry.get("elemental_pov_approval", {})
            receipt = scene.get("elemental_pov_canon_receipt")
            if not isinstance(approved, dict) or approved.get("status") != "FOUNDER_APPROVED":
                errors.append(f"{prefix}: El Niño elemental POV remains unapproved in registry")
            elif not isinstance(receipt, str) or receipt != approved.get("receipt_id") or not receipt:
                errors.append(f"{prefix}: El Niño receipt must match approved registry receipt")
    return errors


def validate_character_provenance(registry, scenes, canon_text):
    """Validate owner identity bindings against canonical owner headings.

    This confirms identity/source linkage only. Appearance, story-time state,
    visual source bytes, and authorizations need separate qualified review.
    """
    if not isinstance(registry, dict) or not isinstance(scenes, list) or not isinstance(canon_text, str):
        return ["character provenance requires registry, scene list, and master canon text"]
    principals = registry.get("principals", [])
    if not isinstance(principals, list) or len(principals) != 12:
        return ["character provenance requires twelve canonical candidates"]
    owners = {}
    for principal in principals:
        if not isinstance(principal, dict):
            return ["malformed principal owner record"]
        pid, owner = principal.get("id"), principal.get("owner_name")
        if not isinstance(pid, str) or not isinstance(owner, str) or not owner.strip():
            return ["principal missing owner name or ID"]
        if pid in owners or ("### " + owner + " /") not in canon_text:
            return ["owner identity not uniquely present in master character canon: " + str(owner)]
        owners[pid] = owner
    errors = []
    source = "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md"
    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            errors.append(f"scene[{i}]: malformed character scene")
            continue
        pov_id = scene.get("principal_pov_id")
        if scene.get("pov_owner_name") != owners.get(pov_id):
            errors.append(f"scene[{i}]: POV owner identity mismatch")
        if scene.get("character_canon_source") != source:
            errors.append(f"scene[{i}]: missing character canon provenance")
        if scene.get("character_state_status") != "REVIEW_REQUIRED":
            errors.append(f"scene[{i}]: invalid candidate state status")
        refs = scene.get("character_refs")
        if not isinstance(refs, list):
            errors.append(f"scene[{i}]: missing character reference list")
            continue
        seen_refs = set()
        for ref in refs:
            if not isinstance(ref, dict):
                errors.append(f"scene[{i}]: malformed character reference")
                continue
            rid = ref.get("principal_id")
            if not isinstance(rid, str) or rid not in owners or rid in seen_refs or rid == pov_id:
                errors.append(f"scene[{i}]: invalid or duplicate character ID")
                continue
            seen_refs.add(rid)
            if ref.get("owner_name") != owners[rid] or ref.get("character_canon_source") != source:
                errors.append(f"scene[{i}]: owner/source mismatch for {rid}")
            if ref.get("state_status") != "REVIEW_REQUIRED":
                errors.append(f"scene[{i}]: unreviewed character state falsely promoted")
    return errors


def validate_character_state_gate(scene, state_receipts, visual_authority):
    """Independent, fail-closed evidence gate for prose state and visual art.

    Evidence records are externally qualified inputs, never self-certified by the scene.
    This validator cannot inspect source image bytes or resolve in-world chronology.
    """
    import re
    errors = []
    if not isinstance(scene, dict) or not isinstance(state_receipts, dict) or not isinstance(visual_authority, dict):
        return ["state gate requires a scene, qualified state receipts, and visual authority"]
    story_time = scene.get("story_time")
    if not isinstance(story_time, str) or not story_time.strip():
        return ["state gate requires story_time"]
    ids = [scene.get("principal_pov_id")]
    refs = scene.get("character_refs")
    if not isinstance(refs, list):
        return ["state gate requires character refs"]
    ids.extend(ref.get("principal_id") for ref in refs if isinstance(ref, dict))
    for pid in ids:
        if not isinstance(pid, str) or not pid:
            errors.append("invalid character identifier")
            continue
        receipt = state_receipts.get(pid)
        if not isinstance(receipt, dict) or receipt.get("status") != "QUALIFIED":
            errors.append(f"{pid}: missing qualified story-time state")
            continue
        if story_time not in receipt.get("story_time_keys", []):
            errors.append(f"{pid}: state not qualified for story_time")
        if not isinstance(receipt.get("authority_path"), str) or not receipt["authority_path"].startswith("canon/"):
            errors.append(f"{pid}: missing canon state source")
    if scene.get("visual_required") is True:
        visual_receipts = scene.get("visual_receipts")
        if not isinstance(visual_receipts, dict):
            return errors + ["character art requires per-character visual receipts"]
        source_hashes = {s["character_id"]: s["expected_sha256"] for s in visual_authority.get("master_lineup", {}).get("stale_for", [])
            if isinstance(s, dict) and isinstance(s.get("character_id"), str) and isinstance(s.get("expected_sha256"), str)}
        for pid in ids:
            receipt = visual_receipts.get(pid)
            if not isinstance(receipt, dict) or receipt.get("status") != "MOUNT_HASH_VERIFIED":
                errors.append(f"{pid}: visual source mount/hash unverified")
                continue
            digest = receipt.get("mounted_sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"{pid}: invalid visual digest")
            if receipt.get("character_id") not in source_hashes:
                errors.append(f"{pid}: active per-owner visual authority unresolved")
            elif digest != source_hashes[receipt["character_id"]]:
                errors.append(f"{pid}: visual digest disagrees with active owner-specific authority")
            if not receipt.get("source_byte_verification_receipt"):
                errors.append(f"{pid}: missing source-byte verification receipt")
    return errors


def main():
    if len(sys.argv) != 3:
        print("usage: validate_twelve_pov.py registry.json scenes.json", file=sys.stderr)
        return 2
    try:
        registry = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        scenes = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        errors = validate(registry, scenes)
    except (OSError, ValueError, TypeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: {len(scenes)} scene records have licensed principal IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
