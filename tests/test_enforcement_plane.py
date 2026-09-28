import copy, json, tempfile, unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("enforcement_validate",ROOT/"governance/enforcement/validate.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class EnforcementKernelTests(unittest.TestCase):
    def setUp(self):
        self.registry=mod.load_registry(ROOT)

    def test_registry_is_valid(self):
        mod.validate_registry(ROOT,self.registry)

    def test_policy_ids_are_unique(self):
        ids=[p["policy_id"] for p in self.registry["policies"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_duplicate_policy_id_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"].append(copy.deepcopy(reg["policies"][0]))
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)

    def test_invalid_severity_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"][0]["severity"]="NUCLEAR"
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)

    def test_missing_validator_fails(self):
        reg=copy.deepcopy(self.registry)
        reg["policies"][0]["validator"]="does_not_exist"
        with self.assertRaises(mod.EnforcementFailure):
            mod.validate_registry(ROOT,reg)

    def test_merge_kernel_runs(self):
        self.assertTrue(mod.run(ROOT,"MERGE"))

if __name__=="__main__":
    unittest.main()
