"""Transport-independent Schemin Member Gateway Phase 1 contracts."""
from dataclasses import dataclass, asdict
from typing import Any, Dict, FrozenSet, Mapping
import uuid

class AuthorizationError(PermissionError):
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

CAPABILITIES: Mapping[str, Capability] = {
    "capabilities.list": Capability("capabilities.list", "1.0", frozenset({"commissioner","league_member"}), "capabilities.read"),
    "league.current_state": Capability("league.current_state", "1.0", frozenset({"commissioner","league_member"}), "league.read"),
    "league.history": Capability("league.history", "1.0", frozenset({"commissioner","league_member"}), "history.read"),
    "owner.identity": Capability("owner.identity", "1.0", frozenset({"commissioner","league_member"}), "identity.read"),
    "pittys_book.inputs": Capability("pittys_book.inputs", "1.0", frozenset({"commissioner","league_member"}), "pittys_book.inputs"),
}

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

def response_envelope(*, principal: Principal, capability: Capability, result: Any,
                      status: str = "OK", freshness: Dict[str, Any] | None = None,
                      provenance: Any = None, limitations: Any = None,
                      authority_status: str = "BULLPEN_ROUTED",
                      qa_status: str = "NOT_CERTIFIED") -> Dict[str, Any]:
    return {
        "request_id": str(uuid.uuid4()),
        "run_id": str(uuid.uuid4()),
        "capability": capability.capability_id,
        "capability_version": capability.version,
        "consumer": {"member_id": principal.member_id, "client_id": principal.client_id},
        "consumer_class": principal.consumer_class,
        "status": status,
        "result": result,
        "provenance": provenance or [],
        "freshness": freshness,
        "limitations": limitations or [],
        "authority_status": authority_status,
        "qa_status": qa_status,
        "disclosure_class": "LEAGUE_SHARED",
    }

def execute_phase1(principal: Principal, capability_id: str) -> Dict[str, Any]:
    cap = authorize(principal, capability_id)
    if capability_id == "capabilities.list":
        result = visible_capabilities(principal)
    else:
        # Provider/SCK wiring is intentionally not fabricated in Phase 1.
        result = {"state": "NOT_WIRED", "message": "Capability contract exists; authoritative execution adapter is pending."}
    return response_envelope(principal=principal, capability=cap, result=result)
