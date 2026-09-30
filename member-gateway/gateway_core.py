"""Transport-independent Schemin Member Gateway implementation contracts."""
from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, Mapping
import hashlib
import json
import uuid

class AuthorizationError(PermissionError):
    pass

class ContractError(ValueError):
    pass

@dataclass(frozen=True)
class Principal:
    member_id: str
    consumer_class: str
    client_id: str
    scopes: FrozenSet[str]

@dataclass(frozen=True)
class Capability:
    capability_id: str
    version: str
    allowed_classes: FrozenSet[str]
    required_scope: str
    read_only: bool = True
    disclosure_class: str = "LEAGUE_SHARED"

CAPABILITIES: Mapping[str, Capability] = {
    "capabilities.list": Capability("capabilities.list", "1.0", frozenset({"commissioner","league_member"}), "capabilities.read"),
    "league.current_state": Capability("league.current_state", "1.0", frozenset({"commissioner","league_member"}), "league.read"),
    "league.history": Capability("league.history", "1.0", frozenset({"commissioner","league_member"}), "history.read"),
    "owner.identity": Capability("owner.identity", "1.0", frozenset({"commissioner","league_member"}), "identity.read"),
    "pittys_book.inputs": Capability("pittys_book.inputs", "1.0", frozenset({"commissioner","league_member"}), "pittys_book.inputs"),
}

PITTS = Principal(
    "pitts", "league_member", "pitts-chatgpt",
    frozenset({"capabilities.read","league.read","history.read","identity.read","pittys_book.inputs"})
)
JAKE = Principal(
    "jake", "commissioner", "jake-chatgpt",
    frozenset({"capabilities.read","league.read","history.read","identity.read","pittys_book.inputs"})
)

def authorize(principal: Principal, capability_id: str) -> Capability:
    cap = CAPABILITIES.get(capability_id)
    if cap is None:
        raise AuthorizationError("CAPABILITY_UNKNOWN")
    if principal.consumer_class not in cap.allowed_classes:
        raise AuthorizationError("CONSUMER_CLASS_DENIED")
    if cap.required_scope not in principal.scopes:
        raise AuthorizationError("SCOPE_DENIED")
    return cap

def visible_capabilities(principal: Principal) -> Dict[str, Dict[str, Any]]:
    visible = {}
    for cid, cap in CAPABILITIES.items():
        try:
            authorize(principal, cid)
        except AuthorizationError:
            continue
        visible[cid] = {"version": cap.version, "read_only": cap.read_only}
    return visible

def validate_truth_packet(packet: Mapping[str, Any]) -> None:
    freshness = packet.get("freshness")
    if not isinstance(freshness, Mapping):
        raise ContractError("MISSING_FRESHNESS")
    required = {"stale","fetched_at","snapshot_age_seconds","failure_reason"}
    missing = sorted(required - set(freshness.keys()))
    if missing:
        raise ContractError("MISSING_FRESHNESS_FIELDS:" + ",".join(missing))
    if not isinstance(freshness["stale"], bool):
        raise ContractError("INVALID_STALE")
    age = freshness["snapshot_age_seconds"]
    if age is not None and (not isinstance(age, (int,float)) or age < 0):
        raise ContractError("INVALID_SNAPSHOT_AGE")
    if "result" not in packet:
        raise ContractError("MISSING_RESULT")
    if "provenance" not in packet:
        raise ContractError("MISSING_PROVENANCE")

def compile_sck_handoff(*, principal: Principal, capability: Capability,
                        normalized_request: Mapping[str, Any], request_id: str,
                        run_id: str) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "assignment_id": str(uuid.uuid4()),
        "from": "member-ai-gateway",
        "to": "SCK",
        "consumer": {"member_id": principal.member_id, "client_id": principal.client_id},
        "capability": capability.capability_id,
        "artifact": "member-capability-request",
        "artifact_version": capability.version,
        "source_authority": "Member AI Gateway",
        "status": "HANDOFF_READY",
        "normalized_request": dict(normalized_request),
        "dependencies": [],
        "prohibited_inferences": [
            "external client possesses Bullpen authority",
            "conversation memory is canonical league truth",
            "Mercer context is available without explicit private authorization",
        ],
        "next_required_action": "SCK_ROUTE",
        "next_gate": "AUTHORITY_AND_DEPENDENCY_RESOLUTION",
        "request_id": request_id,
    }

