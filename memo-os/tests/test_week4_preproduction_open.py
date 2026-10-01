import json
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
            "WEEK_4_PERSONALIZED_INTELLIGENCE_AMENDMENT_DK_HMB_2026-10-01.md",
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

    def test_living_story_room_is_provisional_and_non_release(self):
        story = self.text("WEEK_4_LIVING_STORY_ROOM_AND_PERSONALIZED_INTELLIGENCE_V1.md")
        receipt = self.text("WEEK_4_STORY_ROOM_CURRENT_STATE_RECONCILIATION_2026-10-01.md")
        index = self.text("_INDEX.md")
        self.assertIn("PROVISIONAL STORY DEVELOPMENT ONLY", story)
        self.assertIn("FINAL STORY LOCK BLOCKED", story)
        self.assertIn("No reservoir is STORY_LOCKED", story)
        self.assertIn("WEEK_4_LIVING_STORY_ROOM_AND_PERSONALIZED_INTELLIGENCE_V1.md", index)
        self.assertIn("Week 4 publication record: BLOCKED", receipt)
        self.assertIn("all six matchups: 0.00–0.00 / UNDECIDED", receipt)
        self.assertIn("Publication Manifest V1: ACTIVE DERIVED INDEX ONLY", receipt)

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
        self.assertIn("W4-G6 personalized story intelligence: LIVE / PARTIAL PASS", story)
        self.assertIn("does **not** assign final Week 4 encounter venues", receipt)

        world_state = json.loads((ROOT / "world" / "data" / "current_world_state.json").read_text())
        world_events = json.loads((ROOT / "world" / "data" / "world_state_events.json").read_text())
        self.assertEqual(world_state["as_of"], "end_of_week_3_2026")
        for location_id in world_state["locations"]:
            self.assertIn(location_id, receipt)
        week3_events = [event for event in world_events["events"] if event["week"] == 3]
        self.assertGreaterEqual(len(week3_events), 1)
        for event in week3_events:
            self.assertEqual(event["classification"], "WORLD_CANON", event["id"])
            self.assertIn(event["id"], receipt)

    def test_w4_g6_dk_hmb_personalization_is_governed_and_conditional(self):
        control = self.text("WEEK_4_PRODUCTION_CONTROL_V1.md")
        amendment = self.text("WEEK_4_PERSONALIZED_INTELLIGENCE_AMENDMENT_DK_HMB_2026-10-01.md")
        facts = self.text("WEEK_4_FACT_SCOPE_AND_EVIDENCE_REGISTER_V1.md")
        index = self.text("_INDEX.md")

        self.assertIn("W4-G6 personalized story intelligence | **LIVE / PARTIAL PASS**", control)
        self.assertIn("PROVISIONAL DEVELOPMENT AUTHORIZED / FINAL STORY LOCK BLOCKED", control)
        self.assertIn("not a second Story Room or planning system", amendment)
        self.assertIn("Arsenal Gorilla Warrior", amendment)
        self.assertIn("Breece Hall — Doubtful", amendment)
        self.assertIn("Isiah Pacheco — IR", amendment)
        self.assertIn("not an independent medical diagnosis", amendment)
        self.assertIn("at the beach celebrating", amendment)
        self.assertIn("The LLC", amendment)
        self.assertIn("forbidden before a verified HMB loss", amendment)
        self.assertIn("temporary current-week story setting", amendment)
        self.assertIn("no reservoir is STORY_LOCKED", amendment)
        self.assertIn("provider roster-status observations only", facts)
        self.assertIn("WEEK_4_PERSONALIZED_INTELLIGENCE_AMENDMENT_DK_HMB_2026-10-01.md", index)

if __name__ == "__main__":
    unittest.main()
