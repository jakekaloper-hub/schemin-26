import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
CH=REPO/"living-novel"/"manuscript"/"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"
AUD=REPO/"living-novel"/"qa"/"CHAPTER_03_EDITORIAL_AUDIT_V1.md"
PROP=REPO/"living-novel"/"qa"/"CHAPTER_03_CANON_PROPOSAL_V1.md"
PRE=REPO/"living-novel"/"qa"/"CHAPTER_03_FINAL_PRE_CANON_GATE_V1.md"
FINAL=REPO/"living-novel"/"qa"/"CHAPTER_03_FINAL_CANON_GATE_V1.md"

class Chapter03MissionTests(unittest.TestCase):
    def test_no_retired_centaur_language(self):
        text=CH.read_text().lower()
        self.assertNotIn("centaur",text)
        self.assertNotIn("equine",text)
        self.assertIn("black fur",text)

    def test_no_week4_future_leak(self):
        text=CH.read_text().lower()
        self.assertNotIn("week 4",text)

    def test_founder_approval_promotes_exact_chapter(self):
        self.assertIn("APPROVED / FOUNDER AUTHORIZED",PROP.read_text())
        self.assertIn("SUPERSEDED BY",PRE.read_text())
        text=FINAL.read_text()
        self.assertIn("HARD MANUSCRIPT CANON / CLOSED",text)
        self.assertIn("49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",text)

    def test_editorial_audit_passes(self):
        self.assertIn("PASS — READY FOR CANON PROPOSAL",AUD.read_text())

    def test_chapter_keeps_summit_distinction(self):
        text=CH.read_text()
        self.assertIn("Then below the top.",text)
        self.assertIn("The summit remained bare.",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
