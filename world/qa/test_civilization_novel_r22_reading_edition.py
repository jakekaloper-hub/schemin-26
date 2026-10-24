"""R22 candidate chapter II V2 and reading order regression, without canon promotion."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
MAN=BASE/"manuscript"
def read(f):return (MAN/f).read_text()
class EditorialSequence(unittest.TestCase):
 def test_chapter_two_v2_and_v1_preserved(self):
  a=read("CHAPTER_02_WHAT_COMES_BACK_FULL_RECONSTRUCTION_V1_NONCANON.md")
  b=read("CHAPTER_02_WHAT_COMES_BACK_LINE_EDIT_V2_NONCANON.md")
  self.assertNotEqual(a,b)
  self.assertGreater(len(b.split()),5200)
  self.assertIn("LINE-EDIT V2",b[:90])
  for s in ["191.90","100.90","130.84","122.91","165.78","95.87","194.92","122.97","131.06","113.52","135.38","125.88"]:
   self.assertIn(s,b)
  ids=lambda text:re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",text)
  self.assertEqual(ids(a),ids(b))
  self.assertEqual(len(set(ids(b))),3)
 def test_release_not_authorized_and_w3_not_leaked(self):
  ch=read("CHAPTER_02_WHAT_COMES_BACK_LINE_EDIT_V2_NONCANON.md")
  self.assertNotIn("Sonic chili dog",ch)
  self.assertNotIn("172.48",ch)
  self.assertNotIn("ObiWan received the Belt",ch)
  self.assertNotIn("Edrin Vale",ch)
 def test_reconstructed_sequence_inputs_exist(self):
  for f in ["CHAPTER_01_THE_FIRST_ANSWER_LINE_EDIT_V2_NONCANON.md",
            "CHAPTER_02_WHAT_COMES_BACK_LINE_EDIT_V2_NONCANON.md",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM_LINE_EDIT_V2_NONCANON.md",
            "CHAPTER_04_THE_ROAD_DOES_NOT_BOW_CONTINUITY_CANDIDATE_NONCANON.md",
            "THE_SURVEY_LINE_FULL_CAUSAL_MANUSCRIPT_V2_NONCANON.md"]:
   self.assertTrue((MAN/f).exists())
  self.assertTrue((BASE/"drafts/W5_WILSON_SECOND_FALL_OWNER_POV_NONCANON.md").exists())
 def test_source_hard_chapters_unchanged_rewrite_paths(self):
  for f in ["CHAPTER_01_THE_FIRST_ANSWER.md","CHAPTER_02_WHAT_COMES_BACK.md",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"]:
   self.assertTrue((ROOT/"living-novel/manuscript"/f).exists())
if __name__=="__main__":unittest.main()
