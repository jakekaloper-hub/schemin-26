import unittest
from canon.characters.runtime.render_packet import build_character_render_packet

class RenderPacketFirewall(unittest.TestCase):
 def test_retired_authority_blocked(self):
  r=build_character_render_packet(character_id="CHAR-WILSON-LOOK",active_identity="Arsenal Centaur",canon_version="x",primary_asset=object(),immutable_visual_dna=[],authority_class="SUPERSEDED_QUARANTINED")
  self.assertEqual(r["state"],"GENERATION_BLOCKED")
 def test_history_cannot_add_jake_belt(self):
  r=build_character_render_packet(character_id="CHAR-JAKE-KALOPER",active_identity="The Trade Jedi",canon_version="x",primary_asset=object(),immutable_visual_dna=["blond strategist"],negative_locks=["championship belt"],historical_context={"negative_locks":[]})
  self.assertEqual(r["state"],"GENERATION_BLOCKED")
 def test_missing_asset_blocks_semantic_only_fallback(self):
  r=build_character_render_packet(character_id="CHAR-ZACH-WILSON",active_identity="King of the Impossible Lie",canon_version="x",primary_asset=None,immutable_visual_dna=["anthropomorphic white duck"])
  self.assertEqual(r["state"],"GENERATION_BLOCKED")
if __name__=="__main__": unittest.main()
