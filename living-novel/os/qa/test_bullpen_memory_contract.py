import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
hyd=module("hyd","living-novel/os/adapters/hydrated_author_memory.py")
bridge=module("bridge","living-novel/os/adapters/bullpen_memory_contract.py")
class ContractTests(unittest.TestCase):
 def test_exports_mandatory_fields(self):
  p=hyd.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  a=bridge.export_memories(p,observed_at="2026-10-18T12:00:00Z")
  self.assertTrue(a)
  for e in a:
   for key in ("id","scope","source","owner","observed_at","confidence","freshness_days","supersedes","status","value"):
    self.assertIn(key,e)
   self.assertEqual(e["scope"],"schemin-26")
 def test_no_future_memory(self):
  p=hyd.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2022,scene_week=14)
  self.assertEqual(bridge.export_memories(p,observed_at="2026-10-18T12:00:00Z"),[])
 def test_no_personal_memory_claim(self):
  p=hyd.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  a=bridge.export_memories(p,observed_at="2026-10-18T12:00:00Z")
  self.assertTrue(all(x["value"]["classification"]=="WORLD_EVENT_NOT_PERSONAL_MEMORY" for x in a))
if __name__=="__main__":unittest.main()
