import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

SCRIPT = Path(__file__).with_name("check_execution_drift.py")
spec = importlib.util.spec_from_file_location("execution_drift", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class DriftTest(unittest.TestCase):
    def make_root(self, statuses, with_source=True):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"tasks": [{"task_id": k, "status": v} for k,v in statuses.items()]}))
        if with_source:
            source = root / "living-novel/whole-book/_INDEX.md"
            source.parent.mkdir(parents=True)
            source.write_text("D0nkey K0ng's sole-undefeated claim ends\nREVIEWED SOFT MANUSCRIPT")
        return root

    def test_detects_stale_tasks(self):
        result = module.inspect(self.make_root({"MEMO-W4-002":"WAITING_EXTERNAL","NOVEL-NEXT-002":"NOT_STARTED"}))
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(len(result["findings"]), 2)

    def test_complete_tasks_not_flagged(self):
        result = module.inspect(self.make_root({"MEMO-W4-002":"COMPLETE","NOVEL-NEXT-002":"COMPLETE"}))
        self.assertEqual(result["status"], "NO_KNOWN_DRIFT")

    def test_missing_evidence_fails_conservatively(self):
        result = module.inspect(self.make_root({"MEMO-W4-002":"NOT_STARTED","NOVEL-NEXT-002":"NOT_STARTED"}, False))
        self.assertEqual({x["result"] for x in result["findings"]}, {"MISSING_SOURCE"})

    def test_missing_registry_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(module.inspect(directory)["status"], "ERROR")

if __name__ == "__main__":
    unittest.main()
