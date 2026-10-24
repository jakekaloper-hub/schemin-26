"""No image generation by merely resolving current visual presentation."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from canon.characters.runtime.reference_authority import resolve_approved_lineup_presentation

ROOT=Path(__file__).resolve().parents[3]

class VisualPresentationResolverTests(unittest.TestCase):
    def test_all_twelve_resolve_with_silhouettes_physical_and_spatial_but_never_gen_ready(self):
        m=json.loads((ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json").read_text())
        ids=[x["character_id"] for x in m["individuals"]]
        r=resolve_approved_lineup_presentation(ids)
        self.assertEqual(r["state"],"COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE")
        self.assertEqual(len(r["subjects"]),12)
        self.assertFalse(r["image_generation_eligible"])
        self.assertFalse(r["C1_visual_QA_passed"])
        self.assertEqual(r["T15"],"HOLD")
        self.assertEqual(r["T16"],"HOLD")
        for s in r["subjects"]:
            self.assertTrue(s["not_authorized_as_primary_photo"])
            self.assertTrue(s["presentation"]["negative_rules"])
            self.assertTrue(s["physical_constraints"]["anatomy_constraints"])
            self.assertTrue(s["spatial_anchor"]["home_location_id"].startswith("LOC-"))

    def test_incorrect_id_duplicate_and_missing_are_rejected(self):
        for ids in [[],["CHAR-FAKE"],["CHAR-AUSTIN-BYARS","CHAR-AUSTIN-BYARS"],["BOBBY"]]:
            r=resolve_approved_lineup_presentation(ids)
            self.assertEqual(r["reason"],"LINEUP_CHARACTER_SET_INVALID")

    def test_missing_or_swapped_original_bytes_fail_without_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            m=json.loads((ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json").read_text())
            path=root/"canon/characters/APPROVED_LINEUP_2026_10_18.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(m))
            ids=["CHAR-AUSTIN-BYARS"]
            r=resolve_approved_lineup_presentation(ids,root)
            self.assertEqual(r["reason"],"LINEUP_APPROVED_MASTER_SHA256_FAILED")
            image=root/m["stored_repository_path"]
            image.parent.mkdir(parents=True)
            image.write_bytes(b"fake poster bytes")
            r=resolve_approved_lineup_presentation(ids,root)
            self.assertEqual(r["reason"],"LINEUP_APPROVED_MASTER_SHA256_FAILED")

    def test_hmb_supporting_visual_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            m=json.loads((ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json").read_text())
            doc=root/"canon/characters/APPROVED_LINEUP_2026_10_18.json"
            doc.parent.mkdir(parents=True)
            doc.write_text(json.dumps(m))
            master=root/m["stored_repository_path"]
            master.parent.mkdir(parents=True)
            shutil.copyfile(ROOT/m["stored_repository_path"],master)
            r=resolve_approved_lineup_presentation(["CHAR-AUSTIN-BYARS"],root)
            self.assertEqual(r["reason"],"HMB_CORRECTION_EVIDENCE_MISSING")

if __name__=="__main__":
    unittest.main()
