"""Character provenance gate for Memo release candidates after Week 5 drift.

This is a RECEIPT validator, not a likeness classifier or renderer attestation.
It fails closed when source-asset-to-subject-to-final-raster evidence is absent.
"""
from pathlib import Path
import hashlib
import json
import re

HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_character_provenance(manifest, base):
    if manifest.get("publication_state") not in ("RELEASED", "PUBLISHED"):
        return []
    errors = []
    base = Path(base).resolve()
    for page in manifest.get("pages", []):
        ids = page.get("characters") or []
        if not ids:
            continue
        n = page.get("slot")
        receipts = page.get("character_generation_receipts")
        if not isinstance(receipts, list):
            errors.append(f"page {n}: per-subject generation receipts required")
            continue
        seen = set()
        for receipt in receipts:
            if not isinstance(receipt, dict):
                errors.append(f"page {n}: malformed character generation receipt")
                continue
            cid = receipt.get("character_id")
            if cid not in ids or cid in seen:
                errors.append(f"page {n}: unexpected or duplicated character subject")
            seen.add(cid)
            for field in ("owner_id", "canonical_asset_path", "generation_reference_id",
                          "subject_slot", "subject_binding_id", "renderer_route",
                          "mount_receipt_id", "capability_receipt_id", "output_instance_id",
                          "independent_reviewer_id", "reviewed_raster_path"):
                if not isinstance(receipt.get(field), str) or not receipt[field].strip():
                    errors.append(f"page {n}: {cid} missing {field}")
            for field in ("expected_sha256", "mounted_sha256", "raster_sha256"):
                if not isinstance(receipt.get(field), str) or not HEX64.fullmatch(receipt[field]):
                    errors.append(f"page {n}: {cid} invalid {field}")
            if receipt.get("subject_binding_proven") is not True:
                errors.append(f"page {n}: {cid} unproven reference-to-subject binding")
            if receipt.get("raster_qa_decision") != "PASS":
                errors.append(f"page {n}: {cid} failed final-raster inspection")
            if receipt.get("raster_sha256") != page.get("asset_sha256"):
                errors.append(f"page {n}: {cid} final-raster hash mismatch")
            if receipt.get("mounted_sha256") != receipt.get("expected_sha256"):
                errors.append(f"page {n}: {cid} mounted source hash mismatch")
            if receipt.get("independent_reviewer_id") == receipt.get("generation_operator_id"):
                errors.append(f"page {n}: {cid} raster reviewer not independent")
            for path_field, hash_field in (
                ("canonical_asset_path", "expected_sha256"),
                ("reviewed_raster_path", "raster_sha256"),
            ):
                value = receipt.get(path_field)
                if not isinstance(value, str) or not value:
                    continue
                resolved = (base / value).resolve()
                if not resolved.is_relative_to(base) or not resolved.is_file():
                    errors.append(f"page {n}: {cid} missing accessible {path_field}")
                elif HEX64.fullmatch(str(receipt.get(hash_field, ""))) and _sha(resolved) != receipt[hash_field]:
                    errors.append(f"page {n}: {cid} {path_field} bytes mismatch")
        if set(ids) != seen:
            errors.append(f"page {n}: missing generation receipts for {sorted(set(ids)-seen)}")
    return errors


if __name__ == "__main__":
    import sys
    mpath = Path(sys.argv[1]).resolve()
    errors = validate_character_provenance(json.loads(mpath.read_text()), mpath.parent)
    for err in errors:
        print("FAIL:", err)
    if not errors:
        print("PASS: character receipt consistency only; visual/provider authenticity is not machine-certified")
    raise SystemExit(bool(errors))
