import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from governance.publication.founder_approval_runtime import (
    GateError, initialize, inspect, issue_founder_receipt, transition, verify_receipt,
)
from governance.publication.founder_approval_gate import REQUIRED_QA, BLOCKING_FLAGS

A = "a" * 64
B = "b" * 64
ENV = {"MEMO_APPROVAL_SIGNING_KEY": "x" * 64,
       "MEMO_FOUNDER_PRINCIPAL": "founder:verified-user",
       "MEMO_TRUSTED_IDENTITY_VERIFIER": "trusted-auth-service"}

def initial():
    state = {"issue_id": "week-6", "state": "INTAKE", "approved_plan_sha256": A,
             "final_pdf_sha256": B, "qa": {k: "PASS" for k in REQUIRED_QA},
             "open_critical_defects": 0}
    state.update({k: True for k in BLOCKING_FLAGS})
    return state

def receipt(gate, digest):
    return issue_founder_receipt(issue_id="week-6", gate=gate, artifact_sha256=digest,
                                receipt_id="test-" + gate,
                                authenticated_principal=ENV["MEMO_FOUNDER_PRINCIPAL"],
                                verified_by=ENV["MEMO_TRUSTED_IDENTITY_VERIFIER"])

class DurableApprovalTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, ENV)
        self.env.start()
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "state.json"
        initialize(self.path, initial())

    def tearDown(self):
        self.tmp.cleanup()
        self.env.stop()

    def advance(self):
        transition(self.path, "SOURCE_LOCK")
        transition(self.path, "PREPRODUCTION")
        transition(self.path, "PAGE_PRODUCTION", approvals={"creative": receipt("CREATIVE_DIRECTION", A)})
        transition(self.path, "ASSEMBLY")
        transition(self.path, "RELEASE_CANDIDATE")

    def test_full_release_and_restart(self):
        self.advance()
        self.assertEqual(inspect(self.path)["state"], "RELEASE_CANDIDATE")
        state = transition(self.path, "RELEASED", approvals={"publication": receipt("FINAL_PUBLICATION", B)})
        self.assertEqual(state["state"], "RELEASED")
        self.assertEqual(inspect(self.path)["state"], "RELEASED")

    def test_no_approval_denies_production(self):
        transition(self.path, "SOURCE_LOCK")
        transition(self.path, "PREPRODUCTION")
        with self.assertRaises(GateError):
            transition(self.path, "PAGE_PRODUCTION")
        self.assertEqual(inspect(self.path)["state"], "PREPRODUCTION")

    def test_direct_release_bypass(self):
        with self.assertRaises(GateError):
            transition(self.path, "RELEASED")

    def test_forged_receipt(self):
        bad = receipt("CREATIVE_DIRECTION", A)
        bad["payload"]["principal"] = "attacker"
        with self.assertRaises(GateError):
            verify_receipt(bad, gate="CREATIVE_DIRECTION", issue_id="week-6", artifact_sha256=A)

    def test_wrong_founder(self):
        with self.assertRaises(GateError):
            issue_founder_receipt(issue_id="week-6", gate="CREATIVE_DIRECTION", artifact_sha256=A,
                                 receipt_id="fake", authenticated_principal="attacker",
                                 verified_by=ENV["MEMO_TRUSTED_IDENTITY_VERIFIER"])

    def test_missing_signing_key(self):
        with patch.dict(os.environ, {"MEMO_APPROVAL_SIGNING_KEY": ""}):
            with self.assertRaises(GateError):
                receipt("CREATIVE_DIRECTION", A)

    def test_tampered_persisted_state(self):
        doc = json.loads(self.path.read_text())
        doc["payload"]["state"] = "RELEASED"
        self.path.write_text(json.dumps(doc))
        with self.assertRaises(GateError):
            inspect(self.path)

    def test_stale_approval_hash(self):
        with self.assertRaises(GateError):
            verify_receipt(receipt("FINAL_PUBLICATION", B), gate="FINAL_PUBLICATION",
                           issue_id="week-6", artifact_sha256="c" * 64)

    def test_approval_survives_recovery(self):
        transition(self.path, "SOURCE_LOCK")
        transition(self.path, "PREPRODUCTION")
        transition(self.path, "PAGE_PRODUCTION", approvals={"creative": receipt("CREATIVE_DIRECTION", A)})
        self.assertEqual(inspect(self.path)["approvals"]["creative"]["artifact_sha256"], A)

if __name__ == "__main__":
    unittest.main()
