"""Fail-closed generation eligibility.

Tokens are HMAC-authenticated, request-bound, asset-bound, subject-bound,
route-bound and short-lived. Only a trusted adapter may issue/consume them.
"""
import hashlib
import hmac
import json
import time


def _payload(claims):
    return json.dumps(claims, sort_keys=True, separators=(",", ":")).encode()


def _sign(claims, signing_key):
    if not signing_key:
        raise ValueError("trusted signing key required")
    key = signing_key.encode() if isinstance(signing_key, str) else signing_key
    return hmac.new(key, _payload(claims), hashlib.sha256).hexdigest()


def _mount_claims(mounts):
    return sorted(
        [
            {
                "character_id": mount.character_id,
                "asset_hash": mount.sha256,
                "expected_sha256": mount.expected_sha256 or mount.sha256,
                "mounted_sha256": mount.mounted_sha256,
                "repository_path": mount.repository_path,
                "git_blob_sha": mount.git_blob_sha,
                "byte_size": mount.byte_size,
                "mount_receipt_id": mount.mount_receipt_id,
                "capability_receipt_id": mount.capability_receipt_id,
                "subject_slot": mount.subject_slot,
                "subject_binding_id": mount.subject_binding_id,
                "generation_reference_id": mount.generation_reference_id,
            }
            for mount in mounts
        ],
        key=lambda item: item["character_id"],
    )


def issue_eligibility(
    request_id,
    character_ids,
    mounts,
    route,
    capability,
    authority_receipt=None,
    signing_key=None,
    policy_version="CCCP-INC-4",
    now=None,
    ttl=300,
    nonce=None,
):
    if capability.get("state") != "CAPABILITY_VERIFIED":
        return {
            "state": "GENERATION_BLOCKED",
            "reason": capability.get("reason", "GENERATION_ROUTE_UNPROVEN"),
        }

    if not isinstance(authority_receipt, dict) or authority_receipt.get("state") != "REFERENCE_AUTHORITY_RESOLVED":
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CURRENT_SOURCE_AUTHORITY_REQUIRED",
        }

    authority_results = authority_receipt.get("results", [])
    authority_by_id = {item.get("character_id"): item for item in authority_results}
    if set(authority_by_id) != set(character_ids):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "REFERENCE_AUTHORITY_SET_MISMATCH",
        }

    by_id = {mount.character_id: mount for mount in mounts}
    if len(by_id) != len(mounts) or set(by_id) != set(character_ids):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CHARACTER_REFERENCE_SET_MISMATCH",
        }
    if not all(by_id[cid].renderable(route=route) for cid in character_ids):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CHARACTER_REFERENCE_OR_BINDING_NOT_PROVEN",
        }

    for cid in character_ids:
        expected = authority_by_id[cid].get("expected_sha256")
        if not expected or expected != by_id[cid].expected_sha256 or expected != by_id[cid].mounted_sha256:
            return {
                "state": "GENERATION_BLOCKED",
                "reason": "REFERENCE_AUTHORITY_HASH_MISMATCH",
            }

    capability_receipt_id = capability.get("capability_receipt_id")
    if not capability_receipt_id or any(
        by_id[cid].capability_receipt_id != capability_receipt_id
        for cid in character_ids
    ):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CAPABILITY_RECEIPT_MISMATCH",
        }

    slots = [by_id[cid].subject_slot for cid in character_ids]
    bindings = [by_id[cid].subject_binding_id for cid in character_ids]
    mount_receipts = [by_id[cid].mount_receipt_id for cid in character_ids]
    if (
        len(set(slots)) != len(slots)
        or len(set(bindings)) != len(bindings)
        or len(set(mount_receipts)) != len(mount_receipts)
    ):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "SUBJECT_OR_MOUNT_BINDING_NOT_UNIQUE",
        }

    if not signing_key:
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "TRUSTED_SIGNER_UNAVAILABLE",
        }

    issued = int(now if now is not None else time.time())
    claims = {
        "request_id": request_id,
        "character_ids": sorted(character_ids),
        "mounts": _mount_claims(mounts),
        "route": route,
        "capability_receipt_id": capability_receipt_id,
        "reference_authority": sorted(
            [
                {
                    "character_id": cid,
                    "expected_sha256": authority_by_id[cid].get("expected_sha256"),
                    "source_filename": authority_by_id[cid].get("source_filename"),
                }
                for cid in character_ids
            ],
            key=lambda item: item["character_id"],
        ),
        "policy_version": policy_version,
        "issued_at": issued,
        "expires_at": issued + ttl,
        "nonce": nonce or request_id,
    }
    return {
        "state": "GENERATION_ELIGIBLE",
        "token": _sign(claims, signing_key),
        "claims": claims,
    }


def validate_eligibility(
    eligibility,
    request_id,
    character_ids,
    mounts,
    route,
    authority_receipt=None,
    signing_key=None,
    now=None,
    consumed_nonces=None,
):
    if eligibility.get("state") != "GENERATION_ELIGIBLE" or not signing_key:
        return "GENERATION_BLOCKED"

    claims = eligibility.get("claims", {})
    try:
        authentic = hmac.compare_digest(
            eligibility.get("token", ""),
            _sign(claims, signing_key),
        )
    except Exception:
        authentic = False

    timestamp = int(now if now is not None else time.time())
    nonce = claims.get("nonce")
    replay = consumed_nonces is not None and nonce in consumed_nonces

    checks = [
        authentic,
        claims.get("request_id") == request_id,
        claims.get("character_ids") == sorted(character_ids),
        claims.get("mounts") == _mount_claims(mounts),
        claims.get("route") == route,
        isinstance(authority_receipt, dict),
        authority_receipt.get("state") == "REFERENCE_AUTHORITY_RESOLVED" if isinstance(authority_receipt, dict) else False,
        claims.get("reference_authority") == sorted(
            [
                {
                    "character_id": item.get("character_id"),
                    "expected_sha256": item.get("expected_sha256"),
                    "source_filename": item.get("source_filename"),
                }
                for item in (authority_receipt.get("results", []) if isinstance(authority_receipt, dict) else [])
            ],
            key=lambda item: item["character_id"] or "",
        ),
        timestamp <= claims.get("expires_at", 0),
        not replay,
    ]
    return "GENERATION_ELIGIBLE" if all(checks) else "GENERATION_BLOCKED"
