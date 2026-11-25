import copy
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("execution_adapter", ROOT / "memo-os/collaboration/execution_adapter.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

def observation():
    return {"meta":{"provider":"flaim","platform":"espn","league_id":1417621,"season_year":2026,"week":12,"captured_at":"2026-11-25T14:00:00Z","authority":"PROVIDER_OBSERVATION_NOT_FACT_LOCK"},
            "matchups":[{"home":{"team_id":i,"points":0,"total_points":0},"away":{"team_id":i+1,"points":0,"total_points":0},"winner":"UNDECIDED"} for i in range(1,12,2)]}

class ProvisionalReviewTests(unittest.TestCase):
    def test_partial_final_preserves_unrelated_and_cannot_apply(self):
        a=observation()
        b=copy.deepcopy(a)
        b["meta"]["captured_at"]="2026-11-26T23:00:00Z"
        row=b["matchups"][0]
        row["home"].update(points=100,total_points=100)
        row["away"].update(points=90,total_points=90)
        row["winner"]="HOME"
        deps={"theme":[],"story-a":["W12-H01-A02"],"story-b":["W12-H03-A04"]}
        before=copy.deepcopy((a,b,deps))
        result=adapter.plan_provisional_matchup_review(a,b,deps)
        self.assertEqual(result["status"],"PROVISIONAL_REVIEW_ONLY")
        self.assertEqual(result["affected"],["story-a"])
        self.assertEqual(result["preserved"],["story-b","theme"])
        self.assertFalse(result["application_authorized"])
        self.assertFalse(result["steward_acknowledged"])
        self.assertFalse(result["delta"]["fact_lock"])
        self.assertEqual((a,b,deps),before)

    def test_noop(self):
        a=observation()
        result=adapter.plan_provisional_matchup_review(a,a,{"theme":[]})
        self.assertEqual(result["affected"],[])
        self.assertEqual(result["preserved"],["theme"])

    def test_bad_input_blocks(self):
        a=observation()
        self.assertEqual(adapter.plan_provisional_matchup_review(a,{},{} )["status"],"BLOCKED")

if __name__=="__main__":
    unittest.main()
