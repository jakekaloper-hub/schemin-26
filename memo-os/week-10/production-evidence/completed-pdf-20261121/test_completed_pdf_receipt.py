import copy
import json
import unittest
from pathlib import Path

import validate_completed_pdf_receipt as v


class CompletedPdfReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(v.RECEIPT.read_text())
        cls.manifest = json.loads(v.SOURCE.read_text())
        cls.source_sha = v.sha256(v.SOURCE)

    def errors(self, receipt=None, manifest=None, source_sha=None):
        return v.check_receipt(
            self.receipt if receipt is None else receipt,
            self.manifest if manifest is None else manifest,
            self.source_sha if source_sha is None else source_sha,
        )

    def test_source_crosswalk_and_nonpromotion_pass(self):
        self.assertEqual([], self.errors())

    def test_source_manifest_change_fails_closed(self):
        self.assertIn("source_manifest_changed", self.errors(source_sha="0" * 64))

    def test_unexpected_source_reorder_fails_closed(self):
        altered = copy.deepcopy(self.manifest)
        altered["pages"][1]["reading_position"] = 3
        self.assertIn("source_position_sequence", self.errors(manifest=altered))

    def test_missing_added_pittsys_page_fails_closed(self):
        altered = copy.deepcopy(self.receipt)
        altered["page_crosswalk"][33]["source_page_id"] = "W10-P32"
        self.assertIn("pittsys_book_insertion", self.errors(receipt=altered))

    def test_duplicate_physical_page_fails_closed(self):
        altered = copy.deepcopy(self.receipt)
        altered["page_crosswalk"][34]["pdf_physical_page"] = 34
        self.assertIn("crosswalk_physical_order", self.errors(receipt=altered))

    def test_fake_distribution_pass_is_rejected(self):
        altered = copy.deepcopy(self.receipt)
        altered["status"]["league_distribution_date_and_channel"] = "CONFIRMED"
        self.assertIn("unauthorized_distribution", self.errors(receipt=altered))

    def test_fake_benchmark_promotion_is_rejected(self):
        altered = copy.deepcopy(self.receipt)
        altered["status"]["current_benchmark"] = "WEEK10"
        self.assertIn("unauthorized_benchmark", self.errors(receipt=altered))

    def test_fake_full_pixel_qa_is_rejected(self):
        altered = copy.deepcopy(self.receipt)
        altered["status"]["all_35_pages_full_copy_character_pixel_qa"] = "PASS"
        self.assertIn("unauthorized_qa_claim", self.errors(receipt=altered))

    def test_no_public_pdf_binary(self):
        self.assertFalse(self.receipt["artifact"]["bytes_embedded_in_public_repo"])


if __name__ == "__main__":
    unittest.main()
