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
