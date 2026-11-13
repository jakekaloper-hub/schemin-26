import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PATH=ROOT/"planning/story-production-graph/adapt_week9_matchups.py"
spec=importlib.util.spec_from_file_location("week9_adapter",PATH)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class Week9AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=mod.compile_week9(release_accepted=False)

    def test_all_six_matchups_adapt(self):
        self.assertEqual(len(self.out["events"]),6)
        self.assertEqual(len(self.out["encounters"]),6)

    def test_all_twelve_character_slots_are_present(self):
        chars=[]
        for e in self.out["events"]:
            chars.extend(p["entity_id"] for p in e["participants"] if p["entity_type"]=="CHARACTER")
        self.assertEqual(len(chars),12)
        self.assertEqual(len(set(chars)),12)

    def test_sports_hold_does_not_silently_promote_canon(self):
        self.assertEqual(self.out["source"]["sports_data_release_status"],"HOLD")
        self.assertTrue(all(e["authority"]["evidence_status"]=="PROVISIONAL" for e in self.out["events"]))
        self.assertTrue(all(e["authority"]["canon_status"]=="BRANCHABLE" for e in self.out["events"]))
        self.assertTrue(all(e["state"]["world_writeback_allowed"] is False for e in self.out["events"]))

    def test_result_branch_is_preserved_without_promotion(self):
        branches={e["result"]["selected_branch"] for e in self.out["events"]}
        self.assertTrue(branches.issubset({"HOME_WIN","AWAY_WIN"}))
        self.assertEqual(len(branches),2)

    def test_encounter_inherits_card_anchors(self):
        cards,_=mod.load()
        by_id={c["id"]:c for c in cards["cards"]}
        for enc in self.out["encounters"]:
            mid=enc["encounter_id"].replace("ENC-","")
            self.assertEqual(enc["persistent_scene_anchors"],by_id[mid]["written_storyboard_sequence"]["persistent_scene_anchors"])

if __name__=="__main__":
    unittest.main()
