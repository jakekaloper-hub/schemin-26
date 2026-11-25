#!/usr/bin/env python3
import re,unittest
from pathlib import Path
D=Path(__file__).resolve().parent
S=(D/"P4D_LLC_LIVE_INTERVIEW_FULL_SCRIPT.md").read_text()
F=(D/"P4E_LLC_INTERVIEW_SIX_FOLIOS.md").read_text()
P=re.split(r"(?=^## Page \d\d — )",F,flags=re.M)[1:]
class InterviewCopyLock(unittest.TestCase):
 def test_page_count(self):self.assertEqual(len(P),6)
 def test_guest_presence(self):
  for page in P[1:]:self.assertIn("BABB:",page)
 def test_no_unmatched_dialogue(self):
  quotes=re.findall(r'^(?:HOST|BABB|MANAGER|PRODUCTION MANAGER): “(.+)”$',F,re.M)
  self.assertEqual(len(quotes),29)
  self.assertEqual([q for q in quotes if q not in S],[])
 def test_canon_holds(self):
  for token in ("NONCANON","Atlas","canonical David Babb","undecided"):self.assertIn(token,F)
 def test_image_format(self):self.assertIn("1080 × 1920",F)
if __name__=="__main__":unittest.main(verbosity=2)
