"""Renderer capability negotiation. Prompt-only fallback is prohibited."""
def negotiate(route, capabilities, reference_count):
    c=capabilities.get(route)
    if not c:
        return {"state":"GENERATION_ROUTE_REFERENCE_UNSUPPORTED","reason":"UNKNOWN_ROUTE"}
    required=("supports_image_references","returns_attachment_receipt")
    if not all(c.get(k) is True for k in required):
        return {"state":"GENERATION_ROUTE_REFERENCE_UNSUPPORTED","reason":"REFERENCE_CONTRACT_UNSUPPORTED"}
    if c.get("max_references",0) < reference_count:
        return {"state":"GENERATION_ROUTE_REFERENCE_UNSUPPORTED","reason":"REFERENCE_LIMIT"}
    return {"state":"CAPABILITY_VERIFIED","route":route,"mechanism":c.get("reference_mechanism")}
