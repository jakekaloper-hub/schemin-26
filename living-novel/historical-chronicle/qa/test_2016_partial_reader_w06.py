"""W06 seven-part source-exact noncanonical 2016 partial reader."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/"living-novel/historical-chronicle/seasons/2016"
READER = BASE/"READING_COPY_PROLOGUE_W01_W06_PARTIAL_NONCANON.md"
PARTS=[
    ("PROLOGUE.md","d372cd61c97d698ea34f2f41e7d762775fcdc379"),
    ("weeks/W01.md","728693dd68e8ec314294d55fc1be263af6df7a60"),
    ("weeks/W02.md","a2c179164dc529a34d92479b1c8a93f37acb10dd"),
    ("weeks/W03.md","f515d2e46486f599906fd43cb98232585427ba0c"),
    ("weeks/W04.md","c04700fe674489a5e0aac8f73ce4ddae9ba564eb"),
    ("weeks/W05.md","bab0fe58cd46e77950d59fe0359a92efb78bd1ae"),
    ("weeks/W06.md","6d16b7aca6b337c54d5e96f2f6849b0e6c48bd83"),
]

def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

class ReaderThroughWeekSix2016(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=READER.read_text(encoding="utf-8")

    def test_order_and_uniqueness(self):
        markers=[f"<!-- BEGIN 2016 {p} | git_blob {s} -->" for p,s in PARTS]
        self.assertEqual([self.text.count(x) for x in markers], [1]*7)
        self.assertEqual([self.text.index(x) for x in markers],
                         sorted(self.text.index(x) for x in markers))

    def test_end_markers(self):
        for path,_ in PARTS:
            self.assertEqual(self.text.count(f"<!-- END 2016 {path} -->"),1)

    def test_source_blob_integrity(self):
        for path,sha in PARTS:
            with self.subTest(path=path):
                self.assertEqual(blob((BASE/path).read_bytes()),sha)

    def test_verbatim_bodies(self):
        for path,sha in PARTS:
            start=f"<!-- BEGIN 2016 {path} | git_blob {sha} -->\\n\\n".replace("\\n","\n")
            stop=f"\\n\\n<!-- END 2016 {path} -->".replace("\\n","\n")
            with self.subTest(path=path):
                self.assertIn(start,self.text)
                actual=self.text.split(start,1)[1].split(stop,1)[0]
                self.assertEqual(actual,(BASE/path).read_text(encoding="utf-8").rstrip())

    def test_reader_substance_and_correct_scope(self):
        self.assertGreaterEqual(len(self.text.split()),24000)
        for t in ("PARTIAL READING COPY","NONCANON","Weeks 7–13",
                  "No Founder, independent Authors Council or Umpire approval"):
            self.assertIn(t.lower(),self.text.lower())
        self.assertEqual(self.text.count("<!-- BEGIN 2016 "),7)

    def test_no_protected_chapters_assembled(self):
        for t in ("CHAPTER_01_THE_FIRST_ANSWER","CHAPTER_02_WHAT_COMES_BACK",
                  "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM"):
            self.assertNotIn(t,self.text)

if __name__=="__main__":
    unittest.main()
