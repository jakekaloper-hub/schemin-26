import importlib.util
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "release-evidence" / "release_evidence.py"
REGISTRY = ROOT / "governance" / "release-evidence" / "registry.json"

spec = importlib.util.spec_from_file_location("release_evidence", MODULE)
release_evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_evidence)


class ReleaseEvidenceTests(unittest.TestCase):
    def receipt(self, **overrides):
        base = {
            "receipt_id": "R",
            "system_id": "S",
            "tested_commit_sha": "old",
            "anchor_blob_sha": "digest-a",
            "result": "PASS",
            "required_checks": [{"name": "ci", "conclusion": "success"}],
            "unresolved_blockers": [],
        }
        base.update(overrides)
        return base

    def test_old_green_same_subsystem_is_current_subsystem_not_exact_head(self):
        result = release_evidence.classify_receipt(
            self.receipt(),
            current_head_sha="new-head",
            current_anchor_blob_sha="digest-a",
        )
        self.assertEqual(result["state"], "CURRENT_SUBSYSTEM_PASS")
        self.assertFalse(result["applies_to_repo_head_exactly"])

    def test_changed_subsystem_demotes_old_green_to_historical(self):
        result = release_evidence.classify_receipt(
            self.receipt(),
            current_head_sha="new-head",
            current_anchor_blob_sha="digest-b",
        )
        self.assertEqual(result["state"], "HISTORICAL_ONLY_CHANGED_SUBSYSTEM")

    def test_red_current_check_overrides_pass_label(self):
        receipt = self.receipt(
            required_checks=[{"name": "real-integration", "conclusion": "failure"}]
        )
        result = release_evidence.classify_receipt(
            receipt,
            current_head_sha="old",
            current_anchor_blob_sha="digest-a",
        )
        self.assertEqual(result["state"], "BLOCKED_CURRENT_EVIDENCE")
        self.assertEqual(result["red_checks"], ["real-integration"])

    def test_explicit_historical_pass_never_becomes_current(self):
        result = release_evidence.classify_receipt(
            self.receipt(result="HISTORICAL_PASS"),
            current_head_sha="old",
            current_anchor_blob_sha="digest-a",
        )
        self.assertEqual(result["state"], "HISTORICAL_ONLY")

    def test_exact_commit_and_digest_is_current_head_pass(self):
        result = release_evidence.classify_receipt(
            self.receipt(),
            current_head_sha="old",
            current_anchor_blob_sha="digest-a",
        )
        self.assertEqual(result["state"], "CURRENT_HEAD_PASS")
        self.assertTrue(result["applies_to_repo_head_exactly"])

    def test_block_receipt_stays_blocked_even_when_digest_matches(self):
        result = release_evidence.classify_receipt(
            self.receipt(result="BLOCKED", unresolved_blockers=["REAL_PAGE_MISSING"]),
            current_head_sha="old",
            current_anchor_blob_sha="digest-a",
        )
        self.assertEqual(result["state"], "BLOCKED_CURRENT_EVIDENCE")
        self.assertIn("REAL_PAGE_MISSING", result["unresolved_blockers"])

    def test_repository_registry_has_no_false_active_pass(self):
        registry = json.loads(REGISTRY.read_text())
        findings = release_evidence.validate_registry(
            registry,
            ROOT,
            current_head_sha="test-head-different-from-release-commits",
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
