import importlib.util
from pathlib import Path
import pytest

MODULE = Path(__file__).parents[1] / "member-gateway" / "gateway_core.py"
spec = importlib.util.spec_from_file_location("gateway_core", MODULE)
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)

Principal = gateway.Principal
AuthorizationError = gateway.AuthorizationError
ContractError = gateway.ContractError

def pitts(scopes):
    return Principal("pitts", "league_member", "pitts-chatgpt", frozenset(scopes))

def truth(stale=False):
    return {
        "result": {"league_id": 1417621, "week": 5},
        "freshness": {
            "stale": stale,
            "fetched_at": "2026-09-30T17:00:00Z",
            "snapshot_age_seconds": 900,
            "failure_reason": None,
        },
        "provenance": [{"authority":"League Data Platform","source":"validated-test-fixture"}],
        "limitations": [],
        "qa_status": "TEST_FIXTURE",
    }

def test_capability_discovery_is_scope_aware():
    p = pitts({"capabilities.read", "league.read"})
    visible = gateway.visible_capabilities(p)
    assert "capabilities.list" in visible
    assert "league.current_state" in visible
    assert "pittys_book.inputs" not in visible

def test_unknown_capability_fails_closed():
    with pytest.raises(AuthorizationError, match="CAPABILITY_UNKNOWN"):
        gateway.authorize(pitts({"capabilities.read"}), "call_warden")

def test_scope_denial_fails_closed():
    with pytest.raises(AuthorizationError, match="SCOPE_DENIED"):
        gateway.authorize(pitts({"capabilities.read"}), "pittys_book.inputs")

def test_director_calls_are_not_capabilities():
    assert all(not key.startswith("call_") for key in gateway.CAPABILITIES)

def test_phase1_capabilities_are_read_only():
    assert all(cap.read_only for cap in gateway.CAPABILITIES.values())

def test_pitts_book_can_be_delegated_without_mercer():
    visible = gateway.visible_capabilities(gateway.PITTS)
    assert "pittys_book.inputs" in visible
    assert "mercer" not in " ".join(visible.keys()).lower()

def test_jake_and_pitts_are_distinct_principals():
    assert gateway.JAKE.member_id != gateway.PITTS.member_id
    assert gateway.JAKE.consumer_class == "commissioner"
    assert gateway.PITTS.consumer_class == "league_member"

def test_unwired_authoritative_capability_creates_internal_sck_handoff_without_leaking_it():
    cap = gateway.authorize(gateway.PITTS, "league.current_state")
    out = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                          normalized_request={"week":5})
    assert out["result"] == {"state":"AWAITING_SCK"}
    assert "handoff" not in out["result"]
    h = gateway.compile_sck_handoff(
        principal=gateway.PITTS, capability=cap, normalized_request={"week":5},
        request_id=out["request_id"], run_id=out["run_id"])
    assert h["to"] == "SCK"
    assert h["status"] == "HANDOFF_READY"
    assert h["run_id"] == out["run_id"]

def test_idempotency_run_id_is_stable_for_same_material_request():
    a = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        normalized_request={"week":5})
    b = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        normalized_request={"week":5})
    assert a["run_id"] == b["run_id"]
    assert a["request_id"] != b["request_id"]

def test_idempotency_changes_when_request_changes():
    a = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        normalized_request={"week":5})
    b = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        normalized_request={"week":6})
    assert a["run_id"] != b["run_id"]

def test_truth_plane_freshness_and_provenance_propagate_unchanged():
    source = truth(stale=True)
    out = gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                          normalized_request={"week":5}, truth_packet=source)
    assert out["freshness"] == source["freshness"]
    assert out["provenance"] == source["provenance"]
    assert out["result"]["league_id"] == 1417621

def test_missing_freshness_fails_closed():
    bad = truth()
    del bad["freshness"]["failure_reason"]
    with pytest.raises(ContractError, match="MISSING_FRESHNESS_FIELDS"):
        gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        truth_packet=bad)

def test_missing_provenance_fails_closed():
    bad = truth()
    del bad["provenance"]
    with pytest.raises(ContractError, match="MISSING_PROVENANCE"):
        gateway.execute(principal=gateway.PITTS, capability_id="league.current_state",
                        truth_packet=bad)

def test_private_outflow_is_denied():
    cap = gateway.authorize(gateway.PITTS, "league.current_state")
    with pytest.raises(AuthorizationError, match="OUTFLOW_DISCLOSURE_DENIED"):
        gateway.authorize_outflow(gateway.PITTS, cap, {"disclosure_class":"PRIVATE"})

def test_mercer_material_is_denied_at_egress():
    cap = gateway.authorize(gateway.PITTS, "league.current_state")
    with pytest.raises(AuthorizationError, match="MERCER_FIREWALL_VIOLATION"):
        gateway.authorize_outflow(gateway.PITTS, cap, {"result":"Mercer private valuation"})

def test_response_does_not_self_certify():
    out = gateway.execute(principal=gateway.PITTS, capability_id="capabilities.list")
    assert out["qa_status"] == "NOT_CERTIFIED"
    assert out["authority_status"] == "BULLPEN_ROUTED"
