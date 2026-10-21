import copy
import unittest
from canon.characters.runtime.provider_attachment_receipt import validate_provider_attachment_receipt as verify

H = "a" * 64
I = "b" * 64
ASSETS = [{"character_id": "CHAR-WILSON-LOOK", "sha256": H, "subject_slot": "left"},
          {"character_id": "CHAR-PHILLIP-PITTS", "sha256": I, "subject_slot": "right"}]
RECEIPT = {
    "request_id": "render-001", "route": "test-adapter", "origin": "PROVIDER_OBSERVED",
    "provider_invocation_id": "invocation-001", "provider_evidence_id": "evidence-001",
    "attachments": [
        {"character_id": "CHAR-WILSON-LOOK", "mounted_sha256": H, "subject_slot": "left",
         "provider_attachment_id": "file-1", "provider_subject_binding_id": "binding-1",
         "provider_binding_observed": True},
        {"character_id": "CHAR-PHILLIP-PITTS", "mounted_sha256": I, "subject_slot": "right",
         "provider_attachment_id": "file-2", "provider_subject_binding_id": "binding-2",
         "provider_binding_observed": True},
    ]
}

class TestProviderReceipt(unittest.TestCase):
    def check(self, receipt, expected_state, assets=ASSETS):
        self.assertEqual(verify("render-001", "test-adapter", assets, receipt)["state"], expected_state)

    def test_structural_validity_is_not_generation_eligibility(self):
        result = verify("render-001", "test-adapter", ASSETS, RECEIPT)
        self.assertEqual(result["state"], "ATTACHMENT_RECEIPT_STRUCTURALLY_VALID")
        self.assertFalse(result["generation_eligible"])
        self.assertFalse(result["visual_qa_passed"])

    def test_missing_receipt(self):
        self.check(None, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_missing_provider_evidence(self):
        r = copy.deepcopy(RECEIPT)
        del r["provider_evidence_id"]
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_swapped_subject_slot(self):
        r = copy.deepcopy(RECEIPT)
        r["attachments"][0]["subject_slot"] = "right"
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_swapped_image_bytes(self):
        r = copy.deepcopy(RECEIPT)
        r["attachments"][0]["mounted_sha256"] = I
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_missing_binding(self):
        r = copy.deepcopy(RECEIPT)
        r["attachments"][1]["provider_binding_observed"] = False
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_duplicate_attachment(self):
        r = copy.deepcopy(RECEIPT)
        r["attachments"][1]["provider_attachment_id"] = "file-1"
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

    def test_missing_second_character(self):
        r = copy.deepcopy(RECEIPT)
        r["attachments"].pop()
        self.check(r, "RENDERER_REFERENCE_MOUNT_UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
