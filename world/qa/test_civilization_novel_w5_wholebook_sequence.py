"""Whole-book developmental Week 3-5 chronology, without publishing new canon."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
INTER=(BASE/"drafts/W5_WILSON_SECOND_FALL_OWNER_POV_NONCANON.md").read_text()
SURVEY=(BASE/"manuscript/THE_SURVEY_LINE_FULL_CAUSAL_MANUSCRIPT_V1_NONCANON.md").read_text()
CH4=(BASE/"manuscript/CHAPTER_04_THE_ROAD_DOES_NOT_BOW_CONTINUITY_CANDIDATE_NONCANON.md").read_text()
D=json.loads((BASE/"R15_SURVEY_LINE_SOURCE_AND_RELEASE_REGISTER_V1.json").read_text())
class WholeBookWeekFiveGate(unittest.TestCase):
 def test_wilson_week4_first_then_week5_second_no_wrong_cutoff(self):
  self.assertIn("157.33",CH4)
  self.assertIn("139.67",CH4)
  self.assertNotIn("184.91",CH4)
  self.assertIn("184.91",INTER)
  self.assertIn("141.44",INTER)
  self.assertNotIn("157.33",INTER)
 def test_interlude_exactly_wilson_current_body(self):
  self.assertIn("CHAR-WILSON-LOOK",INTER)
  self.assertIn("four iron-shod equine hooves",INTER)
  self.assertIn("gorilla",INTER)
  self.assertNotIn("Wilson's boots",INTER)
  self.assertIn("NONCANON",INTER[:400])
 def test_survey_two_owner_povs_and_no_transfer(self):
  self.assertIn("193.73",SURVEY)
  self.assertIn("127.09",SURVEY)
  self.assertEqual(D["promotion"],"HOLD")
  self.assertEqual({x["owner"] for x in D["scenes"]},{"CHAR-BOBBY-MITCHELL","CHAR-DAVID-BABB"})
  self.assertIn("No land transferred",SURVEY)
 def test_no_additional_sports_result_or_succession(self):
  self.assertNotIn("ObiWan received the Belt",INTER+SURVEY)
  self.assertNotIn("Duckhook was crowned king",INTER+SURVEY)
  self.assertNotIn("newly signed deed granted",INTER+SURVEY)
 def test_book_structure_not_equal_week_number(self):
  board=(BASE/"R16_WHOLE_BOOK_W5_SEQUENCE_AND_EDITORIAL_DECISION_V1.md").read_text()
  self.assertIn("not yet numbered",board.lower())
  self.assertIn("Survey Line",board)
  self.assertIn("Chapter IV",board)
if __name__=="__main__":
 unittest.main()
