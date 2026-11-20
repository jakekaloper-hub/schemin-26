"""Chapter XXXV V2 mechanical checks for 32-part noncanonical reader. NOT an independent editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIG="THE_COAT_THAT_DID_NOT_BELONG_CHAPTER_35_NONCANON.md"
NEW="THE_COAT_THAT_DID_NOT_BELONG_WHAT_THE_ROOF_WAS_OWED_CH35_V2_NONCANON.md"
PREV="READING_COPY_2016_CAUSAL_CH01_34_THIRTY_ONE_PARTS_BLUE_BOWL_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_35_THIRTY_TWO_PARTS_ROOF_DUE_NONCANON.md"
ORIG_SHA="bb4e2904bead10f403d4eda279cd9eeaf983032e"
NEW_SHA="62bec21c4765016a6156a91450b122669b8c6c98"
PREV_SHA="5424afc1de335b3dd3c2920013751c95a16090f4"
READER_SHA="e0206b6d92f4f65d87b332a79c8e66165668e0e1"
ARCHIVE_SHA="6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(p):
 data=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def rows(s):
 return [(int(n),f,sha,int(w)) for n,f,sha,w in re.findall(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",s,re.M)]
def component(s,name,sha):
 a=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->\n\n"
 b=f"\n\n<!-- END 2016_CAUSAL {name} -->"
 assert s.count(a)==s.count(b)==1, name
 return s.split(a,1)[1].split(b,1)[0]
class ChapterThirtyFiveRoofDue(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.original=(BASE/ORIG).read_text()
  cls.chapter=(BASE/NEW).read_text()
  cls.previous=(BASE/PREV).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.rows=rows(cls.reader)
  cls.prev_rows=rows(cls.previous)
  cls.scene="### VI. What the roof was owed"+cls.chapter.split("### VI. What the roof was owed",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
 def test_01_original_source_blob(self): self.assertEqual(blob(BASE/ORIG),ORIG_SHA)
 def test_02_revision_source_blob(self): self.assertEqual(blob(BASE/NEW),NEW_SHA)
 def test_03_previous_reader_unchanged(self): self.assertEqual(blob(BASE/PREV),PREV_SHA)
 def test_04_new_reader_blob(self): self.assertEqual(blob(BASE/READER),READER_SHA)
 def test_05_six_movements(self):
  self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.chapter,re.M),["I","II","III","IV","V","VI"])
 def test_06_original_five_movements_source_exact(self):
  original=self.original.split("### I. An unfamiliar shoulder",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  self.assertIn(original,self.chapter)
 def test_07_substantial_new_scene(self):
  self.assertGreaterEqual(len(self.scene.split()),1500)
  for line in ("Then that sentence doesn't go on this paper.","You haven't missed a payment yet.","Those are different things."):
   self.assertIn(line,self.scene)
 def test_08_owner_pov_guardrails(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
  self.assertIn("UNAUTHENTICATED",self.chapter)
  for forbidden in ("Edrin","Edin","ESPN final","championship belt"):
   self.assertNotIn(forbidden,self.scene)
 def test_09_prior_manifest_retained(self):
  self.assertEqual([n for n,*_ in self.rows],list(range(1,33)))
  self.assertEqual(self.rows[:31],self.prev_rows)
  self.assertEqual(self.rows[-1],(32,NEW,NEW_SHA,9201))
 def test_10_balanced_component_markers(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),32)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),32)
 def test_11_all_embedded_components_exact(self):
  for n,f,sha,w in self.rows:
   with self.subTest(part=n):
    self.assertEqual(blob(BASE/f),sha)
    src=(BASE/f).read_text()
    self.assertEqual(len(src.split()),w)
    self.assertEqual(component(self.reader,f,sha),src.rstrip("\n"))
 def test_12_prior_31_bodies_unchanged(self):
  for _,f,sha,_ in self.prev_rows:
   with self.subTest(file=f):
    self.assertEqual(component(self.previous,f,sha),component(self.reader,f,sha))
 def test_13_word_counts(self):
  self.assertEqual(len(self.chapter.split()),9201)
  self.assertEqual(sum(w for _,_,_,w in self.rows),233239)
  self.assertIn("Source component words including metadata: 233239",self.reader)
 def test_14_archive_unchanged(self):
  self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)
 def test_15_protected_2026_hard_canon(self):
  for path,sha in PROTECTED.items():
   with self.subTest(path=path): self.assertEqual(blob(ROOT/path),sha)
 def test_16_subsequent_chapter_continuity(self):
  nxt=(BASE/"THE_ASH_AT_FARAS_DOOR_CHAPTER_36_NONCANON.md").read_text()
  for phrase in ("Pell has returned injured","missed a possible shift","Mael"):
   self.assertIn(phrase,nxt)
 def test_17_release_hold(self):
  for phrase in ("FOUNDER-ONLY CANON & PUBLICATION APPROVAL","NO MERGE / NO PUBLICATION / NO CANON PROMOTION"):
   self.assertIn(phrase,self.reader)
  self.assertIn("INDEPENDENT EDITORIAL HOLD",self.chapter)
 def test_18_no_paid_work_or_confirmed_freight(self):
  for phrase in ("no wages are earned","no freight or owner-history facts established"):
   self.assertIn(phrase,self.chapter.lower())
 def test_19_secondary_characters_not_owner_pov(self):
  self.assertNotIn("Mara thought",self.scene)
  self.assertNotIn("Seli wondered",self.scene)
  self.assertNotIn("her private motives",self.scene)
if __name__=="__main__": unittest.main()
