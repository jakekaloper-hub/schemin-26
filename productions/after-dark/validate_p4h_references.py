#!/usr/bin/env python3
"""P4H primary identity asset and next-stage interview readiness. Never auto-promote canon."""
import hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PRIMARY=ROOT/"canon/characters/assets/CHAR-DAVID-BABB/primary/A6F3AA99-CDB1-4265-AB08-3728117089A3.jpeg"
CROP=ROOT/"canon/characters/assets/lineups/2026-10-18-crops/CHAR-DAVID-BABB.png"
EXPECTED_PRIMARY="ce3137d1472d63deb7a026d114d200f338d2461d3d223647f34b473794e1f85b"
EXPECTED_CROP="f7fa692603289275c819dec2e5e1e09ea69bf33309c1bea1da0151a026b8f340"
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
FOLIO=(ROOT/"productions/after-dark/P4E_LLC_INTERVIEW_SIX_FOLIOS.md").read_text()
SCRIPT=(ROOT/"productions/after-dark/P4D_LLC_LIVE_INTERVIEW_FULL_SCRIPT.md").read_text()
REPORT=ROOT/"productions/after-dark/fixtures/p4h_reference_status.json"
def report():
 result={"gate":"P4H","primary":{"path":str(PRIMARY.relative_to(ROOT)),"expected_sha256":EXPECTED_PRIMARY,"actual_sha256":SHA(PRIMARY),"verified":SHA(PRIMARY)==EXPECTED_PRIMARY},"supplementary":{"path":str(CROP.relative_to(ROOT)),"expected_sha256":EXPECTED_CROP,"actual_sha256":SHA(CROP),"verified":SHA(CROP)==EXPECTED_CROP,"can_replace_primary":False},"host_visual_lock":"PENDING","manager_visual_lock":"PENDING","atlas_stage_approval":"PENDING","final_render_authorized":False}
 REPORT.write_text(json.dumps(result,indent=2)+"\n")
 return result
class P4H(unittest.TestCase):
 def test_supplementary_hash_matches(self):self.assertEqual(SHA(CROP),EXPECTED_CROP)
 def test_babb_identity_exists_in_registry(self):self.assertIn("CHAR-DAVID-BABB",(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text())
 def test_six_pages_guest_speaks(self):
  pages=re.split(r"(?=^## Page \d{2} — )",FOLIO,flags=re.M)[1:]
  self.assertEqual(len(pages),6)
  for p in pages[1:]:self.assertIn("BABB:",p)
 def test_all_selected_lines_match_script(self):
  lines=re.findall(r'^(?:HOST|BABB|MANAGER|PRODUCTION MANAGER): “(.+)”$',FOLIO,re.M)
  self.assertEqual(len(lines),29)
  self.assertFalse([x for x in lines if x not in SCRIPT])
 def test_cannot_authorize_without_primary(self):
  s=report()
  self.assertFalse(s["final_render_authorized"])
  self.assertFalse(s["supplementary"]["can_replace_primary"])
  self.assertEqual(s["primary"]["verified"],PRIMARY.exists() and SHA(PRIMARY)==EXPECTED_PRIMARY)
if __name__=="__main__":unittest.main(verbosity=2)
