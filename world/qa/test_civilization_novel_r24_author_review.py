"""Ensure simulation evidence is never misclassified as independent review."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
REPORT=(BASE/"R24_SIMULATED_AUTHOR_ROOM_AND_READER_CHALLENGE.md").read_text()
SCENE=(BASE/"drafts/R24_SURVEY_LINE_IRON_COLLAR_REVERSAL_SCENE_NONCANON.md").read_text()
class SimulatedReviewFirewall(unittest.TestCase):
 def test_label_and_hold(self):
  self.assertIn("NOT genuine independent human readers",REPORT)
  self.assertIn("Release state: HOLD",REPORT)
  self.assertIn("not a quantitative quality score",REPORT.lower())
 def test_all_seven_passages_criticized(self):
  for i in range(1,8):self.assertIn(f"P{i:02d}",REPORT)
 def test_developmental_scene_no_claims(self):
  self.assertIn("CHAR-BOBBY-MITCHELL",SCENE)
  self.assertIn("CHAR-DAVID-BABB",SCENE)
  self.assertIn("193.73",SCENE)
  self.assertIn("127.09",SCENE)
  self.assertIn("no actual act of sabotage",SCENE.lower())
  self.assertIn("NONCANON",SCENE)
if __name__=="__main__": unittest.main()
