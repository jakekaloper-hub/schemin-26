import importlib.util, json
from pathlib import Path
import pytest
ROOT=Path(__file__).parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
service=load("gateway_service",Path("member-gateway/service.py"))
truth=load("truth_plane_adapter4",Path("member-gateway/truth_plane_adapter.py"))
flaim=load("flaim_adapter4",Path("data-gateway/flaim_adapter.py"))
identity=service.identity
core=service.core
RECEIPT=ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json"

def packet():
    return truth.from_normalized_data_gateway(flaim.normalize_capture(json.loads(RECEIPT.read_text()),slo_seconds=3600))

def test_pitts_vertical_slice_delivers_validated_stale_inputs(tmp_path):
    s=service.GatewayService(tmp_path/"runs.json")
    out=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                  normalized_request={"season":2026,"week":5},truth_packet=packet())
    assert out["run"]["workflow_state"]=="COMPLETED"
    assert out["run"]["delivery_state"]=="DELIVERED"
    assert out["packet"]["consumer"]["member_id"]=="pitts"
    assert out["packet"]["freshness"]["stale"] is True
    assert out["packet"]["qa_status"]=="DATA_GATEWAY_VALIDATED"

def test_duplicate_pitts_submit_does_not_reexecute(tmp_path):
    s=service.GatewayService(tmp_path/"runs.json")
    a=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                normalized_request={"season":2026,"week":5},truth_packet=packet())
    b=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                normalized_request={"season":2026,"week":5},truth_packet=packet())
    assert a["duplicate"] is False
    assert b["duplicate"] is True
    assert b["run"]["run_id"]==a["run"]["run_id"]

def test_revoked_client_is_denied_before_truth_load(tmp_path):
    original=identity.CLIENTS["pitts-chatgpt"]
    try:
        identity.revoke_client("pitts-chatgpt")
        s=service.GatewayService(tmp_path/"runs.json")
        with pytest.raises(identity.IdentityError,match="CLIENT_REVOKED"):
            s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                      normalized_request={"week":5},truth_packet=packet())
        assert not (tmp_path/"runs.json").exists()
    finally:
        identity.CLIENTS["pitts-chatgpt"]=original

def test_cross_member_run_ids_are_isolated(tmp_path):
    s=service.GatewayService(tmp_path/"runs.json")
    p=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                normalized_request={"week":5},truth_packet=packet())
    j=s.request(client_id="jake-chatgpt",capability_id="pittys_book.inputs",
                normalized_request={"week":5},truth_packet=packet())
    assert p["run"]["run_id"] != j["run"]["run_id"]
    assert p["packet"]["consumer"]["member_id"]=="pitts"
    assert j["packet"]["consumer"]["member_id"]=="jake"

def test_mercer_injection_is_blocked_at_outflow(tmp_path):
    bad=packet(); bad["result"]["private_note"]="Mercer private valuation"
    s=service.GatewayService(tmp_path/"runs.json")
    with pytest.raises(core.AuthorizationError,match="MERCER_FIREWALL_VIOLATION"):
        s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                  normalized_request={"week":5},truth_packet=bad)

def test_malformed_truth_packet_fails_before_pass(tmp_path):
    bad=packet(); del bad["freshness"]["fetched_at"]
    s=service.GatewayService(tmp_path/"runs.json")
    with pytest.raises(core.ContractError,match="MISSING_FRESHNESS_FIELDS"):
        s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                  normalized_request={"week":5},truth_packet=bad)
    state=json.loads((tmp_path/"runs.json").read_text())
    assert list(state.values())[0]["workflow_state"]=="ROUTED"

def test_delivery_failure_does_not_reexecute_completed_workflow(tmp_path):
    s=service.GatewayService(tmp_path/"runs.json")
    with pytest.raises(service.DeliveryError):
        s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                  normalized_request={"week":5},truth_packet=packet(),deliver=False)
    state=json.loads((tmp_path/"runs.json").read_text())
    row=list(state.values())[0]
    assert row["workflow_state"]=="COMPLETED"
    assert row["delivery_state"]=="NOT_DELIVERED"
    retry=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                    normalized_request={"week":5},truth_packet=packet())
    assert retry["duplicate"] is True

def test_missing_truth_blocks_without_fabrication(tmp_path):
    s=service.GatewayService(tmp_path/"runs.json")
    out=s.request(client_id="pitts-chatgpt",capability_id="pittys_book.inputs",
                  normalized_request={"week":5},truth_packet=None)
    assert out["packet"]["result"]["state"]=="AWAITING_SCK"
    assert out["run"]["workflow_state"]=="BLOCKED"
    assert out["run"]["delivery_state"]=="NOT_DELIVERED"
