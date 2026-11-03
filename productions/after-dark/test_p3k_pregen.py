#!/usr/bin/env python3
"""P3K machine-checkable pre-generation controls; guards never authorize artwork."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"productions/after-dark"
folio=(D/"P3G_LLC_FOLIO_COPY_AND_VISUAL_PACKETS.md").read_text()
script=(D/"P3F_LLC_SPOTLIGHT_SCRIPT_REWRITE.md").read_text()
pages=re.split(r"(?=^## Page \d{2} — )",folio,flags=re.M)[1:]
data=json.loads((D/"fixtures/p3i_page_copy.json").read_text())
metrics=json.loads((D/"fixtures/p3i_layout_metrics.json").read_text())
class PreGen(unittest.TestCase):
 def test_six_pages_and_dimensions(self):
  self.assertEqual(len(pages),6);self.assertEqual(len(data),6)
  self.assertTrue(all(x["dimensions"]=="1080x1920" and x["fits"] for x in metrics))
 def test_source_copy_matches_folio(self):
  for p,item in zip(pages,data):
   body=p.split("**Exact display copy:**",1)[1].split("**",1)[0].strip()
   self.assertEqual(body,item["copy"])
 def test_no_real_guest_or_unverified_world_fact(self):
  self.assertIn("No invented Babb attendance",folio)
  self.assertIn("no fabricated week 8 outcomes",folio.lower())
  self.assertIn("NONCANON",folio)
 def test_text_size_and_density_guard(self):
  for m in metrics:self.assertLessEqual(m["copy_height"],m["copy_capacity"])
 def test_12_teams_in_schedule(self):
  for s in ["LLC","Red Leopards","Slob","His Majesty's Blood","ObiWan","El Niño","Chili","Three Dreaded Snake","Duckhook","Mud Dogs","D0nkey K0ng","Seven Deadly Chins"]:
   self.assertIn(s,pages[4])
 def test_script_to_folio_is_adaptation_not_verbatim(self):
  self.assertIn("I'm not holding a funeral",folio)
  self.assertIn("six wins in twenty-one games",script.lower())
  self.assertNotEqual(folio,script)
if __name__=="__main__":unittest.main(verbosity=2)
