"""Prevent active Memo OS production entrypoints from omitting native PNG geometry."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = (
    "_INDEX.md",
    "SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md",
    "SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md",
    "SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md",
)

class ForwardFormatContractTests(unittest.TestCase):
    def test_active_entrypoints_inherit_canonical_geometry(self):
        for relative in ENTRYPOINTS:
            with self.subTest(entrypoint=relative):
                content = (ROOT / relative).read_text()
                self.assertIn("## Forward PNG geometry (2026-10-28)", content)
                for field in ("output_format: PNG", "output_width_px: 1080",
                              "output_height_px: 1920", "output_aspect_ratio: 9:16",
                              "native_png_contract.py"):
                    self.assertIn(field, content)

    def test_page_packet_schema_requires_output_fields(self):
        content = (ROOT / "PAGE_PRODUCTION_CONTRACT_V1.md").read_text()
        for field in ("output_format: PNG", "output_width_px: 1080",
                      "output_height_px: 1920", "output_aspect_ratio: '9:16'"):
            self.assertEqual(content.count(field), 1)

if __name__ == "__main__":
    unittest.main()
