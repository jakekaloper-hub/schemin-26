"""12-owner authoritative manifest integrity and fail-closed production assertions."""
import json
import pathlib
import re
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"canon/characters/reference_sources_v1.json"
MANIFEST_DIR=ROOT/"canon/characters"
RENDERERS=ROOT/"canon/characters/renderer_capabilities_v1.json"


def scalar(content, field):
    match=re.search(r"(?m)^  "+re.escape(field)+r':\s*"?([^"\n]+)"?\s*$', content)
    return match.group(1).strip() if match else None


class TwelveOwnerManifestIntegrity(unittest.TestCase):
    def test_each_registered_character_has_matching_manifest_and_source_authority(self):
        data=json.loads(REGISTRY.read_text())
        self.assertEqual(len(data["entries"]),12)
        for source in data["entries"]:
            with self.subTest(character=source["character_id"]):
                path=MANIFEST_DIR/source["character_id"]/"REFERENCE_MANIFEST.yaml"
                self.assertTrue(path.is_file(),f"Missing manifest: {path}")
                contents=path.read_text()
                self.assertIn(f'character_id: "{source["character_id"]}"',contents)
                self.assertIn(f'expected_sha256: "{source["expected_sha256"]}"',contents)
                self.assertIn(f'expected_repository_path: "{source["repository_path"]}"',contents)
                self.assertIn('approval_state: "APPROVED"',contents)

    def test_no_manifest_false_claims_portable_reference_without_blob_receipt(self):
        data=json.loads(REGISTRY.read_text())
        for source in data["entries"]:
            with self.subTest(character=source["character_id"]):
                contents=(MANIFEST_DIR/source["character_id"]/"REFERENCE_MANIFEST.yaml").read_text()
                if "git_blob_sha: null" in contents:
                    self.assertIn('renderer_mount: "NOT_PROVEN"',contents)
                    self.assertNotIn('render_eligibility: "PRODUCTION_PASS"',contents)

    def test_provider_never_claims_proof_without_receipts(self):
        cfg=json.loads(RENDERERS.read_text())
        for name,route in cfg["routes"].items():
            with self.subTest(route=name):
                if not route.get("capability_receipt_id"):
                    self.assertNotEqual(route.get("production_state"),"ACTIVE")
                    self.assertNotEqual(route.get("evidence_state"),"PROVEN")


if __name__=="__main__":
    unittest.main()
