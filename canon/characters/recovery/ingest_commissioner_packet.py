#!/usr/bin/env python3
"""Fail-closed source-byte verification and *optional* staging of the Oct 12 Commissioner packet.

Uses the EXISTING Character Canon and repository paths. It does not approve or
promote divergent visual identity, and does not contact a network service.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
LOCK_REL = Path("canon/characters/recovery/COMMISSIONER_2026_10_12_SOURCE_LOCK.json")
RECEIPT_REL = Path("canon/characters/recovery/COMMISSIONER_2026_10_12_INGEST_RECEIPT.json")


class IntegrityError(ValueError):
    """Reject changed bytes, ambiguous mappings or an unexpected archive."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def verify_packet(archive: Path, pins: dict) -> list[dict]:
    rows = pins.get("assets")
    if not isinstance(rows, list) or len(rows) != 12:
        raise IntegrityError("Expected exactly twelve pinned references")
    ids = [x["character_id"] for x in rows]
    if len(set(ids)) != 12:
        raise IntegrityError("Duplicate character IDs in pinned references")
    expected_paths = {x["archive_member"] for x in rows}
    if len(expected_paths) != 12:
        raise IntegrityError("Duplicate reference paths in pinned references")

    targets = {x.get("repository_path", x["archive_member"]) for x in rows}
    if len(targets) != 12:
        raise IntegrityError("Duplicate durable storage paths")

    if digest(archive.read_bytes()) != pins["source_archive_sha256"]:
        raise IntegrityError("Archive hash differs from verified Commissioner packet")

    with zipfile.ZipFile(archive) as z:
        members = z.namelist()
        if len(members) != len(set(members)):
            raise IntegrityError("Duplicate ZIP members")
        if set(members) != expected_paths | {"CHARACTER_UPLOAD_RECEIPTS.json"}:
            raise IntegrityError("ZIP contains missing or unexpected members")
        receipt = json.loads(z.read("CHARACTER_UPLOAD_RECEIPTS.json"))
        embedded = receipt.get("items", [])
        if len(embedded) != 12:
            raise IntegrityError("Embedded Commissioner receipt is not 12/12")
        indexed = {x["character_id"]: x for x in embedded}
        if len(indexed) != 12 or set(indexed) != set(ids):
            raise IntegrityError("Embedded receipt has missing, extra or repeated IDs")
        validated = []
        for item in rows:
            member = item["archive_member"]
            character_id = item["character_id"]
            prefix = "canon/characters/assets/" + character_id + "/primary/"
            target = item.get("repository_path", member)
            owner_prefix = "canon/characters/assets/" + character_id + "/"
            role = item.get("asset_role")
            if (not member.startswith(prefix) or "/../" in member or chr(92) in member
                    or not target.startswith(owner_prefix) or ".." in Path(target).parts
                    or chr(92) in target):
                raise IntegrityError("Unsafe path or cross-character asset mapping")
            required_folder = {
                "PRIMARY_EXACT_MATCH_SOURCE": "primary",
                "SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL": "supplementary",
                "NONACTIVE_VISUAL_CANDIDATE": "candidate",
            }
            if role is not None:
                if role not in required_folder or not target.startswith(owner_prefix + required_folder[role] + "/"):
                    raise IntegrityError("Source-role storage mismatch: " + character_id)
                if role == "PRIMARY_EXACT_MATCH_SOURCE" and item["hash_relation_to_prior"] != "EXACT_MATCH":
                    raise IntegrityError("Nonmatching bytes cannot be primary canon")
            entry = indexed[character_id]
            if (entry.get("target_repository_path") != member
                    or entry.get("sha256") != item["expected_sha256"]
                    or entry.get("bytes") != item["size_bytes"]):
                raise IntegrityError("ZIP metadata differs from externally pinned bytes")
            data = z.read(member)
            if len(data) != item["size_bytes"] or digest(data) != item["expected_sha256"]:
                raise IntegrityError("Character source bytes mismatch: " + character_id)
            suffix = Path(member).suffix.lower()
            if suffix == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise IntegrityError("PNG magic mismatch")
            if suffix in {".jpeg", ".jpg"} and not data.startswith(b"\xff\xd8\xff"):
                raise IntegrityError("JPEG magic mismatch")
            validated.append({
                "character_id": character_id,
                "repository_path": target,
                "archive_member": member,
                "asset_role": role or "LEGACY_UNCLASSIFIED_TEST_FIXTURE",
                "sha256": digest(data),
                "git_blob_sha1": git_blob_sha1(data),
                "size_bytes": len(data),
                "relation_to_prior": item["hash_relation_to_prior"],
                "_data": data,
            })
    return validated


def stage_verified(rows: list[dict], root: Path) -> None:
    root = root.resolve()
    # Preflight *all* paths before writing anything; never overwrite conflicting bytes.
    for entry in rows:
        target = (root / entry["repository_path"]).resolve()
        if not target.is_relative_to(root):
            raise IntegrityError("Staging escaped repository root")
        if target.exists() and digest(target.read_bytes()) != entry["sha256"]:
            raise IntegrityError("Refusing to overwrite divergent bytes at " + str(target))
    for entry in rows:
        target = root / entry["repository_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        fd, tempname = tempfile.mkstemp(prefix=".source-byte-", dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(entry["_data"])
            os.replace(tempname, target)
        finally:
            if os.path.exists(tempname):
                os.unlink(tempname)


def make_receipt(rows: list[dict], source_archive_sha256: str, staged: bool) -> dict:
    safe_rows = [{k: v for k, v in x.items() if k != "_data"} for x in rows]
    return {
        "schema_version": "1.0",
        "status": "LOCAL_STAGED" if staged else "HASH_VERIFIED_NOT_STAGED",
        "archive_sha256": source_archive_sha256,
        "n_verified": len(safe_rows),
        "n_prior_hash_matches": sum(x["relation_to_prior"] == "EXACT_MATCH" for x in safe_rows),
        "n_versions_requiring_reconciliation": sum(x["asset_role"] == "NONACTIVE_VISUAL_CANDIDATE" for x in safe_rows),
        "n_previously_registered_supplementary": sum(x["asset_role"] == "SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL" for x in safe_rows),
        "github_persistence_verified": False,
        "renderer_subject_binding_verified": False,
        "t15": "HOLD",
        "t16": "HOLD",
        "items": safe_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--stage", action="store_true", help="Write exact bytes to their registered Oct 12 candidate paths")
    args = parser.parse_args()
    root = args.root.resolve()
    pinned = json.loads((root / LOCK_REL).read_text())
    rows = verify_packet(args.archive.expanduser(), pinned)
    if args.stage:
        stage_verified(rows, root)
        for row in rows:
            if digest((root / row["repository_path"]).read_bytes()) != row["sha256"]:
                raise IntegrityError("Fresh local retrieval failed for " + row["character_id"])
        receipt = make_receipt(rows, pinned["source_archive_sha256"], True)
        output = root / RECEIPT_REL
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({
        "count": len(rows),
        "hash_verified": all(x["sha256"] for x in rows),
        "staged": args.stage,
        "matching_old": sum(x["relation_to_prior"] == "EXACT_MATCH" for x in rows),
        "supplementary_spotlights": sum(x["asset_role"] == "SUPPLEMENTARY_REGISTERED_SPOTLIGHT_ORIGINAL" for x in rows),
        "unreconciled_candidates": sum(x["asset_role"] == "NONACTIVE_VISUAL_CANDIDATE" for x in rows),
        "t15": "HOLD",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
