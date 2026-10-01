import json
import pathlib
import unittest

from canon.characters.runtime.renderer_capabilities import negotiate


ROOT=pathlib.Path(__file__).resolve().parents[3]
REGISTRY=ROOT/"canon"/"characters"/"renderer_capabilities_v1.json"


class RendererCapabilityEvidenceTests(unittest.TestCase):
    def test_current_available_route_is_truthfully_blocked(self):
        doc=json.loads(REGISTRY.read_text())
        route="CURRENT_CHATGPT_IMAGE_RENDERER"
        result=negotiate(route,doc["routes"],1)
        self.assertEqual(result["state"],"GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN")
        self.assertEqual(result["reason"],"CAPABILITY_EVIDENCE_UNPROVEN")
        self.assertEqual(doc["routes"][route]["production_state"],"PROVIDER_CAPABILITY_BLOCKED")

    def test_claimed_features_without_evidence_receipt_do_not_pass(self):
        caps={"x":{
            "evidence_state":"PROVEN",
            "capability_receipt_id":None,
            "supports_image_references":True,
            "returns_attachment_receipt":True,
            "returns_mounted_byte_hash_receipt":True,
            "supports_subject_binding":True,
            "returns_subject_binding_receipt":True,
            "max_references":12,
        }}
        self.assertEqual(negotiate("x",caps,1)["reason"],"CAPABILITY_EVIDENCE_UNPROVEN")


if __name__=="__main__":
    unittest.main()
