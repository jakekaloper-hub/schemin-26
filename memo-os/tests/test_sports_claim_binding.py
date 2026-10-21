import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from produce_png_page import run
from verify_source_inputs import signature
class TestSportsClaimBinding(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.previous=os.environ.get("SCHEMIN_MEMO_INGEST_HMAC_KEY")
        self.key="synthetic-secret-only-0123456789abcdef"
        os.environ["SCHEMIN_MEMO_INGEST_HMAC_KEY"]=self.key
        source=self.root/"source.json";source.write_text('{"records":[{"id":"r1","matchup":"Home vs Away","status":"SCHEDULED"}]}')
        sha=hashlib.sha256(source.read_bytes()).hexdigest()
        Image.new("RGB",(1024,1536),"#253443").save(self.root/"background.png")
        spec={"format":"schemin-memo-editorial-v1","background":"background.png",
        "regions":[{"text":"TEST SPORTS DESK","x":50,"y":50,"width":800,"height":100}]}
        (self.root/"spec.json").write_text(json.dumps(spec))
        claim={"claim_id":"fixture-1","kind":"UPCOMING_MATCHUP","source_provider":"SYNTHETIC",
        "source_reference":"fixture:1","source_sha256":sha,"source_record_id":"r1","source_fields":{"status":"SCHEDULED"},"event_at":"2026-10-20T12:00:00-04:00",
        "retrieved_at":"2026-10-20T13:00:00-04:00","text":"A synthetic fact"}
        self.packet={"format":"schemin-memo-production-v1","production_kind":"SPORTS_DESK",
            "editorial_approval_reference":"fixture-approval",
            "page_spec":"spec.json","page_spec_sha256":hashlib.sha256((self.root/"spec.json").read_bytes()).hexdigest(),
            "sports":{"editorial_cutoff":"2026-10-21T12:00:00-04:00","claims":[claim]},
            "source_inputs":[{"path":"source.json","sha256":sha,"provider":"SYNTHETIC",
                "provider_receipt":"fixture-receipt","source_reference":"fixture:1",
                "ingest_attestation":signature(self.key,sha,"SYNTHETIC","fixture-receipt")}]}
    def tearDown(self):
        self.temp.cleanup()
        if self.previous is None:os.environ.pop("SCHEMIN_MEMO_INGEST_HMAC_KEY",None)
        else:os.environ["SCHEMIN_MEMO_INGEST_HMAC_KEY"]=self.previous
    def call(self):
        p=self.root/"packet.json";p.write_text(json.dumps(self.packet))
        return run(p,self.root/"candidate.png")
    def test_matching_attested_claim_yields_candidate(self):
        self.assertEqual("CANDIDATE_NOT_APPROVED",self.call()["status"])
    def test_unbound_claim_rejected(self):
        self.packet["sports"]["claims"][0]["source_reference"]="missing"
        self.assertIn("claim source not bound",str(self.call()["errors"]))
    def test_hash_mismatched_claim_rejected(self):
        self.packet["sports"]["claims"][0]["source_sha256"]="0"*64
        self.assertIn("claim source hash mismatch",str(self.call()["errors"]))
    def test_mismatched_claim_field_rejected(self):
        self.packet["sports"]["claims"][0]["source_fields"]["status"]="COMPLETED"
        self.assertIn("published source fields differ from evidence",str(self.call()["errors"]))
    def test_nonexistent_record_rejected(self):
        self.packet["sports"]["claims"][0]["source_record_id"]="missing"
        self.assertIn("source record missing or ambiguous",str(self.call()["errors"]))
    def test_missing_explicit_fields_rejected(self):
        self.packet["sports"]["claims"][0]["source_fields"]={}
        self.assertIn("explicit source fields required",str(self.call()["errors"]))
    def test_self_declared_source_without_valid_attestation_rejected(self):
        self.packet["source_inputs"][0]["ingest_attestation"]="0"*64
        self.assertIn("trusted ingestion attestation mismatch",str(self.call()["errors"]))
if __name__=="__main__":unittest.main()
