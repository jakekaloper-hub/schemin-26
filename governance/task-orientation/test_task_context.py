import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "task-orientation" / "validate_task_context.py"

spec = importlib.util.spec_from_file_location("validate_task_context", MODULE)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class TaskContextMatrixTests(unittest.TestCase):
    def test_all_matrices_validate(self):
        errors = []
        for path in validator.MATRICES:
            errors.extend(validator.validate_matrix(path))
        self.assertEqual(errors, [])

    def test_context_ceiling_is_four(self):
        import json
        for path in validator.MATRICES:
            data = json.loads(path.read_text())
            self.assertLessEqual(data["defaults"]["max_context_sources"], 4)
            for route in data["routes"]:
                self.assertLessEqual(len(route["context_sources"]), 4)

    def test_novel_has_dedicated_routing(self):
        import json
        path = ROOT / "living-novel" / "os" / "TASK_CONTEXT_MATRIX_V1.json"
        data = json.loads(path.read_text())
        route_ids = {route["id"] for route in data["routes"]}
        self.assertIn("chapter-planning-and-drafting", route_ids)
        self.assertIn("canon-and-release", route_ids)
        self.assertIn("live-season-translation", route_ids)

if __name__ == "__main__":
    unittest.main()
