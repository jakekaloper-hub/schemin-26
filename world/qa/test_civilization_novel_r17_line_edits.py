"""Smoke test R17 line-edited development variants without replacing hard canon."""
import re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026/manuscript"
class TestNovelR17LineEdits(unittest.TestCase):
 def test_chapter_one_v2_retains_score_and_three_povs(self):
  a=(BASE/"CHAPTER_01_THE_FIRST_ANSWER_FULL_RECONSTRUCTION_V1_NONCANON.md").read_text()
  b=(BASE/"CHAPTER_01_THE_FIRST_ANSWER_LINE_EDIT_V2_NONCANON.md").read_text()
  self.assertNotEqual(a,b)
  self.assertIn("141.70",b)
  self.assertIn("131.26",b)
  self.assertEqual(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",a),re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",b))
  self.assertIn("LINE-EDIT V2",b[:120])
 def test_chapter_three_v2_retains_source_facts_and_three_povs(self):
  a=(BASE/"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM_FULL_RECONSTRUCTION_V1_NONCANON.md").read_text()
  b=(BASE/"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM_LINE_EDIT_V2_NONCANON.md").read_text()
  self.assertNotEqual(a,b)
  for n in ["172.48","126.86","136.73","114.50","147.43","114.62"]:self.assertIn(n,b)
  self.assertEqual(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",a),re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",b))
  self.assertIn("four-legged equine body",b)
 def test_hard_sources_still_present(self):
  for name in ["CHAPTER_01_THE_FIRST_ANSWER.md","CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"]:
   self.assertTrue((ROOT/"living-novel/manuscript"/name).exists())
 def test_chapter_four_governance_handoff_not_false_prose(self):
  brief=(ROOT/"living-novel/production/full-rewrite-2026/R20_CHAPTER_IV_SURGICAL_LINE_EDIT_PACKET_V1.md").read_text()
  self.assertIn("NOT",brief.upper())
  self.assertIn("157.33",brief)
if __name__=="__main__":unittest.main()
