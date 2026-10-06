from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"memo-os/week-4/publication-readiness"
GATE=(BASE/"WEEK_04_PAGE_GENERATION_GATE.md").read_text()
PROTOCOL=(BASE/"WEEK_04_CLOSER_PAGE_APPROVAL_PROTOCOL.md").read_text()

def test_closer_pre_render_pass_required():
    assert "CLOSER_PRE_RENDER_PASS" in GATE
    assert "before the renderer is invoked" in GATE

def test_closer_post_render_accept_required():
    assert "CLOSER_PAGE_ACCEPT" in GATE
    assert "APPROVED_FOR_LOCAL_FOLDER" in GATE

def test_bullpen_and_umpire_are_mandatory():
    assert "Bullpen Director synthesis" in GATE
    assert "Umpire adversarial preflight" in GATE

def test_operator_is_not_sole_authority():
    assert "operator/compiler" in PROTOCOL
    assert "No Closer approval = no render." in PROTOCOL

def test_commissioner_needs_only_generate_page_command():
    assert "Jake should only need to say:" in PROTOCOL
    assert "generate page N" in PROTOCOL
