import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
CH=REPO/"living-novel"/"manuscript"/"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"
AUD=REPO/"living-novel"/"qa"/"CHAPTER_03_EDITORIAL_AUDIT_V1.md"
PROP=REPO/"living-novel"/"qa"/"CHAPTER_03_CANON_PROPOSAL_V1.md"
GATE=REPO/"living-novel"/"qa"/"CHAPTER_03_FINAL_PRE_CANON_GATE_V1.md"

class Chapter03MissionTests(unittest.TestCase):
    def test_no_retired_centaur_language(self):
        text=CH.read_text().lower()
        self.assertNotIn("centaur",text)
        self.assertNotIn("equine",text)
        self.assertIn("black fur",text)

    def test_no_week4_future_leak(self):
        text=CH.read_text().lower()
        self.assertNotIn("week 4",text)

    def test_no_hard_canon_self_promotion(self):
        self.assertIn("FOUNDER APPROVAL REQUIRED",PROP.read_text())
        self.assertIn("REVIEWED SOFT MANUSCRIPT",GATE.read_text())
        pre=GATE.read_text().split("## Upon Founder approval")[0]
        self.assertIn("**Current manuscript status:** REVIEWED SOFT MANUSCRIPT",pre)
        self.assertNotIn("**Current manuscript status:** HARD MANUSCRIPT CANON / CLOSED",pre)

    def test_editorial_audit_passes(self):
        text=AUD.read_text()
        self.assertIn("PASS — READY FOR CANON PROPOSAL",text)

    def test_chapter_keeps_summit_distinction(self):
        text=CH.read_text()
        self.assertIn("Then below the top.",text)
        self.assertIn("The summit remained bare.",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
