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

    def complete_packet(self, chars=None):
        chars = chars or []
        return {
          "page_id":"TEST-PAGE","page_number":1,"page_function":"test",
          "narrative_purpose":"test","story_beat":"test","fact_dependencies":[],
          "character_ids":chars,
          "character_authority_refs":["canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"] if chars else [],
          "exact_reference_assets":[{"character_id":c,"authority_ref":"canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json","expected_sha256":"x","state":"ACTIVE"} for c in chars],
          "world_state_ref":"world/state/WORLD_STATE_LEDGER_V1.md","venue_ref":"test","geography_ref":"test",
          "composition":"test","foreground":"test","midground":"test","background":"test",
          "text_hierarchy":["headline"],"headline":"test","copy_fields":[],
          "deterministic_data_fields":[],"visual_objects":[],"negative_constraints":[],
          "drift_risks":[],"rejection_conditions":[],"mobile_readability_requirements":["phone"],
          "previous_page":None,"next_page":None,"status":"PAGE_RENDER_ELIGIBLE"
        }

    def test_manifest_has_exactly_twelve_gates(self):
        self.assertEqual([g["gate_id"] for g in self.manifest["gates"]],[f"G{i}" for i in range(1,13)])

    def test_manifest_has_exactly_nineteen_pages(self):
        self.assertEqual([p["page_number"] for p in self.manifest["pages"]], list(range(1,20)))

    def test_missing_page_packet_blocks_render(self):
        r=elig.render_eligibility({"page_id":"bad"})
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"PAGE_PACKET_INVALID")

    def test_character_packet_without_reference_blocks(self):
        p=self.complete_packet(["CHAR-JAKE-KALOPER"])
        p["exact_reference_assets"]=[]
        r=elig.render_eligibility(p)
        self.assertEqual(r["reason"],"CHARACTER_REFERENCE_MISSING")

    def test_dk_current_authority_contract_is_centaur_gorilla(self):
        self.assertTrue(elig.dk_authority_valid())

    def test_dk_render_route_fail_closes_while_provider_proof_unresolved(self):
        p=self.complete_packet(["CHAR-WILSON-LOOK"])
        r=elig.render_eligibility(p)
        self.assertEqual(r["state"],"PAGE_RENDER_BLOCKED")
        self.assertEqual(r["reason"],"GENERATION_BLOCKED_PROVIDER_CAPABILITY_UNPROVEN")

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
