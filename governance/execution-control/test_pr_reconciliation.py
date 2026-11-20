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

    def test_branch_pagination(self):
        calls = []
        def load(url):
            calls.append(url)
            return [{"name": str(i)} for i in range(100)] if len(calls) == 1 else [{"name": "last"}]
        self.assertEqual(len(m.fetch_branches(load)), 101)
        self.assertIn("page=2", calls[-1])

    def test_open_pr_heads_and_stacked_bases_are_tracked(self):
        prs = [
            {"number": 1, "title": "parent", "html_url": "https://github.com/test/1",
             "state": "open", "head": {"ref": "feature"}, "base": {"ref": "main"}},
            {"number": 2, "title": "child", "html_url": "https://github.com/test/2",
             "state": "open", "head": {"ref": "child"}, "base": {"ref": "feature"}},
        ]
        branches = [{"name": x} for x in ("main", "feature", "child", "old-branch")]
        vis = m.collect(prs, branches=branches)["branch_visibility"]
        self.assertTrue(vis["checked"])
        self.assertEqual(vis["branch_count"], 4)
        self.assertEqual(vis["without_open_pr_head_or_base"], ["old-branch"])
        self.assertEqual(vis["without_open_pr_head_or_base_count"], 1)

    def test_missing_branch_inventory_fails_visible(self):
        vis = m.collect([], branches=None)["branch_visibility"]
        self.assertFalse(vis["checked"])
        self.assertIsNone(vis["without_open_pr_head_or_base_count"])

if __name__=="__main__":
    unittest.main()
