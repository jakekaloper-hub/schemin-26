"""A matching old JPEG hash or native Library handle is insufficient when its visual body form is stale."""
import hashlib
import json
import unittest
from pathlib import Path

from canon.characters.runtime.reference_authority import validate_reference_candidate
from canon.characters.runtime.source_byte_integrity import preflight_character_set

ROOT=Path(__file__).resolve().parents[3]
CID="CHAR-WILSON-LOOK"


class DkVisualCanonConflictTests(unittest.TestCase):
    def test_current_bipedal_original_cannot_seed_production_even_with_exact_hash(self):
        src=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
        dk=next(x for x in src["entries"] if x["character_id"]==CID)
        receipt=validate_reference_candidate(CID,{
            "sha256":dk["expected_sha256"],
            "asset_id":"CANONICAL_DK_OLD_EXACT_SOURCE",
            "source_kind":"COMMISSIONER_SOURCE",
            "filename":dk["source_filename"],
        })
        self.assertEqual(receipt["state"],"GENERATION_BLOCKED")
        self.assertEqual(receipt["reason"],"ACTIVE_VISUAL_CANON_CONFLICT")
        self.assertEqual(dk["expected_sha256"],
                         "d6279c5ca904c20de1e5800490d1fed42aa24c8674d051654b29838291459a10")

    def test_native_library_handle_and_old_week4_pages_held_not_promoted(self):
        native=json.loads((ROOT/"canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json").read_text())
        dk=next(x for x in native["characters"] if x["character_id"]==CID)
        self.assertEqual(native["status"],"PARTIAL_NATIVE_REFERENCE_BINDING_DK_VISUAL_CONFLICT_HOLD")
        self.assertEqual(dk["binding_state"],"VISUAL_CANON_CONFLICT_HOLD")
        self.assertFalse(dk["approved_active_render_seed"])
        self.assertEqual(dk["file_id"],"file_00000000df4081f5803f8ba6dfb68b42")
        pages=[p for p in native["pages"] if CID in p.get("character_ids",[])]
        self.assertGreater(len(pages),0)
        self.assertTrue(all(p["binding_state"]=="VISUAL_CANON_CONFLICT_HOLD" for p in pages))
        self.assertTrue(all(
            x.get("binding_state")=="DIRECT_CANONICAL_HANDLE_READY"
            for x in native["characters"] if x["character_id"]!=CID
        ))

    def test_candidate_exact_bytes_present_but_no_automatic_primary_supersession(self):
        src=json.loads((ROOT/"canon/characters/reference_sources_v1.json").read_text())
        dk=next(x for x in src["entries"] if x["character_id"]==CID)
        authority=json.loads((ROOT/"canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json").read_text())
        conflict=next(x for x in authority["source_visual_conflicts"] if x["character_id"]==CID)
        candidate=ROOT/conflict["candidate_asset"]
        self.assertEqual(hashlib.sha256(candidate.read_bytes()).hexdigest(),
                         conflict["candidate_sha256"])
        self.assertNotEqual(conflict["candidate_sha256"],dk["expected_sha256"])
        self.assertEqual(conflict["candidate_role"],
                         "NONACTIVE_VISUAL_CANDIDATE__NOT_APPROVED_PRIMARY")
        self.assertEqual(conflict["state"],"ACTIVE_CANON_VISUAL_CONFLICT_HOLD")
        self.assertIn("INDEPENDENT_UMPIRE_NOT_SIGNED",conflict["review_authority"])

    def test_source_preflight_prioritizes_visual_conflict_and_stays_blocked(self):
        report=preflight_character_set([CID])
        self.assertFalse(report["generation_eligible"])
        self.assertEqual(report["reason"],"ACTIVE_VISUAL_CANON_CONFLICT")
        self.assertEqual(report["visual_conflict_character_ids"],[CID])


if __name__=="__main__":
    unittest.main()
