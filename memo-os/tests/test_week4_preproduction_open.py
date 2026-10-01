import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
W4 = ROOT / "memo-os" / "week-4"

class Week4PreproductionOpenTests(unittest.TestCase):
    def text(self, name):
        return (W4 / name).read_text()

    def test_control_package_exists(self):
        required = [
            "_INDEX.md",
            "WEEK_4_PRODUCTION_CONTROL_V1.md",
            "WEEK_4_FACT_SCOPE_AND_EVIDENCE_REGISTER_V1.md",
            "WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md",
            "WEEK_4_WORLD_ENTRY_RECEIPT_V1.md",
            "WEEK_4_WORLD_AND_STORY_INTELLIGENCE_REGISTER_V1.md",
            "WEEK_4_ISSUE_PREVIS_BOARD_V1.md",
            "WEEK_4_PAGE_PACKET_REGISTER_V1.md",
            "WEEK_4_RELEASE_GATE_V1.md",
        ]
        for name in required:
            self.assertTrue((W4 / name).exists(), name)

    def test_exact_six_week4_matchups(self):
        text = self.text("WEEK_4_PRODUCTION_CONTROL_V1.md")
        matchups = [
            "D0nkey K0ng vs ObiWan Jacoby",
            "Mud Dogs vs Three Dreaded Snake",
            "Red Leopards vs Dr. Duckhook",
            "Slob on my Dobb vs The Chili Cheesers",
            "The LLC vs His Majesty's Blood",
            "El Niño vs Seven Deadly Chins",
        ]
        for matchup in matchups:
            self.assertIn(matchup, text)
        self.assertEqual(sum(1 for line in text.splitlines() if line.startswith(tuple(f"{i}. " for i in range(1,7)))), 6)

    def test_v55_is_governing(self):
        index = self.text("_INDEX.md")
        self.assertIn("V5.5", index)
        self.assertIn("SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md", index)

    def test_no_premature_gotw(self):
        control = self.text("WEEK_4_PRODUCTION_CONTROL_V1.md")
        self.assertIn("NO WEEK 4 GAME OF THE WEEK IS DECLARED AT OPENING", control)
        self.assertIn("selection must wait", control)

    def test_current_high_risk_canon_is_locked(self):
        canon = self.text("WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md")
        self.assertIn("Arsenal Gorilla Warrior", canon)
        self.assertIn("centaur/equine form RETIRED", canon)
        self.assertIn("EXACTLY THREE serpent HEADS", canon)
        self.assertIn("NO championship belt", canon)

    def test_finished_art_and_release_are_blocked(self):
        index = self.text("_INDEX.md")
        release = self.text("WEEK_4_RELEASE_GATE_V1.md")
        previs = self.text("WEEK_4_ISSUE_PREVIS_BOARD_V1.md")
        self.assertIn("FINISHED ART BLOCKED", index)
        self.assertIn("NOT RELEASE READY", release)
        self.assertIn("Finished image generation remains prohibited", previs)

    def test_fact_scope_rejects_live_claim_from_cached_state(self):
        facts = self.text("WEEK_4_FACT_SCOPE_AND_EVIDENCE_REGISTER_V1.md")
        self.assertIn("no \"live\" wording from cached state", facts)
        self.assertIn("current roster membership", facts)

    def test_world_entry_gate_is_bound_to_persisted_week3_state(self):
        control = self.text("WEEK_4_PRODUCTION_CONTROL_V1.md")
        receipt = self.text("WEEK_4_WORLD_ENTRY_RECEIPT_V1.md")
        story = self.text("WEEK_4_WORLD_AND_STORY_INTELLIGENCE_REGISTER_V1.md")
        self.assertIn("W4-G5 continuity/world entry | **PASS**", control)
        self.assertIn("end_of_week_3_2026", receipt)
        self.assertIn("W4-G5 continuity/world entry: PASS", story)
        self.assertIn("W4-G6 personalized story intelligence: OPEN", story)
        self.assertIn("does **not** assign final Week 4 encounter venues", receipt)

if __name__ == "__main__":
    unittest.main()
