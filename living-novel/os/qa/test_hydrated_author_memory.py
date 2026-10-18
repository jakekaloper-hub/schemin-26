import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("hydrated",ROOT/"living-novel/os/adapters/hydrated_author_memory.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class HydratedTests(unittest.TestCase):
 def test_2022_has_no_future_2026_world_events(self):
  x=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2022,scene_week=17)
  self.assertEqual(x["world_memory_events_as_of_scene"],[])
  self.assertEqual(x["period_division_status"],"UNKNOWN_HISTORICAL_DIVISIONS")
  self.assertTrue(x["historical_owner_identity_unknown"])
 def test_2026_cutoff(self):
  w2=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=2)
  w3=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  self.assertTrue(all(e["week"]<=2 for e in w2["world_memory_events_as_of_scene"]))
  self.assertGreater(len(w3["world_memory_events_as_of_scene"]),len(w2["world_memory_events_as_of_scene"]))
 def test_not_personal_or_persistent_memory(self):
  x=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  self.assertFalse(x["persistent_bullpen_memory_connected"])
  self.assertTrue(all(e["status"]=="WORLD_SOURCE_RECORD_NOT_CHARACTER_PERSONAL_KNOWLEDGE" for e in x["world_memory_events_as_of_scene"]))
 def test_period_specific_division(self):
  a=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  self.assertEqual(a["period_division_id"],"DIV-BURGERS")
  b=m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2022,scene_week=3)
  self.assertIsNone(b["period_division_id"])
 def test_invalid_year_rejected(self):
  with self.assertRaises(ValueError):m.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2014,scene_week=2)
if __name__=="__main__":unittest.main()
