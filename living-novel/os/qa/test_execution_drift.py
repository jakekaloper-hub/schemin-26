"""Tests for non-mutating, advisory Novel/Execution Control drift detection."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_execution_drift.py")
spec = importlib.util.spec_from_file_location("execution_drift", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DriftTest(unittest.TestCase):
    def make_root(self, statuses, with_source=True):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"tasks": [
            {"task_id": key, "status": status} for key, status in statuses.items()
        ]}), encoding="utf-8")
        if with_source:
            source = root / "living-novel/whole-book/_INDEX.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "D0nkey K0ng's sole-undefeated claim ends\n"
                "REVIEWED SOFT MANUSCRIPT\n", encoding="utf-8"
            )
        return root

    def test_detects_stale_tasks_without_completing_them(self):
        root = self.make_root({"MEMO-W4-002": "WAITING_EXTERNAL", "NOVEL-NEXT-002": "NOT_STARTED"})
        original = (root / "governance/execution-control/TASK_REGISTRY_V1.json").read_bytes()
        result = module.inspect(root)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual([f["task"] for f in result["findings"]], ["MEMO-W4-002", "NOVEL-NEXT-002"])
        self.assertEqual(result["authority_effect"], "NONE_READ_ONLY_ADVISORY")
        self.assertEqual((root / "governance/execution-control/TASK_REGISTRY_V1.json").read_bytes(), original)

    def test_verified_or_completed_task_is_not_flagged(self):
        root = self.make_root({"MEMO-W4-002": "VERIFYING", "NOVEL-NEXT-002": "COMPLETE"})
        self.assertEqual(module.inspect(root)["status"], "NO_KNOWN_DRIFT")

    def test_missing_source_is_visible_but_not_certified(self):
        root = self.make_root({"MEMO-W4-002": "NOT_STARTED", "NOVEL-NEXT-002": "NOT_STARTED"}, False)
        report = module.inspect(root)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual({f["result"] for f in report["findings"]}, {"MISSING_SOURCE"})

    def test_missing_task_is_visible(self):
        root = self.make_root({"MEMO-W4-002": "WAITING_EXTERNAL"})
        report = module.inspect(root)
        self.assertEqual([f["result"] for f in report["findings"]], ["REVIEW_REQUIRED", "MISSING_TASK"])

    def test_missing_registry_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(module.inspect(directory)["status"], "ERROR")

    def test_malformed_registry_is_error_not_green(self):
        root = self.make_root({"MEMO-W4-002": "NOT_STARTED"})
        registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
        registry.write_text('{"tasks": {"not": "an array"}}', encoding="utf-8")
        self.assertEqual(module.inspect(root)["reason"], "TASK_REGISTRY_TASKS_NOT_ARRAY")

    def test_invalid_task_objects_fail_closed(self):
        root = self.make_root({"MEMO-W4-002": "NOT_STARTED"})
        registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
        registry.write_text('{"tasks": [null, "bad"]}', encoding="utf-8")
        self.assertEqual(module.inspect(root)["reason"], "TASK_REGISTRY_INVALID_TASK_OBJECT")

    def test_no_marker_does_not_claim_drift(self):
        root = self.make_root({"MEMO-W4-002": "NOT_STARTED", "NOVEL-NEXT-002": "NOT_STARTED"})
        (root / "living-novel/whole-book/_INDEX.md").write_text("No corresponding manuscript assertions")
        self.assertEqual(module.inspect(root)["status"], "NO_KNOWN_DRIFT")


if __name__ == "__main__":
    unittest.main()
