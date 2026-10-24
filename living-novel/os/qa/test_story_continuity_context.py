import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
s=importlib.util.spec_from_file_location("story",ROOT/"living-novel/os/adapters/story_continuity_context.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class StoryContinuityTests(unittest.TestCase):
 def test_future_relationship_is_withheld(self):
  x=m.asof(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  self.assertTrue(any(e["id"]=="CONSEQ-003" for e in x["withheld_edges"]))
  self.assertFalse(any(e["id"]=="CONSEQ-003" for e in x["register_assertions_not_independently_verified"]))
 def test_week4_fact_is_register_only(self):
  x=m.asof(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=4)
  self.assertTrue(any(e["id"]=="CONSEQ-003" for e in x["register_assertions_not_independently_verified"]))
  self.assertFalse(x["canon_promoted"])
 def test_promises_not_invented(self):
  x=m.asof(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=4)
  self.assertTrue(x["promise_register_empty"])
  self.assertEqual(x["story_promises"],[])
 def test_unresolved_year_ranges_stay_withheld(self):
  x=m.asof(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=19)
  self.assertTrue(any(e["reason"]=="ANCHOR_NOT_WEEK_SPECIFIC" for e in x["withheld_edges"]))
if __name__=="__main__":unittest.main()
