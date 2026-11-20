"""2016 Chapter XXVII draft-reader mechanical regressions; not editorial or canon approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER="THE_ROOM_WITH_NO_HIGH_SEAT_CHAPTER_27_NONCANON.md"
READER="READING_COPY_CAUSAL_CHAPTERS_01_27_NONCANON.md"
PREVIOUS="READING_COPY_CAUSAL_CHAPTERS_01_26_NONCANON.md"
CHAPTER_SHA="d451e61332ce6da3911cf77957596b09edcaecdf"
READER_SHA="41115b3f158e95d423befba4127063480c60e70b"
PREVIOUS_SHA="0027269704900b8ecb9d7a10c958cec963bd1df0"
ARCHIVE_SHA="6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(p):
 d=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(d)).encode()+b"\0"+d).hexdigest()
def rows(s):
 return [(int(i),name,sha,int(words)) for i,name,sha,words in re.findall(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",s,re.M)]
def passage(s,name,sha):
 start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
 end=f"<!-- END 2016_CAUSAL {name} -->"
 assert s.count(start)==1 and s.count(end)==1,name
 return s.split(start,1)[1].split(end,1)[0].strip()
class TwentySevenChapterReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=(BASE/CHAPTER).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.old=(BASE/PREVIOUS).read_text()
  cls.manifest=rows(cls.reader)
  cls.old_manifest=rows(cls.old)
  cls.prose=cls.chapter.split("### I.",1)[1].split("\n---\n",1)[0]
 def test_01_manifest_order(self):
  self.assertEqual([x[0] for x in self.manifest],list(range(1,28)))
  self.assertEqual(self.manifest[-1],(27,CHAPTER,CHAPTER_SHA,len(self.chapter.split())))
 def test_02_assembly_marker_count(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),27)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),27)
 def test_03_source_exact_assembly(self):
  for n,name,sha,words in self.manifest:
   with self.subTest(n=n):
    src=(BASE/name).read_text()
    self.assertEqual(passage(self.reader,name,sha),src.strip())
    self.assertEqual(len(src.split()),words)
 def test_04_source_blob_fingerprints(self):
  for n,name,sha,_ in self.manifest:
   with self.subTest(n=n):self.assertEqual(blob(BASE/name),sha)
 def test_05_previous_reader_fingerprint(self):
  self.assertEqual(blob(BASE/PREVIOUS),PREVIOUS_SHA)
  self.assertEqual(self.manifest[:26],self.old_manifest)
 def test_06_previous_chapters_not_mutated(self):
  for _,name,sha,_ in self.old_manifest:
   with self.subTest(name=name):self.assertEqual(passage(self.reader,name,sha),passage(self.old,name,sha))
 def test_07_substantial_five_movements(self):
  self.assertGreaterEqual(len(self.chapter.split()),5200)
  self.assertEqual(len(re.findall(r"^### [IVX]+\.",self.chapter,re.M)),5)
  self.assertIn("### Editorial handoff",self.chapter)
 def test_08_exclusive_owner_pov(self):
  self.assertIn("Sole limited interior viewpoint",self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER",self.chapter)
  self.assertIn("NOT an authenticated historical ESPN owner-slot association",self.chapter)
  for term in ("Edrin","Edin","Oren"):self.assertNotIn(term,self.prose)
 def test_09_no_unearned_paid_shift(self):
  self.assertIn("You can sit",self.prose)
  self.assertIn("Nothing for you this morning",self.prose)
  self.assertIn("zero additional paid stoneworks hours",self.chapter)
 def test_10_independent_table_house(self):
  self.assertIn("That's where the roof drips when the wind shifts",self.prose)
  self.assertIn("But it is my room",self.prose)
  self.assertIn("Fara controls her eating house",self.chapter)
 def test_11_pell_disagreement_remains_unresolved(self):
  self.assertIn("They don't owe you a closed passage opened",self.prose)
  self.assertIn("the cloth his mother had been promised",self.prose)
  self.assertIn("The cloth was still missing",self.prose)
 def test_12_vessa_and_letter_boundaries(self):
  self.assertIn("The smoke above the eaves was less",self.prose)
  self.assertIn("But I didn't measure the air in the passage. Vessa did",self.prose)
  self.assertIn("I can't say whose hands take it after",self.prose)
  self.assertIn("beneath a square of dry cloth",self.prose)
  self.assertIn("Delivery to Esi is **NOT confirmed**",self.chapter)
 def test_13_historical_archive_intact(self):
  p=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
  self.assertEqual(blob(p),ARCHIVE_SHA)
 def test_14_protected_hard_canon_intact(self):
  for name,sha in PROTECTED.items():
   with self.subTest(name=name):self.assertEqual(blob(ROOT/name),sha)
 def test_15_reader_hash_and_hold(self):
  self.assertEqual(blob(BASE/CHAPTER),CHAPTER_SHA)
  self.assertEqual(blob(BASE/READER),READER_SHA)
  self.assertGreaterEqual(len(self.reader.split()),145000)
  self.assertIn("Twenty-seven fully assembled",self.reader)
  self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
  self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
  self.assertIn("No founder-only promotion, merge or publication",self.chapter)
if __name__=="__main__":unittest.main()
