#!/usr/bin/env python3
"""P3H editorial-only folio preflight; deliberately does not authorize release."""
import re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"productions/after-dark/P3G_LLC_FOLIO_COPY_AND_VISUAL_PACKETS.md"
S=P.read_text()
sections=re.split(r"(?=^## Page \d{2} — )",S,flags=re.M)[1:]
class P3H(unittest.TestCase):
 def test_six_ordered_pages(self):
  self.assertEqual(len(sections),6)
  self.assertEqual([int(re.search(r"Page (\d{2})",x).group(1)) for x in sections],list(range(1,7)))
 def test_each_page_has_exact_copy_and_image_brief(self):
  for x in sections:
   self.assertIn("**Exact display copy:**",x)
   self.assertTrue("**Visual brief:**" in x or "**Image brief:**" in x)
 def test_geometry_and_authority(self):
  self.assertIn("1080 × 1920",S)
  self.assertIn("NONCANON",S)
  self.assertIn("NOT RENDER APPROVED",S)
 def test_no_character_teleport_authority(self):
  self.assertIn("No invented Babb attendance",S)
  self.assertIn("no fabricated week 8 outcomes",S.lower())
 def test_source_and_mobile_issues_explicit(self):
  self.assertIn("preliminary",S.lower())
  self.assertIn("fully readable in mobile portrait",S)
 def test_12_franchise_pairing_coverage(self):
  page=sections[4]
  for name in ("LLC","Red Leopards","Slob","His Majesty's Blood","ObiWan","El Niño","Chili","Three Dreaded Snake","Duckhook","Mud Dogs","D0nkey K0ng","Seven Deadly Chins"):
   self.assertIn(name,page)
if __name__=="__main__":unittest.main(verbosity=2)
