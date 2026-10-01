"""Single governed character-render entrypoint.

The renderer is never invoked without authenticated, request-bound eligibility.
Successful invocation is not Character QA and never returns publication PASS.
"""
from .generation_eligibility import validate_eligibility


def governed_generate(
    renderer,
    eligibility,
    request_id,
    character_ids,
    mounts,
    route,
    payload,
    signing_key=None,
    consumed_nonces=None,
):
    state = validate_eligibility(
        eligibility,
        request_id,
        character_ids,
        mounts,
        route,
        signing_key=signing_key,
        consumed_nonces=consumed_nonces,
    )
    if state != "GENERATION_ELIGIBLE":
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "INVALID_GENERATION_ELIGIBILITY",
            "renderer_invoked": False,
        }

    nonce = eligibility["claims"].get("nonce")
    if consumed_nonces is not None:
        consumed_nonces.add(nonce)

    result = renderer(payload)
    if not isinstance(result, dict) or not result.get("output_instance_id"):
        return {
            "state": "GENERATION_OUTPUT_BLOCKED",
            "reason": "OUTPUT_INSTANCE_RECEIPT_REQUIRED",
            "renderer_invoked": True,
            "result": result,
        }

    return {
        "state": "GENERATION_EXECUTED_PENDING_CHARACTER_QA",
        "renderer_invoked": True,
        "output_instance_id": result["output_instance_id"],
        "result": result,
    }
