import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "causal_chapter_architecture_v1.json"
WEEK3 = ROOT.parents[1] / "chronicles" / "week-03" / "WEEK_3_AUTHOR_COUNCIL_CAUSAL_ARCHITECTURE_PATCH_V1.md"

class CausalChapterArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT.read_text())

    def test_source_week_is_not_chapter(self):
        self.assertFalse(self.contract["source_week_is_chapter"])

    def test_equal_matchup_coverage_not_required(self):
        self.assertFalse(self.contract["equal_matchup_coverage_required"])

    def test_prose_does_not_require_full_numeric_foreground(self):
        self.assertTrue(self.contract["full_numeric_truth_required_in_evidence"])
        self.assertFalse(self.contract["full_numeric_truth_required_in_prose"])

    def test_chapter_requires_causal_and_omission_fields(self):
        required=set(self.contract["requires"])
        for field in {
            "dramatic_question","causal_spine","pov_packets","location_packets",
            "closing_consequence","open_loop_inputs","open_loop_outputs",
            "omitted_event_ledger","temporal_cutoff"
        }:
            self.assertIn(field, required)

    def test_closed_manuscripts_require_reopen(self):
        targets=set(self.contract["hard_canon_reopen_required_for"])
        self.assertEqual(targets,{
            "PROLOGUE_DRAFT_V1",
            "CHAPTER_01_THE_FIRST_ANSWER",
            "CHAPTER_02_WHAT_COMES_BACK"
        })

    def test_week3_patch_breaks_six_matchups_equals_six_scenes(self):
        text=WEEK3.read_text()
        self.assertIn("A matchup evidence packet is **not** automatically a scene.",text)
        self.assertIn("Week 3 is **not** automatically Chapter III.",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
