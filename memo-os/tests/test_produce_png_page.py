import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from PIL import Image
path=Path(__file__).resolve().parents[1]/"tools"
import sys
sys.path.insert(0,str(path))
import produce_png_page as p
class TestProductionEntry(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        Image.new("RGB",(1024,1536),"#253443").save(self.root/"background.png")
        spec={"format":"schemin-memo-editorial-v1","background":"background.png","regions":[
          {"text":"WEEK 7 — VERIFIED SOURCE FIXTURE","x":60,"y":60,"width":900,"height":90,"font_size":30}]}
        (self.root/"spec.json").write_text(json.dumps(spec))
        self.packet={"format":"schemin-memo-production-v1","production_kind":"FACTUAL_EDITORIAL",
          "page_spec":"spec.json","page_spec_sha256":hashlib.sha256((self.root/"spec.json").read_bytes()).hexdigest(),
          "editorial_approval_reference":"editorial-fixture-lock"}
    def tearDown(self):self.temp.cleanup()
    def run_packet(self):
        inp=self.root/"packet.json";inp.write_text(json.dumps(self.packet))
        return p.run(inp,self.root/"final.png")
    def test_produces_png_candidate_no_pdf(self):
        result=self.run_packet()
        self.assertEqual(result["status"],"CANDIDATE_NOT_APPROVED")
        self.assertTrue((self.root/"final.png").is_file())
        self.assertFalse((self.root/"final.pdf").exists())
        self.assertFalse(result["independent_approval"])
    def test_missing_approval_blocks(self):
        self.packet.pop("editorial_approval_reference")
        result=self.run_packet()
        self.assertFalse(result["render_invoked"])
        self.assertFalse((self.root/"final.png").exists())
    def test_tampered_page_spec_blocks(self):
        self.packet["page_spec_sha256"]="a"*64
        self.assertIn("SHA-256 mismatch",str(self.run_packet()["errors"]))
    def test_unverified_character_blocks(self):
        self.packet["character_ids"]=["CHAR-WILSON-LOOK"]
        self.assertIn("BLOCKED_BY_CHARACTER_REFERENCE_PIPELINE",str(self.run_packet()["errors"]))
    def test_sports_missing_evidence_blocks(self):
        self.packet["production_kind"]="SPORTS_DESK"
        self.assertIn("sports claims required",str(self.run_packet()["errors"]))
    def test_narrative_without_atlas_blocks(self):
        self.packet["production_kind"]="NARRATIVE"
        result=self.run_packet()
        self.assertIn("narrative Atlas preflight required",str(result["errors"]))
if __name__=="__main__":unittest.main()
