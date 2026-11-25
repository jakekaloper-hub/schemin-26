#!/usr/bin/env python3
"""Opening page editorial/geometry preflight. No image generation."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"productions/after-dark"
P=json.loads((D/"P5B_PAGE_00_OPENING_PRODUCTION_KIT.json").read_text())
F=(D/"P4E_LLC_INTERVIEW_SIX_FOLIOS.md").read_text()
class Opening(unittest.TestCase):
 def test_seven_ordered_pages(self):self.assertEqual(P["sequence"],["00","01","02","03","04","05","06"])
 def test_geometry(self):self.assertEqual(P["dimensions"],{"width":1080,"height":1920})
 def test_copy_fields(self):
  for key in ("eyebrow","masthead","tagline","joke","announcer","reveal","bill","guest","identifier"):
   self.assertTrue(P["copy"][key].strip(),key)
 def test_llc_guest_tease(self):
  self.assertIn("DAVID BABB",P["copy"]["guest"]);self.assertIn("THE LLC",P["copy"]["guest"])
  self.assertEqual(len(re.findall(r"^## Page \d\d — ",F,re.M)),6)
 def test_noncanon_world_limits(self):
  self.assertFalse(P["gate"]["render_allowed"])
  self.assertFalse(P["gate"]["publish_allowed"])
  self.assertEqual(P["world"]["site"],"UNAPPROVED")
  self.assertFalse(P["layout"]["babb_visible"])
 def test_layout_proportions(self):self.assertEqual(sum(P["layout"][k] for k in ("title_pct","stage_pct","bill_pct")),100)
if __name__=="__main__":unittest.main(verbosity=2)
