import copy,unittest
from validate_issue import validate
def good():
    return {"expected_pages":1,"publication_state":"REVIEW","results":{"A-B":{"winner":"A","A":10,"B":8}},"team_divisions":{"A":"Pizza"},"division_highlight":{"name":"Pizza","wins":1},
      "pages":[{"slot":1,"printed_page":1,"asset_sha256":"a"*64,"role":"RESULT","matchup_key":"A-B","final_scores":{"winner":"A","A":10,"B":8},"characters":["A"],"character_raster_qa":"PASS","mobile_qa":"PASS","technical_acceptance":"PASS","publication_fidelity":"PASS","narrative_job":"consequence"}]}
class Gate(unittest.TestCase):
    def test_valid(self): self.assertEqual(validate(good()),[])
    def test_wrong_score(self):
        d=good();d["pages"][0]["final_scores"]["A"]=11;self.assertTrue(validate(d))
    def test_bad_printed_number(self):
        d=good();d["pages"][0]["printed_page"]=17;self.assertTrue(validate(d))
    def test_missing_page(self):
        d=good();d["expected_pages"]=2;self.assertTrue(validate(d))
    def test_duplicate_art(self):
        d=good();d["expected_pages"]=2;p=copy.deepcopy(d["pages"][0]);p.update(slot=2,printed_page=2);d["pages"].append(p);self.assertTrue(validate(d))
    def test_missing_canon_qa(self):
        d=good();d["pages"][0]["character_raster_qa"]="HOLD";self.assertTrue(validate(d))
    def test_setup_repeats_result(self):
        d=good();d["pages"][0]["role"]="SETUP";self.assertTrue(validate(d))
    def test_release_without_umpire(self):
        d=good();d["publication_state"]="PUBLISHED";self.assertTrue(validate(d))
    def test_false_division_winner(self):
        d=good();d["division_highlight"]["name"]="Wings";self.assertTrue(validate(d))
    def test_mobile_hold(self):
        d=good();d["pages"][0]["mobile_qa"]="HOLD";self.assertTrue(validate(d))
    def test_invalid_sha(self):
        d=good();d["pages"][0]["asset_sha256"]="z"*64;self.assertTrue(validate(d))
    def test_invalid_release_sha(self):
        d=good();d.update(publication_state="PUBLISHED",pdf_page_count=1,independent_umpire_approval="PASS",published_artifact_sha256="faked");self.assertTrue(validate(d))
    def test_unknown_role(self):
        d=good();d["pages"][0]["role"]="SCOREBOARD_RESULT_TBD";self.assertTrue(validate(d))
    def test_unknown_release_state(self):
        d=good();d["publication_state"]="FINISHED";self.assertTrue(validate(d))
    def test_false_sole_division_on_tie(self):
        d=good();d["results"]["C-D"]={"winner":"C","C":12,"D":9};d["team_divisions"]["C"]="Wings";self.assertTrue(validate(d))
if __name__=="__main__":unittest.main()
