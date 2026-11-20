"""Repository inventory regression tests."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("visibility", Path(__file__).with_name("visibility.py"))
visibility = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visibility)
REPO = "jakekaloper-hub/schemin-26"


def pr(number, head, state="open", draft=True, base="main", merged=None):
    return {"number": number, "state": state, "draft": draft, "merged_at": merged,
            "title": "candidate | review",
            "html_url": f"https://github.com/{REPO}/pull/{number}",
            "updated_at": "2026-11-20T18:00:00Z",
            "head": {"ref": head, "repo": {"full_name": REPO}},
            "base": {"ref": base}}


class VisibilityTests(unittest.TestCase):
    def test_discloses_stacked_and_untracked(self):
        branches = [{"name": "main", "commit": {"sha": "abc"}},
                    {"name": "feat/a"}, {"name": "feat/b"}]
        report = visibility.snapshot(branches, [pr(1, "feat/a", base="story")],
                                     REPO, "2026-11-20", False)
        self.assertIn("3 branches including main", report)
        self.assertIn("1 stacked PRs", report)
        self.assertIn("1 non-main branches without", report)
        self.assertIn("NEEDS TRIAGE", report)
        self.assertIn("UNPROTECTED", report)
        self.assertIn("candidate / review", report)

    def test_merged_branch_not_untracked(self):
        branches = [{"name": "main"}, {"name": "old-branch"}]
        report = visibility.snapshot(branches, [pr(2, "old-branch", state="closed",
                                                  merged="2026-11-01")],
                                     REPO, "2026-11-20", True)
        self.assertIn("MERGED", report)
        self.assertIn("0 non-main branches without", report)
        self.assertIn("PROTECTED", report)

    def test_open_pr_preferred_over_closed(self):
        report = visibility.snapshot([{"name": "main"}, {"name": "same"}],
                                     [pr(1, "same", state="closed"), pr(3, "same")],
                                     REPO, "2026-11-20")
        self.assertIn("[#3](https://github.com", report)
        self.assertNotIn("NEEDS TRIAGE", report)

    def test_fork_does_not_claim_local_branch(self):
        p = pr(4, "local")
        p["head"]["repo"]["full_name"] = "other/remote"
        report = visibility.snapshot([{"name": "main"}, {"name": "local"}],
                                     [p], REPO, "2026-11-20")
        self.assertIn("1 non-main branches without", report)


if __name__ == "__main__":
    unittest.main()
