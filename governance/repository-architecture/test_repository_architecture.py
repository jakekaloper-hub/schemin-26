import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULE = ROOT / "governance" / "repository-architecture" / "validate_repository_architecture.py"
spec = importlib.util.spec_from_file_location("repo_arch", MODULE)
repo_arch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repo_arch)

class RepositoryArchitectureV2Tests(unittest.TestCase):
    def test_current_repository_passes(self):
        errors = repo_arch.validate(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_unauthorized_top_level_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "known").mkdir()
            (root / "surprise").mkdir()
            registry = {
                "domains": [{
                    "path": "known",
                    "owner": "x",
                    "entrypoint_required": False,
                    "canonical_entrypoint": None,
                    "allowed": ["CONTROL"],
                    "prohibited": []
                }]
            }
            errors = repo_arch.validate_registry(root, registry)
            self.assertTrue(any("unauthorized top-level directories" in e for e in errors))

    def test_missing_required_entrypoint_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "domain").mkdir()
            registry = {
                "domains": [{
                    "path": "domain",
                    "owner": "x",
                    "entrypoint_required": True,
                    "canonical_entrypoint": "domain/README.md",
                    "allowed": ["CONTROL"],
                    "prohibited": []
                }]
            }
            errors = repo_arch.validate_registry(root, registry)
            self.assertTrue(any("canonical entrypoint missing" in e for e in errors))

    def test_navigation_scenarios_are_registered(self):
        data = json.loads((ROOT / "governance" / "repository-architecture" / "NAVIGATION_SCENARIOS_V2.json").read_text())
        self.assertEqual({x["id"] for x in data["scenarios"]}, {
            "A-week4-memo","B-living-novel","C-character-rendering",
            "D-world-validator-placement","E-planning-graduation","F-current-architecture"
        })

if __name__ == "__main__":
    unittest.main()
