from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"memo-os/week-4/publication-readiness"
GATE=BASE/"WEEK_04_PAGE_GENERATION_GATE.md"
SALVAGE=BASE/"WEEK_04_LIVE_PRODUCTION_SALVAGE_PROTOCOL.md"
MATRIX=BASE/"WEEK_04_VISUAL_FAMILY_MATRIX.md"
AUDIT=BASE/"WEEK_04_CURRENT_RASTER_AUDIT_2026-10-06.md"

def read(p): return p.read_text()

def test_salvage_protocol_is_bound_into_gate():
    s=read(GATE)
    assert "LIVE PRODUCTION SALVAGE OVERLAY" in s
    assert "1024×1536" in s
    assert "Pages 11–22" in s

def test_remaining_matchup_chapters_are_preflighted_as_three_page_units():
    s=read(SALVAGE)
    for trio in ["Pages 11–13","Pages 14–16","Pages 17–19","Pages 20–22"]:
        assert trio in s
    assert "one chapter / one module family" in s

def test_result_pages_share_reusable_component():
    s=read(MATRIX)
    for p in ["7","10","13","16","19","22"]:
        assert re.search(rf"\| {p} \|", s)
    assert "same bottom result-strip geometry" in s
    assert "deterministic score typography" in s

def test_page_families_are_explicit_for_all_27_pages():
    s=read(MATRIX)
    nums=[int(x) for x in re.findall(r"^\| (\d+) \|",s,re.M)]
    assert nums==list(range(1,28))

def test_current_raster_audit_rejects_commissioner_as_first_qa():
    s=read(AUDIT)
    assert "Commissioner the first reliable QA layer" in s
    assert "This is unacceptable" in s

def test_page2_and_page3_remaster_are_mandatory_before_release():
    s=read(SALVAGE)
    assert "remaster Page 2 to the locked final manuscript" in s
    assert "remaster Page 3 to a clean deterministic board" in s
