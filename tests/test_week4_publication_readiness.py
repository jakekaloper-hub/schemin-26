import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_module(name, rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

readiness = load_module("week4_readiness", "governance/publication/week4_readiness.py")
elig = load_module("week4_render_eligibility", "governance/publication/week4_render_eligibility.py")

class Week4ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT/"memo-os/week-4/publication-readiness/WEEK_04_PUBLICATION_MANIFEST.json").read_text())
        self.char_matrix = json.loads((ROOT/"memo-os/week-4/publication-readiness/WEEK_04_12_CHARACTER_AUTHORITY_MATRIX.json").read_text())
        self.hash_by_id = {x["character_id"]:x["expected_sha256"] for x in self.char_matrix["characters"]}
        self.story_register = json.loads((ROOT/"memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json").read_text())
        self.story_by_id = {x["story_unit_id"]:x for x in self.story_register["story_units"]}

    def complete_packet(self, chars=None, story_id="W4-MODULE-OPENING"):
        chars = chars or []
        story = self.story_by_id[story_id]
        return {
          "page_id":"TEST-PAGE","page_number":1,"page_function":"test",
          "narrative_purpose":"test","story_beat":"test","fact_dependencies":[],
          "character_ids":chars,
          "character_authority_refs":["canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"] if chars else [],
          "exact_reference_assets":[{"character_id":c,"authority_ref":"canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json","expected_sha256":self.hash_by_id[c],"state":"ACTIVE"} for c in chars],
          "character_continuity":{"CHAR-PHILLIP-PITTS":"EXPLICIT_WEEK4_CONTINUITY_RESOLUTION_REQUIRED"} if "CHAR-PHILLIP-PITTS" in chars else {},
          "world_state_ref":"world/state/WORLD_STATE_LEDGER_V1.md","venue_ref":"test","geography_ref":"test",
          "composition":"test","foreground":"test","midground":"test","background":"test",
          "text_hierarchy":["headline"],"headline":"test","copy_fields":[],
          "deterministic_data_fields":[],"visual_objects":[],"negative_constraints":[],
          "drift_risks":[],"rejection_conditions":[],"mobile_readability_requirements":["phone"],
          "previous_page":None,"next_page":None,"status":"PAGE_RENDER_ELIGIBLE",
          "story_authority_id":story_id,
          "story_authority_hash":story["story_authority_hash"],
          "story_authority_receipt":"memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json",
          "story_authority_state":"CURRENT",
          "story_page_role":story["page_role"],
          "visual_job":story["visual_job"],
          "prose_job":story["prose_job"],
          "data_job":story["data_job"],
          "transition_job":story["transition_job"]
        }

    def test_manifest_has_exactly_twelve_gates(self):
        self.assertEqual([g["gate_id"] for g in self.manifest["gates"]],[f"G{i}" for i in range(1,13)])

    def test_active_manifest_waits_on_story_lock_instead_of_using_stale_fixed_page_plan(self):
        self.assertEqual(self.manifest["page_plan_state"],"WAITING_ON_STORY_LOCK")
        self.assertEqual(self.manifest["pages"],[])
        self.assertEqual(self.manifest["legacy_page_plan"]["state"],"SUPERSEDED_NON_CONTROLLING")

    def test_missing_page_packet_blocks_render(self):
        r=elig.render_eligibility({"page_id":"bad"})
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"PAGE_PACKET_INVALID")

    def test_character_packet_without_reference_blocks(self):
        p=self.complete_packet(["CHAR-JAKE-KALOPER"],"W4-STORY-DK-OBI")
        p["exact_reference_assets"]=[]
        r=elig.render_eligibility(p)
        self.assertEqual(r["reason"],"CHARACTER_REFERENCE_MISSING")

    def test_dk_current_authority_contract_is_centaur_gorilla(self):
        self.assertTrue(elig.dk_authority_valid())

    def test_active_registry_uses_frat_star_not_fart_star(self):
        registry=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        resolver=(ROOT/"canon/characters/cccp_resolver.py").read_text()
        self.assertIn("Frat Star", registry)
        self.assertIn("Frat Star", resolver)
        self.assertNotIn('aliases: ["Fart Star"', registry)
        self.assertNotIn('"aliases":["Fart Star"', resolver)

    def test_active_registry_does_not_reject_dk_centaur_anatomy(self):
        registry=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        self.assertIn("Arsenal Gorilla Centaur Warrior", registry)
        self.assertIn("FOUR-LEGGED CENTAUR LOWER BODY", registry)
        self.assertNotIn('hard_reject: ["centaur anatomy"', registry)

    def test_dk_render_route_fail_closes_while_provider_proof_unresolved(self):
        p=self.complete_packet(["CHAR-WILSON-LOOK"],"W4-STORY-DK-OBI")
        r=elig.render_eligibility(p)
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"GENERATION_BLOCKED_PROVIDER_CAPABILITY_UNPROVEN")

    def test_all_twelve_characters_have_unique_authority_rows_and_hashes(self):
        rows=self.char_matrix["characters"]
        self.assertEqual(len(rows),12)
        self.assertEqual(len({x["character_id"] for x in rows}),12)
        self.assertEqual(len({x["expected_sha256"] for x in rows}),12)
        for row in rows:
            self.assertEqual(len(row["expected_sha256"]),64)
            self.assertTrue(row["required"])
            self.assertTrue(row["reject"])

    def test_all_twelve_active_surfaces_match_current_identity_and_hash(self):
        registry=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        records=(ROOT/"canon/character-control-plane-v2/records.py").read_text()
        for row in self.char_matrix["characters"]:
            cid=row["character_id"]
            identity=row["identity"]
            team=row["team"]
            spec=(ROOT/f"canon/characters/{cid}/T04_CHARACTER_SPEC.md").read_text()
            package=(ROOT/f"canon/characters/{cid}/PACKAGE.md").read_text()
            self.assertIn(cid, registry)
            self.assertIn(identity, registry)
            self.assertIn(identity, records)
            self.assertIn(identity, spec)
            self.assertIn(identity, package)
            self.assertIn(row["expected_sha256"], spec)
            self.assertIn(team, spec)

    def test_wrong_owner_reference_hash_blocks_before_provider(self):
        p=self.complete_packet(["CHAR-AUSTIN-BYARS"],"W4-STORY-LLC-HMB")
        p["exact_reference_assets"][0]["expected_sha256"]="0"*64
        r=elig.render_eligibility(p)
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"CHARACTER_REFERENCE_HASH_MISMATCH")

    def test_tds_requires_explicit_week4_continuity_resolution(self):
        p=self.complete_packet(["CHAR-PHILLIP-PITTS"],"W4-STORY-MUD-TDS")
        p["character_continuity"]={}
        r=elig.render_eligibility(p)
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"CHARACTER_CONTINUITY_UNRESOLVED")

    def test_week4_release_is_still_blocked(self):
        pub=readiness.publication_record()
        self.assertEqual(pub["release_state"],"BLOCKED")
        self.assertIsNone(pub["canonical_artifact"])

    def test_pre_mnf_readiness_is_hold_not_false_pass(self):
        result=readiness.validate_internal()
        self.assertNotEqual(result["state"],"PASS")
        self.assertIn(result["state"],{"HOLD_EXTERNAL","FAIL_INTERNAL"})

if __name__=="__main__":
    unittest.main()
