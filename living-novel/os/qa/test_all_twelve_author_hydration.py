import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("hyd",ROOT/"living-novel/os/adapters/hydrated_author_memory.py")
hyd=importlib.util.module_from_spec(spec);spec.loader.exec_module(hyd)
OWNERS=json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]
class AllTwelveAuthorPackets(unittest.TestCase):
 def test_twelve_2026_packets_have_distinct_current_ids(self):
  packets=[hyd.hydrate(character_id=o["character_id"],scene_year=2026,scene_week=3) for o in OWNERS]
  self.assertEqual(len(packets),12)
  self.assertEqual(len({p["character_id"] for p in packets}),12)
  self.assertTrue(all(p["historical_domain_state"]=="CURRENT_2026" for p in packets))
  self.assertTrue(all(p["memory_mutation"] is False for p in packets))
 def test_all_historical_packets_refuse_owner_identity_inference(self):
  for o in OWNERS:
   p=hyd.hydrate(character_id=o["character_id"],scene_year=2022,scene_week=17)
   self.assertTrue(p["historical_owner_identity_unknown"])
   self.assertEqual(p["character_matchups"],[])
   self.assertIsNone(p["period_division_id"])
 def test_no_w3_event_visible_before_w3_to_any_owner(self):
  for o in OWNERS:
   p=hyd.hydrate(character_id=o["character_id"],scene_year=2026,scene_week=2)
   self.assertTrue(all(e["week"]<=2 for e in p["world_memory_events_as_of_scene"]))
if __name__=="__main__":unittest.main()
