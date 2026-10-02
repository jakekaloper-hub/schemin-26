from __future__ import annotations

import json
import tempfile
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

    def _fixture_root(self, tmp: str) -> Path:
        root=Path(tmp)
        (root/"authority.md").write_text("authority v1\n")
        (root/"fact.json").write_text('{"score":1}\n')
        (root/"story.md").write_text("story v1\n")
        return root

    def _checkpoint(self, root: Path, checkpoint_id="TEST-1", completed_at="2026-10-02T00:00:00-04:00"):
        return resilience.build_checkpoint(
            checkpoint_id=checkpoint_id,
            project="Schemin '26",
            workflow="test",
            stage="story-lock",
            owner="the_groundskeeper",
            source_authority="authority.md",
            completed_at=completed_at,
            input_paths=["fact.json"],
            output_paths=["story.md"],
            evidence=["test:fixture"],
            invalidation_triggers=["fact lock changes"],
            root=root,
        )

    def test_checkpoint_reuse_requires_matching_inputs_and_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self._fixture_root(tmp)
            cp=self._checkpoint(root)
            self.assertEqual(resilience.validate_checkpoint(cp,root=root), [])
            self.assertTrue(resilience.checkpoint_inputs_match(cp,root=root))
            (root/"fact.json").write_text('{"score":2}\n')
            self.assertFalse(resilience.checkpoint_inputs_match(cp,root=root))

    def test_missing_or_changed_output_invalidates_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self._fixture_root(tmp)
            cp=self._checkpoint(root)
            (root/"story.md").write_text("mutated story\n")
            errors=resilience.validate_checkpoint(cp,root=root)
            self.assertTrue(any("digest mismatch" in x for x in errors))
            (root/"story.md").unlink()
            errors=resilience.validate_checkpoint(cp,root=root)
            self.assertTrue(any("artifact missing" in x for x in errors))

    def test_missing_evidence_path_invalidates_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self._fixture_root(tmp)
            cp=self._checkpoint(root)
            cp["evidence"]=["evidence/missing.md"]
            errors=resilience.validate_checkpoint(cp,root=root)
            self.assertTrue(any("evidence[0] missing" in x for x in errors))

    def test_persist_and_reload_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as store:
            root=self._fixture_root(tmp)
            cp=self._checkpoint(root)
            target=resilience.persist_checkpoint(cp,store_root=Path(store),root=root)
            self.assertTrue(target.exists())
            rows=resilience.load_workflow_checkpoints("test",store_root=Path(store))
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]["checkpoint_id"],"TEST-1")

    def test_latest_valid_checkpoint_skips_invalidated_newer_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"authority.md").write_text("authority\n")
            (root/"facts-a").write_text("A\n")
            (root/"facts-b").write_text("B\n")
            (root/"out-a").write_text("out A\n")
            (root/"out-b").write_text("out B\n")
            a=resilience.build_checkpoint(
                checkpoint_id="A",project="Schemin '26",workflow="test",stage="facts",owner="the_groundskeeper",
                source_authority="authority.md",completed_at="2026-10-01T10:00:00-04:00",
                input_paths=["facts-a"],output_paths=["out-a"],evidence=["test:fixture"],
                invalidation_triggers=["input drift"],root=root,
            )
            b=resilience.build_checkpoint(
                checkpoint_id="B",project="Schemin '26",workflow="test",stage="story",owner="the_groundskeeper",
                source_authority="authority.md",completed_at="2026-10-01T11:00:00-04:00",
                input_paths=["facts-b"],output_paths=["out-b"],evidence=["test:fixture"],
                invalidation_triggers=["input drift"],root=root,
            )
            (root/"facts-b").write_text("changed\n")
            latest=resilience.latest_valid_checkpoint([a,b],root=root)
            self.assertEqual(latest["checkpoint_id"],"A")

    def test_fresh_operator_recovers_current_work_without_chat_memory(self):
        registry = json.loads((ROOT / "governance/execution-control/TASK_REGISTRY_V1.json").read_text())
        fixtures = {
            "continue week 4 memo":("MEMO-W4-002","WAITING_EXTERNAL"),
            "character portability":("CHAR-PORT-002","READY"),
            "next chapter":("NOVEL-NEXT-002","NOT_STARTED"),
        }
        recovered={}
        for phrase, (task_id,status) in fixtures.items():
            task = resilience.resolve_task_by_alias(registry, phrase)
            self.assertIsNotNone(task, phrase)
            self.assertEqual(task["task_id"], task_id)
            self.assertEqual(task["status"],status)
            self.assertTrue(task.get("next_action"))
            self.assertTrue((ROOT / task["source_authority"]).exists(), task["source_authority"])
            recovered[task_id]=task

        self.assertIn("NOVEL-NEXT-002", recovered["MEMO-W4-002"]["blocks"])
        self.assertIn("MEMO-W4-002", recovered["NOVEL-NEXT-002"]["dependencies"])
        self.assertIn("do not ask for bulk re-upload", recovered["CHAR-PORT-002"]["next_action"].lower())
        novel_gate=(ROOT/recovered["NOVEL-NEXT-002"]["source_authority"]).read_text()
        self.assertIn("HOLD",novel_gate)

    def test_fresh_operator_routes_exist_in_session_context(self):
        project = (ROOT / "docs/SESSION_CONTEXT.md").read_text()
        novel = (ROOT / "living-novel/os/SESSION_CONTEXT.md").read_text()
        self.assertIn("governance/resilience/README.md", project)
        self.assertIn("governance/execution-control/TASK_REGISTRY_V1.json", project)
        self.assertIn("governance/resilience/README.md", novel)
        self.assertTrue((ROOT/"PROJECT_CONTROL_REGISTRY.md").exists())

    def test_no_fla_runtime_dependency_is_introduced(self):
        harvest = (ROOT / "governance/resilience/FLA_PATTERN_HARVEST_V1.md").read_text()
        self.assertIn("as a pattern donor", harvest)
        self.assertIn("no production dependency is installed", harvest)

if __name__ == "__main__":
    unittest.main()
