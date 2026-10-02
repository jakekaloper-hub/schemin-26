from __future__ import annotations

import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "resilience" / "resilience.py"
spec = importlib.util.spec_from_file_location("schemin_resilience", MODULE)
resilience = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resilience)

class ResilienceTests(unittest.TestCase):
    def test_conditioning_registry_has_memo_and_novel_and_valid_authorities(self):
        doc = json.loads((ROOT / "governance/resilience/CREATIVE_CONDITIONING_REGISTRY_V1.json").read_text())
        self.assertEqual(resilience.validate_conditioning_registry(doc), [])
        ids = {x["id"] for x in doc["systems"]}
        self.assertEqual(ids, {"weekly-memo","living-novel"})

    def test_checkpoint_reuse_requires_matching_inputs(self):
        cp = {
            "version":"1.0.0",
            "checkpoint_id":"TEST-1",
            "project":"Schemin '26",
            "workflow":"test",
            "stage":"story-lock",
            "owner":"the_groundskeeper",
            "source_authority":"PROJECT_CONTROL_REGISTRY.md",
            "completed_at":"2026-10-02T00:00:00-04:00",
            "input_fingerprints":[{"path":"FACT_LOCK.json","digest_algo":"sha256","digest":"abc12345"}],
            "outputs":[{"path":"STORY_LOCK.md","digest_algo":"sha256","digest":"def67890"}],
            "evidence":["test:fixture"],
            "invalidation_triggers":["fact lock changes"]
        }
        self.assertEqual(resilience.validate_checkpoint(cp), [])
        self.assertTrue(resilience.checkpoint_inputs_match(cp, {"FACT_LOCK.json":"abc12345"}))
        self.assertFalse(resilience.checkpoint_inputs_match(cp, {"FACT_LOCK.json":"changed"}))

    def test_latest_valid_checkpoint_skips_invalidated_newer_stage(self):
        base = {
            "version":"1.0.0","project":"Schemin '26","workflow":"test","owner":"the_groundskeeper",
            "source_authority":"PROJECT_CONTROL_REGISTRY.md",
            "outputs":[{"path":"x","digest_algo":"sha256","digest":"abcdef12"}],
            "evidence":["fixture"],"invalidation_triggers":["input drift"]
        }
        a = dict(base, checkpoint_id="A", stage="facts", completed_at="2026-10-01T10:00:00-04:00",
                 input_fingerprints=[{"path":"facts","digest_algo":"sha256","digest":"11111111"}])
        b = dict(base, checkpoint_id="B", stage="story", completed_at="2026-10-01T11:00:00-04:00",
                 input_fingerprints=[{"path":"story-input","digest_algo":"sha256","digest":"22222222"}])
        latest = resilience.latest_valid_checkpoint([a,b], {"facts":"11111111","story-input":"changed"})
        self.assertEqual(latest["checkpoint_id"], "A")

    def test_fresh_operator_recovers_current_work_without_chat_memory(self):
        registry = json.loads((ROOT / "governance/execution-control/TASK_REGISTRY_V1.json").read_text())
        fixtures = {
            "continue week 4 memo":"MEMO-W4-002",
            "character portability":"CHAR-PORT-002",
            "next chapter":"NOVEL-NEXT-002",
        }
        for phrase, task_id in fixtures.items():
            task = resilience.resolve_task_by_alias(registry, phrase)
            self.assertIsNotNone(task, phrase)
            self.assertEqual(task["task_id"], task_id)
            self.assertTrue(task.get("next_action"))
            self.assertTrue((ROOT / task["source_authority"]).exists(), task["source_authority"])

    def test_fresh_operator_routes_exist_in_session_context(self):
        project = (ROOT / "docs/SESSION_CONTEXT.md").read_text()
        novel = (ROOT / "living-novel/os/SESSION_CONTEXT.md").read_text()
        self.assertIn("governance/resilience/README.md", project)
        self.assertIn("governance/execution-control/TASK_REGISTRY_V1.json", project)
        self.assertIn("governance/resilience/README.md", novel)

    def test_no_fla_runtime_dependency_is_introduced(self):
        harvest = (ROOT / "governance/resilience/FLA_PATTERN_HARVEST_V1.md").read_text()
        self.assertIn("pattern donor only", harvest)
        self.assertIn("no production dependency is installed", harvest)

if __name__ == "__main__":
    unittest.main()
