"""Regression checks for the read-only Unreal Atlas export."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "world/atlas/integration/export_unreal_manifest.py"
spec = importlib.util.spec_from_file_location("unreal_export", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DATA = json.loads((Path(__file__).resolve().parents[1] / "world/data/locations.json").read_text())
COMMIT = "a" * 40

class UnrealManifestTests(unittest.TestCase):
    def test_export_contains_no_character_generation(self):
        result = module.export(DATA, COMMIT, "b" * 64)
        self.assertEqual(len(result["locations"]), len(DATA["locations"]))
        self.assertTrue(all(not x["character_spawning_allowed"] and not x["canon_writeback_allowed"] for x in result["locations"]))
    def test_canon_classification_preserved(self):
        exported = module.export(DATA, COMMIT, "b" * 64)["locations"]
        original = {x["id"]: x["canon_status"] for x in DATA["locations"]}
        self.assertTrue(all(x["source_canon_status"] == original[x["location_id"]] for x in exported))
    def test_duplicate_rejected(self):
        data = copy.deepcopy(DATA)
        data["locations"].append(copy.deepcopy(data["locations"][0]))
        with self.assertRaises(ValueError):
            module.export(data, COMMIT, "b" * 64)
    def test_nonfinite_coordinates_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                data = copy.deepcopy(DATA)
                data["locations"][0]["abstract_position"][0] = value
                with self.assertRaises(ValueError):
                    module.export(data, COMMIT, "b" * 64)

    def test_cli_pins_committed_source_even_with_working_tree_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / module.SOURCE
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps(DATA))
            for args in (("init", "-q"), ("add", "."),
                         ("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                          "commit", "-qm", "source fixture")):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            source.write_text("uncommitted invalid source")
            output = root / "preview.json"
            subprocess.run([sys.executable, str(SCRIPT), "--output", str(output)],
                           cwd=root, check=True, capture_output=True)
            result = json.loads(output.read_text())
            committed = subprocess.check_output(["git", "show", "HEAD:" + str(module.SOURCE)], cwd=root)
            self.assertEqual(result["source_sha256"], module.hashlib.sha256(committed).hexdigest())
            self.assertEqual(result["source_commit"],
                             subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip())

    def test_invalid_source_hash_rejected(self):
        for digest in (None, "", "b" * 63, "not-a-hash"):
            with self.subTest(digest=digest):
                with self.assertRaises(ValueError):
                    module.export(DATA, COMMIT, digest)

    def test_metric_coordinates_rejected(self):
        data = copy.deepcopy(DATA)
        data["coordinate_space"] = "meters"
        with self.assertRaises(ValueError):
            module.export(data, COMMIT, "b" * 64)

if __name__ == "__main__":
    unittest.main()
