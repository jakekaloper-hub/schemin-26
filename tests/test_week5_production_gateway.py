import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "memo-os/week-5/runtime/production_gate.py"

def load():
    spec = importlib.util.spec_from_file_location("week5_gate", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_existing_pages_blocked():
    gateway = load()
    for page in ("P001", "P004", "P007", "P009", "P011", "P032"):
        result = gateway.check(page)
        assert result["state"] == "GENERATION_BLOCKED", result
        assert result["reason"] == "MANIFEST_RENDER_INELIGIBLE", result

def test_unknown_page_blocked():
    assert load().check("P999")["reason"] == "UNKNOWN_PAGE"

def test_identity_and_capability_requirements_exist():
    source = GATE.read_text(encoding="utf-8")
    for expected in ("renderer_capability_state","mounted_sha256","subject_binding_id","trusted_eligibility_state","eligibility_token_validated_by_adapter","REPEATED_SUBJECT_OR_MOUNT"):
        assert expected in source

if __name__ == "__main__":
    test_existing_pages_blocked()
    test_unknown_page_blocked()
    test_identity_and_capability_requirements_exist()
    print("PASS Week 5 production gateway fail-closed regressions")
