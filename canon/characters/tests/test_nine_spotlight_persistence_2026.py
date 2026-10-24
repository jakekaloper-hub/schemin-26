"""Nine owner spotlight references must be durable Git bytes, never silent primary authority."""
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[3]
REG=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
EXPECTED={
"CHAR-BEN-WHIPPLE","CHAR-KEVIN-ZEEK","CHAR-BOBBY-MITCHELL",
"CHAR-MANNING-WELTY","CHAR-DAVID-BABB","CHAR-ZACH-WILSON",
"CHAR-JAKE-KALOPER","CHAR-BRANDON-PRYOR","CHAR-JORDAN-HOLLINGSHEAD",
}

def test_all_nine_supplementary_assets_present_and_hash_verified():
    registered={entry["character_id"]:entry for entry in REG["entries"]}
    assert len(EXPECTED)==9
    for cid in EXPECTED:
        rp=ROOT/f"canon/characters/{cid}/OWNER_SPOTLIGHT_2026_RECEIPT.json"
        receipt=json.loads(rp.read_text())
        src=ROOT/receipt["stored_repository_path"]
        content=src.read_bytes()
        assert content[:8]==bytes.fromhex("89504e470d0a1a0a")
        assert hashlib.sha256(content).hexdigest()==receipt["stored_sha256"]
        assert len(content)==receipt["stored_size_bytes"]
        assert list(struct.unpack(">II",content[16:24]))==receipt["dimensions"]
        assert receipt["character_id"]==cid
        assert receipt["owner"]==registered[cid]["owner"]
        assert receipt["primary_expected_sha256"]==registered[cid]["expected_sha256"]
        assert receipt["primary_repository_path"]==registered[cid]["repository_path"]
        assert receipt["uploaded_rgba_pixel_sha256"]==receipt["stored_rgba_pixel_sha256"]
        assert "not current score" in receipt["temporal_limit"]
        assert receipt["supersedes_primary_identity"] is False
        assert receipt["renderer_binding_proven"] is False
        assert receipt["final_raster_qa_passed"] is False
        assert receipt["production_state"]=="HOLD"
        manifest=(ROOT/f"canon/characters/{cid}/REFERENCE_MANIFEST.yaml").read_text()
        assert receipt["stored_repository_path"] in manifest
        assert "identity_supersession: false" in manifest
        assert "renderer_gate: \"HOLD_UNTIL_PRIMARY_AND_SUBJECT_BINDING_PROVEN\"" in manifest

def test_explicitly_canonical_primary_does_not_get_silently_replaced():
    for entry in REG["entries"]:
        assert "supplementary/OWNER_SPOTLIGHT_2026.png" not in entry["repository_path"]
    obi=json.loads((ROOT/"canon/characters/CHAR-JAKE-KALOPER/OWNER_SPOTLIGHT_2026_RECEIPT.json").read_text())
    chili=json.loads((ROOT/"canon/characters/CHAR-BRANDON-PRYOR/OWNER_SPOTLIGHT_2026_RECEIPT.json").read_text())
    assert obi["user_upload_filename"].startswith("ChatGPT Image Sep 24")
    assert chili["user_upload_filename"].startswith("0D748D18-")
