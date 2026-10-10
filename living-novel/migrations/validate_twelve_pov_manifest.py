#!/usr/bin/env python3
"""Fail-closed, candidate-scene POV manifest validator for the Twelve migration.

Usage: python living-novel/migrations/validate_twelve_pov_manifest.py
          --registry path/to/twelve_principals.json --manifest path/to/scenes.json
Only validates explicit scene metadata; prose-level narratorial leakage requires editorial QA.
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED = ("scene_id", "story_time", "event_id", "principal_pov_id",
            "knowledge_before", "knowledge_acquired", "knowledge_after",
            "objective", "cost", "decision", "consequence_out",
            "cross_path_dependencies", "spoiler_boundary",
            "duplicate_event_rule", "world_state_in", "world_state_out")
BANNED = {"edrin", "edin", "oren", "archive", "witness", "omniscient", "narrator"}


def validate(registry, scenes):
    errors = []
    if not isinstance(registry, dict) or not isinstance(registry.get("principals"), list):
        return ["Registry must contain a 'principals' array"]
    principals = registry["principals"]
    if len(principals) != 12 or not all(isinstance(x, str) and x.strip() for x in principals):
        errors.append("Registry must contain exactly 12 nonempty principal IDs")
    if len(set(principals)) != len(principals):
        errors.append("Registry contains duplicate principal IDs")
    if any(x.casefold() in BANNED for x in principals if isinstance(x, str)):
        errors.append("Registry contains a prohibited narrator ID")
    if not isinstance(scenes, list) or not scenes:
        return errors + ["Scene manifest must be a nonempty array"]
    seen = set()
    for idx, scene in enumerate(scenes):
        loc = f"scenes[{idx}]"
        if not isinstance(scene, dict):
            errors.append(f"{loc}: must be object")
            continue
        for field in REQUIRED:
            if field not in scene:
                errors.append(f"{loc}: missing {field}")
        scene_id = scene.get("scene_id")
        if not isinstance(scene_id, str) or not scene_id.strip():
            errors.append(f"{loc}: invalid scene_id")
        elif scene_id in seen:
            errors.append(f"{loc}: duplicate scene_id {scene_id}")
        else:
            seen.add(scene_id)
        pov = scene.get("principal_pov_id")
        if not isinstance(pov, str) or pov not in principals:
            errors.append(f"{loc}: unlicensed principal_pov_id {pov!r}")
        for key in ("knowledge_before", "knowledge_acquired", "knowledge_after", "cross_path_dependencies"):
            if key in scene and not isinstance(scene[key], list):
                errors.append(f"{loc}: {key} must be array")
        for key in ("world_state_in", "world_state_out"):
            if key in scene and not isinstance(scene[key], (str, dict)):
                errors.append(f"{loc}: {key} must be state ref or object")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
        scenes = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"HOLD: missing/unreadable source: {exc}", file=sys.stderr)
        return 2
    errors = validate(registry, scenes)
    for error in errors:
        print(f"HOLD: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"PASS: validated {len(scenes)} scenes against exactly 12 principal IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
