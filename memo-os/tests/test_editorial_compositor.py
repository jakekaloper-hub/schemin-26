import hashlib,importlib.util,json,tempfile,unittest
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
    def test_receipt_identifies_actual_font_bytes_and_rendering_versions(self):
        import PIL
        from PIL import features
        receipt=self.run_page()
        font=receipt["typography_environment"]["fonts"]["serif"]
        self.assertEqual(font["sha256"],hashlib.sha256(Path(m.FONTS["serif"]).read_bytes()).hexdigest())
        self.assertEqual(receipt["typography_environment"]["pillow_version"],PIL.__version__)
        self.assertEqual(receipt["typography_environment"]["freetype_version"],features.version_module("freetype2"))
        self.assertEqual(receipt["source_text_regions"][0]["font"],"serif")
        self.assertEqual(receipt["source_text_regions"][0]["font_size"],30)
        self.assertEqual(receipt["output_sha256"],self.run_page()["output_sha256"])
        self.assertFalse(receipt["visual_text_independently_verified"])

    def test_receipt_distinguishes_source_copy_from_rendered_line_commands(self):
        self.s["regions"][0]["text"]="  ALPHA   BETA  "
        region=self.run_page()["source_text_regions"][0]
        self.assertEqual(region["text"],"  ALPHA   BETA  ")
        self.assertEqual(region["rendered_lines"],["ALPHA BETA"])

    def test_font_receipt_hashes_the_bytes_loaded_even_if_path_changes(self):
        from unittest.mock import patch
        font_bytes=Path(m.FONTS["serif"]).read_bytes()
        font_path=self.root/"font.ttf"
        font_path.write_bytes(font_bytes)
        load=m.ImageFont.truetype
        def change_source_after_loading(*args,**kwargs):
            font=load(*args,**kwargs)
            font_path.write_bytes(b"changed after loading")
            return font
        with patch.dict(m.FONTS,{"serif":str(font_path)}), patch.object(m.ImageFont,"truetype",side_effect=change_source_after_loading):
            receipt=self.run_page()
        self.assertEqual(receipt["typography_environment"]["fonts"]["serif"]["sha256"],hashlib.sha256(font_bytes).hexdigest())

    def test_background_receipt_hashes_loaded_bytes_if_path_changes(self):
        from unittest.mock import patch
        background=self.root/"bg.png"
        original_bytes=background.read_bytes()
        load=m.Image.open
        def change_source_after_loading(*args,**kwargs):
            image=load(*args,**kwargs)
            image.load()
            background.write_bytes(b"changed after loading")
            return image
        with patch.object(m.Image,"open",side_effect=change_source_after_loading):
            receipt=self.run_page()
        self.assertEqual(receipt["background_sha256"],hashlib.sha256(original_bytes).hexdigest())

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
