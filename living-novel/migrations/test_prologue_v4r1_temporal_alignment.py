"""Prevent temporal manifest drift from reintroducing discarded story-time claims."""
import json
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
M=json.loads((HERE/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V4R1.json").read_text(encoding="utf-8"))
PROSE=(HERE/"PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V4R1.md").read_text(encoding="utf-8")
class TemporalCorrection(unittest.TestCase):
 def test_champion_visit_time_and_anchor(self):
  p=next(s for s in M["scenes"] if s["scene_id"]=="P04")
  self.assertEqual(p["story_time"],"after-registration-hearings-before-opening-assembly")
  self.assertIn(p["manuscript_anchor"],PROSE)
  self.assertIn("After the last of the registration hearings, and before the opening assembly",PROSE)
  self.assertNotIn("three-days-after-registration",p["story_time"])
 def test_candidate_not_promoted(self):
  self.assertIn("NOT_CANON",M["status"])
  for scene in M["scenes"]:
   self.assertIsNone(scene["atlas_hydration"]["loc_id"])
   self.assertEqual(scene["temporal_state_qualification"]["approval"],"PENDING_PER_SCENE_REVIEW")
if __name__=="__main__": unittest.main()
