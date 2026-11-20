"""Static guardrails for the scheduled repository visibility publisher."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/repository-visibility.yml"


class WorkflowSafetyTests(unittest.TestCase):
    def test_no_direct_push_to_main(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("git push origin HEAD:main", text)
        self.assertNotIn("git push origin main", text)
        self.assertIn("gh pr create", text)
        self.assertIn("--draft", text)
        self.assertIn("pull-requests: write", text)

    def test_token_write_is_not_on_pull_request_job(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'", text)
        self.assertIn("contents: read", text)
        self.assertIn("needs: verify", text)
        self.assertIn("set -euo pipefail", text)


if __name__ == "__main__":
    unittest.main()
