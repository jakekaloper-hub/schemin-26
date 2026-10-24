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
        masters = []
        doc = fitz.open()
        for n, color in [(1, (32, 44, 62)), (2, (62, 44, 32))]:
            png = self.root / f"page{n}.png"
            Image.new("RGB", (1024, 1536), color).save(png)
            page = doc.new_page(width=512, height=768)
            page.insert_image(page.rect, filename=str(png))
            masters.append({"slot":n,"status":"ACCEPTED","asset_path":png.name,"asset_sha256":digest(png)})
        pdf = self.root / "memo.pdf"
        doc.save(pdf)
        doc.close()
        self.data = {"artifact_stage":"ISSUE_PACKAGE","expected_pages":2,"pdf_path":"memo.pdf",
            "published_artifact_sha256":digest(pdf),"pages":masters}

    def test_valid_artifacts(self): self.assertEqual(inspect(self.data,self.root/"issue.json"),[])
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
        d=copy.deepcopy(self.data);d["expected_pages"]=3
        self.assertTrue(any("actual page count" in s for s in inspect(d,self.root/"issue.json")))
    def test_path_escape(self):
        d=copy.deepcopy(self.data);d["pdf_path"]="../memo.pdf"
        self.assertTrue(any("escapes" in s for s in inspect(d,self.root/"issue.json")))
    def test_corrupted_image(self):
        (self.root/"page1.png").write_text("corrupted")
        d=copy.deepcopy(self.data);d["pages"][0]["asset_sha256"]=digest(self.root/"page1.png")
        self.assertTrue(any("corrupt" in s for s in inspect(d,self.root/"issue.json")))

if __name__=="__main__":unittest.main()
