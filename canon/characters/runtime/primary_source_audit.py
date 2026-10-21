"""Audit original approved primary JPEG bytes without silent supplementary fallback."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REGISTER = Path("canon/characters/reference_sources_v1.json")

def audit(root=ROOT):
    registry = json.loads((root / REGISTER).read_text())
    records = []
    for entry in registry["entries"]:
        path = root / entry["repository_path"]
        record = {"character_id": entry["character_id"], "repository_path": entry["repository_path"],
                  "expected_sha256": entry["expected_sha256"]}
        if not path.is_file():
            record.update(state="SOURCE_BYTES_REQUIRED", actual_sha256=None)
        else:
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            jpeg = data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9")
            expected_size = entry["observed_library_size_bytes"]
            ok = digest == entry["expected_sha256"] and jpeg and len(data) == expected_size
            record.update(state="PRIMARY_BYTES_VERIFIED" if ok else "PRIMARY_BYTES_MISMATCH",
                          actual_sha256=digest, size_bytes=len(data), jpeg_signature_valid=jpeg)
        records.append(record)
    counts = {state: sum(x["state"] == state for x in records) for state in
              ("PRIMARY_BYTES_VERIFIED", "SOURCE_BYTES_REQUIRED", "PRIMARY_BYTES_MISMATCH")}
    state = ("PRIMARY_BYTES_VERIFIED" if counts["PRIMARY_BYTES_VERIFIED"] == 12
             else "GENERATION_BLOCKED" if counts["PRIMARY_BYTES_MISMATCH"]
             else "SOURCE_BYTES_REQUIRED")
    return {"state": state, "counts": counts, "records": records,
            "renderer_mount_proven": False, "generation_eligible": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing-for-audit", action="store_true",
                        help="Inventory-only; never means production eligibility")
    args = parser.parse_args()
    outcome = audit()
    print(json.dumps(outcome, indent=2))
    if outcome["state"] == "PRIMARY_BYTES_VERIFIED":
        return 0
    if args.allow_missing_for_audit and outcome["state"] == "SOURCE_BYTES_REQUIRED":
        return 0
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
