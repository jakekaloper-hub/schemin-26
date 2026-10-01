"""Single governed character-render entrypoint.

The renderer is never invoked without authenticated, request-bound eligibility.
Successful invocation is not Character QA and never returns publication PASS.
"""
from .generation_eligibility import validate_eligibility


def _expected_execution_receipt(request_id, route, mounts):
    return {
        "request_id": request_id,
        "route": route,
        "mount_receipt_ids": sorted(m.mount_receipt_id for m in mounts),
        "generation_reference_ids": sorted(m.generation_reference_id for m in mounts),
        "subject_binding_ids": sorted(m.subject_binding_id for m in mounts),
    }


def governed_generate(
    renderer,
    eligibility,
    request_id,
    character_ids,
    mounts,
    route,
    payload,
    authority_receipt=None,
    signing_key=None,
    consumed_nonces=None,
    now=None,
):
    state = validate_eligibility(
        eligibility,
        request_id,
        character_ids,
        mounts,
        route,
        authority_receipt=authority_receipt,
        signing_key=signing_key,
        now=now,
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

    expected = _expected_execution_receipt(request_id, route, mounts)
    if result.get("execution_receipt") != expected:
        return {
            "state": "GENERATION_OUTPUT_BLOCKED",
            "reason": "REFERENCE_EXECUTION_RECEIPT_REQUIRED_OR_MISMATCH",
            "renderer_invoked": True,
            "output_instance_id": result.get("output_instance_id"),
            "expected_execution_receipt": expected,
            "result": result,
        }

    return {
        "state": "GENERATION_EXECUTED_PENDING_CHARACTER_QA",
        "renderer_invoked": True,
        "output_instance_id": result["output_instance_id"],
        "execution_receipt": result["execution_receipt"],
        "result": result,
    }
