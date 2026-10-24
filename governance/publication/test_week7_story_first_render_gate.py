"""Negative integration tests: Week 7 publication cannot bypass story review."""
import unittest
from week4_render_eligibility import render_eligibility

class Week7StoryFirstRenderGateTests(unittest.TestCase):
    def test_missing_scene_is_blocked(self):
        out = render_eligibility({"production_week": 7})
        self.assertEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")
    def test_malformed_scene_is_blocked(self):
        out = render_eligibility({"production_week": 7, "scene_direction": None})
        self.assertEqual(out["reason"], "STORY_FIRST_SCENE_INVALID")
    def test_false_flag_does_not_bypass(self):
        out = render_eligibility({"production_week": 7, "scene_direction": {"publication_candidate": False}})
        self.assertEqual(out["reason"], "SCENE_DIRECTION_NOT_READY")
        self.assertIn("publication candidate missing story_first evidence", out["review"]["errors"])
    def test_explicit_candidate_without_scene_is_blocked(self):
        out = render_eligibility({"publication_candidate": True})
        self.assertEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")

if __name__ == "__main__":
    unittest.main()
