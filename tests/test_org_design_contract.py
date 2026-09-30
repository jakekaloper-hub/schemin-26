from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"docs"/"governance"

def read(name):
    return (GOV/name).read_text()

def test_all_phase_artifacts_exist():
    required=[
      "SCHEMIN_ORG_DESIGN_PROGRAM_CHARTER_V1.md",
      "SCHEMIN_CAPABILITY_MAP_V1.md",
      "SCHEMIN_BULLPEN_AUTHORITY_MATRIX_V1.md",
      "SCHEMIN_ORGANIZATIONAL_FAILURE_REGISTER_V1.md",
      "SCHEMIN_ZERO_BASE_OPERATING_MODEL_V1.md",
      "SCHEMIN_ORG_GAP_RESOLUTION_DECISION_V1.md",
      "SCHEMIN_PROJECT_COMMAND_V1.md",
      "SCHEMIN_ROLE_CONTRACTS_V1.md",
      "SCHEMIN_ORGANIZATIONAL_RUNTIME_V1.md",
      "SCHEMIN_ORG_ACCEPTANCE_SUITE_V1.md",
      "SCHEMIN_ORG_RATIFICATION_V1.md",
    ]
    assert all((GOV/x).exists() for x in required)

def test_18_director_constitution_not_amended():
    text=read("SCHEMIN_ORG_GAP_RESOLUTION_DECISION_V1.md")
    assert "Do not create Director #19" in text
    assert "PROJECT FUNCTION" in text

def test_visual_lead_cannot_override_canon():
    text=read("SCHEMIN_ROLE_CONTRACTS_V1.md")
    section=text.split("## Visual Direction Lead",1)[1].split("## The Pitching Coach",1)[0]
    assert "CANNOT alter character identity" in section
    assert "not a universal Bullpen Director" in section

def test_umpire_independent():
    text=read("SCHEMIN_ROLE_CONTRACTS_V1.md")
    assert "CANNOT be the producing role for an artifact it certifies" in text

def test_reference_mount_fails_closed():
    text=read("SCHEMIN_ORGANIZATIONAL_RUNTIME_V1.md")
    assert "GENERATION_BLOCKED" in text
    assert "authenticated mount proof" in text

def test_mercer_firewall():
    text=read("SCHEMIN_ORGANIZATIONAL_RUNTIME_V1.md")
    assert "FIREWALL_BLOCK" in text

def test_shadow_titles_normalized():
    text=read("SCHEMIN_BULLPEN_AUTHORITY_MATRIX_V1.md")
    for title in ["Visual Director","Character Director","Continuity Director","Memo OS Director","Novel Director"]:
        assert title in text
    assert "PROJECT FUNCTIONS" in text

def test_character_failures_not_misclassified():
    text=read("SCHEMIN_ORGANIZATIONAL_FAILURE_REGISTER_V1.md")
    assert "do NOT by themselves prove a missing Bullpen Director" in text
