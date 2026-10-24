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


def verify_character_visual_coverage(root: Path = ROOT, registry: dict | None = None) -> dict:
    """Report owner-specific Git bytes for 12 characters; never treat posters as primary."""
    registry = registry or load_registry()
    primary = verify_source_bytes(root, registry)
    records_by_id = {r["character_id"]: r for r in primary["records"]}
    out = []
    for entry in registry.get("entries", []):
        cid = entry["character_id"]
        primary_record = records_by_id[cid]
        row = {
            "character_id": cid, "owner": entry["owner"],
            "primary_sha256": entry["expected_sha256"],
            "primary_state": primary_record["state"],
            "primary_repository_path": entry["repository_path"],
            "visual_reference_path": None, "visual_reference_sha256": None,
            "reference_status": None, "release_eligible": False,
            "renderer_binding_verified": False,
        }
        if primary_record["state"] == "PASS":
            row["visual_reference_path"] = entry["repository_path"]
            row["visual_reference_sha256"] = primary_record["actual_sha256"]
            row["reference_status"] = "PRIMARY_BYTES_VERIFIED_RENDERER_UNPROVEN"
        elif primary_record["state"] == "GENERATION_BLOCKED":
            row["reference_status"] = "PRIMARY_CORRUPT_FAIL_CLOSED"
        else:
            if cid == "CHAR-WILSON-LOOK":
                filename = "W3_COVER_VISUAL_REFERENCE_RECEIPT.json"
                expected_path = f"canon/characters/assets/{cid}/supplementary/WEEK_03_LAST_UNDEFEATED_COVER.png"
                path_key, hash_key = "repository_path", "stored_file_sha256"
            else:
                filename = "OWNER_SPOTLIGHT_2026_RECEIPT.json"
                expected_path = f"canon/characters/assets/{cid}/supplementary/OWNER_SPOTLIGHT_2026.png"
                path_key, hash_key = "stored_repository_path", "stored_sha256"
            receipt_path = root / f"canon/characters/{cid}/{filename}"
            try:
                receipt = json.loads(receipt_path.read_text())
                path = receipt.get(path_key)
                if path != expected_path or receipt.get("character_id") != cid:
                    raise ValueError("owner or path mismatch")
                if cid == "CHAR-WILSON-LOOK":
                    expected_primary = receipt["primary_reference"]["expected_sha256"]
                    assert receipt.get("classification") == "SUPPLEMENTARY_APPEARANCE_AND_HISTORICAL_COVER_ONLY"
                else:
                    expected_primary = receipt.get("primary_expected_sha256")
                    assert receipt.get("supersedes_primary_identity") is False
                    assert receipt.get("production_state") == "HOLD"
                if expected_primary != entry["expected_sha256"]:
                    raise ValueError("primary authority mismatch")
                actual = sha256_bytes((root / path).read_bytes())
                if actual != receipt.get(hash_key):
                    raise ValueError("supplementary source hash mismatch")
                row["visual_reference_path"] = path
                row["visual_reference_sha256"] = actual
                row["reference_status"] = "SUPPLEMENTARY_PREVIEW_ONLY_PRIMARY_REQUIRED"
            except (OSError, KeyError, ValueError, AssertionError, TypeError):
                row["reference_status"] = "NO_TRUSTED_DURABLE_REFERENCE"
        out.append(row)
    verified = sum(r["visual_reference_path"] is not None for r in out)
    primaries = sum(r["primary_state"] == "PASS" for r in out)
    preview = sum(r["reference_status"] == "SUPPLEMENTARY_PREVIEW_ONLY_PRIMARY_REQUIRED" for r in out)
    return {
        "state": "HOLD",
        "total": len(out), "owner_references_verified": verified,
        "primary_sources_verified": primaries,
        "supplementary_only": preview,
        "unavailable": len(out) - verified,
        "final_render_eligible": 0,
        "records": out,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--coverage", action="store_true", help="Report Git-backed per-owner visual reference coverage without promoting renderer eligibility")
    args = parser.parse_args()
    result = verify_character_visual_coverage() if args.coverage else verify_source_bytes()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if args.coverage:
            print(f"{result['state']} visual={result['owner_references_verified']}/{result['total']} primary={result['primary_sources_verified']}/{result['total']} supplementary_only={result['supplementary_only']} final_render_eligible=0")
            return 2
        print(
            f"{result['state']} "
            f"pass={result['pass_count']}/{result['total']} "
            f"missing={result['source_bytes_required_count']} "
            f"blocked={result['blocked_count']}"
        )
    if args.coverage:
        return 2
    if result["state"] == "PASS":
        return 0
    if result["state"] == "SOURCE_BYTES_REQUIRED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
