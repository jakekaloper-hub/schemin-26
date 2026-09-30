"""Single governed entrypoint. Renderer invocation is denied without valid eligibility."""
from .generation_eligibility import validate_eligibility

def governed_generate(renderer, eligibility, request_id, character_ids, route, asset_hashes, payload):
    if validate_eligibility(eligibility,request_id,character_ids,route,asset_hashes)!="GENERATION_ELIGIBLE":
        return {"state":"GENERATION_BLOCKED","reason":"INVALID_GENERATION_ELIGIBILITY"}
    return renderer(payload)
