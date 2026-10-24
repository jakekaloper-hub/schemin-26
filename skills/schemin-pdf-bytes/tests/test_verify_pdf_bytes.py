import hashlib,importlib.util,tempfile,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify_pdf_bytes.py"
spec=importlib.util.spec_from_file_location("pdfbytes",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class VerifyTests(unittest.TestCase):
 def setUp(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
  self.root=Path(tmp.name);self.file=self.root/"archive/publications/2026/week-06/memo.pdf"
  self.file.parent.mkdir(parents=True);self.pdf=b"%PDF-1.4\nfixture\n%%EOF"
  self.row={"week":6,"archive_path":str(self.file.relative_to(self.root)),"sha256":hashlib.sha256(self.pdf).hexdigest(),"size_bytes":len(self.pdf)}
 def check(self):return m.verify({"files":[self.row]},self.root,6)
 def test_valid(self):self.file.write_bytes(self.pdf);self.assertEqual(self.check()["status"],"VERIFIED_REAL_BYTES")
 def test_pointer(self):self.file.write_bytes(m.POINTER+b"oid sha256:abc\n");self.assertEqual(self.check()["status"],"POINTER_ONLY")
 def test_missing(self):self.assertEqual(self.check()["reason"],"FILE_MISSING")
 def test_tampered(self):self.file.write_bytes(self.pdf+b"bad");self.assertEqual(self.check()["status"],"FAIL")
 def test_not_pdf(self):self.file.write_bytes(b"not pdf");self.assertEqual(self.check()["reason"],"NOT_PDF_BYTES")
 def test_traversal(self):
  self.row["archive_path"]="archive/publications/2026/week-06/../../../secret.pdf"
  with self.assertRaises(ValueError):self.check()
if __name__=="__main__":unittest.main()
