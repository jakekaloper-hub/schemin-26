"""GitHub must retain the actual DK historical reference; it cannot replace the primary."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RECEIPT=ROOT/"canon/characters/CHAR-WILSON-LOOK/W3_COVER_VISUAL_REFERENCE_RECEIPT.json"

def test_dk_week3_cover_bytes_persist_as_supplementary():
    receipt=json.loads(RECEIPT.read_text())
    p=ROOT/receipt["repository_path"]
    assert p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt["stored_file_sha256"]
    assert len(p.read_bytes())==receipt["stored_file_size_bytes"]
    assert receipt["character_id"]=="CHAR-WILSON-LOOK"
    assert receipt["classification"]=="SUPPLEMENTARY_APPEARANCE_AND_HISTORICAL_COVER_ONLY"
    assert receipt["primary_reference"]["repository_byte_ingest"]=="NOT_PROVEN"
    assert receipt["provider_mount_verified"] is False
    assert receipt["subject_binding_verified"] is False

def test_dk_manifest_respects_active_centaur_canon():
    source=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
    entry=next(x for x in source["entries"] if x["character_id"]=="CHAR-WILSON-LOOK")
    manifest=(ROOT/"canon/characters/CHAR-WILSON-LOOK/REFERENCE_MANIFEST.yaml").read_text()
    spec=(ROOT/"canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md").read_text()
    assert entry["identity"]=="Arsenal Gorilla Centaur Warrior"
    assert 'identity: "Arsenal Gorilla Centaur Warrior"' in manifest
    assert 'supersession_state: "CURRENT_COMMISSIONER_CLARIFIED_2026_10_02"' in manifest
    assert "FOUR-LEGGED centaur/equine lower body" in spec
    assert 'primary_identity_supersession: false' in manifest
