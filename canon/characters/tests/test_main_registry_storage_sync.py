"""Current canon registry must match actual approved bytes in GitHub, not old paperwork."""
import hashlib
import json
from pathlib import Path
from canon.characters.runtime.source_byte_integrity import ROOT

def test_live_registry_source_byte_state_matches_present_files():
    data=json.loads((ROOT/'canon/characters/reference_sources_v1.json').read_text())
    assert len(data["entries"])==12
    present=0
    for e in data["entries"]:
        target=ROOT/e["repository_path"]
        manifest=(ROOT/f'canon/characters/{e["character_id"]}/REFERENCE_MANIFEST.yaml').read_text()
        assert 'renderer_mount: "NOT_PROVEN"' in manifest
        if target.is_file():
            blob=target.read_bytes()
            assert hashlib.sha256(blob).hexdigest()==e["expected_sha256"]
            assert len(blob)==e["observed_library_size_bytes"]
            assert e["current_byte_verification"].startswith("VERIFIED_CANONICAL_MAIN_SHA256_")
            assert 'current_state: "SOURCE_BYTES_VERIFIED_CANONICAL_MAIN"' in manifest
            assert 'fresh_context_fetch: "VERIFIED_CLEAN_MAIN_CHECKOUT_' in manifest
            present+=1
        else:
            assert e["current_byte_verification"]=="PENDING_DURABLE_RAW_BYTE_ACCESS"
    assert present==sum(e["current_byte_verification"].startswith("VERIFIED_CANONICAL_MAIN_SHA256_") for e in data["entries"])
