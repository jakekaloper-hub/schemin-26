"""CP9 member-facing experience over the governed transport adapter."""
from pathlib import Path
import importlib.util
HERE=Path(__file__).parent
def _load(name,file):
    s=importlib.util.spec_from_file_location(name,HERE/file); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
transport=_load("member_transport","transport_adapter.py")

CAPABILITY_LABELS={
 "league.current_state":"Current league state",
 "league.history":"League history",
 "owner.identity":"Owner identity",
 "pittys_book.inputs":"Pittsy's Book inputs",
}

class MemberExperience:
    def __init__(self,ledger_path:Path,limiter=None):
        self.transport=transport.AITransportAdapter(ledger_path,limiter=limiter)

    def available_jobs(self,client_id:str):
        caps=self.transport.discover(client_id=client_id)
        return [{"capability":k,"label":CAPABILITY_LABELS.get(k,k)}
                for k in caps if k!="capabilities.list"]

    def run_book_inputs(self,*,client_id:str,season:int,week:int,truth_packet=None,deliver=True):
        out=self.transport.invoke(client_id=client_id,capability_id="pittys_book.inputs",
            request={"season":season,"week":week},truth_packet=truth_packet,deliver=deliver)
        # A duplicate completed request is intentionally returned from the run
        # ledger without re-executing the provider/service path. Rehydrate the
        # member-safe packet from the persisted run rather than assuming a new
        # packet exists.
        p=out.get("packet")
        state=(p.get("result") or {}).get("state")
        if state=="AWAITING_SCK":
            message="Schemin is waiting for validated league truth; no Book inputs were fabricated."
        elif p["freshness"]["stale"]:
            message="Schemin returned validated Book inputs, but the underlying league snapshot is stale."
        else:
            message="Schemin returned validated Book inputs."
        return {"status":out["run"]["workflow_state"],"message":message,
                "data":p.get("result"),"freshness":p["freshness"],
                "limitations":p.get("limitations",[]),"authority_status":p["authority_status"],
                "qa_status":p["qa_status"],"request_id":p["request_id"],
                "duplicate":out.get("duplicate",False)}
