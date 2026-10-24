import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
import fitz
TOOLS=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(TOOLS))
from produce_png_page import run
import importlib.util
path=Path(__file__).resolve().parent/"validate_artifacts.py"
spec=importlib.util.spec_from_file_location("artifact_gate_multifolio",path)
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class MultiPageCandidateRegression(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.outputs=[]
        for n,copy in [(1,"WEEK 7 EDITORIAL — VERIFIED FIXTURE"),(2,"SECOND PAGE — FOLLOW-UP FIXTURE")]:
            Image.new("RGB",(1024,1536),(30*n,40,80)).save(self.root/f"background{n}.png")
            src={"format":"schemin-memo-editorial-v1","background":f"background{n}.png",
                "regions":[{"text":copy,"x":40,"y":50,"width":930,"height":150,"font_size":28}]}
            sp=self.root/f"spec{n}.json";sp.write_text(json.dumps(src))
            pkt={"format":"schemin-memo-production-v1","production_kind":"FACTUAL_EDITORIAL",
                 "editorial_approval_reference":f"synthetic-copy-lock-{n}",
                 "page_spec":sp.name,"page_spec_sha256":hashlib.sha256(sp.read_bytes()).hexdigest()}
            pp=self.root/f"packet{n}.json";pp.write_text(json.dumps(pkt))
            output=self.root/f"page{n}.png"
            verdict=run(pp,output)
            self.assertEqual(verdict["status"],"CANDIDATE_NOT_APPROVED")
            self.outputs.append(output)
    def tearDown(self):self.tmp.cleanup()
    def manifest(self,swap=False):
        pdf=self.root/"issue.pdf";doc=fitz.open()
        for path in (self.outputs[::-1] if swap else self.outputs):
            pg=doc.new_page(width=512,height=768);pg.insert_image(pg.rect,filename=str(path))
        doc.save(pdf);doc.close()
        return {"artifact_stage":"ISSUE_PACKAGE","pdf_path":pdf.name,
                "published_artifact_sha256":gate.sha256(pdf),"expected_pages":2,
                "pages":[{"slot":i,"status":"ACCEPTED","asset_path":p.name,
                          "asset_sha256":gate.sha256(p)} for i,p in enumerate(self.outputs,1)]}
    def test_two_produced_pngs_assemble_in_order(self):
        self.assertEqual([],gate.inspect(self.manifest(),self.root/"manifest.json"))
    def test_swapped_produced_pngs_rejected(self):
        self.assertIn("embedded pixels differ",str(gate.inspect(self.manifest(swap=True),self.root/"manifest.json")))
    def test_candidate_pages_do_not_auto_qualify_for_assembly(self):
        m=self.manifest()
        for p in m["pages"]:p["status"]="CANDIDATE"
        self.assertIn("requires accepted PNG masters",str(gate.inspect(m,self.root/"manifest.json")))
if __name__=="__main__":unittest.main()
