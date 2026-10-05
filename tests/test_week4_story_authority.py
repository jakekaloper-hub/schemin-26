import copy
import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
PACK=ROOT/"memo-os/week-4/publication-readiness"

def load_module(name, rel):
    path=ROOT/rel
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

story=load_module("week4_story_authority","governance/publication/week4_story_authority.py")
render=load_module("week4_render_eligibility_story","governance/publication/week4_render_eligibility.py")
assembly=load_module("week4_assembly_validator_story","governance/publication/week4_assembly_validator.py")

class Week4StoryAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.register=json.loads((PACK/"WEEK_04_STORY_AUTHORITY_REGISTER.json").read_text())
        self.manifest=json.loads((PACK/"WEEK_04_PUBLICATION_MANIFEST.json").read_text())
        self.ownership=json.loads((PACK/"WEEK_04_DIRECTOR_OWNERSHIP_MATRIX.json").read_text())
        self.by_id={u["story_unit_id"]:u for u in self.register["story_units"]}

    def packet(self, story_id):
        u=self.by_id[story_id]
        return {
          "page_id":"TEST-PAGE","page_number":1,"page_function":"test",
          "narrative_purpose":"test","story_beat":"test","fact_dependencies":[],
          "character_ids":[],"character_authority_refs":[],"exact_reference_assets":[],
          "world_state_ref":"world/state/WORLD_STATE_LEDGER_V1.md","venue_ref":"test","geography_ref":"test",
          "composition":"test","foreground":"test","midground":"test","background":"test",
          "text_hierarchy":["headline"],"headline":"test","copy_fields":[],
          "deterministic_data_fields":[],"visual_objects":[],"negative_constraints":[],
          "drift_risks":[],"rejection_conditions":[],"mobile_readability_requirements":["phone"],
          "previous_page":None,"next_page":None,"status":"PAGE_RENDER_ELIGIBLE",
          "story_authority_id":story_id,
          "story_authority_hash":u["story_authority_hash"],
          "story_authority_receipt":"memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json",
          "story_authority_state":"CURRENT"
        }

    def test_story_authority_validator_passes(self):
        result=story.validate()
        self.assertEqual(result["state"],"PASS",result)

    def test_six_matchups_and_required_modules_are_registered(self):
        self.assertEqual(len(self.register["required_matchup_story_units"]),6)
        for uid in self.register["required_matchup_story_units"]+self.register["required_editorial_modules"]:
            self.assertIn(uid,self.by_id)
            self.assertEqual(self.by_id[uid]["status"],"CURRENT")

    def test_llc_hmb_current_story_authority_rejects_three_page_stale_architecture(self):
        u=self.by_id["W4-STORY-LLC-HMB"]
        self.assertEqual(u["current_page_count"],1)
        self.assertIn("one substantial matchup page",u["page_role"].lower())
        self.assertIn("THE HOUSE GETS BEAT",u["headline_direction"])
        self.assertIn("$100",u["visual_job"])
        self.assertIn("Achane",u["prose_job"])
        self.assertIn("Darnold $15",u["prose_job"])
        self.assertIn("LEDGER",u["transition_job"])
        self.assertIn("BAROMETER",u["transition_job"])
        self.assertTrue(any("three-page" in x for x in u["superseded_sources"]))

    def test_active_publication_manifest_does_not_seed_stale_fixed_19_page_plan(self):
        self.assertEqual(self.manifest["page_plan_state"],"WAITING_ON_STORY_LOCK")
        self.assertEqual(self.manifest["pages"],[])
        self.assertEqual(self.manifest["legacy_page_plan"]["state"],"SUPERSEDED_NON_CONTROLLING")

    def test_page_packet_schema_requires_story_authority_receipt_and_hash(self):
        schema=json.loads((ROOT/"schemas/week4-page-packet.schema.json").read_text())
        for field in ("story_authority_id","story_authority_hash","story_authority_receipt","story_authority_state"):
            self.assertIn(field,schema["required"])

    def test_stale_story_hash_blocks_render(self):
        p=self.packet("W4-STORY-LLC-HMB")
        p["story_authority_hash"]="0"*64
        result=render.render_eligibility(p)
        self.assertEqual(result["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(result["reason"],"PAGE_PACKET_STALE")
        self.assertEqual(result["detail"],"STORY_AUTHORITY_HASH_MISMATCH")

    def test_unknown_story_authority_blocks_render(self):
        p=self.packet("W4-STORY-LLC-HMB")
        p["story_authority_id"]="W4-STORY-OLD-LLC-HMB"
        result=render.render_eligibility(p)
        self.assertEqual(result["reason"],"PAGE_PACKET_STALE")
        self.assertEqual(result["detail"],"STORY_AUTHORITY_ID_UNKNOWN")

    def test_generation_hold_blocks_even_current_story_packet(self):
        p=self.packet("W4-MODULE-OPENING")
        result=render.render_eligibility(p)
        self.assertEqual(result["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(result["reason"],"STORY_AUTHORITY_GENERATION_HOLD")

    def test_source_blob_change_invalidates_story_authority(self):
        bad=copy.deepcopy(self.register)
        bad["story_units"][0]["current_controlling_sources"][0]["blob_sha"]="0"*40
        result=story.validate(bad)
        self.assertEqual(result["state"],"FAIL_INTERNAL")
        self.assertTrue(any(x["code"]=="STORY_AUTHORITY_SOURCE_STALE" for x in result["errors"]))

    def test_director_ownership_has_12_named_gates_and_counterweights(self):
        gates=self.ownership["gates"]
        self.assertEqual([g["gate_id"] for g in gates],[f"G{i}" for i in range(1,13)])
        for g in gates:
            self.assertTrue(g["owner"])
            self.assertTrue(g["counterweight"])
            self.assertEqual(g["control_status"],"PASS")

    def test_assembly_waits_on_story_lock(self):
        doc=json.loads((PACK/"WEEK_04_ASSEMBLY_MANIFEST.json").read_text())
        result=assembly.validate(doc)
        self.assertEqual(result["state"],"HOLD_EXTERNAL")
        self.assertEqual(result["reason"],"WAITING_ON_STORY_LOCK")

if __name__=="__main__":
    unittest.main()
