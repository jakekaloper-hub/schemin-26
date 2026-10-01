from __future__ import annotations

ALLOWED_PROFILES={"CHARACTER_GROUNDED_STATIC","DATA_STORY","MOTION"}

def _nonempty(value):
    return isinstance(value,str) and bool(value.strip())

def validate_render_request(req:dict)->list[str]:
    errors=[]
    if req.get("schema_version")!="1.0": errors.append("schema_version must be 1.0")
    if not _nonempty(req.get("request_id")): errors.append("request_id required")
    profile=req.get("profile")
    if profile not in ALLOWED_PROFILES: errors.append("unsupported profile")

    authority=req.get("authority") or {}
    for key in ("project_control_receipt","character_authority","world_authority","publication_authority"):
        if not _nonempty(authority.get(key)): errors.append(f"authority.{key} required")

    evidence=req.get("evidence") or {}
    if evidence.get("status")!="VERIFIED": errors.append("evidence must be VERIFIED")
    if evidence.get("freshness") not in {"FRESH","LOCKED_RELEASE"}: errors.append("evidence freshness must be FRESH or LOCKED_RELEASE")
    if not evidence.get("receipts"): errors.append("evidence receipts required")

    output=req.get("output_contract") or {}
    if output.get("provenance_required") is not True: errors.append("artifact provenance must be required")
    if not output.get("qa_gates"): errors.append("output qa_gates required")

    safety=req.get("safety") or {}
    if safety.get("authority_mutation_allowed") is not False: errors.append("renderer authority mutation must be false")
    if safety.get("dependency_installation_allowed") is not False: errors.append("dependency installation must be false in candidate")
    if safety.get("external_dependency")!="NONE": errors.append("external dependency must remain NONE in research candidate")

    inputs=req.get("inputs") or {}

    if profile=="CHARACTER_GROUNDED_STATIC":
        packets=inputs.get("character_packets") or []
        if not packets: errors.append("character_packets required")
        if not inputs.get("publication_packet"): errors.append("publication_packet required")
        for i,p in enumerate(packets):
            if p.get("authority_state")!="ACTIVE": errors.append(f"character_packets[{i}] authority must be ACTIVE")
            if p.get("source_integrity_state")!="PASS": errors.append(f"character_packets[{i}] source integrity must PASS")
            if p.get("render_ready") is not True: errors.append(f"character_packets[{i}] must be render_ready")
            if not p.get("reference_assets"): errors.append(f"character_packets[{i}] reference_assets required")
            if not p.get("mount_receipts"): errors.append(f"character_packets[{i}] mount_receipts required")
            if not p.get("capability_receipt_id"): errors.append(f"character_packets[{i}] capability receipt required")
            if p.get("execution_receipt_required") is not True: errors.append(f"character_packets[{i}] execution receipt must be required")
        if inputs.get("location_bearing") is True and not inputs.get("world_packet"):
            errors.append("world_packet required for location-bearing render")

    if profile=="DATA_STORY":
        data=inputs.get("deterministic_data") or {}
        if data.get("mutation_policy")!="READ_ONLY": errors.append("deterministic_data must be READ_ONLY")
        if data.get("missing_values_policy")!="DO_NOT_INFER": errors.append("missing values must not be inferred")
        if not data.get("source_receipts"): errors.append("deterministic_data source_receipts required")
        if not inputs.get("data_definitions"): errors.append("data_definitions required")

    if profile=="MOTION":
        if not _nonempty(inputs.get("storyboard_packet_ref")): errors.append("storyboard_packet_ref required")
        if not inputs.get("source_artifacts"): errors.append("source_artifacts required")
        session=inputs.get("session") or {}
        if not _nonempty(session.get("session_id")): errors.append("motion session_id required")
        if not isinstance(session.get("revision"),int) or session.get("revision",0)<1: errors.append("motion revision must be >=1")
        if session.get("output_verification_required") is not True: errors.append("motion output verification must be required")

    return errors
