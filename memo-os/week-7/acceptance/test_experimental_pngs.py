"""Non-generative test-image checks; never certify final illustrated QA."""
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "memo-os/week-7/experimental-pngs"

class ExperimentalPngTests(unittest.TestCase):
    def test_three_native_pngs_have_correct_geometry(self):
        for folio in ("P005", "P006", "P007"):
            with self.subTest(folio=folio):
                data = (BASE / f"{folio}_SOURCE_BOUND_TEST.png").read_bytes()
                self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
                self.assertEqual(struct.unpack(">II", data[16:24]), (1024, 1536))
                self.assertGreater(len(data), 100000)

    def test_receipt_never_promotes_composite_to_artwork(self):
        r = json.loads((BASE / "receipt.json").read_text())
        self.assertEqual(r["pages"], ["P005", "P006", "P007"])
        self.assertFalse(r["provider_subject_binding_proven"])
        self.assertFalse(r["publication_eligible"])
        self.assertIn("not generative illustration", r["type"])

if __name__ == "__main__":
    unittest.main()
