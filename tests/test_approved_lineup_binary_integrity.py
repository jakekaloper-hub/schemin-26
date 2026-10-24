"""Real repository-byte regression for twelve approved lineup crops.

Does not promote the crops to primary source or certify renderer attachment.
"""
import base64
import json
import pathlib
import unittest

from canon.characters.runtime.verified_reference_transport import verify_repository_png

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "canon/characters/APPROVED_LINEUP_2026_10_18.json"

class ApprovedLineupBinaryIntegrity(unittest.TestCase):
    def test_all_twelve_actual_crop_bytes(self):
        manifest = json.loads(MANIFEST.read_text())
        individuals = manifest["individuals"]
        self.assertEqual(len(individuals), 12)
        self.assertEqual(len({person["character_id"] for person in individuals}), 12)
        for person in individuals:
            with self.subTest(character_id=person["character_id"]):
                path = person["crop"]
                data = (ROOT / path).read_bytes()
                rect = person["crop_rectangle_top_left"]
                result = verify_repository_png(
                    person["character_id"], path, base64.b64encode(data).decode(),
                    person["crop_sha256"], expected_dimensions=(rect["width"], rect["height"]))
                self.assertEqual(result["state"], "BINARY_RETRIEVAL_VERIFIED")
                self.assertFalse(result["renderer_attachment_proven"])
                self.assertFalse(result["generation_eligible"])

if __name__ == "__main__":
    unittest.main()
