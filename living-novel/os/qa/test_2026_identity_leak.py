import importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("h",ROOT/"living-novel/os/adapters/hydrated_author_memory.py")
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
class CurrentOwnerHistoryIsolation(unittest.TestCase):
 def test_all_twelve_2026_characters_do_not_inherit_prior_team_slot(self):
  for d in json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]:
   packet=h.hydrate(character_id=d["character_id"],scene_year=2026,scene_week=3)
   self.assertEqual(packet["character_matchups"],[],d["character_id"])
   self.assertGreater(len(packet["other_public_matchups"]),0)
if __name__=="__main__":unittest.main()
