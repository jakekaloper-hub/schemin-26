"""Durable character-source-byte integrity audit.

This module is deliberately independent of Character Control Plane v2 promotion.
It verifies exact bytes when they exist in the repository and fails closed on
missing or corrupted assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "canon" / "characters" / "reference_sources_v1.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict:
    return json.loads(path.read_text())


def verify_source_bytes(root: Path = ROOT, registry: dict | None = None) -> dict:
    registry = registry or load_registry()
    records = []
    for entry in registry.get("entries", []):
        repo_path = entry["repository_path"]
        path = root / repo_path
        record = {
            "character_id": entry["character_id"],
            "owner": entry["owner"],
            "identity": entry["identity"],
            "active_version": entry["active_version"],
            "approved_reference_id": entry["conversation_file_id"],
            "source_provenance": entry["source_provenance"],
            "expected_sha256": entry["expected_sha256"],
            "repository_path": repo_path,
            "media_type": entry["media_type"],
            "supersession_state": entry["supersession_state"],
        }
        if not path.is_file():
            record.update({
                "state": "SOURCE_BYTES_REQUIRED",
                "reason": "MISSING_DURABLE_BYTES",
                "actual_sha256": None,
                "git_blob_sha": None,
                "byte_size": None,
            })
            records.append(record)
            continue

        data = path.read_bytes()
        actual = sha256_bytes(data)
        blob = git_blob_sha(data)
        record.update({
            "actual_sha256": actual,
            "git_blob_sha": blob,
            "byte_size": len(data),
        })
        if actual != entry["expected_sha256"]:
            record.update({"state": "GENERATION_BLOCKED", "reason": "SOURCE_HASH_MISMATCH"})
        elif len(data) != entry["observed_library_size_bytes"]:
            record.update({"state": "GENERATION_BLOCKED", "reason": "SOURCE_BYTE_SIZE_MISMATCH"})
        else:
            record.update({"state": "PASS", "reason": None})
        records.append(record)

    states = {r["state"] for r in records}
    if "GENERATION_BLOCKED" in states:
        state = "GENERATION_BLOCKED"
    elif "SOURCE_BYTES_REQUIRED" in states:
        state = "SOURCE_BYTES_REQUIRED"
    elif records and all(r["state"] == "PASS" for r in records):
        state = "PASS"
    else:
        state = "HUMAN_REVIEW_REQUIRED"

    return {
        "state": state,
        "total": len(records),
        "pass_count": sum(r["state"] == "PASS" for r in records),
        "source_bytes_required_count": sum(r["state"] == "SOURCE_BYTES_REQUIRED" for r in records),
        "blocked_count": sum(r["state"] == "GENERATION_BLOCKED" for r in records),
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify_source_bytes()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"{result['state']} "
            f"pass={result['pass_count']}/{result['total']} "
            f"missing={result['source_bytes_required_count']} "
            f"blocked={result['blocked_count']}"
        )
    if result["state"] == "PASS":
        return 0
    if result["state"] == "SOURCE_BYTES_REQUIRED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
