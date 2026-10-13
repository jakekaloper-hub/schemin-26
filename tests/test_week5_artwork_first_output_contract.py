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


def test_every_png_has_specific_week4_visual_comparison():
    p = WEEK5 / "production-evidence" / "WEEK_5_PAGE_BY_PAGE_WEEK4_VISUAL_COMPARATOR_MATRIX_2026-10-13.json"
    ref = json.loads(p.read_text(encoding="utf-8"))
    assert ref["source_pdf"]["page_count"] == 33
    assert ref["source_pdf"]["each_page_px"] == [1024, 1536]
    assert ref["target"]["format"] == "PNG"
    assert ref["target"]["pdf_assembler"] == "Commissioner"
    pages = ref["pages"]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["pages"]
    assert len(pages) == len(manifest) == 32
    assert [x["source_page_id"] for x in pages] == [x["page_id"] for x in manifest]
    assert [x["expected_png"] for x in pages] == [x["expected_flattened_png"] for x in manifest]
    for row in pages:
        assert row["week4_reference_pages"], row["source_page_id"]
        assert all(1 <= i <= 33 for i in row["week4_reference_pages"])
        assert row["review_focus"].strip()
    assert pages[0]["week4_reference_pages"] == [1]
    assert 2 in pages[1]["week4_reference_pages"]
    assert 30 in pages[27]["week4_reference_pages"]
    assert 31 in pages[29]["week4_reference_pages"]
    assert 33 in pages[31]["week4_reference_pages"]
    assert 25 in pages[11]["week4_reference_pages"]  # P012 Western storm, not coastal golf
    assert 13 in pages[15]["week4_reference_pages"]  # P016 golf, not tavern
    assert 25 in pages[19]["week4_reference_pages"]  # P020 Jeep rain, not Pitty's Book
    assert 4 in pages[23]["week4_reference_pages"]   # P024 joust, not unrelated weather



def test_fidelity_scores_never_override_character_identity_gate():
    ref = json.loads((WEEK5 / "production-evidence" / "WEEK_5_PAGE_BY_PAGE_WEEK4_VISUAL_COMPARATOR_MATRIX_2026-10-13.json").read_text(encoding="utf-8"))
    assert len(ref["review"]["mandatory_dimensions"]) == 6
    assert "identity/canon" in ref["review"]["art_acceptance"]
    assert ref["proof_status"]["page"] == "P002"
    assert ref["proof_status"]["state"] == "FAILED_W4_FIDELITY"


def _character_title_contract():
    return json.loads((WEEK5 / "production-evidence" / "WEEK_5_CHARACTER_AND_TITLE_RENDER_GATES_2026-10-13.json").read_text(encoding="utf-8"))

def test_exact_32_visible_titles_and_no_repeated_dominant_masthead():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    c = _character_title_contract()
    assert len(m["pages"]) == len(c["pages"]) == 32
    assert [x["page_id"] for x in c["pages"]] == [x["page_id"] for x in m["pages"]]
    for p, expected in zip(m["pages"], c["pages"]):
        assert p["reader_facing_primary_header"] == expected["display_header"]
        assert p["primary_header_brand_policy"] == expected["league_wordmark_policy"]
        assert p["reader_facing_primary_header_priority"] == "REQUIRED_TOP_TEXT_ON_PAGE"
        assert p["render_eligible"] is False
        assert expected["accepted_final_art"] is False
        if int(p["page_id"][1:]) != 1:
            assert p["primary_header_brand_policy"] == "NO_LARGE_REPEATED_SCHEMIN_26_MASTHEAD"
    assert m["pages"][0]["reader_facing_primary_header"] == "FOR DA BEARS"
    assert m["pages"][1]["reader_facing_primary_header"] == "THE LAND REMEMBERS"
    assert m["pages"][8]["reader_facing_primary_header"] == "The LLC. at Mud Dogs"

def test_each_matchup_primary_header_matches_actual_home_and_away():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    waves = m["matchup_waves"]
    assert len(waves) == 6
    for wave in waves:
        expected = f"{wave['away']} at {wave['home']}"
        assert len(wave["page_ids"]) == 4
        for page_id in wave["page_ids"]:
            p = next(x for x in m["pages"] if x["page_id"] == page_id)
            assert p["reader_facing_primary_header"] == expected, page_id

