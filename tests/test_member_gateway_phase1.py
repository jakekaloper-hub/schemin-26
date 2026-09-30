import importlib.util
from pathlib import Path
import pytest

MODULE = Path(__file__).parents[1] / "member-gateway" / "gateway_core.py"
spec = importlib.util.spec_from_file_location("gateway_core", MODULE)
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)

Principal = gateway.Principal
AuthorizationError = gateway.AuthorizationError

def pitts(scopes):
    return Principal("pitts", "league_member", "pitts-chatgpt", frozenset(scopes))

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
    p = pitts({"capabilities.read", "pittys_book.inputs"})
    visible = gateway.visible_capabilities(p)
    assert "pittys_book.inputs" in visible
    assert "mercer" not in " ".join(visible.keys()).lower()

def test_response_does_not_claim_certification():
    p = pitts({"capabilities.read"})
    out = gateway.execute_phase1(p, "capabilities.list")
    assert out["qa_status"] == "NOT_CERTIFIED"
    assert out["authority_status"] == "BULLPEN_ROUTED"
    assert out["consumer"]["member_id"] == "pitts"

def test_unwired_authoritative_capability_is_explicit():
    p = pitts({"league.read"})
    out = gateway.execute_phase1(p, "league.current_state")
    assert out["result"]["state"] == "NOT_WIRED"
    assert out["qa_status"] == "NOT_CERTIFIED"
