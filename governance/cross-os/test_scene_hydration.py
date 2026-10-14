import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
src=ROOT/"governance/cross-os/hydrate_scene.py"
spec=importlib.util.spec_from_file_location("scene_hydrator_test",src)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class HydrationTests(unittest.TestCase):
    def test_missing_provenance_fails(self):
        r=mod.hydrate_scene({"scene_id":"x"})
        self.assertEqual(r["status"],"BLOCKED")
        self.assertEqual(r["reason"],"MISSING_SCENE_SOURCE_EVIDENCE")

    def test_unapproved_write_fails(self):
        data={"scene_id":"S","verified_event_ref":"evidence","source_timestamp":"2026-10-14T12:00:00-04:00",
        "character_id":"CHAR-TEST","character_source_ref":"ref","location_id":"LOC-TEST","world_state_ref":"state",
        "world_mutation":True}
        self.assertEqual(mod.hydrate_scene(data)["reason"],"UNAUTHORIZED_CROSS_OS_WRITE")

    def test_unknown_location_fails_via_active_resolver(self):
        data={"scene_id":"S","verified_event_ref":"evidence","source_timestamp":"2026-10-14T12:00:00-04:00",
        "character_id":"CHAR-TEST","character_source_ref":"ref","location_id":"LOC-UNKNOWN-NOT-CANON",
        "world_state_ref":"state"}
        result=mod.hydrate_scene(data)
        self.assertEqual(result["status"],"BLOCKED")
        self.assertEqual(result["reason"],"AUTHORITATIVE_LOCATION_HYDRATION_NOT_READY")
        self.assertIn("memo_os",result["packets"])

    def test_candidate_location_fails(self):
        data={"scene_id":"S","verified_event_ref":"evidence","source_timestamp":"2026-10-14T12:00:00-04:00",
        "character_id":"CHAR-TEST","character_source_ref":"ref","location_id":"CAND-INVALID",
        "world_state_ref":"state"}
        result=mod.hydrate_scene(data)
        self.assertEqual(result["status"],"BLOCKED")

if __name__=="__main__":
    unittest.main()
