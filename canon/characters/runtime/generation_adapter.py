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


def canonical_renderer_payload(request_id, mounts, prompt):
    """Construct a request with an explicit per-subject reference map.

    This is local preflight evidence, NOT proof that a downstream image
    provider consumed the supplied references.
    """
    by_character = sorted(mounts, key=lambda mount: mount.character_id)
    return {
        "request_id": request_id,
        "prompt": prompt,
        "referenced_image_ids": [mount.generation_reference_id for mount in by_character],
        "subject_bindings": [
            {
                "character_id": mount.character_id,
                "subject_slot": mount.subject_slot,
                "generation_reference_id": mount.generation_reference_id,
                "subject_binding_id": mount.subject_binding_id,
            }
            for mount in by_character
        ],
    }


def _renderer_payload_valid(payload, request_id, mounts):
    """Fail closed before the renderer sees missing/swapped/unbound subjects."""
    if not isinstance(payload, dict) or payload.get("request_id") != request_id:
        return False
    expected = canonical_renderer_payload(request_id, mounts, payload.get("prompt"))
    provided_refs = payload.get("referenced_image_ids")
    provided_bindings = payload.get("subject_bindings")
    if not isinstance(provided_refs, list) or not isinstance(provided_bindings, list):
        return False
    if any(not isinstance(reference, str) or not reference for reference in provided_refs):
        return False
    if len(set(provided_refs)) != len(provided_refs):
        return False
    if sorted(provided_refs) != sorted(expected["referenced_image_ids"]):
        return False
    if len(provided_bindings) != len(expected["subject_bindings"]):
        return False
    # A subject-to-reference swap must never be accepted as equivalent.
    return sorted(provided_bindings, key=lambda item: str(item.get("character_id")) if isinstance(item, dict) else "") == expected["subject_bindings"]


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

    if not _renderer_payload_valid(payload, request_id, mounts):
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "RENDERER_REFERENCE_PAYLOAD_MISMATCH",
            "renderer_invoked": False,
        }

    if consumed_nonces is None:
        return {
            "state": "GENERATION_BLOCKED",
            "reason": "REPLAY_PROTECTION_REQUIRED",
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
