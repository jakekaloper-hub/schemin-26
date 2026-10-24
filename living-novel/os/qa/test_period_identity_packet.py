import importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
def load(n,path):
 s=importlib.util.spec_from_file_location(n,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=load("h","living-novel/os/adapters/hydrated_author_memory.py")
i=load("i","living-novel/os/adapters/historical_owner_identity.py")
class PeriodIdentityTests(unittest.TestCase):
 def test_historical_owners_cannot_be_inferred(self):
  for y in range(2015,2026):
   rows=i.season_slot_evidence(y)
   self.assertTrue(all(r["owner"] is None and r["identity_status"]=="UNKNOWN_HISTORICAL_OWNER" for r in rows))
 def test_current_owners_exactly_twelve(self):
  rows=i.season_slot_evidence(2026)
  self.assertEqual(len(rows),12)
  self.assertEqual(len({r["character_id"] for r in rows}),12)
 def test_hydrated_packet_relationship_and_obligation_cutoff(self):
  w3=h.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3)
  w4=h.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=4)
  self.assertTrue(any(r["id"]=="CONSEQ-003" for r in w3["relationship_and_story_obligations"]["withheld_edges"]))
  self.assertTrue(any(r["id"]=="CONSEQ-003" for r in w4["relationship_and_story_obligations"]["register_assertions_not_independently_verified"]))
  self.assertTrue(w3["relationship_and_story_obligations"]["promise_register_empty"])
 def test_2017_team_ids_incomplete_not_invented(self):
  self.assertLess(len(i.season_slot_evidence(2017)),12)
if __name__=="__main__":unittest.main()
