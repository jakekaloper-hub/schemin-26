import hashlib,json,tempfile,unittest,sys,os
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from verify_source_inputs import verify_sources,signature
from produce_png_page import run
class TestSourceAndTelemetry(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/"evidence.json").write_text('{"completed":true}')
        self.key="test-fixture-only-secret-0123456789abcdef"
        self._previous=os.environ.get("SCHEMIN_MEMO_INGEST_HMAC_KEY")
        os.environ["SCHEMIN_MEMO_INGEST_HMAC_KEY"]=self.key
        self.input={"source_inputs":[{"path":"evidence.json",
            "sha256":hashlib.sha256((self.root/"evidence.json").read_bytes()).hexdigest(),
            "provider":"TEST_FIXTURE","provider_receipt":"provider-auth-fixture"}]}
        x=self.input["source_inputs"][0]
        x["ingest_attestation"]=signature(self.key,x["sha256"],x["provider"],x["provider_receipt"])
        self.packet=self.root/"packet.json"
    def tearDown(self):
        self.tmp.cleanup()
        if self._previous is None:os.environ.pop("SCHEMIN_MEMO_INGEST_HMAC_KEY",None)
        else:os.environ["SCHEMIN_MEMO_INGEST_HMAC_KEY"]=self._previous
    def test_bound_source_snapshot(self):
        self.assertEqual([],verify_sources(self.input,self.packet))
    def test_source_tamper_blocked(self):
        self.input["source_inputs"][0]["sha256"]="0"*64
        self.assertIn("evidence hash mismatch",str(verify_sources(self.input,self.packet)))
    def test_unverified_source_blocked(self):
        self.input["source_inputs"][0]["ingest_attestation"]="f"*64
        self.assertIn("trusted ingestion attestation mismatch",str(verify_sources(self.input,self.packet)))
    def test_source_path_traversal_blocked(self):
        self.input["source_inputs"][0]["path"]="../bad.txt"
        self.assertIn("inaccessible evidence",str(verify_sources(self.input,self.packet)))
    def test_missing_key_blocks_self_verification(self):
        os.environ.pop("SCHEMIN_MEMO_INGEST_HMAC_KEY",None)
        self.assertIn("verification key unavailable",str(verify_sources(self.input,self.packet)))
    def test_missing_live_source_blocked(self):
        self.assertIn("live source inputs required",str(verify_sources({"requires_live_sources":True},self.packet)))
    def test_blocked_attempt_persists_receipt(self):
        self.packet.write_text(json.dumps({"format":"schemin-memo-production-v1","production_kind":"SPORTS_DESK"}))
        result=run(self.packet,self.root/"render.png")
        self.assertEqual("BLOCKED",result["status"])
        self.assertFalse(result["render_invoked"])
        self.assertTrue((self.root/"render.production.json").is_file())
        self.assertFalse((self.root/"render.png").exists())
if __name__=="__main__":unittest.main()
