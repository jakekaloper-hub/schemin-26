"""Recovered primaries must match approved original bytes without claiming render admission."""
from pathlib import Path
import hashlib, json
from canon.characters.runtime.source_byte_integrity import verify_source_bytes
ROOT=Path(__file__).resolve().parents[3]
def test_byars_and_pitts_exact_primaries():
    reg=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
    for cid in ("CHAR-AUSTIN-BYARS","CHAR-PHILLIP-PITTS"):
        e=next(x for x in reg["entries"] if x["character_id"]==cid)
        content=(ROOT/e["repository_path"]).read_bytes()
        assert len(content)==e["observed_library_size_bytes"]
        assert hashlib.sha256(content).hexdigest()==e["expected_sha256"]
        yaml=(ROOT/f"canon/characters/{cid}/REFERENCE_MANIFEST.yaml").read_text()
        assert e["expected_sha256"] in yaml
        assert 'renderer_mount: "NOT_PROVEN"' in yaml
    report=verify_source_bytes()
    assert report["pass_count"]>=2
    assert report["source_bytes_required_count"] + report["pass_count"]==12
    assert report["blocked_count"]==0
def test_byars_supplementary_byte_identity():
    paths={"IMG_2175.jpeg":"ef5039481c5614de9d3397b738a6ac1243228a5647fbd27b7e5654d417bba93e","moonlit_hood.png":"f3b82d914f489531a7f4ff68a35f6baf570be4abfe1514c0d49b6f0645544c97"}
    for fn,expected in paths.items():
        content=(ROOT/f"canon/characters/assets/CHAR-AUSTIN-BYARS/supplementary/{fn}").read_bytes()
        assert hashlib.sha256(content).hexdigest()==expected
