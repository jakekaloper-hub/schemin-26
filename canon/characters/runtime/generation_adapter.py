"""Single governed entrypoint. Renderer invocation is denied without authenticated eligibility."""
from .generation_eligibility import validate_eligibility

def governed_generate(renderer, eligibility, request_id, character_ids, route, asset_hashes, payload, signing_key=None, consumed_nonces=None):
    state=validate_eligibility(eligibility,request_id,character_ids,route,asset_hashes,signing_key=signing_key,consumed_nonces=consumed_nonces)
    if state!="GENERATION_ELIGIBLE":
        return {"state":"GENERATION_BLOCKED","reason":"INVALID_GENERATION_ELIGIBILITY","renderer_invoked":False}
    nonce=eligibility["claims"].get("nonce")
    if consumed_nonces is not None:
        consumed_nonces.add(nonce)
    result=renderer(payload)
    return {"state":"GENERATION_EXECUTED","renderer_invoked":True,"result":result}
