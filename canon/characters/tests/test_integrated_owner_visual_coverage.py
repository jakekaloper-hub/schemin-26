"""12-owner repository reference coverage must never imply production green."""
import copy
import json
import shutil
import tempfile
from pathlib import Path
from canon.characters.runtime.source_byte_integrity import (
    DEFAULT_REGISTRY, ROOT, verify_character_visual_coverage,
)

def test_all_twelve_have_some_durable_approved_reference_not_twelve_primaries():
    summary=verify_character_visual_coverage()
    assert summary["total"]==12
    assert summary["owner_references_verified"]==12
    assert summary["primary_sources_verified"]==2
    assert summary["supplementary_only"]==10
    assert summary["unavailable"]==0
    assert summary["final_render_eligible"]==0
    assert summary["state"]=="HOLD"
    assert len({r["character_id"] for r in summary["records"]})==12
    for r in summary["records"]:
        assert r["visual_reference_path"]
        assert r["release_eligible"] is False
        assert r["renderer_binding_verified"] is False
    for cid in ("CHAR-AUSTIN-BYARS","CHAR-PHILLIP-PITTS"):
        match=next(r for r in summary["records"] if r["character_id"]==cid)
        assert match["reference_status"]=="PRIMARY_BYTES_VERIFIED_RENDERER_UNPROVEN"

def test_tampered_spotlight_is_not_accepted_as_fallback():
    all_records=json.loads(DEFAULT_REGISTRY.read_text())
    one=next(x for x in all_records["entries"] if x["character_id"]=="CHAR-BEN-WHIPPLE")
    reg={"entries":[copy.deepcopy(one)]}
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        receipt_rel="canon/characters/CHAR-BEN-WHIPPLE/OWNER_SPOTLIGHT_2026_RECEIPT.json"
        orig=ROOT/receipt_rel
        receipt=json.loads(orig.read_text())
        rp=root/receipt_rel
        rp.parent.mkdir(parents=True)
        shutil.copyfile(orig,rp)
        source=root/receipt["stored_repository_path"]
        source.parent.mkdir(parents=True)
        source.write_bytes(b"wrong-owner-imposter-art")
        result=verify_character_visual_coverage(root,reg)
        assert result["owner_references_verified"]==0
        assert result["final_render_eligible"]==0
        assert result["records"][0]["reference_status"]=="NO_TRUSTED_DURABLE_REFERENCE"

def test_wrong_owner_or_forged_primary_authority_does_not_pass():
    all_records=json.loads(DEFAULT_REGISTRY.read_text())
    one=next(x for x in all_records["entries"] if x["character_id"]=="CHAR-BEN-WHIPPLE")
    reg={"entries":[copy.deepcopy(one)]}
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        receipt_rel="canon/characters/CHAR-BEN-WHIPPLE/OWNER_SPOTLIGHT_2026_RECEIPT.json"
        receipt=json.loads((ROOT/receipt_rel).read_text())
        source=root/receipt["stored_repository_path"]
        source.parent.mkdir(parents=True)
        shutil.copyfile(ROOT/receipt["stored_repository_path"],source)
        rp=root/receipt_rel
        rp.parent.mkdir(parents=True,exist_ok=True)
        for attack in ({"character_id":"CHAR-JAKE-KALOPER"},
                       {"primary_expected_sha256":"0"*64},
                       {"stored_repository_path":"../../other.png"}):
            bad={**receipt,**attack}
            rp.write_text(json.dumps(bad))
            result=verify_character_visual_coverage(root,reg)
            assert result["unavailable"]==1
            assert result["final_render_eligible"]==0
