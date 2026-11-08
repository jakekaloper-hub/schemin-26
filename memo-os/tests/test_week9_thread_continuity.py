"""Week 9 handoff regressions. These do not certify images, facts or publication."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
WEEK = ROOT / "memo-os/week-9"

class Week9ContinuityTests(unittest.TestCase):
    def load(self):
        path = WEEK / "THREAD_CONTINUITY.json"
        self.assertTrue(path.is_file(), "Missing durable thread continuity record")
        return json.loads(path.read_text())

    def test_read_order_reaches_thread_context(self):
        self.assertIn("memo-os/_INDEX.md", (ROOT / "README.md").read_text())
        self.assertIn("week-9/_INDEX.md", (ROOT / "memo-os/_INDEX.md").read_text())
        self.assertIn("THREAD_CONTINUITY.md", (WEEK / "_INDEX.md").read_text())
        self.assertIn("Resume existing issue before", (ROOT / "memo-os/SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md").read_text())

    def test_source_capture_is_present_and_hash_bound(self):
        d = self.load()
        p = ROOT / d["source_capture"]["path"]
        self.assertTrue(p.is_file())
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), d["source_capture"]["sha256"])
        text = p.read_text()
        for token in ["1=A&B", "charity golf event at CCOJ", "dirt bike endurence race", "lifted truck", "chili cookout", "gladitor scene", "custom paintball professional course"]:
            self.assertIn(token, text)

    def test_all_six_premises_and_two_result_forks_survive(self):
        d = self.load()
        old = json.loads((WEEK / "WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json").read_text())
        self.assertEqual(len(d["matchups"]), 6)
        self.assertEqual({m["id"] for m in d["matchups"]}, {m["id"] for m in old["cards"]})
        for m in d["matchups"]:
            self.assertEqual(set(m["endings"]), {"home_win", "away_win"})
            self.assertEqual(m["origin"], "FOUNDER_DIRECTION_WITH_LABELED_TEAM_CHOICES")
            self.assertIsNone(m["actual_winner"])

    def test_settled_identity_and_truth_status_are_not_reopened(self):
        d = self.load()
        self.assertEqual(set(d["character_policy"]["focused_exception_ids"]), {"CHAR-AUSTIN-BYARS", "CHAR-WILSON-LOOK"})
        self.assertFalse(d["character_policy"]["repeat_questionnaire"])
        self.assertFalse(d["status"]["published"])
        self.assertFalse(d["status"]["final_results_verified_by_this_change"])
        self.assertEqual(d["status"]["rough_gotw"], "DRAWN_IN_PR287_NOT_FINAL_ART")
        self.assertFalse(d["status"]["polished_proofs_complete"])
        self.assertEqual(d["resume"]["entrypoint"], "memo-os/week-9/_INDEX.md")

    def test_rehearsal_reuses_actual_board_and_alternatives_stay_conditional(self):
        p = WEEK / "storyboards/W09_GOTW_PAGE_TURN_REHEARSAL_V1.html"
        self.assertTrue(p.is_file(), "Page-turn rehearsal has not been built")
        text = p.read_text()
        self.assertIn('const actualResult = null;', text)
        self.assertIn('let branch = null;', text)
        self.assertIn('body.classList.toggle("hide-captions")', text)
        for page in ["P04", "P05", "P06", "P07A", "P07B"]:
            self.assertIn('data-page="' + page + '"', text)
        for i in range(1, 10):
            self.assertIn('data-source-frame="frame-' + str(i) + '"', text)
        self.assertIn('IF OBIWAN WINS', text)
        self.assertIn('IF DUCKHOOK WINS', text)
        self.assertNotIn("localStorage", text)

    def test_new_check_is_wired_to_existing_memo_ci(self):
        text = (ROOT / ".github/workflows/weekly-memo-authority-ci.yml").read_text()
        self.assertIn("test_week9_thread_continuity.py", text)
        self.assertTrue((WEEK / "THREAD_CONTINUITY.md").is_file())

if __name__ == "__main__":
    unittest.main()
