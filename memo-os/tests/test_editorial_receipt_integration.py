import importlib.util,hashlib,json,tempfile,unittest
from pathlib import Path
from PIL import Image
import fitz
path=Path(__file__).resolve().parent/"validate_artifacts.py"
spec=importlib.util.spec_from_file_location("validate_artifacts",path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestEditorialReceiptIntegration(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
        Image.new("RGB",(1024,1536),"navy").save(self.root/"art.png")
        (self.root/"spec.json").write_text('{"format":"example"}')
        doc=fitz.open();doc.new_page(width=512,height=768)
        doc.save(self.root/"issue.pdf");doc.close()
        self.receipt={"status":"CANDIDATE_NOT_APPROVED","visual_text_independently_verified":False,
            "spec_sha256":m.sha256(self.root/"spec.json"),"output_sha256":m.sha256(self.root/"art.png")}
        self.manifest={"pdf_path":"issue.pdf","published_artifact_sha256":m.sha256(self.root/"issue.pdf"),
           "expected_pages":1,"pages":[{"slot":1,"asset_path":"art.png","asset_sha256":m.sha256(self.root/"art.png"),
                    "editorial_spec_path":"spec.json","editorial_receipt_path":"receipt.json"}]}
    def tearDown(self):self.t.cleanup()
    def check(self):
        (self.root/"receipt.json").write_text(json.dumps(self.receipt))
        return str(m.inspect(self.manifest,self.root/"manifest.json"))
    def test_matching_receipt_passes(self):self.assertEqual(self.check(),"[]")
    def test_output_tamper_fails(self):
        self.receipt["output_sha256"]="0"*64
        self.assertIn("editorial output hash mismatch",self.check())
    def test_source_tamper_fails(self):
        self.receipt["spec_sha256"]="0"*64
        self.assertIn("editorial source spec hash mismatch",self.check())
    def test_self_approval_rejected(self):
        self.receipt["visual_text_independently_verified"]=True
        self.assertIn("invalid compositor acceptance claim",self.check())
if __name__=="__main__":unittest.main()
