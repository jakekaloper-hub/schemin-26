import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
service=load("cp9m_service",Path("member-gateway/service.py"))
truth=load("cp9m_truth",Path("member-gateway/truth_plane_adapter.py"))
flaim=load("cp9m_flaim",Path("data-gateway/flaim_adapter.py"))
receipt=json.loads((ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json").read_text())
def packet(): return truth.from_normalized_data_gateway(flaim.normalize_capture(receipt))
def request(s,deliver=True):
 return s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",normalized_request={"season":2026,"week":5},truth_packet=packet(),deliver=deliver)

def test_new_run_stores_response(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json"); out=request(s)
 assert out["run"]["ledger_version"]==3
 assert out["run"]["response_state"]=="STORED"

def test_duplicate_returns_same_packet(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json"); a=request(s); b=request(s)
 assert b["duplicate"] is True
 assert b["packet"]["request_id"]==a["packet"]["request_id"]

def test_delivery_failure_keeps_response(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json")
 with pytest.raises(service.DeliveryError): request(s,False)
 assert request(s)["duplicate"] is True

def test_old_completed_row_without_packet_is_not_served(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json")
 p=service.principal_for_client("pitts-chatgpt"); cap=service.core.authorize(p,"pittys_book.inputs")
 rid=service.core.idempotency_key(principal=p,capability=cap,normalized_request={"season":2026,"week":5})
 row={"run_id":rid,"first_request_id":"old","capability":"pittys_book.inputs","workflow_state":"PASSED","delivery_state":"DELIVERED"}
 (tmp_path/"runs.json").write_text(json.dumps({rid:row}))
 with pytest.raises(service.runs.RunConflictError,match="LEGACY_COMPLETED_RUN_NOT_REPLAYABLE"): request(s)

def test_revoked_client_cannot_receive_stored_response(tmp_path):
 s=service.GatewayService(tmp_path/"runs.json"); request(s)
 ident=service.identity; original=ident.CLIENTS["pitts-chatgpt"]
 try:
  ident.revoke_client("pitts-chatgpt")
  with pytest.raises(ident.IdentityError,match="CLIENT_REVOKED"): request(s)
 finally: ident.CLIENTS["pitts-chatgpt"]=original
