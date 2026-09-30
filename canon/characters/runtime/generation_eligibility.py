"""Fail-closed generation eligibility. Eligibility is request-bound, never global."""
import hashlib, json, time

LEGAL={"GENERATION_ELIGIBLE","GENERATION_BLOCKED","HUMAN_REVIEW_REQUIRED"}

def issue_eligibility(request_id, character_ids, mounts, route, capability, policy_version="CCCP-INC-1", now=None, ttl=300):
    if capability.get("state")!="CAPABILITY_VERIFIED":
        return {"state":"GENERATION_BLOCKED","reason":"GENERATION_ROUTE_REFERENCE_UNSUPPORTED"}
    by_id={m.character_id:m for m in mounts}
    if set(by_id)!=set(character_ids) or not all(by_id[c].renderable() for c in character_ids):
        return {"state":"GENERATION_BLOCKED","reason":"CHARACTER_REFERENCE_NOT_MOUNTED"}
    issued=int(now if now is not None else time.time())
    claims={"request_id":request_id,"character_ids":sorted(character_ids),"asset_hashes":sorted(by_id[c].sha256 for c in character_ids),"route":route,"policy_version":policy_version,"issued_at":issued,"expires_at":issued+ttl}
    token=hashlib.sha256(json.dumps(claims,sort_keys=True).encode()).hexdigest()
    return {"state":"GENERATION_ELIGIBLE","token":token,"claims":claims}

def validate_eligibility(eligibility, request_id, character_ids, route, asset_hashes, now=None):
    if eligibility.get("state")!="GENERATION_ELIGIBLE": return "GENERATION_BLOCKED"
    c=eligibility.get("claims",{})
    t=int(now if now is not None else time.time())
    checks=[c.get("request_id")==request_id, c.get("character_ids")==sorted(character_ids), c.get("route")==route, c.get("asset_hashes")==sorted(asset_hashes), t<=c.get("expires_at",0)]
    return "GENERATION_ELIGIBLE" if all(checks) else "GENERATION_BLOCKED"
