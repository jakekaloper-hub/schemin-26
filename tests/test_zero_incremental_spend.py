import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
PATH=ROOT/"governance"/"capability-budget"/"validate_zero_spend.py"
spec=importlib.util.spec_from_file_location("budget",PATH)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ZeroSpendTests(unittest.TestCase):
    def setUp(self):
        self.doc=json.loads((ROOT/"governance"/"capability-budget"/"ZERO_INCREMENTAL_SPEND_V1.json").read_text())

    def test_registry_passes(self):
        self.assertEqual(mod.validate(self.doc),[])

    def test_creative_claw_is_not_critical_path(self):
        p=next(x for x in self.doc["providers"] if x["provider"]=="Creative Claw")
        self.assertEqual(p["class"],"UNFUNDED_EXTERNAL")
        self.assertFalse(p["critical_path_allowed"])

    def test_native_chatgpt_is_baseline(self):
        p=next(x for x in self.doc["providers"] if x["provider"]=="ChatGPT native image generation/editing")
        self.assertEqual(p["class"],"NATIVE_INCLUDED")
        self.assertTrue(p["critical_path_allowed"])

    def test_unknown_cost_fails_closed(self):
        bad=json.loads(json.dumps(self.doc))
        bad["providers"].append({"provider":"Mystery Renderer","class":"UNKNOWN_COST_BLOCKED","critical_path_allowed":True})
        self.assertTrue(any("critical path" in x for x in mod.validate(bad)))

if __name__=="__main__":
    unittest.main()
