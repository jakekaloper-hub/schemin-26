#!/usr/bin/env python3
"""Source-controlled, read-only Atlas to Unreal preview export.

Run from repository root. Refuses to export malformed locations. No geometry,
characters, live sports claims, or world-state mutations are generated.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

SOURCE = Path("world/data/locations.json")
COORDINATES = "schemin-local-v1 (abstract, non-metric)"
STATUSES = {"PERMANENT_CANON", "PROVISIONAL_CANON", "INTERPRETIVE_CANON"}
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")

def export(data: dict, commit: str, source_sha256: str) -> dict:
    if data.get("coordinate_space") != COORDINATES:
        raise ValueError("unexpected source coordinate system")
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("full source commit required")
    if not isinstance(source_sha256, str) or not re.fullmatch(r"[a-f0-9]{64}", source_sha256):
        raise ValueError("full source SHA-256 required")
    results = []
    seen = set()
    for item in data.get("locations", []):
        ident = item.get("id")
        if not isinstance(ident, str) or not IDENTIFIER.fullmatch(ident) or ident in seen:
            raise ValueError("invalid or duplicate location ID")
        seen.add(ident)
        if item.get("canon_status") not in STATUSES:
            raise ValueError("unknown canon classification: " + ident)
        pos = item.get("abstract_position")
        if not isinstance(pos, list) or len(pos) != 2 or any(type(n) not in (int, float) or not math.isfinite(n) for n in pos):
            raise ValueError("invalid abstract coordinates: " + ident)
        results.append({
            "location_id": ident,
            "display_name": item.get("name"),
            "source_canon_status": item["canon_status"],
            "region_id": item.get("physical_zone_id"),
            "owner_character_id": item.get("owner_character_id"),
            "abstract_position": pos,
            "landmarks": item.get("persistent_landmarks", []),
            "preview_only": True,
            "character_spawning_allowed": False,
            "metric_scale_approved": False,
            "canon_writeback_allowed": False,
        })
    if not results:
        raise ValueError("empty locations collection")
    return {
        "schema_version": "schemin.unreal.preview.v0.1",
        "authority": "DERIVED_NON_CANONICAL_PREVIEW",
        "source_repository": "jakekaloper-hub/schemin-26",
        "source_path": str(SOURCE),
        "source_commit": commit,
        "source_sha256": source_sha256,
        "coordinate_space": COORDINATES,
        "locations": sorted(results, key=lambda x: x["location_id"]),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    # Export the immutable committed source; working-tree edits cannot acquire a
    # misleading commit provenance label.
    raw = subprocess.check_output(["git", "show", f"{commit}:{SOURCE.as_posix()}"])
    result = export(json.loads(raw), commit, hashlib.sha256(raw).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print("Unreal preview manifest exported:", len(result["locations"]), "locations")

if __name__ == "__main__":
    main()
