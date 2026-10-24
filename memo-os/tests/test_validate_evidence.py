import copy,json,tempfile,unittest
from pathlib import Path
from validate_evidence import digest,validate_evidence
from PIL import Image

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
        games=[{"matchup_key":str(i),"home":"H"+str(i),"away":"A"+str(i),"final_scores":{"winner":"H"+str(i),"home":120+i,"away":110+i}} for i in range(6)]
        src=self.root/"source.json";src.write_text(json.dumps({"league_id":"1417621","week":5,"source":"FLAIM_ESPN","status":"FINAL","matchups":games}))
        for scope in ("character","atlas","visual","mobile"): Image.new("RGB",(390,700),(22,33,44)).save(self.root/(scope+".png"))
        sha="a"*64; pdf="b"*64
        receipts=[dict(scope=scope,reviewer_id="review-"+scope,reviewed_at="2026-10-14",decision="PASS",page_sha256=sha,pdf_sha256=pdf,
                       evidence_path=scope+".png",evidence_sha256=digest(self.root/(scope+".png")),reference_sha256="c"*64,
                       canonical_character_ids=["CHAR-A"],venue_id="LOC-A") for scope in ("character","atlas","visual","mobile")]
        self.d={"publication_state":"PUBLISHED","league_id":"1417621","week":5,"provider_receipt_path":"source.json","provider_receipt_sha256":digest(src),
                "results":{g["matchup_key"]:g["final_scores"] for g in games},
                "published_artifact_sha256":pdf,
                "pages":[{"slot":1,"asset_sha256":sha,"characters":["CHAR-A"],"review_receipts":receipts}],
                "umpire_receipt":{"reviewer_id":"independent-umpire","reviewed_at":"2026-10-14","decision":"PASS","pdf_sha256":pdf}}
    def test_valid(self): self.assertEqual(validate_evidence(self.d,self.root),[])
    def test_future_release_requires_founder_transaction(self):
        x=copy.deepcopy(self.d)
        x["season"]=2026
        x["week"]=6
        errors=validate_evidence(x,self.root)
        self.assertIn("Founder release transaction missing",errors)

    def test_future_release_rejects_missing_transaction_file(self):
        x=copy.deepcopy(self.d)
        x["season"]=2026
        x["week"]=6
        x["founder_release_state_path"]="not-found.json"
        errors=validate_evidence(x,self.root)
        self.assertIn("Founder release transaction inaccessible",errors)

    def test_future_release_rejects_tampered_transaction(self):
        x=copy.deepcopy(self.d)
        x["season"]=2026
        x["week"]=6
        x["founder_release_state_path"]="tampered.json"
        (self.root/"tampered.json").write_text(json.dumps({"payload":{"state":"RELEASED"},"signature":"forged"}))
        errors=validate_evidence(x,self.root)
        self.assertTrue(any("Founder transaction integrity" in e for e in errors))

    def test_wrong_provider_result(self):
        x=copy.deepcopy(self.d);x["results"]["0"]["home"]=999;self.assertTrue(validate_evidence(x,self.root))
    def test_missing_provider(self):
        x=copy.deepcopy(self.d);x.pop("provider_receipt_path");self.assertTrue(validate_evidence(x,self.root))
    def test_wrong_page_hash(self):
        x=copy.deepcopy(self.d);x["pages"][0]["asset_sha256"]="f"*64;self.assertTrue(validate_evidence(x,self.root))
    def test_missing_visual_receipt(self):
        x=copy.deepcopy(self.d);x["pages"][0]["review_receipts"]=[r for r in x["pages"][0]["review_receipts"] if r["scope"]!="visual"];self.assertTrue(validate_evidence(x,self.root))
    def test_tampered_evidence(self):
        (self.root/"atlas.png").write_text("tampered");self.assertTrue(validate_evidence(self.d,self.root))
    def test_umpire_not_independent(self):
        x=copy.deepcopy(self.d);x["umpire_receipt"]["reviewer_id"]="review-visual";self.assertTrue(validate_evidence(x,self.root))
    def test_invalid_atlas_venue(self):
        x=copy.deepcopy(self.d);x["pages"][0]["review_receipts"][1].pop("venue_id");self.assertTrue(validate_evidence(x,self.root))
if __name__=="__main__":unittest.main()
