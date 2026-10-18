"""Seven real semantic canaries are never confused with generated visual QA."""
import unittest,json
from pathlib import Path
from world.production.audit_lineup_render_readiness import audit

ROOT=Path(__file__).resolve().parents[2]
FILE=ROOT/"world/location-control-plane/evidence/LINEUP_RUNTIME_CANARY_AUDIT_2026_10_18.json"

class RuntimeCanaryEvidenceTests(unittest.TestCase):
    def test_actual_live_semantic_invocations_match_saved_evidence(self):
        result=json.loads(FILE.read_text())
        self.assertEqual(result,audit())
        self.assertEqual(len(result["canaries"]),7)
        self.assertEqual(result["actual_generated_output_count"],0)
        self.assertEqual(result["live_image_generation_calls"],0)
        self.assertFalse(result["production_character_image_eligible"])
        self.assertEqual(result["provider_status"],"PROVIDER_CAPABILITY_BLOCKED")
        self.assertEqual(result["t15"],"HOLD")
        self.assertEqual(result["t16"],"HOLD")
        for a in result["canaries"]:
            self.assertEqual(a["generated_artwork"],"NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN")

    def test_matchup_uses_actual_existing_venue_and_both_subjects(self):
        d=json.loads(FILE.read_text())
        x=next(y for y in d["canaries"] if y["id"]=="G_RED_LEOPARDS_HOST_DK_MATCHUP")
        self.assertEqual(x["existing_venue_id"],"LOC-RED-RUINS")
        self.assertEqual(x["memo_visual_subjects"],2)
        self.assertFalse(x["geography_new_or_invented"])
