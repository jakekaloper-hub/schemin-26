import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class Week4CrossOsSyncTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text()

    def test_live_memo_snapshot_is_not_prekickoff(self):
        text = self.read("memo-os/week-4/WEEK_4_STORY_ROOM_CURRENT_STATE_RECONCILIATION_2026-10-02.md")
        self.assertIn("D0nkey K0ng 17.5 — ObiWan Jacoby 0.0", text)
        self.assertIn("Slob on my Dobb 21.8 — The Chili Cheesers 7.1", text)
        self.assertIn("all six matchups remain provider-`UNDECIDED`", text)

    def test_novel_consumes_same_live_snapshot_without_chapter_promotion(self):
        text = self.read("living-novel/weekly-ledger/2026_WEEK_04_LIVE_EVIDENCE_AND_SIGNIFICANCE.md")
        self.assertIn("D0nkey K0ng 17.5 — ObiWan Jacoby 0.0", text)
        self.assertIn("cannot assign Chapter IV", text)

    def test_world_state_remains_end_of_week_3(self):
        state = json.loads(self.read("world/data/current_world_state.json"))
        self.assertEqual(state["as_of"], "end_of_week_3_2026")

    def test_cross_os_receipt_forbids_world_apply(self):
        text = self.read("world/atlas/integration/WEEK_4_CROSS_OS_LIVE_SYNC_RECEIPT_2026-10-02.md")
        self.assertIn("NO WORLD APPLY", text)
        self.assertIn("ATLAS-XOS-007` remains OPEN", text)

if __name__ == "__main__":
    unittest.main()
