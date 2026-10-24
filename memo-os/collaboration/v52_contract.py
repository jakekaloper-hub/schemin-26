"""V5.2-RC collaboration contract executable reference validator.

This module validates fixture semantics only. Production integration must independently
demonstrate that the live orchestration system uses equivalent enforcement.
"""
REASONS = {"MISSING_PROVENANCE", "STALE_INPUT", "INVALID_STATE", "MISSING_DEPENDENCY",
"CONTRACT_VIOLATION", "SOURCE_NOT_APPROVED", "BENCHMARK_LEAKAGE",
"CHARACTER_PACKET_MISMATCH", "UNSUPPORTED_CLAIM", "QA_NOT_PERFORMED",
"WRONG_ARTIFACT_VERSION", "MERCER_FIREWALL_VIOLATION"}
REQUIRED = {"run_id", "assignment_id", "from", "to", "artifact", "artifact_version",
"source_authority", "source_snapshot", "status", "verified_facts",
"interpretations", "assumptions", "unavailable", "unresolved", "confidence",
"qa_already_performed", "prohibited_inferences", "dependencies",
"next_required_action", "next_gate"}

def handoff(payload):
    if not REQUIRED.issubset(payload) or not payload.get("source_authority") or not payload.get("source_snapshot"):
        return "MISSING_PROVENANCE"
    if payload.get("stale"):
        return "STALE_INPUT"
    if payload.get("mercer_derived"):
        return "MERCER_FIREWALL_VIOLATION"
    if payload.get("benchmark_only") and payload.get("blank_canvas"):
        return "BENCHMARK_LEAKAGE"
    if payload.get("missing_context"):
        return "CONTRACT_VIOLATION"
    return "VALID"

def ready(dependencies):
    return all(state == "PASSED" for state in dependencies)

def work_key(*material_inputs):
    return tuple(material_inputs)

def correction(affected, locked):
    affected = set(affected)
    return {"reopen": affected, "preserve": set(locked) - affected}

def release_allowed(artifacts):
    return all(item["state"] == "PASSED" and item.get("qa") == "PASS" for item in artifacts)

def route(defect):
    return {"QA_FAILURE": "responsible_checkpoint", "CHARACTER_FAILURE": "Character / Art",
            "MOBILE_FAILURE": "Design / Layout", "MISSING_EVIDENCE": "Data / Research"}.get(defect, "Executive Control")

def escalation_needed(reason):
    return reason in {"OWNER_POLICY_EXCEPTION", "AMBIGUOUS_CANON", "MAJOR_CREATIVE_TRADEOFF"}

def acknowledged(handoff_state):
    return handoff_state in {"RECEIVED", "VALIDATED"}

def accept(payload):
    return handoff(payload) == "VALID" and acknowledged(payload.get("ack_state"))
