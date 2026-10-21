import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from world.atlas.spatial.candidate_packet import build_candidate_spatial_packet

class CandidatePacketTests(unittest.TestCase):
    def test_all_consumers_same_object(self):
        p=build_candidate_spatial_packet()
        self.assertTrue(p["ok"],p)
        self.assertEqual({p[x]["context_id"] for x in ("memo","novel","atlas","art_environment")},{p["shared_candidate_spatial_context"]["context_id"]})
        self.assertTrue(all(p[x]["spatial"] is p["shared_candidate_spatial_context"] for x in ("memo","novel","atlas","art_environment")))
        self.assertFalse(p["shared_candidate_spatial_context"]["canonical_world_mutation"])
        self.assertFalse(p["art_environment"]["approved_cinematic_reference"])

    def test_dated_season_no_location_shift(self):
        autumn=build_candidate_spatial_packet("2026-10-21")
        winter=build_candidate_spatial_packet("2026-12-21")
        self.assertTrue(autumn["ok"] and winter["ok"])
        a,b=autumn["shared_candidate_spatial_context"],winter["shared_candidate_spatial_context"]
        self.assertEqual(a["candidate_location_geometry"],b["candidate_location_geometry"])
        self.assertNotEqual(a["scenario"]["season"],b["scenario"]["season"])

    def test_unmodeled_date_fails_closed(self):
        p=build_candidate_spatial_packet("2027-03-01")
        self.assertFalse(p["ok"])
        self.assertEqual(p["code"],"UNMODELED_SCENARIO_DATE")

if __name__=="__main__":
    unittest.main()
