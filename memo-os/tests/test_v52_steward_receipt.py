"""Negative acceptance coverage for Steward receipt verifier.

All signatures here are test-only fixtures, NOT evidence of authenticated
independent acceptance in any live Memo workflow.
"""
import hashlib
import hmac
import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "adapter", ROOT / "memo-os/collaboration/execution_adapter.py"
)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
receipt = adapter.receipt

KEY = "test-fixture-key-for-acceptance-only-not-prod-123456"
ENV = {
    "SCK_STEWARD_RECEIPT_VERIFICATION_KEY": KEY,
    "SCK_STEWARD_TRUSTED_PRINCIPAL": "independent-steward-test",
    "SCK_STEWARD_TRUSTED_ISSUER": "trusted-backend-test",
}


def signed(h, path, **overrides):
    payload = {
        "assignment_id": h["assignment_id"], "run_id": h["run_id"],
        "trace_id": h["trace_id"], "work_key": h["work_key"],
        "artifact": h["artifact"], "artifact_version": h["artifact_version"],
        "artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "source_snapshot": h["source_snapshot"],
        "receiver_principal": ENV["SCK_STEWARD_TRUSTED_PRINCIPAL"],
        "trusted_issuer": ENV["SCK_STEWARD_TRUSTED_ISSUER"],
        "decision": "VALIDATED",
    }
    payload.update(overrides)
    mac = hmac.new(KEY.encode(), json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode(), hashlib.sha256).hexdigest()
    return {"payload": payload, "signature": mac}


def handoff():
    h = {key: "present" for key in adapter.contract.REQUIRED}
    h.update(
        assignment_id="CHAR-PORT-002",
        run_id="S26-TEST",
        trace_id="TRACE-TEST",
        work_key="test/artifact/v1",
        artifact="artifact.json",
        artifact_version=1,
        source_snapshot="source:sha256:test-fixture",
        ack_state="VALIDATED",
    )
    return h


class StewardReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.path = self.root / "artifact.json"
        self.path.write_text('{"test":"facts"}')
        self.patch_root = patch.object(receipt, "ROOT", self.root)
        self.patch_root.start()
        self.addCleanup(self.patch_root.stop)
        self.patch_env = patch.dict(os.environ, ENV)
        self.patch_env.start()
        self.addCleanup(self.patch_env.stop)

    def test_signed_scoped_fixture_can_ready_only_assignment_not_fact_lock(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path)
        result = adapter.evaluate_assignment(h["assignment_id"], h)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["reason"], "SIGNED_STEWARD_VALIDATED")
        self.assertNotIn("fact_lock", result)

    def test_unverified_claimed_ack_blocks(self):
        h = handoff()
        self.assertEqual(receipt.verify(h), "MISSING_STEWARD_RECEIPT")

    def test_no_external_key_fails_closed(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path)
        with patch.dict(os.environ, {"SCK_STEWARD_RECEIPT_VERIFICATION_KEY": ""}):
            self.assertEqual(receipt.verify(h), "MISSING_TRUSTED_STEWARD_VERIFIER")

    def test_tampered_signature_rejected(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path)
        h["steward_receipt"]["signature"] = "0" * 64
        self.assertEqual(receipt.verify(h), "STEWARDSHIP_SIGNATURE_INVALID")

    def test_signed_but_wrong_principal_rejected(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path, receiver_principal="not-independent")
        self.assertEqual(receipt.verify(h), "STEWARDSHIP_IDENTITY_MISMATCH")

    def test_signed_scope_swapping_rejected(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path, assignment_id="OTHER")
        self.assertEqual(receipt.verify(h), "STEWARDSHIP_SCOPE_MISMATCH")

    def test_artifact_mutation_invalidates_receipt(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path)
        self.path.write_text('{"test":"tampered"}')
        self.assertEqual(receipt.verify(h), "STEWARDSHIP_ARTIFACT_MISMATCH")

    def test_traversal_or_missing_artifact_rejected(self):
        h = handoff()
        h["artifact"] = "../outside.json"
        h["steward_receipt"] = signed(h, self.path)
        self.assertEqual(receipt.verify(h), "SOURCE_ARTIFACT_NOT_FOUND")

    def test_explicit_non_validation_rejected(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path, decision="REJECTED")
        self.assertEqual(receipt.verify(h), "STEWARD_NOT_VALIDATED")

    def test_without_ack_state_not_ready_even_with_signature(self):
        h = handoff()
        h["steward_receipt"] = signed(h, self.path)
        h["ack_state"] = "HANDOFF_READY"
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", h)["reason"], "ACK_MISSING")


if __name__ == "__main__":
    unittest.main()
