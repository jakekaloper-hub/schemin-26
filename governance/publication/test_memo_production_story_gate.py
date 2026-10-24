"""Week-neutral render entrypoint regression tests for future Memo issues."""
import unittest
from week4_render_eligibility import render_eligibility

class MemoProductionStoryGateTests(unittest.TestCase):
    def test_future_week_missing_scene_rejected(self):
        for week in (5, 7, 8, 12, 14, 202):
            with self.subTest(week=week):
                out = render_eligibility({"production_week": week})
                self.assertEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")
    def test_future_week_false_candidate_flag_cannot_bypass(self):
        out = render_eligibility({"production_week": 9, "publication_candidate": False})
        self.assertEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")
    def test_explicit_publication_requires_scene_without_week(self):
        out = render_eligibility({"publication_candidate": True})
        self.assertEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")
    def test_week_four_legacy_flow_not_newly_blocked_by_story_gate(self):
        out = render_eligibility({"production_week": 4})
        self.assertNotEqual(out["reason"], "STORY_FIRST_SCENE_MISSING")

if __name__ == "__main__":
    unittest.main()
