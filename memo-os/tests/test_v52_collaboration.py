import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).resolve().parents[1] / "collaboration" / "v52_contract.py"
spec = importlib.util.spec_from_file_location("v52_contract", path)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def valid():
    p = {k: "present" for k in v.REQUIRED}
    p["ack_state"] = "VALIDATED"
    return p

class CollaborationAcceptance(unittest.TestCase):
    def test_COLLAB_001(self):
        p = valid(); p.pop("source_authority")
        self.assertEqual(v.handoff(p), "MISSING_PROVENANCE")
    def test_COLLAB_002(self):
        self.assertFalse(v.ready(["PASSED", "WAITING"]))
    def test_COLLAB_003(self):
        p = valid(); p.update(benchmark_only=True, blank_canvas=True)
        self.assertEqual(v.handoff(p), "BENCHMARK_LEAKAGE")
    def test_COLLAB_004(self):
        self.assertEqual(v.work_key("W03", "snapshot7"), v.work_key("W03", "snapshot7"))
        self.assertNotEqual(v.work_key("W03", "snapshot7"), v.work_key("W03", "snapshot8"))
    def test_COLLAB_005(self):
        x = v.correction(["page2"], ["page1", "page2", "page3"])
        self.assertEqual(x["reopen"], {"page2"})
        self.assertEqual(x["preserve"], {"page1", "page3"})
    def test_COLLAB_006(self):
        self.assertEqual(v.route("CHARACTER_FAILURE"), "Character / Art")
    def test_COLLAB_007(self):
        self.assertFalse(v.escalation_needed("ROUTINE_DEFECT"))
    def test_COLLAB_008(self):
        p = valid(); p["ack_state"] = "HANDOFF_READY"
        self.assertFalse(v.accept(p))
    def test_COLLAB_009(self):
        self.assertFalse(v.release_allowed([{"state": "SUPERSEDED", "qa": "PASS"}]))
    def test_COLLAB_010(self):
        p = valid(); p["mercer_derived"] = True
        self.assertEqual(v.handoff(p), "MERCER_FIREWALL_VIOLATION")
    def test_COLLAB_011(self):
        p = valid(); p["missing_context"] = True
        self.assertEqual(v.handoff(p), "CONTRACT_VIOLATION")
    def test_COLLAB_012(self):
        self.assertFalse(v.ready(["BLOCKED"]))
    def test_valid_handoff(self):
        self.assertTrue(v.accept(valid()))
    def test_unverified_release(self):
        self.assertFalse(v.release_allowed([{"state": "PASSED", "qa": "FAIL"}]))

if __name__ == "__main__":
    unittest.main()
