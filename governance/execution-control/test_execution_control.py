import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[2]
MODULE=ROOT/"governance"/"execution-control"/"validate_execution_control.py"
spec=importlib.util.spec_from_file_location("ec",MODULE)
ec=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)

class ExecutionControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=ec.load_registry()
        cls.index={t["task_id"]:t for t in cls.data["tasks"]}

    def test_registry_validates(self):
        self.assertEqual(ec.validate_registry(self.data),[])

    def test_character_portability_resolves_existing_work(self):
        hit=ec.resolve("Where are we with character portability?",self.data)
        self.assertEqual(hit["task_id"],"CHAR-PORT-002")
        self.assertEqual(hit["status"],self.index["CHAR-PORT-002"]["status"])
        self.assertEqual(self.index["CHAR-PORT-001"]["status"],"COMPLETE")
        self.assertTrue(self.index["CHAR-PORT-001"]["evidence"])

    def test_week4_resume_finds_live_evidence_gate_not_new_plan(self):
        hit=ec.resolve("Continue Week 4 Memo.",self.data)
        self.assertEqual(hit["task_id"],"MEMO-W4-002")
        self.assertEqual(hit["status"],self.index["MEMO-W4-002"]["status"])
        self.assertIn("MEMO-W4-002",self.index["MEMO-W4-003"]["dependencies"])

    def test_week6_preproduction_preserves_final_result_gate(self):
        task=self.index["MEMO-W6-001"]
        self.assertTrue(task["acceptance_criteria"])
        self.assertIn("week-6/",task["source_authority"])
        self.assertTrue((ROOT / task["source_authority"]).exists())
        intake=(ROOT / task["source_authority"]).read_text()
        self.assertIn("UNDECIDED",intake)
        self.assertIn("not facts or locked creative outcomes",intake)
        if task["status"]=="COMPLETE":
            self.assertTrue(any(e.get("status")=="PASS" for e in task["evidence"]))

    def test_novel_distinguishes_closed_canon_from_future_work(self):
        self.assertEqual(self.index["NOVEL-NEXT-001"]["status"],"COMPLETE")
        self.assertEqual(self.index["NOVEL-NEXT-002"]["status"],"NOT_STARTED")
        self.assertIn("MEMO-W4-002",self.index["NOVEL-NEXT-002"]["dependencies"])
        self.assertEqual(self.index["NOVEL-NEXT-003"]["status"],"NOT_STARTED")

    def test_bullpen_next_returns_executable_task(self):
        nxt=ec.select_next(self.data)
        self.assertIsNotNone(nxt)
        self.assertIn(nxt["task_id"],self.index)
        self.assertIn(nxt["status"],{"READY","NOT_STARTED","REOPENED","IN_PROGRESS","VERIFYING"})
        self.assertTrue(ec.dependency_complete(nxt,self.index))

    def test_complete_tasks_are_evidence_backed(self):
        for task in self.data["tasks"]:
            if task["status"]=="COMPLETE":
                self.assertTrue(task["acceptance_criteria"],task["task_id"])
                self.assertTrue(any(e.get("status")=="PASS" for e in task["evidence"]),task["task_id"])

    def test_rollup_is_derived(self):
        result=ec.rollup(self.data,"Schemin '26 Living Novel")
        self.assertEqual(result["total"],3)
        self.assertEqual(result["complete"],1)
        self.assertEqual(result["completion_pct"],33.3)

    def test_clean_context_retrieval_is_deterministic(self):
        first=ec.select_next(ec.load_registry())
        second=ec.select_next(ec.load_registry())
        self.assertEqual(first["task_id"],second["task_id"])

if __name__=="__main__":
    unittest.main()
