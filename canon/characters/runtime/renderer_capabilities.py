"""Renderer capability negotiation.

Prompt-only or pooled-reference fallback is prohibited. A renderer route must
provide auditable evidence for attachment, mounted-byte integrity and
per-subject binding before it can be used for governed character rendering.
"""


def negotiate(route, capabilities, reference_count):
    c = capabilities.get(route)
    if not c:
        return {
            "state": "GENERATION_ROUTE_REFERENCE_UNSUPPORTED",
            "reason": "UNKNOWN_ROUTE",
        }

    if c.get("evidence_state") != "PROVEN" or not c.get("capability_receipt_id"):
        return {
            "state": "GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN",
            "reason": "CAPABILITY_EVIDENCE_UNPROVEN",
        }

    reference_required = (
        "supports_image_references",
        "returns_attachment_receipt",
        "returns_mounted_byte_hash_receipt",
    )
    if not all(c.get(key) is True for key in reference_required):
        return {
            "state": "GENERATION_ROUTE_REFERENCE_UNSUPPORTED",
            "reason": "REFERENCE_CONTRACT_UNSUPPORTED",
        }

    binding_required = (
        "supports_subject_binding",
        "returns_subject_binding_receipt",
    )
    if not all(c.get(key) is True for key in binding_required):
        return {
            "state": "GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN",
            "reason": "SUBJECT_BINDING_CONTRACT_UNPROVEN",
        }

    max_references = c.get("max_references")
    if not isinstance(max_references, int) or max_references < reference_count:
        return {
            "state": "GENERATION_ROUTE_REFERENCE_UNSUPPORTED",
            "reason": "REFERENCE_LIMIT",
        }

    return {
        "state": "CAPABILITY_VERIFIED",
        "route": route,
        "capability_receipt_id": c["capability_receipt_id"],
        "reference_mechanism": c.get("reference_mechanism"),
        "subject_binding_mechanism": c.get("subject_binding_mechanism"),
    }
