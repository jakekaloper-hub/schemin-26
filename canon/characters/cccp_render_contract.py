"""CCCP render-contract compiler. No reference bytes = HUMAN_REVIEW_REQUIRED for recognizable generation."""
from cccp_resolver import resolve_character
PORTABLE_REFERENCE_READY=False
def compile_render_contract(queries, scene=None):
    packets=[]
    for q in queries:
        r=resolve_character(q)
        if r["status"]!="CURRENT_CANON_RESOLVED": return {"status":"HUMAN_REVIEW_REQUIRED","resolution":r}
        packets.append({"character_id":r["character_id"],"owner":r["owner"],"team":r["team"],"identity":r["identity"],"version":r["version"],"packet_path":f'canon/characters/{r["character_id"]}/T04_CHARACTER_SPEC.md',"reference_register":"canon/characters/COMMISSIONER_REFERENCE_REGISTER_12_OF_12.md"})
    if len({p["character_id"] for p in packets}) != len(packets):
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"DUPLICATE_OR_AMBIGUOUS_CHARACTER"}
    return {"status":"READY_FOR_SEMANTIC_QA" if not PORTABLE_REFERENCE_READY else "READY_FOR_RENDER","portable_reference_ready":PORTABLE_REFERENCE_READY,"characters":packets,"scene":scene or {},"rule":"Packets remain owner-scoped; scene variables cannot override identity."}