def idempotency_key(*, principal: Principal, capability: Capability,
                    normalized_request: Mapping[str, Any]) -> str:
    material = {
        "member_id": principal.member_id,
        "client_id": principal.client_id,
        "capability": capability.capability_id,
        "version": capability.version,
        "request": normalized_request,
    }
    raw = json.dumps(material, sort_keys=True, separators=(",",":"), default=str)
    return hashlib.sha256(raw.encode()).hexdigest()

def authorize_outflow(principal: Principal, capability: Capability,
                      packet: Mapping[str, Any]) -> None:
    # Re-evaluate capability at egress; ingress authorization alone is insufficient.
    authorize(principal, capability.capability_id)
    disclosure = packet.get("disclosure_class", capability.disclosure_class)
    if disclosure in {"PRIVATE","SYSTEM_INTERNAL","SECRET"}:
        raise AuthorizationError("OUTFLOW_DISCLOSURE_DENIED")
    serialized = json.dumps(packet, default=str).lower()
    if "mercer" in serialized:
        raise AuthorizationError("MERCER_FIREWALL_VIOLATION")

def response_envelope(*, principal: Principal, capability: Capability, result: Any,
                      request_id: str, run_id: str, freshness: Dict[str, Any] | None = None,
                      provenance: Any = None, limitations: Any = None,
                      authority_status: str = "BULLPEN_ROUTED",
                      qa_status: str = "NOT_CERTIFIED") -> Dict[str, Any]:
    packet = {
        "request_id": request_id,
        "run_id": run_id,
        "capability": capability.capability_id,
        "capability_version": capability.version,
        "consumer": {"member_id": principal.member_id, "client_id": principal.client_id},
        "consumer_class": principal.consumer_class,
        "status": "OK",
        "result": result,
        "provenance": provenance or [],
        "freshness": freshness,
        "limitations": limitations or [],
        "authority_status": authority_status,
        "qa_status": qa_status,
        "disclosure_class": capability.disclosure_class,
    }
    authorize_outflow(principal, capability, packet)
    return packet

def execute(*, principal: Principal, capability_id: str,
            normalized_request: Mapping[str, Any] | None = None,
            truth_packet: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    cap = authorize(principal, capability_id)
    normalized_request = normalized_request or {}
    request_id = str(uuid.uuid4())
    run_id = idempotency_key(principal=principal, capability=cap, normalized_request=normalized_request)

    if capability_id == "capabilities.list":
        return response_envelope(
            principal=principal, capability=cap, result=visible_capabilities(principal),
            request_id=request_id, run_id=run_id,
        )

    # The gateway consumes validated Truth Plane output; it never becomes a second fetcher.
    if truth_packet is None:
        handoff = compile_sck_handoff(
            principal=principal, capability=cap, normalized_request=normalized_request,
            request_id=request_id, run_id=run_id,
        )
        # Internal handoff is intentionally not embedded in the external packet.
        # Transport/runtime code forwards it to SCK using the shared run_id.
        return response_envelope(
            principal=principal, capability=cap,
            result={"state":"AWAITING_SCK"},
            request_id=request_id, run_id=run_id,
        )

    validate_truth_packet(truth_packet)
    return response_envelope(
        principal=principal, capability=cap, result=truth_packet["result"],
        request_id=request_id, run_id=run_id,
        freshness=dict(truth_packet["freshness"]),
        provenance=truth_packet["provenance"],
        limitations=truth_packet.get("limitations", []),
        authority_status=truth_packet.get("authority_status","BULLPEN_ROUTED"),
        qa_status=truth_packet.get("qa_status","NOT_CERTIFIED"),
    )

# Backward-compatible Phase 1 entry point.
def execute_phase1(principal: Principal, capability_id: str) -> Dict[str, Any]:
    return execute(principal=principal, capability_id=capability_id)
