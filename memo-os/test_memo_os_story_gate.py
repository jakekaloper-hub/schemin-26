import unittest
from memo_os_story_gate import validate_story_gate

GOOD = {"publication_candidate": True, "story_first": {
"verified_week_event":"Slob placed completed $71 $51 $31 bids in Week 7",
"source_receipt":"FLAIM transaction ID and 2026-10-22 editorial cutoff",
"causal_action":"A clerk reveals Slob's enormous waiver ledger",
"visible_consequence":"The LLC changes strategy opposite him",
"atlas_dependency":"League Chamber records desk is the event's institutional location",
"character_relationship":"Slob and LLC are confirmed Week 7 rivals",
"camera_decisive_instant":"Receipt is revealed as LLC reacts",
"non_reusable_league_detail":"Slob's Week 7 three-bid $153 sequence",
"independent_editorial_review":"Umpire review receipt attached",
"visual_grammar":"news_event",
"most_principals_acting":True,
"atlas_necessary":True,
"independent_editorial_verdict":"PASS",
"source_fact_classification":"VERIFIED_FACT"
}}

class StoryGateTests(unittest.TestCase):
 def test_complete_candidate_passes(self):
  self.assertEqual(validate_story_gate(GOOD), [])
 def test_generic_group_photo_rejected(self):
  p={**GOOD,"story_first":{**GOOD["story_first"],"visual_grammar":"static_ensemble_portrait"}}
  self.assertIn("rejected generic visual grammar",validate_story_gate(p))
 def test_pretty_but_inactive_characters_rejected(self):
  p={**GOOD,"story_first":{**GOOD["story_first"],"most_principals_acting":False}}
  self.assertIn("principals lack consequential action",validate_story_gate(p))
 def test_replaceable_location_rejected(self):
  p={**GOOD,"story_first":{**GOOD["story_first"],"atlas_necessary":False}}
  self.assertIn("atlas is a replaceable backdrop",validate_story_gate(p))
 def test_missing_editorial_review_rejected(self):
  p={**GOOD,"story_first":{**GOOD["story_first"],"independent_editorial_verdict":"HOLD"}}
  self.assertIn("independent editorial acceptance missing",validate_story_gate(p))
 def test_missing_fact_anchor_rejected(self):
  p={**GOOD,"story_first":{**GOOD["story_first"],"source_fact_classification":"FICTIONALIZATION"}}
  self.assertIn("no supported current-week fact anchor",validate_story_gate(p))
 def test_legacy_unaffected(self):
  self.assertEqual(validate_story_gate({}), [])

if __name__=="__main__":unittest.main()
