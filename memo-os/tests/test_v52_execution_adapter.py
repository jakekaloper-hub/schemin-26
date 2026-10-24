import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "memo-os/collaboration/execution_adapter.py"
spec = importlib.util.spec_from_file_location("adapter", p)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

def handoff(task_id="CHAR-PORT-002"):
    p = {key: "present" for key in adapter.contract.REQUIRED}
    p.update(assignment_id=task_id, ack_state="VALIDATED")
    return p

class IntegratedCollaborationTests(unittest.TestCase):
    def test_real_registry_validated_assignment(self):
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", handoff())["status"], "READY")
    def test_missing_provenance_blocked(self):
        h = handoff(); h.pop("source_snapshot")
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", h)["reason"], "MISSING_PROVENANCE")
    def test_unacknowledged_blocked(self):
        h = handoff(); h["ack_state"] = "HANDOFF_READY"
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", h)["reason"], "ACK_MISSING")
    def test_private_mercer_blocked(self):
        h = handoff(); h["mercer_derived"] = True
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", h)["reason"], "MERCER_FIREWALL_VIOLATION")
    def test_wrong_assignment_blocked(self):
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", handoff("OTHER"))["reason"], "CONTRACT_VIOLATION")
    def test_incomplete_dependencies_blocked(self):
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-003", handoff("CHAR-PORT-003"))["reason"], "MISSING_DEPENDENCY")
    def test_complete_task_not_rescheduled(self):
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-001", handoff("CHAR-PORT-001"))["reason"], "INVALID_STATE")
    def test_unknown_task_blocked(self):
        self.assertEqual(adapter.evaluate_assignment("UNKNOWN", handoff("UNKNOWN"))["reason"], "UNKNOWN_ASSIGNMENT")
    def test_benchmark_leakage_blocked(self):
        h = handoff(); h.update(benchmark_only=True, blank_canvas=True)
        self.assertEqual(adapter.evaluate_assignment("CHAR-PORT-002", h)["reason"], "BENCHMARK_LEAKAGE")

if __name__ == "__main__":
    unittest.main()