def test_all_32_page_preflights_enforce_character_and_title():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    script = (WEEK5 / "production-evidence" / "WEEK_5_ORDERED_PNG_PRODUCTION_SCRIPT_2026-10-13.md").read_text(encoding="utf-8")
    for p in m["pages"]:
        content = (ROOT / p["packet_path"]).read_text(encoding="utf-8")
        assert content.count("## Commissioner 2026-10-13 hard render correction: species and visible header") == 1, p["page_id"]
        assert p["reader_facing_primary_header"] in content
        assert "NO" in content or "not" in content.lower()
        assert f"## {p['page_id']} —" in script
        assert f"LATEST COMMISSIONER 2026-10-13 TITLE / CHARACTER LOCK" in script
    assert script.count("LATEST COMMISSIONER 2026-10-13 TITLE / CHARACTER LOCK") == 32

def test_original_mud_dogs_subject_species_and_llc_costume_survive_all_swamp_pages():
    c = _character_title_contract()
    d = c["owner_visual_invariants"]["CHAR-BOBBY-MITCHELL"]
    llc = c["owner_visual_invariants"]["CHAR-DAVID-BABB"]
    assert d["species"] == "MONSTROUS_QUADRUPED_CANINE"
    assert "FOUR" not in d["species"] or "QUADRUPED" in d["species"]
    assert "human body" in d["reject"] and "human torso" in d["reject"]
    assert "shotgun-bearing human" in d["reject"]
    assert llc["species"] == "HUMAN_CORPORATE_RAIDER"
    for n in range(8, 12):
        p = c["pages"][n-1]
        text = (ROOT / json.loads(MANIFEST.read_text(encoding="utf-8"))["pages"][n-1]["packet_path"]).read_text(encoding="utf-8")
        assert p["display_header"] == "The LLC. at Mud Dogs", n
        assert set(p["owner_character_ids"]) == {"CHAR-DAVID-BABB", "CHAR-BOBBY-MITCHELL"}
        assert "FOR DA BEARS" in text
        assert "human" in text.lower()
    assert c["pages"][8]["secondary_scene_headline"] == "INDUSTRIAL FORCES ARRIVE"

def test_mud_dogs_uploaded_original_byte_identity_equals_registered_git_source():
    source = json.loads((WEEK5 / "production-evidence" / "WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json").read_text(encoding="utf-8"))
    entry = next(x for x in source["assets"] if x["character_id"] == "CHAR-BOBBY-MITCHELL")
    assert entry["raw_sha256"] == "462e5d6517b5653458c8d32c20692e94d037b134de7aac18325c1af41647eefc"
    c = _character_title_contract()
    assert c["pages"][8]["owner_reference_requirements"][1]["raw_sha256"] == entry["raw_sha256"]
    assert c["pages"][8]["rendering_provenance"] == "NOT_PROVEN"

def test_commissioner_rejection_is_binding_and_not_promoted():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    c = _character_title_contract()
    p = m["pages"][8]
    assert p["page_id"] == "P009"
    assert p["page_specific_art_rejection"] == "REJECTED_BOBBY_SPECIES_AND_MATCHUP_HEADER"
    assert p["image_artifact_status"] != "ACCEPTED_FINAL"
    assert p["render_eligible"] is False
    assert c["page_rejection"]["verdict"] == "REJECTED"
    assert len(c["page_rejection"]["failure_codes"]) == 3
    report = (WEEK5 / "production-evidence" / "WEEK_5_P009_REJECTION_AND_32_PAGE_RENDER_CORRECTION_2026-10-13.md").read_text(encoding="utf-8")
    assert "FATAL CANON SUBJECT REPLACEMENT" in report
    assert "FATAL HEADER HIERARCHY" in report
    assert "462e5d6517b5653458c8d32c20692e94d037b134de7aac18325c1af41647eefc" in report

if __name__ == "__main__":
    checks = [v for name, v in sorted(globals().items()) if name.startswith("test_") and callable(v)]
    for check in checks:
        check()
        print("PASS", check.__name__)
    print("Week 5 PNG-only handoff: %d checks passed" % len(checks))
