import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
POLICY=ROOT/"planning"/"render-adapter"/"provider_policy_v1.json"
CAP=ROOT/"canon"/"characters"/"renderer_capabilities_v1.json"

class ProviderNeutralPhase0Tests(unittest.TestCase):
    def test_no_required_external_renderer(self):
        p=json.loads(POLICY.read_text())
        self.assertIsNone(p["required_external_renderer"])
        self.assertTrue(p["no_render_mode_supported"])
        self.assertEqual(p["provider_classes"]["core_required"],[])

    def test_creative_claw_is_optional_not_official(self):
        p=json.loads(POLICY.read_text())
        cc=next(x for x in p["provider_classes"]["optional_external"] if x["provider"]=="CREATIVE_CLAW")
        self.assertEqual(cc["state"],"OPTIONAL_NOT_OFFICIAL")
        self.assertFalse(cc["required"])
        self.assertFalse(cc["canonical_storage"])
        self.assertFalse(cc["authority_owner"])
        self.assertFalse(cc["production_dependency"])

    def test_provider_selection_is_deferred(self):
        p=json.loads(POLICY.read_text())
        self.assertEqual(p["provider_selection_state"],"DEFERRED_UNTIL_PROVIDER_NEUTRAL_BASELINE")

    def test_character_capability_registry_does_not_mark_paid_route_required(self):
        c=json.loads(CAP.read_text())
        self.assertEqual(c["status"],"NO_PRODUCTION_ROUTE_PROVEN")
        self.assertNotIn("required_provider",c)
        for route in c.get("routes",{}).values():
            self.assertNotEqual(route.get("production_state"),"REQUIRED_PROVIDER")

    def test_provider_admission_requires_cost_and_disconnect_semantics(self):
        p=json.loads(POLICY.read_text())
        req=set(p["provider_admission_requirements"])
        self.assertIn("cost_model",req)
        self.assertIn("rollback_or_disconnect_path",req)
        self.assertIn("quality_acceptance_fixture",req)

if __name__=="__main__":
    unittest.main(verbosity=2)
