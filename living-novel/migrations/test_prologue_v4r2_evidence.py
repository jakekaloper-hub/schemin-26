import json,unittest
from pathlib import Path
H=Path(__file__).parent
M=json.loads((H/"PROLOGUE_TWELVE_POV_SCENE_MANIFEST_V4R2.json").read_text())
T=(H/"PROLOGUE_TWELVE_POV_EDITORIAL_CANDIDATE_V4R2.md").read_text()
class Checks(unittest.TestCase):
 def test_revision(self):
  self.assertEqual("2744c2f3b8984e12e85ba95464f3876607f2c3dc",M["manuscript_blob_sha"])
  self.assertEqual(12,len(M["scenes"]))
  for s in M["scenes"]: self.assertIn(s["manuscript_anchor"],T)
 def test_repair(self):
  self.assertIn("Austin Byars remained champion and Belt Keeper.",T)
  self.assertIn("The dockworkers called the weather El Niño.",T)
  self.assertEqual("after-registration-hearings-before-opening-assembly",next(s for s in M["scenes"] if s["scene_id"]=="P04")["story_time"])
if __name__=="__main__":unittest.main()
