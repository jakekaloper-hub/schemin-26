"""Enforce Commissioner Week 5 image-page output without creating a parallel Memo OS.

This suite checks page handoff metadata, not artistic merit or renderer-conditioning
proof. Final image QA requires actual generated PNGs and independent review.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEEK5 = ROOT / "memo-os" / "week-5"
MANIFEST = WEEK5 / "PUBLICATION_PAGE_MANIFEST.json"
AMENDMENT = WEEK5 / "WEEK_5_CINEMATIC_ARTWORK_FIRST_FIDELITY_AMENDMENT_2026-10-13.md"

def test_one_numbered_png_expected_per_source_page():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pages = m["pages"]
    expected_ids = [f"P{i:03d}" for i in range(1, 33)]
    assert [p["page_id"] for p in pages] == expected_ids
    names = [p["expected_flattened_png"] for p in pages]
    assert len(set(names)) == 32
    for p in pages:
        assert p["expected_flattened_png"].startswith("SCHEMIN26_W05_" + p["page_id"] + "_")
        assert p["expected_flattened_png"].endswith(".png")
        assert p["image_artifact_status"] != "ACCEPTED_FINAL"
        assert p["image_qa_status"] != "APPROVED"
        assert p["render_eligible"] is False
    assert m["page_count_provisional"] == 32 and m["locked_page_count"] is False

def test_png_page_handoff_excludes_bullpen_pdf_assembly():
    c = json.loads(MANIFEST.read_text(encoding="utf-8"))["output_artifact_contract"]
    assert c["production_unit"] == "COMPLETE_INDIVIDUAL_PAGE_IMAGE"
    assert c["format"] == "PNG"
    assert (c["pixel_width"], c["pixel_height"]) == (1024, 1536)
    assert c["pdf_assembler"] == "Commissioner"
    assert c["pdf_is_bullpen_deliverable"] is False
    assert c["mobile_review_width_px"] == 390

def test_authentic_33_page_benchmark_is_explicit():
    s = AMENDMENT.read_text(encoding="utf-8")
    assert "33 pages" in s
    assert "1024 × 1536" in s
    assert "1fc322a3eb0e8b43499ee4556c715ba4c00a8c388e7a92a904954a35f0482124" in s
    for key in ["P1–P3", "P4–P8", "P9–P12", "P13–P16", "P17–P20", "P21–P24", "P25–P28", "P29–P33"]:
        assert key in s
    assert "VISUAL_PROOF_ONLY" in s

def test_master_packet_supersedes_pdf_first_without_canon_promotion():
    master = (WEEK5 / "MASTER_PRODUCTION_PACKET.md").read_text(encoding="utf-8")
    assert "Controlling Commissioner production-format correction" in master
    assert "WEEK_5_CINEMATIC_ARTWORK_FIRST_FIDELITY_AMENDMENT_2026-10-13.md" in master
    assert "The Commissioner will compile" in master
    assert "render_eligible=false" in master

def test_pitty_deferred_cover_locked_and_owner_conditioning_honest():
    p001 = (WEEK5 / "pages/P001-cover/PAGE_PACKET.md").read_text(encoding="utf-8")
    p030 = (WEEK5 / "pages/P030-pittys-book/PAGE_PACKET.md").read_text(encoding="utf-8")
    assert "Mike Ditka" in p001 and "CANON_RENDER_HOLD" in p001
    assert "PITTY_INPUT_DEFERRED_TO_2026-10-14" in p030
    assert "PITTY" in json.loads(MANIFEST.read_text(encoding="utf-8"))["pages"][29]["expected_flattened_png"]
    asset = json.loads((WEEK5 / "production-evidence/WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json").read_text(encoding="utf-8"))
    assert asset["source_state"] == "12_OF_12_SOURCE_BYTES_SHA256_AND_GIT_BLOB_MATCH"
    assert asset["renderer_mount_state"] == "NOT_PROVEN"
    assert asset["subject_binding_state"] == "NOT_PROVEN"

if __name__ == "__main__":
    checks = [v for name, v in sorted(globals().items()) if name.startswith("test_") and callable(v)]
    for check in checks:
        check()
        print("PASS", check.__name__)
    print("Week 5 PNG-only handoff: %d checks passed" % len(checks))
