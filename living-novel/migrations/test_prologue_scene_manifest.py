"""Prologue manuscript-to-scene provenance and candidate POV contract tests."""
import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate, validate_character_provenance

HERE = Path(__file__).resolve().parent
REGISTRY = json.loads((HERE / "TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((HERE / "PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V2.json").read_text(encoding="utf-8"))
MANUSCRIPT = (HERE / "PROLOGUE_TWELVE_POV_FOUNDER_REVIEW_CANDIDATE_V2.md").read_text(encoding="utf-8")
PROSE = MANUSCRIPT.split("\n---\n\n## V2 approval boundaries")[0]

class PrologueSceneContract(unittest.TestCase):
    def test_validate_scene_records(self):
        self.assertEqual(validate(REGISTRY, MANIFEST["scenes"]), [])

    def test_twelve_unique_anchors_in_story(self):
        anchors = [s["manuscript_anchor"] for s in MANIFEST["scenes"]]
        self.assertEqual(len(anchors), 12)
        self.assertEqual(len(anchors), len(set(anchors)))
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, PROSE)

    def test_no_unauthorized_pov(self):
        self.assertEqual({s["principal_pov_id"] for s in MANIFEST["scenes"]}, {"obiwan_jacoby"})
        self.assertNotIn("Edrin", PROSE)

    def test_character_validator_enforced(self):
        canon = (HERE.parents[1] / "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")
        self.assertEqual([], validate_character_provenance(REGISTRY, MANIFEST["scenes"], canon))
        mutated = [dict(x) for x in MANIFEST["scenes"]]
        mutated[0]["pov_owner_name"] = "Unknown"
        self.assertTrue(validate_character_provenance(REGISTRY, mutated, canon))
        mutated[0]["pov_owner_name"] = MANIFEST["scenes"][0]["pov_owner_name"]
        mutated[0].pop("character_canon_source")
        self.assertTrue(validate_character_provenance(REGISTRY, mutated, canon))

    def test_character_owner_provenance(self):
        canon = (HERE.parents[1] / "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")
        owners = {p["id"]: p["owner_name"] for p in REGISTRY["principals"]}
        for scene in MANIFEST["scenes"]:
            with self.subTest(scene=scene["scene_id"]):
                self.assertEqual(scene["pov_owner_name"], owners[scene["principal_pov_id"]])
                self.assertEqual(scene["character_canon_source"], "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md")
                self.assertIn("### " + scene["pov_owner_name"] + " /", canon)
                self.assertEqual(scene["character_state_status"], "REVIEW_REQUIRED")
                for ref in scene["character_refs"]:
                    self.assertEqual(ref["owner_name"], owners[ref["principal_id"]])
                    self.assertIn("### " + ref["owner_name"] + " /", canon)
                    self.assertEqual(ref["state_status"], "REVIEW_REQUIRED")

    def test_character_provenance_is_not_promotion(self):
        self.assertTrue(all(s["character_state_status"] != "APPROVED" for s in MANIFEST["scenes"]))

    def test_source_sha_bound(self):
        self.assertEqual(MANIFEST["manuscript_blob_sha"], "ecdf0e292be24f8b20cd72df88cf637e81258805")

    def test_required_pov_provenance(self):
        for scene in MANIFEST["scenes"]:
            with self.subTest(scene=scene["scene_id"]):
                for k in ("location", "knowledge_before", "knowledge_acquired", "knowledge_after", "objective", "decision", "consequence_out", "evidence_mode", "spoiler_boundary"):
                    self.assertTrue(scene.get(k))

if __name__ == "__main__":
    unittest.main()
