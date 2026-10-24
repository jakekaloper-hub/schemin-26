import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
s=importlib.util.spec_from_file_location("candidate",ROOT/"living-novel/os/adapters/build_reading_candidate.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CandidateChecks(unittest.TestCase):
 def test_legacy_institutional_narrators_are_excluded(self):
  text,manifest=m.build()
  self.assertEqual(len(manifest["legacy_files_excluded"]),3)
  self.assertTrue(all(x["legacy_institutional_pov_risk"] for x in manifest["legacy_files_excluded"]))
  self.assertTrue(all(not x["legacy_institutional_pov_risk"] for x in manifest["source_files"]))
  self.assertNotIn("Edrin",text)
 def test_no_claim_of_final_acceptance(self):
  _,p=m.build()
  self.assertEqual(p["release_status"],"HOLD_NOT_FINAL_NOVEL")
  for key in ("independent_umpire_approved","founder_approved","published","art_byte_verified"):
   self.assertFalse(p[key])
 def test_digest_is_reproducible(self):
  import hashlib
  _,p=m.build()
  for r in p["source_files"]:
   self.assertEqual(hashlib.sha256((ROOT/r["path"]).read_bytes()).hexdigest(),r["sha256"])
if __name__=="__main__":unittest.main()
