import importlib.util,json,tempfile,unittest
from pathlib import Path
from PIL import Image
path=Path(__file__).resolve().parents[1]/"tools"/"render_editorial_page.py"
spec=importlib.util.spec_from_file_location("compositor",path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestCompositor(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        Image.new("RGB",(1024,1536),"#253443").save(self.root/"bg.png")
        self.s={"format":"schemin-memo-editorial-v1","background":"bg.png","regions":[{"text":"D0nkey K0ng — 118.96","x":80,"y":100,"width":850,"height":90,"font_size":30}]}
    def tearDown(self):self.tmp.cleanup()
    def run_page(self):
        p=self.root/"spec.json";p.write_text(json.dumps(self.s));return m.render(p,self.root/"out.png")
    def test_exact_unicode_receipt(self):
        r=self.run_page();self.assertEqual(r["source_text_regions"][0]["text"],"D0nkey K0ng — 118.96")
        self.assertEqual(r["dimensions"],[1024,1536]);self.assertFalse(r["visual_text_independently_verified"])
    def test_overflow_fails(self):
        self.s["regions"][0]["height"]=10
        with self.assertRaisesRegex(ValueError,"overflows"):self.run_page()
    def test_overlap_fails(self):
        self.s["regions"].append(dict(self.s["regions"][0]))
        with self.assertRaisesRegex(ValueError,"overlapping"):self.run_page()
    def test_wrong_dimensions_fails(self):
        Image.new("RGB",(100,100)).save(self.root/"bg.png")
        with self.assertRaisesRegex(ValueError,"background dimensions"):self.run_page()
    def test_path_escape_fails(self):
        self.s["background"]="../elsewhere.png"
        with self.assertRaisesRegex(ValueError,"unsafe background"):self.run_page()
    def test_unapproved_font_fails(self):
        self.s["regions"][0]["font"]="external.ttf"
        with self.assertRaisesRegex(ValueError,"font rejected"):self.run_page()
if __name__=="__main__":unittest.main()
