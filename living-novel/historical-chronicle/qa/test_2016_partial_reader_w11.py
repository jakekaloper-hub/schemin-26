"""2016 W11 twelve-component exact-source partial reading copy."""
from pathlib import Path
import hashlib
import unittest
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016"
R=BASE/"READING_COPY_PROLOGUE_W01_W11_PARTIAL_NONCANON.md"
PARTS=[
 ("PROLOGUE.md","d372cd61c97d698ea34f2f41e7d762775fcdc379"),
 ("weeks/W01.md","728693dd68e8ec314294d55fc1be263af6df7a60"),
 ("weeks/W02.md","a2c179164dc529a34d92479b1c8a93f37acb10dd"),
 ("weeks/W03.md","f515d2e46486f599906fd43cb98232585427ba0c"),
 ("weeks/W04.md","c04700fe674489a5e0aac8f73ce4ddae9ba564eb"),
 ("weeks/W05.md","bab0fe58cd46e77950d59fe0359a92efb78bd1ae"),
 ("weeks/W06.md","6d16b7aca6b337c54d5e96f2f6849b0e6c48bd83"),
 ("weeks/W07.md","6174757e09c9dc9cf2f5e99f8a18a7116d660b73"),
 ("weeks/W08.md","f96082ae79cae7cae5681a8ceec2cd69601ea403"),
 ("weeks/W09.md","b615615d42980b32d37b8773f861ee9cba5b9505"),
 ("weeks/W10.md","1b30e4e36fa9e3cca585a5f43d3e96ca422d79d1"),
 ("weeks/W11.md","7b7c53091e1dec4c253b271677468b8256bb8f75"),
]
def blob(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()
class ReaderW11(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.text=R.read_text(encoding="utf-8")
 def test_order(self):
  keys=[f"<!-- BEGIN 2016 {p} | git_blob {s} -->" for p,s in PARTS]
  self.assertEqual([self.text.count(x) for x in keys],[1]*12)
  self.assertEqual([self.text.index(x) for x in keys],sorted(self.text.index(x) for x in keys))
 def test_end_markers(self):
  for p,_ in PARTS:self.assertEqual(self.text.count(f"<!-- END 2016 {p} -->"),1)
 def test_pinned_source_blobs(self):
  for p,s in PARTS:
   with self.subTest(path=p):self.assertEqual(blob((BASE/p).read_bytes()),s)
 def test_exact_verbatim_bodies(self):
  for p,s in PARTS:
   a=f"<!-- BEGIN 2016 {p} | git_blob {s} -->\n\n"
   b=f"\n\n<!-- END 2016 {p} -->"
   with self.subTest(path=p):
    self.assertIn(a,self.text)
    self.assertEqual(self.text.split(a,1)[1].split(b,1)[0],(BASE/p).read_text(encoding="utf-8").rstrip())
 def test_partial_noncanonical_scope(self):
  self.assertGreaterEqual(len(self.text.split()),53000)
  self.assertEqual(self.text.count("<!-- BEGIN 2016 "),12)
  for t in ("PARTIAL READING COPY","NONCANON","Weeks 12–13","No Founder, independent Authors Council or Umpire approval"):
   self.assertIn(t.lower(),self.text.lower())
 def test_no_protected_2026_chapters(self):
  for t in ("CHAPTER_01_THE_FIRST_ANSWER","CHAPTER_02_WHAT_COMES_BACK","CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM"):
   self.assertNotIn(t,self.text)
if __name__=="__main__":
 unittest.main()
