"""V4R1 acceptance preflight: evidence-aware, no self-certified canon."""
import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate, validate_character_provenance
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
M=json.loads((HERE/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V4R1.json").read_text())
R=json.loads((HERE/"TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text())
PROSE=(HERE/"PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V4R1.md").read_text().split("## V4R1 approval boundaries")[0]
CANON=(ROOT/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text()
class V4R1Preflight(unittest.TestCase):
 def test_pov_and_owner_links(self):
  self.assertEqual([],validate(R,M["scenes"]))
  self.assertEqual([],validate_character_provenance(R,M["scenes"],CANON))
 def test_exact_blob_binding(self):
  self.assertEqual("7a5c9f2a079e2ee4df2fc2f191b8397e22e6a7ad",M["manuscript_blob_sha"])
  self.assertEqual("5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",M["source_canon_blob_sha"])
 def test_scene_anchor_coverage(self):
  self.assertEqual(12,len(M["scenes"]))
  for s in M["scenes"]:
   self.assertIn(s["manuscript_anchor"],PROSE)
 def test_atlas_and_temporal_holds_explicit(self):
  for s in M["scenes"]:
   self.assertIsNone(s["atlas_hydration"]["loc_id"])
   self.assertTrue(s["atlas_hydration"]["qualification"])
   self.assertEqual("BLOCKED_PENDING_AUTHORITATIVE_LOC_OR_APPROVED_UNKNOWN",s["atlas_hydration"]["canon_promotion"])
   self.assertEqual("after_2026_draft_before_week_1_results",s["temporal_state_qualification"]["story_era"])
   self.assertEqual("PENDING_PER_SCENE_REVIEW",s["temporal_state_qualification"]["approval"])
 def test_repaired_viewpoint_and_preseason(self):
  self.assertNotIn("Edrin Vale",PROSE)
  self.assertNotIn("Each had noticed the other noticing",PROSE)
  self.assertIn("Neither man smiled. Brandon held his gaze",PROSE)
  self.assertIn("No face",PROSE) if "No face" in PROSE else self.assertIn("without a face",PROSE)
  self.assertIn("four iron-shod equine legs",PROSE)
  self.assertIn("beneath three serpent heads",PROSE)
if __name__=="__main__": unittest.main()
