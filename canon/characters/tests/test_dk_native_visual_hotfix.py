"""Fails closed when an exact historical DK Library handle conflicts with active morphology."""
import json
import unittest
from pathlib import Path

from canon.characters.runtime.reference_authority import validate_reference_candidate

ROOT=Path(__file__).resolve().parents[3]
CID="CHAR-WILSON-LOOK"


class DkNativeVisualHotfixTests(unittest.TestCase):
    def test_registered_original_sha_retained_but_visually_quarantined(self):
        registry=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
        src=next(x for x in registry["entries"] if x["character_id"]==CID)
        self.assertEqual(src["expected_sha256"],"d6279c5ca904c20de1e5800490d1fed42aa24c8674d051654b29838291459a10")
        verdict=validate_reference_candidate(CID,{
            "asset_id":"original-dk",
            "sha256":src["expected_sha256"],
            "filename":src["source_filename"],
            "source_kind":"COMMISSIONER_SOURCE",
        })
        self.assertEqual(verdict["reason"],"ACTIVE_VISUAL_CANON_CONFLICT")
        self.assertEqual(verdict["state"],"GENERATION_BLOCKED")

    def test_native_dk_handle_and_dependent_pages_blocked(self):
        n=json.loads((ROOT/"canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json").read_text())
        dk=next(x for x in n["characters"] if x["character_id"]==CID)
        self.assertEqual(dk["file_id"],"file_00000000df4081f5803f8ba6dfb68b42")
        self.assertEqual(dk["binding_state"],"VISUAL_CANON_CONFLICT_HOLD")
        self.assertFalse(dk["approved_active_render_seed"])
        self.assertIn("VISUAL_CONFLICT_HOLD",n["status"])
        pages=[p for p in n["pages"] if CID in p.get("character_ids",[])]
        self.assertGreaterEqual(len(pages),4)
        self.assertTrue(all(p["binding_state"]=="VISUAL_CANON_CONFLICT_HOLD" for p in pages))

    def test_rest_of_owner_reference_handles_not_revoked(self):
        n=json.loads((ROOT/"canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json").read_text())
        states=[x["binding_state"] for x in n["characters"] if x["character_id"]!=CID]
        self.assertEqual(len(states),11)
        self.assertTrue(all(x=="DIRECT_CANONICAL_HANDLE_READY" for x in states))


if __name__=="__main__":
    unittest.main()
