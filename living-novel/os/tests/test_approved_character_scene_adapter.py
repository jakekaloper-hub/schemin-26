"""NovelVisualJob compositor must hydrate canon before a character job can compile."""
import importlib.util
import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
import copy

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location("current_novel_renderer_adapter",ROOT/"living-novel/os/adapters/comfyui_adapter.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
JOB=json.loads((ROOT/"chronicles/proof-of-concept/prologue/S03_NOVEL_VISUAL_JOB_V1.json").read_text())

class CurrentApprovedCharacterSceneAdapterTests(TestCase):
    def test_legacy_environment_only_job_remains_compiled_unrendered(self):
        d=MOD.compile_job(JOB)
        self.assertEqual(d["state"],"COMPILED_UNRENDERED")
        self.assertNotIn("approved_character_visual_context",d["controls"])

    def test_character_job_hydrates_real_novel_runtime_but_provider_stays_blocked(self):
        job=copy.deepcopy(JOB)
        job["character_locks"]=[{"character_id":"CHAR-JAKE-KALOPER"}]
        job["environment_packet"]={"location_id":"LOC-TRADE-JEDI-MOUNTAIN-BASE"}
        d=MOD.compile_job(job)
        self.assertEqual(d["state"],"COMPILED_UNRENDERED_CHARACTER_PROVIDER_QA_HOLD")
        v=d["controls"]["approved_character_visual_context"]
        self.assertEqual(v["current_visual_authority"]["subjects"][0]["character_id"],"CHAR-JAKE-KALOPER")
        self.assertFalse(v["source_and_subject_binding_verified"])
        self.assertFalse(v["image_generation_eligible"])
        self.assertTrue(v["physical_constraints"]["CHAR-JAKE-KALOPER"]["anatomy_constraints"])
        self.assertEqual(v["spatial_anchors"]["CHAR-JAKE-KALOPER"]["home_location_id"],"LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertEqual(v["t15"],"HOLD")

    def test_bad_location_and_identity_block_before_comfyui_transport(self):
        bad=copy.deepcopy(JOB)
        bad["character_locks"]=[{"character_id":"CHAR-JAKE-KALOPER"}]
        for env in ("ENV-ARCHIVE",{"location_id":"LOC-UNREGISTERED"}):
            bad["environment_packet"]=env
            with self.assertRaises(ValueError):
                MOD.compile_job(bad)
        bad["environment_packet"]={"location_id":"LOC-TRADE-JEDI-MOUNTAIN-BASE"}
        bad["character_locks"]=[{"character_id":"CHAR-FAKE"}]
        with self.assertRaises(ValueError):
            MOD.compile_job(bad)
        bad["character_locks"]=[{"character_id":"CHAR-JAKE-KALOPER"}]*2
        with self.assertRaisesRegex(ValueError,"duplicates"):
            MOD.compile_job(bad)
