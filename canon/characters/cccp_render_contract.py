"""CCCP render-contract compiler. Semantic resolution never authorizes rendering."""
try:
    from .cccp_resolver import resolve_character
except ImportError:
    from cccp_resolver import resolve_character

LEGAL_STATES = {"GENERATION_ELIGIBLE", "GENERATION_BLOCKED", "HUMAN_REVIEW_REQUIRED"}

def compile_render_contract(queries, scene=None):
    packets = []
    for query in queries:
        resolved = resolve_character(query)
        if resolved["status"] != "CURRENT_CANON_RESOLVED":
            return {"state": "HUMAN_REVIEW_REQUIRED", "resolution": resolved}
        packets.append({
            "character_id": resolved["character_id"],
            "owner": resolved["owner"],
            "team": resolved["team"],
            "identity": resolved["identity"],
            "version": resolved["version"],
            "packet_path": f'canon/characters/{resolved["character_id"]}/T04_CHARACTER_SPEC.md',
            "reference_register": "canon/characters/COMMISSIONER_REFERENCE_REGISTER_12_OF_12.md",
        })

    if len({packet["character_id"] for packet in packets}) != len(packets):
        return {
            "state": "HUMAN_REVIEW_REQUIRED",
            "reason": "DUPLICATE_OR_AMBIGUOUS_CHARACTER",
        }

    return {
        "state": "GENERATION_BLOCKED",
        "reason": "CHARACTER_REFERENCE_MOUNT_AND_SUBJECT_BINDING_REQUIRED",
        "characters": packets,
        "scene": scene or {},
        "rule": (
            "Semantic packets cannot authorize rendering. Only the governed runtime "
            "may issue request/asset/subject/route-bound GENERATION_ELIGIBLE."
        ),
    }
