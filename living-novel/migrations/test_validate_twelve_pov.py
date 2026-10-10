import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate

REGISTRY = json.loads((Path(__file__).parent / "TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text())

class TestPOV(unittest.TestCase):
    def test_owner_bindings_match_master_canon(self):
        canon = (Path(__file__).resolve().parents[2] / "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md").read_text(encoding="utf-8")
        owners = [p.get("owner_name") for p in REGISTRY["principals"]]
        self.assertEqual(len(set(owners)), 12)
        for owner in owners:
            with self.subTest(owner=owner):
                self.assertIn("### " + owner + " /", canon)

    def test_accept(self):
        self.assertEqual([], validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"obiwan_jacoby"}]))

    def test_reject_outsider(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"edrin"}]))

    def test_reject_missing(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3"}]))

    def test_elemental_receipt(self):
        self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":"el_nino"}]))

    def test_arbitrary_elemental_receipt_is_rejected(self):
        scene = {"scene_id":"e1","story_time":"w3","principal_pov_id":"el_nino","elemental_pov_canon_receipt":"ANY_STRING"}
        self.assertTrue(validate(REGISTRY, [scene]))

    def test_elemental_receipt_requires_registry_approval(self):
        scene = {"scene_id":"e1","story_time":"w3","principal_pov_id":"el_nino","elemental_pov_canon_receipt":"R1"}
        candidate = {**REGISTRY, "elemental_pov_approval":{"status":"PENDING", "receipt_id":"R1"}}
        self.assertTrue(validate(candidate, [scene]))

    def test_malformed_pov_type(self):
        for value in ([], {}, 7):
            self.assertTrue(validate(REGISTRY, [{"scene_id":"a","story_time":"w3","principal_pov_id":value}]))

    def test_invalid_registry_type(self):
        self.assertTrue(validate([], []))

    def test_twelve_count(self):
        self.assertTrue(validate({**REGISTRY, "principals":REGISTRY["principals"][:11]}, []))

if __name__ == "__main__":
    unittest.main()
