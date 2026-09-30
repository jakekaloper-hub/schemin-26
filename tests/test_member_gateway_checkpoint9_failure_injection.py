import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
service=load("cp9fi_service",Path("member-gateway/service.py"))
truth=load("cp9fi_truth",Path("member-gateway/truth_plane_adapter.py"))
flaim=load("cp9fi_flaim",Path("data-gateway/flaim_adapter.py"))
receipt=json.loads((ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json").read_text())
def packet(): return truth.from_normalized_data_gateway(flaim.normalize_capture(receipt))
def call(s,deliver=True):
 return s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",normalized_request={"week":5},truth_packet=packet(),deliver=deliver)

def test_interruption_before_complete_never_looks_replayable(tmp_path,monkeypatch):
 s=service.GatewayService(tmp_path/"runs.json")
 def fail_complete(*args,**kwargs): raise OSError("simulated durable-write failure")
 monkeypatch.setattr(s.store,"complete",fail_complete)
 with pytest.raises(OSError): call(s)
 row=next(iter(json.loads((tmp_path/"runs.json").read_text()).values()))
 assert row["workflow_state"]=="ROUTED"
 assert row["response_state"]=="ABSENT"

def test_after_complete_before_delivery_is_replayable(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json")
 with pytest.raises(service.DeliveryError): call(s,False)
 row=next(iter(json.loads((tmp_path/"runs.json").read_text()).values()))
 assert row["workflow_state"]=="COMPLETED"
 assert row["response_state"]=="STORED"
 assert row["delivery_state"]=="NOT_DELIVERED"
 assert call(s)["duplicate"] is True

def test_mark_delivered_cannot_promote_incomplete_run(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json")
 p=service.principal_for_client("pitts-chatgpt"); cap=service.core.authorize(p,"pittys_book.inputs")
 rid=service.core.idempotency_key(principal=p,capability=cap,normalized_request={"week":5})
 s.store.begin(rid,"r1","pittys_book.inputs")
 with pytest.raises(service.runs.RunConflictError,match="RUN_NOT_REPLAYABLE"): s.store.mark_delivered(rid)

def test_arbitrary_terminal_transition_is_forbidden(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json")
 s.store.begin("r","q","pittys_book.inputs")
 with pytest.raises(service.runs.RunConflictError,match="USE_COMPLETE_FOR_TERMINAL_SUCCESS"):
  s.store.transition("r","COMPLETED")
