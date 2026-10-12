#!/usr/bin/env python3
"""Regression fixtures for Week 5 preliminary V5.5 packet crosswalk."""
import copy
import unittest
from week5_preflight import check_issue

def page(n, family, match=None):
    return {"id": f"W5-P{n:02d}", "family":family, "matchup_id":match,
            "narrative_job":"regression test", "copy_budget":100,
            "world_anchor":"LOC-TEST", "text_safe_zone":"left",
            "source_refs":["TEST_FIXTURE"]}

def example():
    return {"week":5,"result_state":"PROVISIONAL",
            "pages":[page(1,"cover")]+[page(i+2,"overture",i+1) for i in range(6)]+[page(8,"matchup")]}

class PreflightRegressions(unittest.TestCase):
    def assert_reject(self, mutate, token):
        obj=example()
        mutate(obj)
        errors=check_issue(obj)
        self.assertTrue(any(token in e for e in errors),errors)

    def test_valid_candidate(self):
        self.assertEqual(check_issue(example()),[])

    def test_wrong_week(self):
        self.assert_reject(lambda d:d.update(week=4),"wrong_week")

    def test_duplicate_ids(self):
        self.assert_reject(lambda d:d["pages"].append(copy.deepcopy(d["pages"][0])),"duplicate_ids")

    def test_missing_overture(self):
        self.assert_reject(lambda d:d["pages"].pop(1),"six_distinct_overtures_required")

    def test_premature_winner(self):
        self.assert_reject(lambda d:d["pages"][1].update(winner_pov="Duckhook"),"premature_winner_pov")

    def test_character_mount_missing(self):
        self.assert_reject(lambda d:d["pages"][0].update(characters=["DK"]),"missing_character_mount_receipt")

    def test_generated_data(self):
        self.assert_reject(lambda d:d["pages"][0].update(has_exact_data=True),"untrusted_generated_data")

    def test_superseded_story(self):
        self.assert_reject(lambda d:d["pages"][0].update(story="Outlaw & Sheriff"),"superseded_story_premise")

    def test_approved_without_qa(self):
        self.assert_reject(lambda d:d["pages"][0].update(status="APPROVED"),"approved_without_qa")

    def test_missing_source_refs(self):
        self.assert_reject(lambda d:d["pages"][0].pop("source_refs"),"missing_source_refs")

if __name__=="__main__":
    unittest.main()
