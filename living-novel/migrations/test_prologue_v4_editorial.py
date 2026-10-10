"""Prologue V4 narrative-source integrity and character gate regression."""
import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate, validate_character_provenance

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
M=json.loads((HERE/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V4.json").read_text(encoding="utf-8"))
R=json.loads((HERE/"TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text(encoding="utf-8"))
TEXT=(HERE/"PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V4.md").read_text(encoding="utf-8").split("## V4 approval boundaries")[0]
CANON=(ROOT/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")

class PrologueV4Review(unittest.TestCase):
    def test_licensed_characters(self):
        self.assertEqual(validate(R,M["scenes"]),[])
        self.assertEqual(validate_character_provenance(R,M["scenes"],CANON),[])
    def test_scene_anchors_present(self):
        self.assertEqual(len(M["scenes"]),12)
        self.assertEqual(len({x["scene_id"] for x in M["scenes"]}),12)
        for scene in M["scenes"]:
            self.assertIn(scene["manuscript_anchor"],TEXT)
    def test_specific_causality_and_ontology(self):
        for anchor in ["The Leopards brought their own cord","The stablemaster was eating too",
                       "Nobody answered. El Niño had crossed the quay without a face",
                       "the rule rather than to the traveler","Jake offered the man a place on his own hired cart"]:
            self.assertIn(anchor,TEXT)
        self.assertNotIn("Edrin Vale",TEXT)
        self.assertNotIn("A figure of cloud and lightning emerged",TEXT)
        self.assertIn("four iron-shod equine legs",TEXT)
        self.assertIn("beneath three serpent heads",TEXT)
    def test_blob_binding(self):
        self.assertEqual(M["manuscript_blob_sha"],"111a6e52e433da0fb3aab4b2a8635ac393b6a57f")
        self.assertEqual(M["source_canon_blob_sha"],"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0")
    def test_ordered_registration(self):
        ids=[x["scene_id"] for x in M["scenes"]]
        self.assertLess(ids.index("P05"),ids.index("P04"))
        self.assertLess(ids.index("P10"),ids.index("P04"))
        self.assertLess(ids.index("P04"),ids.index("P11"))

if __name__=="__main__":
    unittest.main()
