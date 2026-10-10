"""Prologue manuscript-to-scene provenance and candidate POV contract tests."""
import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate

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

    def test_source_sha_bound(self):
        self.assertEqual(MANIFEST["manuscript_blob_sha"], "ecdf0e292be24f8b20cd72df88cf637e81258805")

    def test_required_pov_provenance(self):
        for scene in MANIFEST["scenes"]:
            with self.subTest(scene=scene["scene_id"]):
                for k in ("location", "knowledge_before", "knowledge_acquired", "knowledge_after", "objective", "decision", "consequence_out", "evidence_mode", "spoiler_boundary"):
                    self.assertTrue(scene.get(k))

if __name__ == "__main__":
    unittest.main()
