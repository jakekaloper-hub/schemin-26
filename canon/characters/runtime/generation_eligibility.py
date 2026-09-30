"""Fail-closed generation eligibility.
Tokens are HMAC-authenticated, request-bound, asset-bound, route-bound and short-lived.
The signing key is injected by the trusted adapter and is never derived from public claims.
"""
import hashlib, hmac, json, time

LEGAL={"GENERATION_ELIGIBLE","GENERATION_BLOCKED","HUMAN_REVIEW_REQUIRED"}

def _payload(claims):
    return json.dumps(claims,sort_keys=True,separators=(",",":")).encode()

def _sign(claims, signing_key):
    if not signing_key:
        raise ValueError("trusted signing key required")
    key=signing_key.encode() if isinstance(signing_key,str) else signing_key
    return hmac.new(key,_payload(claims),hashlib.sha256).hexdigest()

def issue_eligibility(request_id, character_ids, mounts, route, capability, signing_key=None, policy_version="CCCP-INC-2", now=None, ttl=300, nonce=None):
    if capability.get("state")!="CAPABILITY_VERIFIED":
        return {"state":"GENERATION_BLOCKED","reason":"GENERATION_ROUTE_REFERENCE_UNSUPPORTED"}
    by_id={m.character_id:m for m in mounts}
    if set(by_id)!=set(character_ids) or not all(by_id[c].renderable() for c in character_ids):
        return {"state":"GENERATION_BLOCKED","reason":"CHARACTER_REFERENCE_NOT_MOUNTED"}
    if not signing_key:
        return {"state":"GENERATION_BLOCKED","reason":"TRUSTED_SIGNER_UNAVAILABLE"}
    issued=int(now if now is not None else time.time())
    claims={"request_id":request_id,"character_ids":sorted(character_ids),"asset_hashes":sorted(by_id[c].sha256 for c in character_ids),"route":route,"policy_version":policy_version,"issued_at":issued,"expires_at":issued+ttl,"nonce":nonce or request_id}
    return {"state":"GENERATION_ELIGIBLE","token":_sign(claims,signing_key),"claims":claims}

def validate_eligibility(eligibility, request_id, character_ids, route, asset_hashes, signing_key=None, now=None, consumed_nonces=None):
    if eligibility.get("state")!="GENERATION_ELIGIBLE" or not signing_key: return "GENERATION_BLOCKED"
    c=eligibility.get("claims",{})
    try:
        authentic=hmac.compare_digest(eligibility.get("token",""),_sign(c,signing_key))
    except Exception:
        authentic=False
    t=int(now if now is not None else time.time())
    nonce=c.get("nonce")
    replay=consumed_nonces is not None and nonce in consumed_nonces
    checks=[authentic,c.get("request_id")==request_id,c.get("character_ids")==sorted(character_ids),c.get("route")==route,c.get("asset_hashes")==sorted(asset_hashes),t<=c.get("expires_at",0),not replay]
    return "GENERATION_ELIGIBLE" if all(checks) else "GENERATION_BLOCKED"
