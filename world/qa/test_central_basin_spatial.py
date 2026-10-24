import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from world.atlas.spatial.candidate_validation import load_candidate, validate_candidate


class CandidateSpatialTests(unittest.TestCase):
    def setUp(self):
        self.data = load_candidate()

    def test_valid_synthetic_baseline(self):
        self.assertEqual(validate_candidate(self.data), [])

    def test_wrong_region_rejected(self):
        self.data["region_id"] = "REG-EASTERN-STORM-COAST"
        self.assertIn("REGION_DRIFT", validate_candidate(self.data))

    def test_uphill_flow_rejected(self):
        self.data["synthetic_drainage"][1]["z"] = 110
        self.assertIn("UPHILL_FLOW", validate_candidate(self.data))

    def test_route_drift_rejected(self):
        self.data["paths"][0]["locations"].reverse()
        self.assertIn("ROUTE_TOPOLOGY_DRIFT", validate_candidate(self.data))

    def test_landmark_identity_rejected(self):
        self.data["anchors"][0]["location_id"] = "LOC-INVENTED"
        self.assertIn("ANCHOR_DRIFT", validate_candidate(self.data))

    def test_distance_claim_rejected(self):
        self.data["coordinate_reference"]["real_distance_claim"] = True
        self.assertIn("INVALID_COORDINATE_POLICY", validate_candidate(self.data))

    def test_weather_authority_rejected(self):
        self.data["scenarios"][0]["model_tag"] = "OBSERVED"
        self.assertIn("IMPROPER_WEATHER_AUTHORITY", validate_candidate(self.data))


if __name__ == "__main__":
    unittest.main()
