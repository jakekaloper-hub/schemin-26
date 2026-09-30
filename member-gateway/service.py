"""Checkpoint 4 vertical-slice service: authenticated member request -> governed result -> delivery."""
from pathlib import Path
import importlib.util

HERE=Path(__file__).parent
def _load(name,file):
    spec=importlib.util.spec_from_file_location(name,HERE/file)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
core=_load("gateway_core","gateway_core.py")
identity=_load("identity_registry","identity_registry.py")
runs=_load("run_store","run_store.py")

class DeliveryError(RuntimeError): pass

def principal_for_client(client_id: str):
    member, client = identity.resolve_client(client_id)
    consumer_class = "commissioner" if "commissioner" in member.roles else "league_member"
    return core.Principal(member.member_id, consumer_class, client.client_id, client.scopes)

class GatewayService:
    def __init__(self, ledger_path: Path):
        self.store=runs.RunStore(ledger_path)

    def request(self, *, client_id: str, capability_id: str, normalized_request: dict,
                truth_packet=None, deliver=True):
        principal=principal_for_client(client_id)
        cap=core.authorize(principal,capability_id)
        run_id=core.idempotency_key(principal=principal,capability=cap,normalized_request=normalized_request)
        request_id=__import__("uuid").uuid4().hex
        begin=self.store.begin(run_id,request_id,capability_id)
        if not begin["created"] and begin["run"]["workflow_state"]=="PASSED":
            return {"duplicate":True,"run":begin["run"]}

        self.store.transition(run_id,"ROUTED")
        packet=core.execute(principal=principal,capability_id=capability_id,
                            normalized_request=normalized_request,truth_packet=truth_packet)
        # execute() generates its own request id but must converge on the same material run identity.
        if packet["run_id"] != run_id:
            raise RuntimeError("RUN_ID_DIVERGENCE")
        if truth_packet is None:
            self.store.transition(run_id,"BLOCKED")
            return {"duplicate":False,"packet":packet,"run":self.store._read()[run_id]}

        # Warden egress gate: re-resolve the live delegated client immediately
        # before delivery so mid-run revocation cannot reuse ingress authority.
        live_principal=principal_for_client(client_id)
        live_cap=core.authorize(live_principal,capability_id)
        core.authorize_outflow(live_principal,live_cap,packet)

        self.store.transition(run_id,"PASSED")
        if not deliver:
            raise DeliveryError("DELIVERY_FAILED")
        self.store.mark_delivered(run_id)
        return {"duplicate":False,"packet":packet,"run":self.store._read()[run_id]}
