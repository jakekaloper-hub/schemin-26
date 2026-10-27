import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("inklings_workshop", ROOT / "inklings_workshop.py")
workshop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workshop)

REGISTRY = {"author_council": {"core_eight": ["cs_lewis", "jrr_tolkien"]}}
BENCH = {"profiles": [{"name": "Frank Masi"}]}
SHA = "a" * 64

def packet():
    return {
        "assignment_id": "pilot-novel-1", "production": "novel-os",
        "evidence_sha": SHA, "decision_question": "What changes?",
        "synthesis": "One revised causal story spine.",
        "findings": [
            {"id": "f1", "advisor": "cs_lewis", "observation": "Weak moral stakes",
             "source_anchor": "chapter:4", "proposal": "Make the sacrifice costly",
             "decision": "ADAPT", "rationale": "Character agency"},
            {"id": "f2", "advisor": "Frank Masi", "observation": "Unclear silhouette",
             "source_anchor": "scene:2", "proposal": "Change camera position",
             "decision": "HOLD", "rationale": "Location continuity pending"}
        ],
    }

class InklingsWorkshopTests(unittest.TestCase):
    def test_candidate_and_dissent(self):
        result = workshop.reconcile(packet(), REGISTRY, BENCH)
        self.assertEqual(result["status"], "CANDIDATE_PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(len(result["accepted"]), 1)
        self.assertEqual(len(result["dissent"]), 1)
        self.assertFalse(result["canon_promoted"])
    def test_memo_supported(self):
        p = packet(); p["production"] = "memo-os"
        self.assertEqual(workshop.reconcile(p, REGISTRY, BENCH)["production"], "memo-os")
    def test_unregistered_advisor_rejected(self):
        p = packet(); p["findings"][0]["advisor"] = "unknown"
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)
    def test_missing_source_hash_rejected(self):
        p = packet(); p["evidence_sha"] = ""
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)
    def test_no_synthesis_rejected(self):
        p = packet(); p["synthesis"] = ""
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)
    def test_no_accepted_direction_rejected(self):
        p = packet(); p["findings"][0]["decision"] = "REJECT"
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)
    def test_duplicate_id_rejected(self):
        p = packet(); p["findings"][1]["id"] = "f1"
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)
    def test_per_advisor_cap(self):
        p = packet()
        p["findings"] = [dict(p["findings"][0], id=f"f{i}") for i in range(4)]
        with self.assertRaises(workshop.WorkshopError):
            workshop.reconcile(p, REGISTRY, BENCH)

if __name__ == "__main__":
    unittest.main()
