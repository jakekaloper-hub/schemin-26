"""Exact authoritative source-byte recovery regression — never promotes a render route."""
import json
import hashlib
import unittest
from pathlib import Path

from canon.characters.runtime.source_byte_integrity import verify_source_bytes

ROOT = Path(__file__).resolve().parents[3]
RECOVERY = ROOT / "canon/characters/recovery/EXACT_PRIMARY_CACHE_RECOVERY_2026_10_17.json"
REGISTRY = ROOT / "canon/characters/reference_sources_v1.json"

class RecoveredPrimaryTests(unittest.TestCase):
    def test_recovered_primaries_match_original_authority_byte_for_byte(self):
        receipt=json.loads(RECOVERY.read_text())
        authority=json.loads(REGISTRY.read_text())
        active={item["character_id"]:item for item in authority["entries"]}
        self.assertEqual(len(receipt["items"]),2)
        self.assertEqual({x["character_id"] for x in receipt["items"]},
                         {"CHAR-MANNING-WELTY","CHAR-BRANDON-PRYOR"})
        for item in receipt["items"]:
            expected=active[item["character_id"]]
            p=ROOT/item["repository_path"]
            raw=p.read_bytes()
            self.assertEqual(item["repository_path"],expected["repository_path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item["sha256"])
            self.assertEqual(item["sha256"],expected["expected_sha256"])
            self.assertEqual(len(raw),expected["observed_library_size_bytes"])
            self.assertTrue(raw.startswith(b"\xff\xd8\xff"))
            self.assertFalse(item["renderer_mount_verified"])
            self.assertFalse(item["subject_binding_verified"])

    def test_actual_approved_primary_count_four_and_remaining_eight_fail_closed(self):
        result=verify_source_bytes()
        self.assertEqual(result["total"],12)
        self.assertEqual(result["pass_count"],4)
        self.assertEqual(result["source_bytes_required_count"],8)
        self.assertEqual(result["blocked_count"],0)
        self.assertEqual(result["state"],"SOURCE_BYTES_REQUIRED")
