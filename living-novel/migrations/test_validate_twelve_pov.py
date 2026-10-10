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

    def test_twelve_count(self):
        self.assertTrue(validate({**REGISTRY, "principals":REGISTRY["principals"][:11]}, []))

if __name__ == "__main__":
    unittest.main()
