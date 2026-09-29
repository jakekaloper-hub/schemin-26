import unittest
from records import RECORDS,ASSETS
from registry import compile_index,resolve
from models import CharacterRecord,Layer,QACheck
from compose import compose
from assets import resolve_asset
from qa import decide
from compiler import compile_contract
from receipts import publication_receipt
from validate import validate_record,validate_asset

class CCPV2Tests(unittest.TestCase):
 def test_records_validate(self):
  self.assertTrue(all(validate_record(r)==[] for r in RECORDS))
  self.assertTrue(all(validate_asset(a)==[] for a in ASSETS.values()))
 def test_12_unique(self):
  by_id,index,retired=compile_index(RECORDS); self.assertEqual(len(by_id),12)
 def test_aliases(self):
  self.assertEqual(resolve("Baker Moore Purdy",RECORDS)["record"].character_id,"CHAR-WILSON-LOOK")
  self.assertEqual(resolve("The Immortal",RECORDS)["record"].character_id,"CHAR-AUSTIN-BYARS")
  self.assertEqual(resolve("That's Fantasy",RECORDS)["record"].character_id,"CHAR-AUSTIN-BYARS")
 def test_retired_wilson_forward_resolves(self):
  x=resolve("Arsenal Centaur",RECORDS); self.assertEqual(x["record"].identity,"Arsenal Gorilla Warrior"); self.assertEqual(x["input_state"],"SUPERSEDED_ALIAS")
 def test_pitts_anatomy(self):
  p=resolve("Three Dreaded Snake",RECORDS)["record"]; self.assertIn("exactly THREE",p.species_body); self.assertIn("ONE BODY",p.hard_locks)
 def test_jake_belt(self):
  j=resolve("ObiWan Jacoby",RECORDS)["record"]; self.assertIn("NO CHAMPIONSHIP BELT",j.hard_locks)
 def test_alias_collision_fails(self):
  a=RECORDS[0]; b=CharacterRecord("2.0","CHAR-X","X","X","X",aliases=("ObiWan Jacoby",))
  with self.assertRaises(ValueError): compile_index([a,b])
 def test_missing_assets_fail_closed(self):
  self.assertEqual(resolve_asset("REF-JAKE-001",ASSETS)["status"],"HUMAN_REVIEW_REQUIRED")
 def test_weekly_cannot_change_anatomy(self):
  with self.assertRaises(ValueError): compose(RECORDS[0],[Layer("WEEKLY_STORY_STATE",{"species_body":"dragon"})])
 def test_scene_cannot_change_companion(self):
  with self.assertRaises(ValueError): compose(RECORDS[6],[Layer("SCENE_STATE",{"companions":["raccoon"]})])
 def test_scene_can_change_pose_without_identity_mutation(self):
  s,t=compose(RECORDS[6],[Layer("SCENE_STATE",{"pose":"mounted","lighting":"sunset"})]); self.assertEqual(s["_scene_state"]["pose"],"mounted"); self.assertEqual(s["species_body"],RECORDS[6].species_body)
 def test_weekly_story_state_is_namespaced(self):
  s,t=compose(RECORDS[8],[Layer("WEEKLY_STORY_STATE",{"pressure":"must recover","verified_event_ids":["W3"]})]); self.assertEqual(s["_weekly_story_state"]["pressure"],"must recover"); self.assertEqual(s["identity"],"The Belt Keeper")
 def test_override_without_provenance_fails(self):
  with self.assertRaises(ValueError): compose(RECORDS[0],[Layer("EXPLICIT_COMMISSIONER_OVERRIDE",{"silhouette":"x"})])
 def test_commissioner_override_can_change_identity_with_trace(self):
  s,t=compose(RECORDS[0],[Layer("EXPLICIT_COMMISSIONER_OVERRIDE",{"silhouette":"approved future silhouette"},("Jake approval event",))]); self.assertEqual(t[0]["kind"],"EXPLICIT_COMMISSIONER_OVERRIDE")
 def test_contract_not_render_ready_without_portable_asset(self):
  c=compile_contract("Donkey Kong",RECORDS,ASSETS); self.assertFalse(c["render_ready"])
 def test_qa_fail_closed(self):
  self.assertEqual(decide([],False)["status"],"HUMAN_REVIEW_REQUIRED")
  self.assertEqual(decide([QACheck("species","gorilla","centaur","FATAL")],True)["status"],"REGENERATE")
 def test_receipt_requires_pass(self):
  with self.assertRaises(ValueError): publication_receipt({},{"status":"REGENERATE"},"abc")
if __name__=="__main__": unittest.main()
