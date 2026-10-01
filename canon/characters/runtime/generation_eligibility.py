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
    signing_key=None,
    policy_version="CCCP-INC-3",
    now=None,
    ttl=300,
    nonce=None,
):
    if capability.get("state") != "CAPABILITY_VERIFIED":
        return {
            "state": "GENERATION_BLOCKED",
            "reason": capability.get("reason", "GENERATION_ROUTE_UNPROVEN"),
        }

    by_id = {mount.character_id: mount for mount in mounts}
    if set(by_id) != set(character_ids):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CHARACTER_REFERENCE_SET_MISMATCH",
        }
    if not all(by_id[cid].renderable(route=route) for cid in character_ids):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "CHARACTER_REFERENCE_OR_BINDING_NOT_PROVEN",
        }

    slots = [by_id[cid].subject_slot for cid in character_ids]
    bindings = [by_id[cid].subject_binding_id for cid in character_ids]
    if len(set(slots)) != len(slots) or len(set(bindings)) != len(bindings):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "SUBJECT_BINDING_NOT_UNIQUE",
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
        timestamp <= claims.get("expires_at", 0),
        not replay,
    ]
    return "GENERATION_ELIGIBLE" if all(checks) else "GENERATION_BLOCKED"
