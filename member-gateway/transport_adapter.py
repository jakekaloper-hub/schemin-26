"""CP7 thin AI-facing transport adapter.

This module deliberately models transport semantics without choosing/deploying a
network server. Authentication is delegated-client identity; authority remains
in GatewayService and the Schemin control plane.
"""
from pathlib import Path
import importlib.util

HERE=Path(__file__).parent
def _load(name,file):
    spec=importlib.util.spec_from_file_location(name,HERE/file)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
service=_load("transport_service","service.py")
core=service.core

class TransportContractError(ValueError): pass
class TransportRateLimitError(RuntimeError): pass

MAX_REQUEST_KEYS=8
MAX_STRING_LENGTH=4096

class InMemoryLimiter:
    """Deterministic CP7 limiter proving the transport boundary; not production distributed rate limiting."""
    def __init__(self, max_requests=20):
        self.max_requests=max_requests
        self.counts={}
    def check(self, client_id):
        n=self.counts.get(client_id,0)+1
        if n>self.max_requests:
            raise TransportRateLimitError("CLIENT_RATE_LIMITED")
        self.counts[client_id]=n

def _validate_request(value):
    if not isinstance(value,dict):
        raise TransportContractError("REQUEST_MUST_BE_OBJECT")
    if len(value)>MAX_REQUEST_KEYS:
        raise TransportContractError("REQUEST_TOO_WIDE")
    for k,v in value.items():
        if not isinstance(k,str):
            raise TransportContractError("REQUEST_KEY_INVALID")
        if isinstance(v,str) and len(v)>MAX_STRING_LENGTH:
            raise TransportContractError("REQUEST_VALUE_TOO_LARGE")
        if isinstance(v,(dict,list,tuple,set)):
            raise TransportContractError("NESTED_REQUEST_NOT_ALLOWED")

class AITransportAdapter:
    def __init__(self, ledger_path: Path, limiter=None):
        self.service=service.GatewayService(ledger_path)
        self.limiter=limiter or InMemoryLimiter()

    def discover(self, *, client_id: str):
        self.limiter.check(client_id)
        principal=service.principal_for_client(client_id)
        # Discovery is itself governed; it cannot enumerate hidden/internal tools.
        return core.execute(principal=principal,capability_id="capabilities.list")["result"]

    def invoke(self, *, client_id: str, capability_id: str, request: dict,
               truth_packet=None, deliver=True):
        self.limiter.check(client_id)
        _validate_request(request)
        if capability_id not in core.CAPABILITIES:
            raise core.AuthorizationError("CAPABILITY_UNKNOWN")
        if not core.CAPABILITIES[capability_id].read_only:
            raise core.AuthorizationError("MUTATING_CAPABILITY_DENIED")
        return self.service.request(client_id=client_id,capability_id=capability_id,
                                    normalized_request=request,truth_packet=truth_packet,
                                    deliver=deliver)
