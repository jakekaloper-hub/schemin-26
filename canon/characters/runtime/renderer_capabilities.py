"""Renderer capability negotiation. Prompt-only or pooled-reference fallback is prohibited."""


def negotiate(route, capabilities, reference_count):
    c = capabilities.get(route)
    if not c:
        return {
            "state": "GENERATION_ROUTE_REFERENCE_UNSUPPORTED",
            "reason": "UNKNOWN_ROUTE",
        }

    reference_required = (
        "supports_image_references",
        "returns_attachment_receipt",
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

    if c.get("max_references", 0) < reference_count:
        return {
            "state": "GENERATION_ROUTE_REFERENCE_UNSUPPORTED",
            "reason": "REFERENCE_LIMIT",
        }

    return {
        "state": "CAPABILITY_VERIFIED",
        "route": route,
        "reference_mechanism": c.get("reference_mechanism"),
        "subject_binding_mechanism": c.get("subject_binding_mechanism"),
    }
