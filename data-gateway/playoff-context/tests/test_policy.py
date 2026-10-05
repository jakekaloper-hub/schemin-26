import unittest
from playoff_context import classify_candidates, validate_wording, require_final_week

class TestPolicy(unittest.TestCase):
    def test_false_certainty_block(self):
        p={"A":{"playoff_probability":1.0}}
        e={"A":{"status":"ALIVE","class":"EXACT","proof":"not_eliminated_by_bounds"}}
        self.assertEqual(classify_candidates(p,e),[])
    def test_exact_candidate(self):
        c=classify_candidates({},{"A":{"status":"CLINCHED","class":"EXACT","proof":"win_bounds"}})
        self.assertEqual(c[0]["kind"],"CLINCHED")
        validate_wording(c[0],"EXACT")
        with self.assertRaises(ValueError): validate_wording(c[0],"PROBABILISTIC")
    def test_result_lock(self):
        with self.assertRaises(RuntimeError): require_final_week({"matchups":[{"winner":"UNDECIDED"}]})
        require_final_week({"matchups":[{"winner":"HOME"}]})

if __name__=="__main__": unittest.main()
