import copy
import unittest

from governance.publication.founder_approval_gate import evaluate_transition, REQUIRED_QA, BLOCKING_FLAGS

HASH_A = "a" * 64
HASH_B = "b" * 64

def approval(gate, digest):
    return {"gate": gate, "issue_id": "week-6", "artifact_sha256": digest,
            "decision": "APPROVED", "authenticated": True,
            "approver_role": "FOUNDER", "receipt_id": "verified-receipt"}

def fixture():
    item = {"issue_id": "week-6", "state": "RELEASE_CANDIDATE",
            "approved_plan_sha256": HASH_A, "final_pdf_sha256": HASH_B,
            "approvals": {"creative": approval("CREATIVE_DIRECTION", HASH_A),
                          "publication": approval("FINAL_PUBLICATION", HASH_B)},
            "qa": {k: "PASS" for k in REQUIRED_QA}, "open_critical_defects": 0}
    item.update({k: True for k in BLOCKING_FLAGS})
    return item

class FounderApprovalGateTests(unittest.TestCase):
    def test_intake_cannot_skip_source_lock(self):
        item=fixture()
        item["state"]="INTAKE"
        self.assertIn("INVALID_STATE_TRANSITION", evaluate_transition(item,"PREPRODUCTION").errors)

    def test_blocked_cannot_jump_directly_to_assembly(self):
        item=fixture()
        item["state"]="BLOCKED"
        self.assertIn("INVALID_STATE_TRANSITION", evaluate_transition(item,"ASSEMBLY").errors)

    def test_declared_early_transitions_remain_usable(self):
        self.assertEqual(evaluate_transition({"state":"INTAKE"},"SOURCE_LOCK").state,"PASS")
        self.assertEqual(evaluate_transition({"state":"SOURCE_LOCK"},"PREPRODUCTION").state,"PASS")

    def test_valid_release(self):
        self.assertEqual(evaluate_transition(fixture(), "RELEASED").state, "PASS")

    def test_creative_approval_required_before_production(self):
        item = fixture()
        item["state"] = "PREPRODUCTION"
        del item["approvals"]["creative"]
        self.assertIn("FOUNDER_CREATIVE_APPROVAL_MISSING_OR_STALE", evaluate_transition(item, "PAGE_PRODUCTION").errors)

    def test_publication_approval_required(self):
        item = fixture()
        del item["approvals"]["publication"]
        self.assertIn("FOUNDER_PUBLICATION_APPROVAL_MISSING_OR_STALE", evaluate_transition(item, "RELEASED").errors)

    def test_stale_pdf_approval_rejected(self):
        item = fixture()
        item["final_pdf_sha256"] = "c" * 64
        self.assertIn("FOUNDER_PUBLICATION_APPROVAL_MISSING_OR_STALE", evaluate_transition(item, "RELEASED").errors)

    def test_stale_creative_approval_rejected(self):
        item = fixture()
        item["approved_plan_sha256"] = "d" * 64
        self.assertIn("FOUNDER_CREATIVE_APPROVAL_MISSING_OR_STALE", evaluate_transition(item, "PAGE_PRODUCTION").errors)

    def test_wrong_character_reference_blocks(self):
        item = fixture()
        item["character_reference_verified"] = False
        self.assertIn("REQUIRED_PROOF_MISSING:character_reference_verified", evaluate_transition(item, "RELEASED").errors)

    def test_missing_subject_binding_blocks(self):
        item = fixture()
        item["subject_binding_verified"] = False
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_wrong_venue_blocks(self):
        item = fixture()
        item["venue_verified"] = False
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_undecided_result_blocks(self):
        item = fixture()
        item["finality_verified"] = False
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_failed_umpire_blocks(self):
        item = fixture()
        item["qa"]["release_audit"] = "FAIL"
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_pdf_changed_after_approval_blocks(self):
        item = fixture()
        item["final_pdf_inspected"] = False
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_no_bypass_from_preproduction(self):
        item = fixture()
        item["state"] = "PREPRODUCTION"
        self.assertIn("INVALID_RELEASE_TRANSITION", evaluate_transition(item, "RELEASED").errors)

    def test_unauthenticated_approval_rejected(self):
        item = fixture()
        item["approvals"]["publication"]["authenticated"] = False
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_critical_defects_block(self):
        item = fixture()
        item["open_critical_defects"] = 1
        self.assertEqual(evaluate_transition(item, "RELEASED").state, "HOLD")

    def test_invalid_state_rejected(self):
        self.assertEqual(evaluate_transition(fixture(), "PUBLISHED").state, "HOLD")

if __name__ == "__main__":
    unittest.main()
