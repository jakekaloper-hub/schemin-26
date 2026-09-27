import unittest
from living_novel_os import *

class NovelOSTests(unittest.TestCase):
    def test_authority_beats_recency(self):
        r=resolve_assertions([
          {"authority":"PROPOSED_CANON","approved":True,"value":"new"},
          {"authority":"CHARACTER_CANON","approved":True,"value":"locked"}])
        self.assertEqual(r["assertion"]["value"],"locked")
    def test_equal_authority_conflict(self):
        r=resolve_assertions([
          {"authority":"CHARACTER_CANON","approved":True,"value":"a"},
          {"authority":"CHARACTER_CANON","approved":True,"value":"b"}])
        self.assertEqual(r["status"],"CONFLICTED")
    def test_trade_jedi_belt_drift(self):
        self.assertFalse(can_accept(validate_character_text("ObiWan Jacoby wore his championship belt.")))
    def test_donkey_kong_species_drift(self):
        self.assertFalse(can_accept(validate_character_text("Donkey Kong, a giant gorilla, entered.")))
    def test_oracle_guard(self):
        self.assertFalse(can_accept(validate_oracle_mutation({"temporal_layer":"ORACLE","authority":"WORLD_CANON"})))
    def test_promise_abandon_requires_reason(self):
        self.assertFalse(can_accept(validate_promise({"status":"ABANDONED_WITH_JUSTIFICATION"})))
    def test_router_visual_prologue(self):
        roles=route("produce next Prologue composition")
        self.assertIn("Visual Director",roles); self.assertIn("Canon Guardian",roles)

if __name__=="__main__": unittest.main()
