"""Unit-stills advisory contract regression tests. Run: python -m unittest discover -s living-novel/os/adapters -p 'test_*unit_stills*.py'"""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("adapter", Path(__file__).with_name("comfyui_adapter.py"))
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def review(**overrides):
    fields = {
        "reference_id": "frank-masi-unit-stills-v1",
        "consultation_tier": 1,
        "beat_id": "beat",
        "beat_evidence_class": "FICTIONALIZATION",
        "decisive_instant": "the threshold opens",
        "emotional_objective": "dread",
        "camera_role": "witness",
        "camera_position_and_axis": "eye-level north",
        "virtual_shot_scale_and_perspective": "wide",
        "foreground_midground_background": "road/gate/hills",
        "motivated_light_and_shadow_check": "torch left",
        "character_pose_silhouette_readability": "clear",
        "action_and_occlusion_check": "none",
        "text_safe_region": "upper right",
        "atlas_location_and_horizon_lock": "approved location",
        "continuity_in_out": "open/closed",
        "reviewer": "Cinematography Director",
        "review_status": "PASS",
    }
    fields.update(overrides)
    return fields


class UnitStillsTests(unittest.TestCase):
    def test_valid_pass(self):
        adapter.validate_unit_stills(review())

    def test_missing_camera_rejected(self):
        with self.assertRaises(ValueError):
            adapter.validate_unit_stills(review(camera_position_and_axis=""))

    def test_unapproved_rejected(self):
        with self.assertRaises(ValueError):
            adapter.validate_unit_stills(review(review_status="NOT_RUN"))

    def test_bad_reference_rejected(self):
        with self.assertRaises(ValueError):
            adapter.validate_unit_stills(review(reference_id="unknown"))

    def test_non_tier_one_advisory(self):
        adapter.validate_unit_stills(review(consultation_tier=2, review_status="NOT_RUN"))

    def test_optional_contract_keeps_existing_job_valid(self):
        job = {
            "schema": "NovelVisualJob/v1", "job_id": "test", "beat_id": "beat",
            "manuscript_anchor": "anchor", "composition_map": "map",
            "reference_assets": [], "object_locks": [], "character_locks": [],
            "environment_packet": "ENV", "camera_spec": "eye-level",
            "lighting_spec": "natural", "negative_constraints": [],
            "continuity_predecessors": [], "output": {"width": 1024, "height": 1536, "format": "png"},
            "seed_policy": {"mode": "record"}, "qa_contract": {},
        }
        adapter.validate_job(job)
        job["unit_stills_review"] = review()
        result = adapter.compile_job(job)
        self.assertEqual(result["state"], "COMPILED_UNRENDERED")
        self.assertEqual(result["controls"]["unit_stills_review"]["reference_id"], "frank-masi-unit-stills-v1")


if __name__ == "__main__":
    unittest.main()
