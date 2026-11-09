"""Regression tests for the read-only Commonwealth creative context adapter."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "creative_context.py"
spec = importlib.util.spec_from_file_location("creative_context", MODULE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        files = {
            adapter.ROUTER: json.dumps({
                "defaults": {"max_matches": 2},
                "routes": [{"id": "draft", "terms": ["chapter"],
                            "context_sources": ["living-novel/pre-prose.md"]}]
            }),
            adapter.AUTHORITY: "# Source matrix",
            adapter.REGISTRY: "{}",
            "living-novel/pre-prose.md": "# Gate",
        }
        for name, data in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data, encoding="utf-8")

    def test_routes_and_pins_authority(self):
        result = adapter.resolve_context(self.root, "write a chapter")
        self.assertEqual(result["status"], "CONTEXT_READY_NOT_APPROVED")
        self.assertEqual(result["routes"], ["draft"])
        self.assertEqual(result["sources"][0]["path"], adapter.AUTHORITY)
        self.assertEqual(result["sources"][1]["path"], adapter.REGISTRY)

    def test_empty_or_unknown_intent_is_blocked(self):
        for intent in ("", "do something unknown"):
            with self.subTest(intent=intent), self.assertRaises(adapter.ContextError):
                adapter.resolve_context(self.root, intent)

    def test_missing_authority_is_blocked(self):
        (self.root / adapter.AUTHORITY).unlink()
        with self.assertRaises(adapter.ContextError):
            adapter.resolve_context(self.root, "write chapter")

    def test_missing_scene_source_is_blocked(self):
        (self.root / "living-novel/pre-prose.md").unlink()
        with self.assertRaises(adapter.ContextError):
            adapter.resolve_context(self.root, "write chapter")

    def test_traversal_is_blocked(self):
        path = self.root / adapter.ROUTER
        data = json.loads(path.read_text())
        data["routes"][0]["context_sources"] = ["../../secrets"]
        path.write_text(json.dumps(data))
        with self.assertRaises(adapter.ContextError):
            adapter.resolve_context(self.root, "write chapter")


if __name__ == "__main__":
    unittest.main()
