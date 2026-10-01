import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "task-orientation" / "validate_task_context.py"

spec = importlib.util.spec_from_file_location("validate_task_context", MODULE)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

def load_matrix(relative_path):
    import json
    return json.loads((ROOT / relative_path).read_text())

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

    def test_week4_memo_simulation_stays_in_memo_context(self):
        matrix = load_matrix("governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json")
        result = validator.route_task("Create Week 4 Weekly Memo.", matrix)
        self.assertEqual(result["routes"][0], "weekly-memo")
        self.assertLessEqual(len(result["context_sources"]), 4)
        self.assertNotIn("living-novel/os/NOVEL_BOOK_ARCHITECTURE_V2.md", result["context_sources"])
        self.assertNotIn("world/atlas/ATLAS_CONTROL_PLANE_V2.md", result["context_sources"])

    def test_hmb_character_repair_simulation_starts_with_character_authority(self):
        matrix = load_matrix("governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json")
        result = validator.route_task("Fix incorrect His Majesty's Blood character rendering.", matrix)
        self.assertEqual(result["routes"][0], "character-visual")
        self.assertIn("canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md", result["context_sources"])
        self.assertNotIn("memo-os/_INDEX.md", result["context_sources"])
        self.assertNotIn("living-novel/os/NOVEL_BOOK_ARCHITECTURE_V2.md", result["context_sources"])

    def test_next_chapter_simulation_delegates_to_novel_then_chapter_packet(self):
        schemin = load_matrix("governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json")
        first = validator.route_task("Plan next chapter.", schemin)
        self.assertEqual(first["routes"][0], "living-novel")
        self.assertIn("living-novel/os/TASK_CONTEXT_MATRIX_V1.json", first["context_sources"])

        novel = load_matrix("living-novel/os/TASK_CONTEXT_MATRIX_V1.json")
        second = validator.route_task("Plan next chapter.", novel)
        self.assertEqual(second["routes"][0], "chapter-planning-and-drafting")
        self.assertLessEqual(len(second["context_sources"]), 4)
        self.assertIn("living-novel/os/templates/MINIMUM_PRE_PROSE_GATE_V1.md", second["context_sources"])
        self.assertNotIn("living-novel/consultants/NOVEL_EXTERNAL_ADVISORY_COUNCIL_V1.md", second["context_sources"])

    def test_boundary_matching_does_not_route_art_from_start(self):
        matrix = {
            "defaults": {"max_matches": 2, "max_context_sources": 4, "context_sources": []},
            "routes": [{"id": "art", "terms": ["art"], "context_sources": ["README.md"]}],
        }
        self.assertEqual(validator.route_task("start the workflow", matrix)["routes"], [])
        self.assertEqual(validator.route_task("review the art", matrix)["routes"], ["art"])

if __name__ == "__main__":
    unittest.main()
