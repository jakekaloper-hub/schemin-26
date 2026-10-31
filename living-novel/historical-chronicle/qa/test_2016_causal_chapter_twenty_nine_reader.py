"""2016 Chapter XXIX NONCANON source-exact reader, preservation and continuity regressions.
Technical proof only; never independent literary, historical or Founder acceptance.
"""
import hashlib, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_PLAY_WITH_NO_END_CHAPTER_29_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_29_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_28_NONCANON.md"
CHAPTER_SHA = "815329d6d69dd875929f26e0a4c7974cd77415dd"
READER_SHA = "34627f4085da0f7019975125ac1d0822d246edf5"
PREVIOUS_SHA = "d273d050f1554a087119df4141e340dd795fed9b"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(path):
 data = path.read_bytes()
 return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def rows(text):
 return [(int(n), name, sha, int(words)) for n,name,sha,words in re.findall(
  r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$",text,re.M)]
def passage(text,name,sha):
 start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
 end=f"<!-- END 2016_CAUSAL {name} -->"
 assert text.count(start)==1 and text.count(end)==1
 return text.split(start,1)[1].split(end,1)[0].strip()
class TwentyNineChapterReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=(BASE/CHAPTER).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.old=(BASE/PREVIOUS).read_text()
  cls.manifest=rows(cls.reader)
  cls.old_manifest=rows(cls.old)
  cls.prose=cls.chapter.split("### I.",1)[1].split("\n---\n",1)[0]
 def test_01_order_and_last_row(self):
  self.assertEqual([n for n,_,_,_ in self.manifest],list(range(1,30)))
  self.assertEqual(self.manifest[-1],(29,CHAPTER,CHAPTER_SHA,len(self.chapter.split())))
 def test_02_marker_balance(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),29)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),29)
 def test_03_complete_source_exact(self):
  for n,name,sha,words in self.manifest:
   with self.subTest(chapter=n):
    src=(BASE/name).read_text()
    self.assertEqual(passage(self.reader,name,sha),src.strip())
    self.assertEqual(len(src.split()),words)
 def test_04_manifest_blobs(self):
  for n,name,sha,_ in self.manifest:
   with self.subTest(chapter=n): self.assertEqual(blob(BASE/name),sha)
 def test_05_previous_reading_copy_unchanged(self):
  self.assertEqual(blob(BASE/PREVIOUS),PREVIOUS_SHA)
  self.assertEqual(self.manifest[:28],self.old_manifest)
 def test_06_all_previous_prose_preserved(self):
  for n,name,sha,_ in self.old_manifest:
   with self.subTest(chapter=n):
    self.assertEqual(passage(self.reader,name,sha),passage(self.old,name,sha))
 def test_07_substantive_five_movement_chapter(self):
  self.assertGreaterEqual(len(self.chapter.split()),5400)
  self.assertEqual(len(re.findall(r"^### [IVX]+\.",self.chapter,re.M)),5)
  self.assertIn("### Editorial handoff",self.chapter)
 def test_08_only_authorized_pov(self):
  self.assertIn("Sole limited interior viewpoint",self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER",self.chapter)
  self.assertIn("UNAUTHENTICATED",self.chapter)
  for forbidden in ("Edrin","Edin","Oren"):
   self.assertNotIn(forbidden,self.prose)
 def test_09_vessa_does_not_open_passage(self):
  self.assertIn("Because it was unsafe when we last checked it",self.prose)
  self.assertIn("I won't open it for your play",self.prose)
  self.assertIn("The warning strip across the sealed passage remained",self.prose)
 def test_10_art_does_not_become_factual_record(self):
  self.assertIn("It isn't the same as what happened",self.prose)
  self.assertIn("The play isn't a work order",self.prose)
  self.assertIn("a wooden person has opened it",self.prose)
 def test_11_nontriumphal_consequence(self):
  self.assertIn("None of us knows it tonight",self.prose)
  self.assertIn("It did not come",self.prose)
  self.assertIn("The next part belongs to another night",self.prose)
 def test_12_live_preexisting_loops_not_false_closed(self):
  for item in ("half-paid cart-mark commission is incomplete","Pell has departed","receipt remains unconfirmed","four stoneworks hours"):
   self.assertIn(item,self.chapter)
  self.assertIn("Eren's cart marks would be finished when Eren finished them",self.prose)
 def test_13_source_archive_preserved(self):
  self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
 def test_14_hard_canon_untouched(self):
  for p,sha in PROTECTED.items():
   with self.subTest(path=p): self.assertEqual(blob(ROOT/p),sha)
 def test_15_new_reader_blob_and_hold(self):
  self.assertEqual(blob(BASE/CHAPTER),CHAPTER_SHA)
  self.assertEqual(blob(BASE/READER),READER_SHA)
  self.assertGreaterEqual(len(self.reader.split()),155000)
  self.assertIn("Twenty-nine fully assembled",self.reader)
  self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
  self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
  self.assertIn("No independent Authors Council",self.chapter)
if __name__=="__main__":
 unittest.main()
