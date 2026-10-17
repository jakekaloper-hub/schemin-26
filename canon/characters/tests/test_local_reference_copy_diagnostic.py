"""Diagnostic transport images are traceable but cannot certify AI rendering."""
import json
import hashlib
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[3]
REPORT=ROOT/"canon/characters/recovery/LOCAL_REFERENCE_COPY_DIAGNOSTIC_2026_10_17.json"
SOURCES=ROOT/"canon/characters/reference_sources_v1.json"


class StaticCopyDiagnosticTests(unittest.TestCase):
    def test_four_output_images_are_specific_and_hash_verified(self):
        doc=json.loads(REPORT.read_text())
        auth={x["character_id"]:x for x in json.loads(SOURCES.read_text())["entries"]}
        self.assertEqual(doc["tested_primary_count"],4)
        self.assertEqual(doc["unavailable_primary_count"],8)
        self.assertEqual(len(doc["outputs"]),4)
        self.assertEqual(len({x["output_sha256"] for x in doc["outputs"]}),4)
        self.assertEqual(len({x["subject_slot"] for x in doc["outputs"]}),4)
        for x in doc["outputs"]:
            self.assertEqual(x["input_repository_path"],auth[x["character_id"]]["repository_path"])
            self.assertEqual(x["input_sha256"],auth[x["character_id"]]["expected_sha256"])
            self.assertEqual(hashlib.sha256((ROOT/x["input_repository_path"]).read_bytes()).hexdigest(),
                             x["input_sha256"])
            p=ROOT/x["output_repository_path"]
            self.assertEqual(p.read_bytes()[:8],b"\x89PNG\r\n\x1a\n")
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x["output_sha256"])
            self.assertTrue(x["source_hash_checked_before_copy"])
            self.assertTrue(x["repeat_conversion_byte_identical"])
            self.assertFalse(x["provider_image_generation_binding_proven"])

    def test_diagnostic_does_not_override_production_and_umpire_gates(self):
        doc=json.loads(REPORT.read_text())
        self.assertFalse(doc["production_renderer"])
        self.assertFalse(doc["renderer_subject_binding_proven"])
        self.assertFalse(doc["c1_generated_raster_qa_passed"])
        self.assertEqual(doc["t15"],"HOLD")
        self.assertEqual(doc["t16"],"HOLD")


if __name__=="__main__":
    unittest.main()
