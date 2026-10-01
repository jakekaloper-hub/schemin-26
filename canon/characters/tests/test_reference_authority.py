import json
import pathlib
import unittest

from canon.characters.runtime.reference_authority import validate_reference_candidate, request_authority_state

ROOT=pathlib.Path(__file__).resolve().parents[3]
SRC=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
AUTH=json.loads((ROOT/"canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json").read_text())

def expected(cid):
    return next(x for x in SRC["entries"] if x["character_id"]==cid)

class ReferenceAuthorityTests(unittest.TestCase):
    def test_exact_current_source_hash_passes(self):
        cid="CHAR-AUSTIN-BYARS"
        e=expected(cid)
        result=validate_reference_candidate(cid,{
            "sha256":e["expected_sha256"],
            "asset_id":"source-handle",
            "source_kind":"COMMISSIONER_SOURCE",
            "filename":e["source_filename"],
        },SRC,AUTH)
        self.assertEqual(result["state"],"REFERENCE_AUTHORITY_RESOLVED")

    def test_stale_master_lineup_blocks_for_three_known_characters(self):
        for cid in ("CHAR-WILSON-LOOK","CHAR-PHILLIP-PITTS","CHAR-AUSTIN-BYARS"):
            result=validate_reference_candidate(cid,{
                "sha256":"a"*64,
                "asset_id":AUTH["master_lineup"]["creative_claw_asset_id"],
                "source_kind":"COMPOSITE",
                "filename":AUTH["master_lineup"]["name"],
            },SRC,AUTH)
            self.assertEqual(result["reason"],"MASTER_LINEUP_STALE_FOR_CHARACTER")

    def test_master_lineup_never_seeds_production_even_for_other_nine(self):
        cid="CHAR-JAKE-KALOPER"
        result=validate_reference_candidate(cid,{
            "sha256":"a"*64,
            "asset_id":AUTH["master_lineup"]["creative_claw_asset_id"],
            "source_kind":"COMPOSITE",
            "filename":AUTH["master_lineup"]["name"],
        },SRC,AUTH)
        self.assertEqual(result["reason"],"MASTER_LINEUP_NOT_PRODUCTION_AUTHORITY")

    def test_generated_hmb_convenience_asset_is_quarantined(self):
        cid="CHAR-AUSTIN-BYARS"
        e=expected(cid)
        result=validate_reference_candidate(cid,{
            "sha256":e["expected_sha256"],
            "asset_id":"e6649118-bb8b-4507-bd74-69a7d8e218ea",
            "source_kind":"GENERATED",
            "filename":"CANON_HMB_AUSTIN_BYARS_ACTIVE_REF.png",
        },SRC,AUTH)
        self.assertEqual(result["reason"],"QUARANTINED_OR_DERIVED_ASSET")

    def test_hash_mismatch_blocks_even_with_correct_filename(self):
        cid="CHAR-PHILLIP-PITTS"
        e=expected(cid)
        result=validate_reference_candidate(cid,{
            "sha256":"f"*64,
            "asset_id":"source-handle",
            "source_kind":"COMMISSIONER_SOURCE",
            "filename":e["source_filename"],
        },SRC,AUTH)
        self.assertEqual(result["reason"],"REFERENCE_SOURCE_HASH_MISMATCH")

    def test_multi_character_request_requires_all_current_sources(self):
        ids=["CHAR-AUSTIN-BYARS","CHAR-WILSON-LOOK"]
        candidates={}
        for cid in ids:
            e=expected(cid)
            candidates[cid]={
                "sha256":e["expected_sha256"],
                "asset_id":"source-"+cid,
                "source_kind":"COMMISSIONER_SOURCE",
                "filename":e["source_filename"],
            }
        result=request_authority_state(ids,candidates,SRC,AUTH)
        self.assertEqual(result["state"],"REFERENCE_AUTHORITY_RESOLVED")

if __name__=="__main__":
    unittest.main(verbosity=2)
