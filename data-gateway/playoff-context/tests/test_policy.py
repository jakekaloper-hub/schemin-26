import unittest
from playoff_context import classify_candidates, validate_wording, require_final_week

class TestPolicy(unittest.TestCase):
    def test_false_certainty_block(self):
        p={"A":{"playoff_probability":1.0}}
        e={"A":{"status":"UNKNOWN","class":"UNRESOLVED","proof":None}}
        self.assertEqual(classify_candidates(p,e),[])
    def test_exact_candidate(self):
        c=classify_candidates({},{"A":{"status":"CLINCHED","class":"EXACT","proof":"win_bounds"}})
        self.assertEqual(c[0]["kind"],"CLINCHED")
        validate_wording(c[0],"EXACT")
        with self.assertRaises(ValueError): validate_wording(c[0],"PROBABILISTIC")
    def test_result_lock(self):
        with self.assertRaises(RuntimeError): require_final_week({"matchups":[{"winner":"UNDECIDED"}]})
        require_final_week({"week":3,"matchups":[{
            "winner":"HOME", "home":{"teamId":"A","totalPoints":110},
            "away":{"teamId":"B","totalPoints":100},
        }]}, expected_team_ids=["A","B"], expected_week=3)
    def test_same_priority_candidates_follow_material_effect(self):
        leverage={tid:{'leverage_delta_pp':delta,'conditional_win_probability':.8,
                       'conditional_loss_probability':.8-delta/100}
                  for tid,delta in [('small',26),('largest',39),('middle',35)]}
        c=classify_candidates({}, {}, leverage, max_notes=2)
        self.assertEqual([v['team_id'] for v in c], ['largest','middle'])
    def test_nonexact_status_cannot_self_promote(self):
        self.assertEqual(classify_candidates({}, {'A':{'status':'CLINCHED','class':'PROBABILISTIC'}}), [])

if __name__=="__main__": unittest.main()
