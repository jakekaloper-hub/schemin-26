"""Prologue V3R1 editorial candidate is byte-bound and prevents old defects."""
import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate, validate_character_provenance

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MANIFEST=json.loads((HERE/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V3R1.json").read_text(encoding="utf-8"))
REGISTRY=json.loads((HERE/"TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text(encoding="utf-8"))
PROSE=(HERE/"PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V3R1.md").read_text(encoding="utf-8").split("## V3R1 approval boundaries")[0]
CANON=(ROOT/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")

class PrologueV3R1Regression(unittest.TestCase):
    def test_owner_and_principal_provenance(self):
        self.assertEqual(validate(REGISTRY, MANIFEST["scenes"]), [])
        self.assertEqual(validate_character_provenance(REGISTRY, MANIFEST["scenes"], CANON), [])
    def test_all_twelve_scene_anchors(self):
        self.assertEqual(len(MANIFEST["scenes"]), 12)
        for scene in MANIFEST["scenes"]:
            self.assertIn(scene["manuscript_anchor"], PROSE)
    def test_no_unlicensed_interior_or_humanoid_weather(self):
        self.assertNotIn("Edrin", PROSE)
        self.assertNotIn("A figure of cloud and lightning emerged", PROSE)
        self.assertIn("No face emerged from the weather", PROSE)
    def test_registration_and_championship_procedure(self):
        self.assertIn("visitor's authorization", PROSE)
        self.assertNotIn("Three days after the opening registration", PROSE)
        self.assertIn("the champion's public submission to challenge", PROSE)
    def test_exact_source_metadata(self):
        self.assertEqual(MANIFEST["manuscript_blob_sha"], "24fa186280c731faac4391af0a2e3baffc162909")
        self.assertEqual(MANIFEST["source_canon_blob_sha"], "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0")
    def test_narrative_scene_order(self):
        ids=[x["scene_id"] for x in MANIFEST["scenes"]]
        self.assertLess(ids.index("P10"),ids.index("P04"))
        self.assertLess(ids.index("P04"),ids.index("P11"))
if __name__=="__main__":
    unittest.main()
