import importlib.util,json,tempfile,unittest,hashlib
from pathlib import Path
from PIL import Image
import fitz
p=Path(__file__).resolve().parent/"validate_artifacts.py"
spec=importlib.util.spec_from_file_location("artifact_check",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestPNGFirst(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
        for i in (1,2):Image.new("RGB",(1024,1536),("navy" if i==1 else "maroon")).save(self.root/f"{i}.png")
        self.pages=[{"slot":i,"status":"ACCEPTED","asset_path":f"{i}.png","asset_sha256":m.sha256(self.root/f"{i}.png")} for i in (1,2)]
    def tearDown(self):self.t.cleanup()
    def check(self,manifest):
        return str(m.inspect(manifest,self.root/"manifest.json"))
    def test_png_only_production_passes(self):
        self.assertEqual("[]",self.check({"artifact_stage":"PAGE_PRODUCTION","expected_pages":1,"pages":[self.pages[0]]}))
    def test_page_production_rejects_pdf(self):
        self.assertIn("cannot claim PDF",self.check({"artifact_stage":"PAGE_PRODUCTION","pdf_path":"one.pdf","expected_pages":1,"pages":[self.pages[0]]}))
    def test_single_page_pdf_not_full_issue(self):
        d=fitz.open();d.new_page();d.save(self.root/"one.pdf");d.close()
        x={"artifact_stage":"ISSUE_PACKAGE","pdf_path":"one.pdf","published_artifact_sha256":m.sha256(self.root/"one.pdf"),"expected_pages":1,"pages":[self.pages[0]]}
        self.assertIn("requires multiple",self.check(x))
    def test_unaccepted_png_blocks_pdf_issue(self):
        d=fitz.open();d.new_page();d.new_page();d.save(self.root/"two.pdf");d.close()
        self.pages[1]["status"]="REVIEWED"
        x={"artifact_stage":"ISSUE_PACKAGE","pdf_path":"two.pdf","published_artifact_sha256":m.sha256(self.root/"two.pdf"),"expected_pages":2,"pages":self.pages}
        self.assertIn("requires accepted",self.check(x))
if __name__=="__main__":unittest.main()
