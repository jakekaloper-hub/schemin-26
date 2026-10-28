"""Actual release artifact tests use synthetic imagery/PDF, not QA signoffs."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import fitz
from PIL import Image
from validate_artifacts import inspect

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class RealArtifactGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        png = self.root / "page1.png"
        Image.new("RGB", (1080, 1920), (32, 44, 62)).save(png)
        pdf = self.root / "memo.pdf"
        doc = fitz.open()
        page = doc.new_page(width=540,height=960)
        page.insert_text((30,40), "Page 1")
        doc.save(pdf)
        doc.close()
        self.data = {"expected_pages":1,"pdf_path":"memo.pdf","published_artifact_sha256":digest(pdf),
            "pages":[{"slot":1,"asset_path":"page1.png","asset_sha256":digest(png)}]}

    def test_valid_artifacts(self): self.assertEqual(inspect(self.data,self.root/"issue.json"),[])
    def test_forward_native_week8_valid(self):
        d=copy.deepcopy(self.data);d["week"]=8
        self.assertEqual(inspect(d,self.root/"issue.json"),[])

    def test_forward_native_week8_reject_legacy(self):
        d=copy.deepcopy(self.data);d["week"]=8
        png=self.root/"page1.png"
        Image.new("RGB",(1024,1536)).save(png)
        d["pages"][0]["asset_sha256"]=digest(png)
        self.assertTrue(any("native 1080x1920 PNG rejected" in e for e in inspect(d,self.root/"issue.json")))

    def test_week7_opt_in_reject_legacy(self):
        d=copy.deepcopy(self.data);d["week"]=7;d["native_page_format"]="1080x1920"
        png=self.root/"page1.png"
        Image.new("RGB",(1024,1536)).save(png)
        d["pages"][0]["asset_sha256"]=digest(png)
        self.assertTrue(any("native 1080x1920 PNG rejected" in e for e in inspect(d,self.root/"issue.json")))

    def test_wrong_pdf_checksum(self):
        d=copy.deepcopy(self.data);d["published_artifact_sha256"]="0"*64
        self.assertTrue(any("actual SHA256" in s for s in inspect(d,self.root/"issue.json")))
    def test_missing_image(self):
        d=copy.deepcopy(self.data);d["pages"][0]["asset_path"]="missing.png"
        self.assertTrue(inspect(d,self.root/"issue.json"))
    def test_wrong_image_checksum(self):
        d=copy.deepcopy(self.data);d["pages"][0]["asset_sha256"]="f"*64
        self.assertTrue(any("hash mismatch" in s for s in inspect(d,self.root/"issue.json")))
    def test_pdf_page_count(self):
        d=copy.deepcopy(self.data);d["expected_pages"]=2
        self.assertTrue(any("actual page count" in s for s in inspect(d,self.root/"issue.json")))
    def test_path_escape(self):
        d=copy.deepcopy(self.data);d["pdf_path"]="../memo.pdf"
        self.assertTrue(any("escapes" in s for s in inspect(d,self.root/"issue.json")))
    def test_corrupted_image(self):
        (self.root/"page1.png").write_text("corrupted")
        d=copy.deepcopy(self.data);d["pages"][0]["asset_sha256"]=digest(self.root/"page1.png")
        self.assertTrue(any("corrupt" in s for s in inspect(d,self.root/"issue.json")))

if __name__=="__main__":unittest.main()
