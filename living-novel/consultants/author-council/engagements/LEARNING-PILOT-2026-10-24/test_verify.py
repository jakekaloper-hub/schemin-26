import copy
import unittest
from verify import reading_errors, handoff_errors, verify_artifacts

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.assembly = {"chapter-a.md": "hash-a", "chapter-b.md": "hash-b"}
        self.sources = {"sample": {"full_book_read": False, "read_depth": "EXCERPT_PARTIAL"}, "catalog": {"full_book_read": False, "read_depth": "CATALOG_ONLY"}}
        self.receipt = {"scope": "FULL_ASSEMBLED_MANUSCRIPT", "read_files": self.assembly.copy(), "gaps": [], "accepted": False, "reference_revisits": [{"source_id": "sample", "claim_depth": "EXCERPT_PARTIAL", "method_applied": True}], "findings": [{"passage": "chapter-a.md paragraph 2", "alternatives": ["retain", "targeted revision"]}]}
    def test_exact_assembly_receipt(self):
        self.assertEqual(reading_errors(self.receipt, self.assembly, self.sources), [])
    def test_missing_chapter_rejected(self):
        del self.receipt["read_files"]["chapter-b.md"]
        self.assertIn("incomplete assembled-manuscript coverage", reading_errors(self.receipt, self.assembly, self.sources))
    def test_changed_revision_rejected(self):
        self.receipt["read_files"]["chapter-b.md"] = "old-hash"
        self.assertTrue(reading_errors(self.receipt, self.assembly, self.sources))
    def test_recorded_gap_rejected(self):
        self.receipt["gaps"] = ["unread ending"]
        self.assertTrue(reading_errors(self.receipt, self.assembly, self.sources))
    def test_book_depth_inflation_rejected(self):
        self.receipt["reference_revisits"][0]["claim_depth"] = "FULL_BOOK"
        self.assertIn("reference depth inflated", reading_errors(self.receipt, self.assembly, self.sources))
    def test_catalog_method_rejected(self):
        self.receipt["reference_revisits"][0]["source_id"] = "catalog"
        self.assertIn("catalog is not a learned method", reading_errors(self.receipt, self.assembly, self.sources))
    def test_unknown_source_rejected(self):
        self.receipt["reference_revisits"][0]["source_id"] = "invented"
        self.assertTrue(reading_errors(self.receipt, self.assembly, self.sources))
    def test_missing_alternatives_rejected(self):
        self.receipt["findings"][0]["alternatives"] = ["rewrite everything"]
        self.assertTrue(reading_errors(self.receipt, self.assembly, self.sources))
    def test_acceptance_rejected(self):
        self.receipt["accepted"] = True
        self.assertTrue(reading_errors(self.receipt, self.assembly, self.sources))
    def test_handoff_overclaims_rejected(self):
        self.assertEqual(len(handoff_errors({"historical_claim": True, "owner_binding": "UNVERIFIED", "coverage_claim": "FULL_MANUSCRIPT", "coverage": "FIXTURE_ONLY", "review_mode": "SIMULATED", "accepted": True})), 3)
    def test_bounded_handoff_allowed(self):
        self.assertEqual(handoff_errors({"historical_claim": False, "owner_binding": "UNVERIFIED", "coverage_claim": "EXCERPT_ONLY", "coverage": "EXCERPT_ONLY", "review_mode": "SIMULATED", "accepted": False}), [])
    def test_actual_artifacts(self):
        self.assertEqual(verify_artifacts()["full_manuscript_passes"], 0)

if __name__ == "__main__":
    unittest.main()
