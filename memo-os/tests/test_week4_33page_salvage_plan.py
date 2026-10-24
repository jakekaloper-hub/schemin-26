from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "memo-os/week-4/publication-readiness"

def text(name):
    return (BASE / name).read_text()

def test_overture_final_manuscript_has_all_six():
    s=text("WEEK_04_MATCHUP_OVERTURE_FINAL_MANUSCRIPT_2026-10-06.md")
    for i in range(1,7):
        assert f"W4-OV0{i}" in s

def test_p24_uses_matchup_payoff_sources():
    s=text("WEEK_04_P24_POWER_RANKINGS_REGENERATION_PACKET.md")
    for p in ["W4-P07","W4-P10","W4-P13","W4-P16","W4-P19","W4-P22"]:
        assert p in s
    assert "REGENERATE REQUIRED" in s
    assert "independently regenerate" in s

def test_repair_sweep_includes_front_book_and_summary_pages():
    s=text("WEEK_04_MASTER_REPAIR_SWEEP_PACKET.md")
    for page in ["W4-P01","W4-P02","W4-P03","W4-P23","W4-P24"]:
        assert page in s

def test_salvage_board_targets_33_pages():
    s=text("WEEK_04_SALVAGE_COMPLETION_BOARD.md")
    assert "33 accepted page masters" in s
    assert "OV01 → OV02 → OV03 → OV04 → OV05 → OV06" in s
