"""Current character production gates must not silently use a spotlight fallback."""
import unittest
from pathlib import Path

from canon.characters.runtime.source_byte_integrity import preflight_character_set

ROOT=Path(__file__).resolve().parents[3]


class CurrentCharacterPreflightTests(unittest.TestCase):
    def test_four_approved_primaries_have_hashes_but_unproved_renderer_is_blocked(self):
        report=preflight_character_set([
            "CHAR-BRANDON-PRYOR","CHAR-AUSTIN-BYARS",
            "CHAR-MANNING-WELTY","CHAR-PHILLIP-PITTS",
        ])
        self.assertEqual(report["source_verified_count"],4)
        self.assertEqual(report["source_required_count"],0)
        self.assertFalse(report["generation_eligible"])
        self.assertEqual(report["reason"],"RENDERER_CAPABILITY_OR_SUBJECT_BINDING_UNPROVEN")
        self.assertEqual(report["route_state"],"GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN")

    def test_eight_missing_originals_cannot_be_replaced_by_existing_spotlights(self):
        ids=[
            "CHAR-BEN-WHIPPLE","CHAR-BOBBY-MITCHELL","CHAR-DAVID-BABB",
            "CHAR-JAKE-KALOPER","CHAR-JORDAN-HOLLINGSHEAD",
            "CHAR-KEVIN-ZEEK","CHAR-WILSON-LOOK","CHAR-ZACH-WILSON",
        ]
        report=preflight_character_set(ids)
        self.assertEqual(report["source_verified_count"],0)
        self.assertEqual(report["source_required_count"],8)
        self.assertEqual(set(report["missing_character_ids"]),set(ids))
        self.assertEqual(report["reason"],"APPROVED_PRIMARY_BYTES_MISSING")
        self.assertFalse(report["generation_eligible"])

    def test_duplicate_and_unknown_characters_are_rejected(self):
        for values in (
            [],["CHAR-FAKE"],
            ["CHAR-AUSTIN-BYARS","CHAR-AUSTIN-BYARS"],
        ):
            r=preflight_character_set(values)
            self.assertEqual(r["reason"],"CHARACTER_SET_INVALID_OR_UNRECOGNIZED")
            self.assertFalse(r["generation_eligible"])

    def test_render_request_cannot_smuggle_supplementary_as_primary(self):
        report=preflight_character_set(["CHAR-JAKE-KALOPER"])
        self.assertFalse(report["generation_eligible"])
        self.assertEqual(report["records"][0]["source_state"],"SOURCE_BYTES_REQUIRED")
        self.assertIn("/primary/",report["records"][0]["approved_primary_path"])


if __name__=="__main__":
    unittest.main()
