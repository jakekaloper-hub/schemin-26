import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).with_name("pr_reconciliation.py")
spec = importlib.util.spec_from_file_location("pr_reconciliation", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PRReconciliationTests(unittest.TestCase):
    def test_merge_evidence_precedes_body(self):
        self.assertEqual(m.classify({"merged_at":"2026-10-22T10:00:00Z","state":"closed","body":"superseded by"}),"MERGED")

    def test_claim_is_not_proof(self):
        self.assertEqual(m.classify({"merged_at":None,"state":"closed","body":"Superseded by PR #233"}),"CLOSED_REPLACEMENT_CLAIM_UNVERIFIED")

    def test_open_stays_unverified(self):
        self.assertEqual(m.classify({"merged_at":None,"state":"open","body":"completed"}),"OPEN_UNVERIFIED")

    def test_pagination(self):
        calls=[]
        def load(url):
            calls.append(url)
            return [{"number":i} for i in range(100)] if len(calls)==1 else [{"number":100}]
        self.assertEqual(len(m.fetch_pulls(load)),101)
        self.assertEqual(len(calls),2)

    def test_closed_no_claim(self):
        self.assertEqual(m.classify({"merged_at":None,"state":"closed","body":"failed"}),"CLOSED_UNMERGED_DISPOSITION_UNVERIFIED")

if __name__=="__main__":
    unittest.main()
