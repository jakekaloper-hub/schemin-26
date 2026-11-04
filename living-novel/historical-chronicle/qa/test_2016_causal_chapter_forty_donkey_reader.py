"""2016 Chapter XL V2 source-exact 37-part developmental reading checks — NONCANON."""
import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD="THE_HOUSE_MADE_FROM_A_ROAD_CHAPTER_40_NONCANON.md"
SCENE="THE_DONKEY_AND_THE_BROKEN_MEASURE_CH40_V2_NONCANON.md"
CHAPTER="THE_HOUSE_MADE_FROM_A_ROAD_THE_DONKEY_AND_THE_BROKEN_MEASURE_CH40_V2_NONCANON.md"
PREV="READING_COPY_2016_CAUSAL_CH01_39_THIRTY_SIX_PARTS_WHITE_CLOTH_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_40_THIRTY_SEVEN_PARTS_DONKEY_MEASURE_NONCANON.md"
OLD_SHA="d5a4e6778c705b5f3e655071e04a67892ef22b95"
SCENE_SHA="daf67c6c6e871e6ad327a61685468019238b23e6"
CHAPTER_SHA="5b7410cb55007b42bed9f2cdcb9fdb0111e5a964"
PREV_SHA="64396b4e7527ba1586737b9b23d9373bd6a98881"
READER_SHA="e74d3edd1ac8606f350f41270f1ca8fb7b65c03f"
WORDS=9258
TOTAL=277463
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def gitblob(p):
 data=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
def rows(s):
 return [(int(n),f,sha,int(w)) for n,f,sha,w in re.findall(r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$",s,re.M)]
def body(s,f,sha):
 a=f"<!-- BEGIN 2016_CAUSAL {f} | git_blob {sha} -->\n\n"
 b=f"\n\n<!-- END 2016_CAUSAL {f} -->"
 assert s.count(a)==s.count(b)==1,f
 return s.split(a,1)[1].split(b,1)[0]
class ChapterFortyDonkeyReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=(BASE/OLD).read_text()
  cls.scene=(BASE/SCENE).read_text()
  cls.ch=(BASE/CHAPTER).read_text()
  cls.prev=(BASE/PREV).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.a=rows(cls.prev);cls.b=rows(cls.reader)
 def test_01_original_blob(self): self.assertEqual(gitblob(BASE/OLD),OLD_SHA)
 def test_02_scene_blob(self): self.assertEqual(gitblob(BASE/SCENE),SCENE_SHA)
 def test_03_revised_blob(self): self.assertEqual(gitblob(BASE/CHAPTER),CHAPTER_SHA)
 def test_04_prior_reader_preserved(self): self.assertEqual(gitblob(BASE/PREV),PREV_SHA)
 def test_05_assembled_blob(self): self.assertEqual(gitblob(BASE/READER),READER_SHA)
 def test_06_original_six_movements_exact_renumbered(self):
  old=self.old.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  new=self.ch.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  scene=self.scene.split("### V. The donkey and the broken measure",1)[1].split("\n---\n",1)[0]
  new=new.replace("### V. The donkey and the broken measure"+scene.strip("\n")+"\n\n","")
  new=new.replace("### VI. The part of the cart that stayed","### V. The part of the cart that stayed")
  new=new.replace("### VII. A light where cloth had hung","### VI. A light where cloth had hung")
  self.assertEqual(new,old)
 def test_07_scene_exact_and_substantial(self):
  scene=self.scene.split("### V. The donkey and the broken measure",1)[1].split("\n---\n",1)[0]
  self.assertGreater(len(scene.split()),2000)
  self.assertIn("### V. The donkey and the broken measure"+scene.strip("\n"),self.ch)
 def test_08_headings_seven(self):
  self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.ch,re.M),["I","II","III","IV","V","VI","VII"])
 def test_09_manifest_37(self):
  self.assertEqual(len(self.a),36);self.assertEqual(len(self.b),37)
  self.assertEqual(self.a,self.b[:36])
  self.assertEqual(self.b[36],(37,CHAPTER,CHAPTER_SHA,WORDS))
 def test_10_all_embedded_sources_exact(self):
  for _,f,sha,w in self.b:
   with self.subTest(file=f):
    self.assertEqual(gitblob(BASE/f),sha)
    self.assertEqual(body(self.reader,f,sha),(BASE/f).read_text().rstrip("\n"))
    self.assertEqual(len((BASE/f).read_text().split()),w)
 def test_11_prior_embedded_36_unchanged(self):
  for _,f,sha,_ in self.a:
   self.assertEqual(body(self.prev,f,sha),body(self.reader,f,sha))
 def test_12_counts(self):
  self.assertEqual(len(self.ch.split()),WORDS)
  self.assertEqual(sum(r[3] for r in self.b),TOTAL)
  self.assertIn(f"Source component words including metadata: {TOTAL}",self.reader)
 def test_13_historical_archive_unchanged(self):
  self.assertEqual(gitblob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
 def test_14_protected_hard_canon_unchanged(self):
  for p,sha in PROTECTED.items():self.assertEqual(gitblob(ROOT/p),sha)
 def test_15_exclusive_pov_and_history_firewall(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.ch)
  for bad in ("Edrin thought","Edin knew","Orin wondered","Hessa remembered","keeper thought","stable boy knew"):
   self.assertNotIn(bad,self.ch)
  self.assertIn("UNAUTHENTICATED",self.reader)
 def test_16_donkey_state_and_ch41_approach(self):
  for s in ("Orin placed the rope on the indicated peg","### VII. A light where cloth had hung","Speak to Ina","twenty-one nights"):
   self.assertIn(s,self.ch)
 def test_17_jars_and_water_not_cleared(self):
  for s in ("clean water","No one had proved the unknown water fit for drinking","covered jars"):
   self.assertIn(s,self.ch)
 def test_18_prohibition_and_review_hold(self):
  for s in ("NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","Historical Librarian","Umpire"):
   self.assertIn(s,self.reader)
if __name__=="__main__": unittest.main()
