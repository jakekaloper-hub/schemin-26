import copy
import importlib.util
import pathlib
import unittest

PATH = pathlib.Path(__file__).resolve().parents[1] / "matchup_delta.py"
spec = importlib.util.spec_from_file_location("matchup_delta", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def receipt():
    return {"meta": {"provider":"flaim","platform":"espn","league_id":1417621,
                     "season_year":2026,"week":12,"captured_at":"2026-11-25T14:00:00Z",
                     "authority":"PROVIDER_OBSERVATION_NOT_FACT_LOCK"},
            "matchups":[{"home":{"team_id":i,"points":0,"total_points":0},
                         "away":{"team_id":i+1,"points":0,"total_points":0},
                         "winner":"UNDECIDED"} for i in range(1,12,2)]}


def final(r, index, winner="HOME"):
    r["meta"]["captured_at"]="2026-11-26T22:00:00Z"
    row=r["matchups"][index]
    for side, points in (("home",100),("away",100 if winner=="TIE" else 90)):
        row[side].update(points=points,total_points=points)
    row["winner"]=winner


class DeltaTests(unittest.TestCase):
    def setUp(self):
        self.a=receipt()
        self.b=copy.deepcopy(self.a)
        self.deps={"approved-theme":[],"first-payoff":["W12-H01-A02"],
                   "second-payoff":["W12-H03-A04"],"scoreboard":["W12-H01-A02","W12-H03-A04"]}

    def test_noop_preserves_all(self):
        x=module.plan(self.a,self.b,self.deps)
        self.assertEqual(x["review_artifacts"],[])
        self.assertEqual(x["preserve_artifacts"],sorted(self.deps))

    def test_partial_final_preserves_unaffected_and_never_writes(self):
        final(self.b,0)
        saved=copy.deepcopy((self.a,self.b,self.deps))
        x=module.plan(self.a,self.b,self.deps)
        self.assertEqual(x["provider_final_count"],1)
        self.assertEqual(x["review_artifacts"],["first-payoff","scoreboard"])
        self.assertEqual(x["preserve_artifacts"],["approved-theme","second-payoff"])
        self.assertEqual(x["transitions"]["W12-H01-A02"],"PROVISIONAL_FINAL_BRANCH_REVIEW")
        self.assertFalse(any(x[k] for k in ("fact_lock","source_accepted","render_authorized","release_approved","writes_authoritative_files")))
        self.assertEqual((self.a,self.b,self.deps),saved)

    def test_second_final_and_replay(self):
        final(self.a,0)
        self.b=copy.deepcopy(self.a)
        final(self.b,1)
        self.b["meta"]["captured_at"]="2026-11-27T22:00:00Z"
        x=module.plan(self.a,self.b,self.deps)
        self.assertEqual(x["review_artifacts"],["scoreboard","second-payoff"])
        self.assertEqual(module.plan(self.b,self.b,self.deps)["changed_matchups"],[])

    def test_correction_requires_review(self):
        final(self.a,0)
        self.b=copy.deepcopy(self.a)
        self.b["meta"]["captured_at"]="2026-11-27T22:00:00Z"
        self.b["matchups"][0]["home"].update(points=101,total_points=101)
        self.assertEqual(module.plan(self.a,self.b,self.deps)["transitions"]["W12-H01-A02"],"REVIEW_PREVIOUS_FINAL_CHANGE")

    def test_tie_requires_review(self):
        final(self.b,0,"TIE")
        self.assertEqual(module.plan(self.a,self.b,self.deps)["transitions"]["W12-H01-A02"],"TIEBREAK_REVIEW_REQUIRED")

    def test_stale_conflicting_and_invalid(self):
        final(self.a,0)
        with self.assertRaises(ValueError): module.plan(self.a,self.b,self.deps)
        self.b=copy.deepcopy(self.a)
        self.b["matchups"][0]["home"].update(points=101,total_points=101)
        with self.assertRaises(ValueError): module.plan(self.a,self.b,self.deps)

    def test_unknown_dependency(self):
        with self.assertRaises(ValueError): module.plan(self.a,self.b,{"unknown":["W11-H01-A02"]})

    def test_wrong_scope_or_missing_fixture(self):
        self.b["meta"]["week"]=11
        with self.assertRaises(ValueError): module.plan(self.a,self.b,self.deps)
        self.b=copy.deepcopy(self.a)
        self.b["matchups"].pop()
        with self.assertRaises(ValueError): module.plan(self.a,self.b,self.deps)

if __name__=="__main__":
    unittest.main()
