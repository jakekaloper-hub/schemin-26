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
          "story_authority_state":"CURRENT",
          "story_page_role":u["page_role"],
          "visual_job":u["visual_job"],
          "prose_job":u["prose_job"],
          "data_job":u["data_job"],
          "transition_job":u["transition_job"]
        }

    def test_story_authority_validator_passes(self):
        result=story.validate()
        self.assertEqual(result["state"],"PASS",result)

    def test_six_matchups_and_required_modules_are_registered(self):
        self.assertEqual(len(self.register["required_matchup_story_units"]),6)
        for uid in self.register["required_matchup_story_units"]+self.register["required_editorial_modules"]:
            self.assertIn(uid,self.by_id)
            self.assertEqual(self.by_id[uid]["status"],"CURRENT")

    def test_llc_hmb_current_story_authority_is_locked_three_page_architecture(self):
        u=self.by_id["W4-STORY-LLC-HMB"]
        self.assertEqual(u["current_page_count"],3)
        self.assertIn("three-page financial institutional irony",u["page_role"].lower())
        self.assertIn("THE HOUSE GETS BEAT",u["headline_direction"])
        self.assertIn("confidence",u["visual_job"].lower())
        self.assertIn("financial",u["prose_job"].lower())

    def test_active_publication_manifest_locks_exact_27_page_plan(self):
        self.assertEqual(self.manifest["page_plan_state"],"LOCKED")
        self.assertEqual(len(self.manifest["pages"]),27)
        self.assertEqual([p["page_number"] for p in self.manifest["pages"]],list(range(1,28)))
        self.assertEqual(self.manifest["legacy_19_page_plan"]["state"],"SUPERSEDED_NON_CONTROLLING")

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

    def test_current_hash_cannot_hide_semantically_wrong_page(self):
        p=self.packet("W4-STORY-LLC-HMB")
        p["visual_job"]="Generic capital-versus-champion stadium poster."
        result=render.render_eligibility(p)
        self.assertEqual(result["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(result["reason"],"STORY_AUTHORITY_MISMATCH")
        self.assertIn("VISUAL_JOB_MISMATCH",result["detail"])

    def test_source_blob_change_invalidates_story_authority(self):
        bad=copy.deepcopy(self.register)
        bad["story_units"][0]["current_controlling_sources"][0]["blob_sha"]="0"*40
        result=story.validate(bad)
        self.assertEqual(result["state"],"FAIL_INTERNAL")
        self.assertTrue(any(x["code"]=="STORY_AUTHORITY_SOURCE_STALE" for x in result["errors"]))

    def test_supersession_map_marks_stale_llc_hmb_and_sandbox_non_controlling(self):
        smap=json.loads((PACK/"WEEK_04_STORY_SUPERSESSION_MAP.json").read_text())
        rows=smap["classifications"]
        self.assertTrue(any(
            r["classification"]=="SUPERSEDED"
            and "W4-STORY-LLC-HMB" in r.get("scope",[])
            and "one-page llc" in r.get("source","").lower()
            for r in rows
        ))
        self.assertTrue(any(
            r["classification"]=="NON_CONTROLLING"
            and ("#115" in r.get("source","") or "sandbox" in r.get("source","").lower())
            for r in rows
        ))

    def test_director_ownership_has_12_named_gates_and_counterweights(self):
        gates=self.ownership["gates"]
        self.assertEqual([g["gate_id"] for g in gates],[f"G{i}" for i in range(1,13)])
        for g in gates:
            self.assertTrue(g["owner"])
            self.assertTrue(g["counterweight"])
            self.assertNotIn(" + ",g["owner"])
            self.assertNotIn(" / ",g["owner"])
            self.assertEqual(g["control_status"],"PASS")

    def test_assembly_is_locked_to_27_pages_and_waits_on_approved_pngs(self):
        doc=json.loads((PACK/"WEEK_04_ASSEMBLY_MANIFEST.json").read_text())
        result=assembly.validate(doc)
        self.assertEqual(len(doc["pages"]),27)
        self.assertEqual(result["state"],"HOLD_EXTERNAL")
        self.assertEqual(len(result["unresolved_pages"]),27)

if __name__=="__main__":
    unittest.main()
