"""Static compatibility acceptance for the existing Memo OS visual packet template.

This validates routing documentation, not image execution or independent Umpire signoff.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "memo-os/post-production/PAGE_DESIGN_PACKET_TEMPLATE_V2.md"
REFERENCE = ROOT / "memo-os/cinematography/FRANK_MASI_UNIT_STILLS_REFERENCE_V1.md"

class UnitStillsMemoPacketTests(unittest.TestCase):
    def test_priority_trigger_documented(self):
        value = TEMPLATE.read_text()
        for marker in ("CONSULTATION TIER:", "cover", "decisive matchup beat", "UNIT-STILLS REVIEW STATUS:", "NOT_RUN"):
            self.assertIn(marker, value)

    def test_existing_page_fields_retained(self):
        value = TEMPLATE.read_text()
        for marker in ("OWNER→CHARACTER RESOLUTION:", "MAP/ATLAS ID:", "DETERMINISTIC TYPOGRAPHY/DATA:", "APPROVAL/LOCK STATE:"):
            self.assertIn(marker, value)

    def test_authority_and_stop_rules(self):
        value = TEMPLATE.read_text() + REFERENCE.read_text()
        for marker in ("source reference bytes", "independent Umpire", "MS-05", "Failure of MS-05 is BLOCK"):
            self.assertIn(marker, value)

if __name__ == "__main__":
    unittest.main()
