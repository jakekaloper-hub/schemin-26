import importlib.util,tempfile,unittest
from pathlib import Path
from PIL import Image
import fitz
source=Path(__file__).resolve().parent/"validate_artifacts.py"
spec=importlib.util.spec_from_file_location("artifact_gate",source)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class TestPNGAssemblyParity(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for i,c in enumerate(("navy","maroon"),1):
            Image.new("RGB",(1024,1536),c).save(self.root/f"p{i}.png")
    def tearDown(self):self.temp.cleanup()
    def build(self,swap=False):
        doc=fitz.open()
        for i in ([2,1] if swap else [1,2]):
            page=doc.new_page(width=512,height=768)
            page.insert_image(page.rect,filename=str(self.root/f"p{i}.png"))
        path=self.root/"issue.pdf";doc.save(path);doc.close()
        return {"artifact_stage":"ISSUE_PACKAGE","pdf_path":"issue.pdf",
            "published_artifact_sha256":gate.sha256(path),"expected_pages":2,
            "pages":[{"slot":i,"status":"ACCEPTED","asset_path":f"p{i}.png",
            "asset_sha256":gate.sha256(self.root/f"p{i}.png")} for i in (1,2)]}
    def test_matches_accepted_png_order(self):
        self.assertEqual([],gate.inspect(self.build(),self.root/"manifest.json"))
    def test_rejects_swapped_pdf_pages(self):
        errors=gate.inspect(self.build(swap=True),self.root/"manifest.json")
        self.assertTrue(any("embedded pixels differ" in x for x in errors),errors)
    def test_rejects_wrong_master_content(self):
        m=self.build();Image.new("RGB",(1024,1536),"green").save(self.root/"p2.png")
        errors=gate.inspect(m,self.root/"manifest.json")
        self.assertTrue(any("embedded pixels differ" in x for x in errors),errors)
    def alter_pdf(self, mode):
        manifest=self.build()
        pdf=self.root/"issue.pdf"
        with fitz.open(pdf) as doc:
            if mode == "overlay":
                doc[0].draw_rect(fitz.Rect(30,30,150,150),color=(1,1,1),fill=(1,1,1))
            elif mode == "rotation":
                doc[0].set_rotation(90)
            elif mode == "crop":
                doc[0].set_cropbox(fitz.Rect(0,0,400,700))
            doc.saveIncr()
        manifest["published_artifact_sha256"]=gate.sha256(pdf)
        return manifest
    def test_visible_overlay_cannot_hide_behind_matching_embedded_master(self):
        self.assertIn("rendered pixels differ",str(gate.inspect(self.alter_pdf("overlay"),self.root/"manifest.json")))
    def test_rotation_changes_page_presentation(self):
        self.assertIn("page geometry",str(gate.inspect(self.alter_pdf("rotation"),self.root/"manifest.json")))
    def test_crop_changes_page_presentation(self):
        self.assertIn("page geometry",str(gate.inspect(self.alter_pdf("crop"),self.root/"manifest.json")))
if __name__=="__main__":unittest.main()
