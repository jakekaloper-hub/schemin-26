"""Fail-closed verifier for externally issued V5.2-RC Steward receipts.

This is NOT a Steward receiver or a signer. A separate authenticated,
independent service must verify source provenance and issue signed decisions.
Local fixture signatures establish only test behavior, not live acceptance.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEX = set("0123456789abcdef")


def _hash_on_disk(relative_path):
    if not isinstance(relative_path, str) or not relative_path:
        return None
    root = ROOT.resolve()
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        return None
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verify(handoff):
    """Return VALID or a stable reason code. No output promotes a Fact Lock.

    The receipt's HMAC key and allowed issuer/principal must be injected from a
    protected deployment, not from the handoff. The caller is NOT authorized to
    mint receipts; key custody and independent source review are out of scope.
    """
    if not isinstance(handoff, dict):
        return "CONTRACT_VIOLATION"
    if handoff.get("ack_state") != "VALIDATED":
        return "ACK_MISSING"
    receipt = handoff.get("steward_receipt")
    if not isinstance(receipt, dict) or set(receipt) != {"payload", "signature"}:
        return "MISSING_STEWARD_RECEIPT"
    payload, signature = receipt["payload"], receipt["signature"]
    if not isinstance(payload, dict) or not isinstance(signature, str) or len(signature) != 64:
        return "MALFORMED_STEWARD_RECEIPT"
    key = os.environ.get("SCK_STEWARD_RECEIPT_VERIFICATION_KEY", "").encode()
    principal = os.environ.get("SCK_STEWARD_TRUSTED_PRINCIPAL", "")
    issuer = os.environ.get("SCK_STEWARD_TRUSTED_ISSUER", "")
    if len(key) < 32 or not principal or not issuer:
        return "MISSING_TRUSTED_STEWARD_VERIFIER"
    expected = hmac.new(key, _canonical(payload), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return "STEWARDSHIP_SIGNATURE_INVALID"
    required = {
        "assignment_id", "run_id", "trace_id", "work_key", "artifact",
        "artifact_version", "artifact_sha256", "source_snapshot",
        "receiver_principal", "trusted_issuer", "decision",
    }
    if set(payload) != required:
        return "MALFORMED_STEWARD_RECEIPT"
    if payload.get("receiver_principal") != principal or payload.get("trusted_issuer") != issuer:
        return "STEWARDSHIP_IDENTITY_MISMATCH"
    if payload.get("decision") != "VALIDATED":
        return "STEWARD_NOT_VALIDATED"
    for field in ("assignment_id", "run_id", "trace_id", "work_key", "artifact",
                  "artifact_version", "source_snapshot"):
        if not payload.get(field) or payload.get(field) != handoff.get(field):
            return "STEWARDSHIP_SCOPE_MISMATCH"
    sha = payload["artifact_sha256"]
    if not isinstance(sha, str) or len(sha) != 64 or not set(sha).issubset(HEX):
        return "MALFORMED_STEWARD_RECEIPT"
    actual = _hash_on_disk(handoff["artifact"])
    if actual is None:
        return "SOURCE_ARTIFACT_NOT_FOUND"
    if not hmac.compare_digest(sha, actual):
        return "STEWARDSHIP_ARTIFACT_MISMATCH"
    return "VALID"
