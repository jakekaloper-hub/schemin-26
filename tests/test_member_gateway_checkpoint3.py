import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name, ROOT/path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

identity=load("identity_registry",Path("member-gateway/identity_registry.py"))
runs=load("run_store",Path("member-gateway/run_store.py"))
truth=load("truth_plane_adapter",Path("member-gateway/truth_plane_adapter.py"))
flaim=load("flaim_adapter",Path("data-gateway/flaim_adapter.py"))

RECEIPT=ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json"

def test_pitts_client_resolves_to_pitts_not_jake():
    member,client=identity.resolve_client("pitts-chatgpt")
    assert member.member_id=="pitts"
    assert client.member_id=="pitts"
    assert "commissioner" not in member.roles

def test_client_rotation_preserves_member_and_revokes_old_client():
    original=identity.CLIENTS["pitts-chatgpt"]
    try:
        new=identity.rotate_client("pitts-chatgpt","pitts-chatgpt-v2")
        assert new.member_id=="pitts"
        with pytest.raises(identity.IdentityError,match="CLIENT_REVOKED"):
            identity.resolve_client("pitts-chatgpt")
        member,_=identity.resolve_client("pitts-chatgpt-v2")
        assert member.member_id=="pitts"
    finally:
        identity.CLIENTS["pitts-chatgpt"]=original
        identity.CLIENTS.pop("pitts-chatgpt-v2",None)

def test_duplicate_run_is_not_recreated(tmp_path):
    store=runs.RunStore(tmp_path/"runs.json")
    a=store.begin("run-1","req-a","pittys_book.inputs")
    b=store.begin("run-1","req-b","pittys_book.inputs")
    assert a["created"] is True
    assert b["created"] is False
    assert b["run"]["first_request_id"]=="req-a"

def test_delivery_state_is_separate_from_workflow_state(tmp_path):
    store=runs.RunStore(tmp_path/"runs.json")
    store.begin("run-1","req-a","pittys_book.inputs")
    store.transition("run-1","PASSED")
    row=store.mark_delivered("run-1")
    assert row["workflow_state"]=="PASSED"
    assert row["delivery_state"]=="DELIVERED"

def test_existing_flaim_receipt_can_enter_truth_plane_but_is_recomputed_for_freshness():
    raw=json.loads(RECEIPT.read_text())
    normalized=flaim.normalize_capture(raw,slo_seconds=3600)
    packet=truth.from_normalized_data_gateway(normalized)
    assert packet["result"]["league"]["league_id"]==1417621
    assert len(packet["result"]["standings"])==12
    assert len(packet["result"]["matchups"])==6
    assert packet["freshness"]["snapshot_age_seconds"]>=0
    assert packet["freshness"]["stale"] is True
    assert packet["provenance"][0]["authority"]=="League Data Platform"

def test_truth_adapter_rejects_unvalidated_shape():
    with pytest.raises(truth.TruthPlaneAdapterError,match="INVALID_DATA_GATEWAY_META"):
        truth.from_normalized_data_gateway({"meta":{"stale":False}})
