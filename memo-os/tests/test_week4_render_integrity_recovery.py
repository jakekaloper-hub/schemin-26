import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "memo-os/week-4/publication-readiness/WEEK_04_OFFICIAL_MANUAL_PRODUCTION_PACKET.md"
REGISTRY = ROOT / "memo-os/week-4/publication-readiness/WEEK_04_PUBLISHABLE_IDENTITY_REGISTRY.json"
GATE = ROOT / "memo-os/week-4/publication-readiness/WEEK_04_PAGE_GENERATION_GATE.md"


def test_publishable_registry_has_12_unique_teams():
    d=json.loads(REGISTRY.read_text())
    teams=d["teams"]
    assert len(teams)==12
    assert len({t["team_id"] for t in teams})==12
    assert len({t["publishable_name"] for t in teams})==12


def test_divisions_are_four_teams_each():
    d=json.loads(REGISTRY.read_text())
    assert {k:len(v) for k,v in d["divisions"].items()}=={"Burgers":4,"Wings":4,"Pizza":4}
    assert "D0nkey K0ng" in d["divisions"]["Burgers"]
    assert "ObiWan Jacoby" in d["divisions"]["Burgers"]
    assert "Red Leopards" in d["divisions"]["Wings"]
    assert "The Chili Cheesers" in d["divisions"]["Wings"]
    assert "The LLC" in d["divisions"]["Pizza"]
    assert "His Majesty's Blood" in d["divisions"]["Pizza"]


def test_wings_semantics_locked_to_chicken_wings():
    s=PACKET.read_text()
    assert "Wings = chicken wings" in s
    assert "never angel/bird/dragon wings" in s


def test_page3_forbids_character_icons_and_generative_data():
    s=PACKET.read_text()
    p3=s.split("# PAGE 3",1)[1].split("# PAGE 4",1)[0]
    assert "Character icons:** **FORBIDDEN" in p3
    assert "deterministic composition only" in p3
    for name in ["D0nkey K0ng","ObiWan Jacoby","Mud Dogs","Three Dreaded Snake","Red Leopards","Dr. Duckhook","Slob on my Dobb","The Chili Cheesers","The LLC","His Majesty's Blood","El Niño","Seven Deadly Chins"]:
        assert name in p3


def test_gotw_exact_names_persist_pages_4_to_7():
    s=PACKET.read_text()
    for n in range(4,8):
        section=s.split(f"# PAGE {n}",1)[1].split(f"# PAGE {n+1}",1)[0]
        assert "D0nkey K0ng" in section
        assert "ObiWan Jacoby" in section
        assert "GAME OF THE WEEK" in section


def test_internal_dk_obi_shorthand_not_publishable_heading():
    s=PACKET.read_text()
    assert "# PAGE 4 — DK × OBI" not in s
    assert "# PAGE 5 — DK × OBI" not in s
    assert "# PAGE 6 — DK × OBI" not in s
    assert "# PAGE 7 — DK × OBI" not in s


def test_page2_is_issue_specific_not_generic_division_explainer():
    s=PACKET.read_text()
    p2=s.split("# PAGE 2",1)[1].split("# PAGE 3",1)[0]
    assert "THE WORLD REMEMBERS" in p2
    for signal in ["highland ridge","marsh blind","coastal golf","man-cave","gaming-exchange","storm wall"]:
        assert signal in p2
    assert "generic three-castle division poster" in p2


def test_gate_is_closed_during_recovery():
    s=GATE.read_text()
    assert "PRODUCTION HOLD" in s
    assert "Commissioner review is not the first defect-detection layer" in s
