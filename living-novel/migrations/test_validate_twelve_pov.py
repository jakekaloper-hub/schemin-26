import json
import unittest
from pathlib import Path
from validate_twelve_pov import validate

REGISTRY = json.loads((Path(__file__).parent / "TWELVE_PRINCIPAL_REGISTRY_CANDIDATE_V1.json").read_text())

class TestPOV(unittest.TestCase):
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
