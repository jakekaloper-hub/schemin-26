#!/usr/bin/env python3
"""Fail-closed integrity audit for Schemin Commonwealth visual library.

Run from any working directory:
  python3 docs/visual/verify_assets.py
Checks local binary files against manifest digests; no network or deployment writes.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/visual/manifest.json"
SOURCE = ROOT / "canon/characters/APPROVED_LINEUP_2026_10_18.json"


def safe_file(relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("invalid relative asset path")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("unsafe relative asset path")
    resolved = (ROOT / candidate).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise ValueError("asset resolves outside repository")
    return resolved


def validate():
    registry = json.loads(MANIFEST.read_text(encoding="utf-8"))
    upstream = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = registry["assets"]
    canonical = {item["character_id"]: item for item in upstream["individuals"]}
    errors = []
    if len(rows) != len(canonical) or len({r["id"] for r in rows}) != len(rows):
        errors.append("MANIFEST_MEMBERSHIP_DRIFT")
    for row in rows:
        id_ = row["id"]
        original = canonical.get(id_)
        if original is None:
            errors.append(f"{id_}: UNKNOWN_CHARACTER")
            continue
        if row.get("asset_path") != original["crop"] or row.get("expected_sha256") != original["crop_sha256"]:
            errors.append(f"{id_}: CANON_RECORD_MISMATCH")
            continue
        if row.get("visibility") != "internal" or "HOLD" not in row.get("approval", ""):
            errors.append(f"{id_}: APPROVAL_OR_PRIVACY_ESCALATION")
        try:
            path = safe_file(row["asset_path"])
            payload = path.read_bytes()
            actual = hashlib.sha256(payload).hexdigest()
            if not payload.startswith(bytes.fromhex("89504e470d0a1a0a")):
                errors.append(f"{id_}: INVALID_PNG")
            if actual != row["expected_sha256"]:
                errors.append(f"{id_}: SHA256_MISMATCH")
        except (ValueError, OSError) as exc:
            errors.append(f"{id_}: MISSING_OR_UNSAFE_ASSET ({exc})")
    print(f"records={len(rows)} canonical={len(canonical)} errors={len(errors)}")
    for issue in errors:
        print("FAIL", issue)
    if errors:
        raise SystemExit(1)
    print("PASS: all referenced source assets match canonical hashes; Umpire approval remains separate")


if __name__ == "__main__":
    validate()
