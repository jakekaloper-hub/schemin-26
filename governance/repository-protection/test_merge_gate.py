import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "repository-protection" / "merge_gate.py"

spec = importlib.util.spec_from_file_location("merge_gate", MODULE)
merge_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(merge_gate)


class MergeGatePlannerTests(unittest.TestCase):
    def test_docs_only_has_no_heavy_suite(self):
        self.assertEqual(merge_gate.plan(["docs/notes/README.md"]), [])

    def test_memo_change_runs_memo(self):
        self.assertIn("memo", merge_gate.plan(["memo-os/week-4/_INDEX.md"]))

    def test_world_change_runs_world(self):
        self.assertIn("world", merge_gate.plan(["world/data/locations.json"]))

    def test_novel_engine_runs_novel_world_and_character(self):
        suites = merge_gate.plan(["living-novel/os/engine/novel_os.py"])
        self.assertIn("novel", suites)
        self.assertIn("world", suites)

    def test_character_runtime_runs_character(self):
        self.assertIn(
            "character",
            merge_gate.plan(["canon/characters/runtime/generation_adapter.py"]),
        )

    def test_bullpen_runtime_runs_bullpen(self):
        self.assertEqual(
            merge_gate.plan(["bullpen-runtime/src/runtime.js"]),
            ["bullpen"],
        )

    def test_data_change_runs_data(self):
        self.assertIn("data", merge_gate.plan(["data-gateway/refresh_espn_snapshot.py"]))

    def test_whole_book_change_runs_novel(self):
        self.assertIn("novel", merge_gate.plan(["living-novel/whole-book/_INDEX.md"]))

    def test_character_native_render_plan_runs_mission(self):
        self.assertIn(
            "mission",
            merge_gate.plan(["planning/character-native-render/PHASE_1_13_EXECUTION_PLANS_V1.md"]),
        )

    def test_project_registry_runs_mission(self):
        self.assertIn("mission", merge_gate.plan(["PROJECT_CONTROL_REGISTRY.md"]))

    def test_publication_manifest_runs_publication_suite(self):
        self.assertIn(
            "publication",
            merge_gate.plan(["governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"]),
        )

    def test_publication_inventory_change_runs_publication_suite(self):
        self.assertIn("publication", merge_gate.plan(["docs/INVENTORY.md"]))

    def test_release_evidence_change_runs_release(self):
        self.assertIn(
            "release",
            merge_gate.plan(["governance/release-evidence/registry.json"]),
        )

    def test_character_anchor_runs_release_evidence_too(self):
        suites = merge_gate.plan(["canon/_INDEX.md"])
        self.assertIn("release", suites)

    def test_failed_required_command_propagates_failure(self):
        old = merge_gate.SUITE_COMMANDS["mission"]
        merge_gate.SUITE_COMMANDS["mission"] = ["python -c 'raise SystemExit(7)'"]
        try:
            with self.assertRaises(Exception):
                merge_gate.run_suite("mission")
        finally:
            merge_gate.SUITE_COMMANDS["mission"] = old


if __name__ == "__main__":
    unittest.main()
