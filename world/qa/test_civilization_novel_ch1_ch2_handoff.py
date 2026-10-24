"""Fail-closed interchapter continuity checks on the noncanonical opening candidates."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/"living-novel/production/full-rewrite-2026"
C1REG=json.loads((PROD/"R7_CHAPTER_I_NINE_CARD_RECONSTRUCTION_REGISTER_V1.json").read_text())
C2REG=json.loads((PROD/"R9_CHAPTER_II_TEN_CARD_CAUSAL_CONTINUITY_REGISTER_V1.json").read_text())
C1=(ROOT/C1REG["manuscript_path"]).read_text()
C2=(ROOT/C2REG["manuscript_path"]).read_text()

class TestWholeOpeningReconstruction(unittest.TestCase):
    def test_three_protagonists_per_chapter_four_segments_each(self):
        for text,expected in (
            (C1,["CHAR-JAKE-KALOPER","CHAR-BRANDON-PRYOR","CHAR-AUSTIN-BYARS","CHAR-JAKE-KALOPER"]),
            (C2,["CHAR-BRANDON-PRYOR","CHAR-BOBBY-MITCHELL","CHAR-PHILLIP-PITTS","CHAR-BRANDON-PRYOR"]),
        ):
            self.assertEqual(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",text),expected)
        self.assertEqual(len(set(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",C1+C2))),5)

    def test_chili_opening_win_precedes_returned_defeat(self):
        self.assertIn("198.00",C1)
        self.assertIn("198.00",C2)
        self.assertIn("191.90",C2)
        self.assertIn("100.90",C2)
        self.assertNotIn("191.90",C1)
        self.assertIn("ENJOY THE L, BUD.",C2)
        self.assertNotIn("Sonic chili dog",C2)

    def test_jedi_title_and_swamp_continuity(self):
        self.assertIn("OBIWAN JACOBY — 141.70",C1)
        self.assertIn("HIS MAJESTY'S BLOOD — 131.26",C1)
        self.assertIn("MUD DOGS — 130.84",C2)
        self.assertIn("OBIWAN JACOBY — 122.91",C2)
        self.assertIn("He had not lost the Belt.",C1)
        self.assertNotIn("ObiWan received the Belt",C2)

    def test_week_two_state_does_not_anticipate_week_three(self):
        self.assertIn("D0nkey K0ng.",C2)
        self.assertIn("Mud Dogs.",C2)
        self.assertIn("the familiar dreadlocks were gone",C2)
        self.assertNotIn("172.48",C2) # Week 3 DK result
        self.assertNotIn("136.73",C2) # Week 3 ObiWan result
        self.assertEqual(len(C1REG["card_fate"])+len(C2REG["card_disposition"]),19)

    def test_development_only_no_forged_approvals(self):
        self.assertEqual(C1REG["status"],"FULL_LENGTH_DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertEqual(C2REG["status"],"FULL_LENGTH_DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertEqual(C1REG["policy"]["output_release"],"HOLD_NO_FOUNDER_OR_INDEPENDENT_UMPIRE_APPROVAL")
        self.assertEqual(C2REG["approval"]["canon_transaction"],"HOLD")
        self.assertEqual(C2REG["prologue_candidate"]["status"],"UNCHANGED_NONCANON_DEVELOPMENT_BASE")
        self.assertNotRegex(C1+C2,re.compile(r"\bEdrin(?: Vale)?\b|\bEdin\b",re.I))

if __name__=="__main__":
    unittest.main()
