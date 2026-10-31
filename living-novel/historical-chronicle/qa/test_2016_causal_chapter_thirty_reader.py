"""Source-exact noncanonical 2016 causal Chapter XXX reader regressions; no editorial approval implied."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_FOURTH_NOTE_AT_THE_RIVER_CHAPTER_30_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_30_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_29_NONCANON.md"
CHAPTER_SHA = "1b65f32ca5b41b52e8d362b8cfea95b4e2a03b8d"
READER_SHA = "48eb9453b05b4ce30fb948badedefdf79c91d8d6"
PREVIOUS_SHA = "34627f4085da0f7019975125ac1d0822d246edf5"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(path):
 data = path.read_bytes()
 return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()
def rows(text):
 return [(int(n),name,sha,int(words)) for n,name,sha,words in re.findall(
  r"^\\| (\\d+) \\| \\x60([^\\x60]+)\\x60 \\| \\x60([a-f0-9]{40})\\x60 \\| (\\d+) \\|$",text,re.M)]
def passage(text,name,sha):
 start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
 end=f"<!-- END 2016_CAUSAL {name} -->"
 assert text.count(start)==1 and text.count(end)==1
 return text.split(start,1)[1].split(end,1)[0].strip()
class ThirtyChapterReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=(BASE/CHAPTER).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.old=(BASE/PREVIOUS).read_text()
  cls.manifest=rows(cls.reader)
  cls.old_manifest=rows(cls.old)
  cls.prose=cls.chapter.split("### I.",1)[1].split("\\n---\\n",1)[0]
 def test_01_order_and_last_row(self):
  self.assertEqual([n for n,_,_,_ in self.manifest],list(range(1,31)))
  self.assertEqual(self.manifest[-1],(30,CHAPTER,CHAPTER_SHA,len(self.chapter.split())))
 def test_02_marker_balance(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),30)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),30)
 def test_03_source_exact(self):
  for n,name,sha,words in self.manifest:
   with self.subTest(chapter=n):
    src=(BASE/name).read_text()
    self.assertEqual(passage(self.reader,name,sha),src.strip())
    self.assertEqual(len(src.split()),words)
 def test_04_manifest_blob_checks(self):
  for n,name,sha,_ in self.manifest:
   with self.subTest(chapter=n): self.assertEqual(blob(BASE/name),sha)
 def test_05_prior_copy_preserved(self):
  self.assertEqual(blob(BASE/PREVIOUS),PREVIOUS_SHA)
  self.assertEqual(self.manifest[:29],self.old_manifest)
 def test_06_prior_passages_unchanged(self):
  for n,name,sha,_ in self.old_manifest:
   with self.subTest(chapter=n):
    self.assertEqual(passage(self.reader,name,sha),passage(self.old,name,sha))
 def test_07_five_substantive_movements(self):
  self.assertGreaterEqual(len(self.chapter.split()),5600)
  self.assertEqual(len(re.findall(r"^### [IVX]+\\.",self.chapter,re.M)),5)
  self.assertIn("### Editorial handoff",self.chapter)
 def test_08_exclusive_principal_pov(self):
  self.assertIn("Sole limited interior viewpoint",self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER",self.chapter)
  self.assertIn("UNAUTHENTICATED",self.chapter)
  for forbidden in ("Edrin","Edin","Oren"): self.assertNotIn(forbidden,self.prose)
 def test_09_kiln_remains_closed(self):
  self.assertIn("The closure remained in force",self.prose)
  self.assertIn("The gate remained shut behind her",self.prose)
  self.assertIn("No one opened the kiln passage",self.prose)
 def test_10_child_found_without_reopening_kiln(self):
  self.assertIn("He had not gone through the dangerous kiln gate",self.prose)
  self.assertIn("Only then did the boy climb",self.prose)
  self.assertIn("no one went into the river",self.prose)
 def test_11_fourth_note_is_new(self):
  self.assertIn("A fourth note came",self.prose)
  self.assertIn("That's not how she played it",self.prose)
  self.assertIn("He did not correct his son",self.prose)
 def test_12_continuity_unsettled(self):
  for phrase in ("half-paid cart-mark commission is incomplete",
                 "Pell's three-day hauling engagement and wages are unconfirmed",
                 "four paid hours","Mev holds Jake's outward letter"):
   self.assertIn(phrase,self.chapter)
  self.assertIn("the second half of the payment had not been earned",self.prose)
 def test_13_archive_untouched(self):
  self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
 def test_14_hard_canon_untouched(self):
  for path,sha in PROTECTED.items():
   with self.subTest(path=path): self.assertEqual(blob(ROOT/path),sha)
 def test_15_reader_integrity_and_hold(self):
  self.assertEqual(blob(BASE/CHAPTER),CHAPTER_SHA)
  self.assertEqual(blob(BASE/READER),READER_SHA)
  self.assertGreaterEqual(len(self.reader.split()),160000)
  self.assertIn("Thirty fully assembled",self.reader)
  self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)
  self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
  self.assertIn("not accepted this candidate",self.chapter)
if __name__=="__main__":
 unittest.main()
