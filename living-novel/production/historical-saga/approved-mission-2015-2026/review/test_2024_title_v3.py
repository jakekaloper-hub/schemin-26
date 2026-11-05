"""Noncanonical 2024 title six-scene V3 preservation and source regressions.

Passing these tests is not an editorial/Umpire endorsement or historical owner binding.
"""
import json
import re
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent / "manuscript" / "2024-title"
REPO = REVIEW.parents[4]
V2 = ROOT / "THE_DOOR_AFTER_THE_CROWN_CAUSAL_READING_CANDIDATE_V2_NONCANON.md"
V3 = ROOT / "THE_DOOR_AFTER_THE_CROWN_CAUSAL_READING_CANDIDATE_V3_NONCANON.md"
NEW = ROOT / "THE_WEIGHT_OF_A_PROMISE_NONCANON.md"
REGISTRY = ROOT / "SCENE_REGISTER_V3.json"
HISTORY = REPO / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"

class TestTitleCausalV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v2 = V2.read_text(encoding="utf-8")
        cls.v3 = V3.read_text(encoding="utf-8")
        cls.new = NEW.read_text(encoding="utf-8")
        cls.register = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.events = json.loads(HISTORY.read_text(encoding="utf-8"))["matchups"]

    def test_predecessor_five_movement_story_unchanged(self):
        old = self.v2[self.v2.index("## I. The Speech for Tomorrow"):].strip()
        self.assertIn(old, self.v3)

    def test_sixth_scene_body_reproduced_verbatim(self):
        new = self.new[self.new.index("The people who had done the lifting"):].strip()
        self.assertIn(new, self.v3)

    def test_six_movement_order(self):
        headers = re.findall(r"^## ([IVX]+)\. ", self.v3, flags=re.M)
        self.assertEqual(headers, ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual(len(self.register["scenes"]), 6)

    def test_sustained_development_not_only_notes(self):
        self.assertGreaterEqual(len(self.new.split()), 2000)
        self.assertGreaterEqual(len(self.v3.split()), 6500)

    def test_sole_canonical_owner_pov(self):
        self.assertEqual(self.register["primary_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual({s["pov_character_id"] for s in self.register["scenes"]}, {"CHAR-JAKE-KALOPER"})
        self.assertNotRegex(self.v3, r"(?m)^## [IVX]+\. .*\b(?:Teren|Sorel|The King|Edrin|Oren)\b")

    def test_source_scored_final_verified_in_existing_history(self):
        match = next(e for e in self.events if e["id"] == "HIST-2024-CHAMPIONSHIP-1")
        self.assertEqual((match["season"],match["round"]), (2024, "championship"))
        self.assertEqual((match["winner"],match["winner_score"]), ("ObiWan Jacoby", 187.52))
        self.assertEqual((match["loser"],match["loser_score"]), ("The King", 161.68))
        self.assertIn("187.52", self.v3)
        self.assertIn("161.68", self.v3)

    def test_future_knowledge_not_inserted_in_story(self):
        story = self.v3[self.v3.index("## I. The Speech for Tomorrow"):]
        self.assertNotRegex(story, r"\b202[56]\b")

    def test_new_movement_enacts_not_falsely_settles_dispute(self):
        sixth = self.v3[self.v3.index("## VI. The Weight of a Promise"):]
        self.assertIn("A gift isn't their wage", sixth)
        self.assertIn("does not release anyone else from a debt", sixth)
        self.assertIn("the longer claim remained unresolved".lower(), sixth.lower())
        self.assertIn("Change it", sixth)

    def test_registry_preserves_source_and_venue_holds(self):
        self.assertEqual(self.register["historical_source_event"], "HIST-2024-CHAMPIONSHIP-1")
        self.assertEqual(self.register["historical_owner_binding"], "UNKNOWN")
        self.assertEqual(self.register["historical_venue"], "PROPOSED_UNAPPROVED")
        self.assertEqual(self.register["scenes"][-1]["historical_venue_status"], "PROPOSED_UNAPPROVED")
        self.assertEqual(self.register["scenes"][-1]["scene_id"], "2024-T-06")

    def test_release_fail_closed(self):
        self.assertEqual(self.register["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertFalse(self.register["canonical_merge"])
        self.assertFalse(self.register["independent_editorial_acceptance"])
        self.assertIn("NOT HARD CANON", self.v3)
        self.assertIn("wholly invented", self.register["scenes"][-1]["provenance"])

    def test_v2_retained_not_overwritten(self):
        self.assertNotEqual(V2, V3)
        self.assertIn("## V. The Names Not on the Receipt", self.v2)
        self.assertNotIn("## VI. The Weight of a Promise", self.v2)

if __name__ == "__main__":
    unittest.main()
