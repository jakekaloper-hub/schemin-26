"""CCCP deterministic QA outcome contract."""
ALLOWED={"PASS","REGENERATE","HUMAN_REVIEW_REQUIRED"}
def evaluate_character(packet, observations):
    if not packet or not observations: return "HUMAN_REVIEW_REQUIRED"
    if observations.get("reference_retrievable") is False: return "HUMAN_REVIEW_REQUIRED"
    fatal=("owner_match","active_identity","species_body","head_face","silhouette","no_retired_design","no_cross_character_contamination","reference_provenance")
    if any(observations.get(k) is False for k in fatal): return "REGENERATE"
    if any(observations.get(k) is None for k in fatal): return "HUMAN_REVIEW_REQUIRED"
    return "PASS"
def publication_gate(results):
    if not results or any(r not in ALLOWED for r in results): return "HUMAN_REVIEW_REQUIRED"
    return "PASS" if all(r=="PASS" for r in results) else ("REGENERATE" if "REGENERATE" in results else "HUMAN_REVIEW_REQUIRED")
