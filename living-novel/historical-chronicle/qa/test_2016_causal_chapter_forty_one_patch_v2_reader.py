"""Source-exact Chapter XLI V2 and 38-part developmental manuscript checks (NONCANON)."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD="THE_MARKS_AT_THE_CROSSROADS_CHAPTER_41_NONCANON.md"
SCENE="THE_MARKS_AT_THE_CROSSROADS_PRICE_OF_A_PATCH_CH41_V2_SCENE_NONCANON.md"
CHAPTER="THE_MARKS_AT_THE_CROSSROADS_PRICE_OF_A_PATCH_CH41_V2_NONCANON.md"
PREV="READING_COPY_2016_CAUSAL_CH01_40_THIRTY_SEVEN_PARTS_DONKEY_MEASURE_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_41_THIRTY_EIGHT_PARTS_PATCH_NONCANON.md"
OLD_SHA="4526f2c278167c43630aa10732f10e47a8fb1ef1"
SCENE_SHA="5c4cc7c8153b695aa486ae9668a4dc855c592f47"
CHAPTER_SHA="293ff9d63debad3fff7686fa23bdfabb597965d8"
PREV_SHA="e74d3edd1ac8606f350f41270f1ca8fb7b65c03f"
READER_SHA="aa1137b33f35e02828296b6c671fade5b51f5044"
WORDS=10090
TOTAL=287553
PROTECTED={
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
def gitblob(p):
 data=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def rows(s):
 found=[]
 for line in s.splitlines():
  if not line.startswith("| "):continue
  bits=[x.strip() for x in line.split("|")]
  if len(bits)!=6 or not bits[1].isdigit():continue
  n,name,sha,words=bits[1:5]
  if not (name.startswith(chr(96)) and name.endswith(chr(96))):continue
  found.append((int(n),name.strip(chr(96)),sha.strip(chr(96)),int(words)))
 return found
def body(s,f,sha):
 a=f"<!-- BEGIN 2016_CAUSAL {f} | git_blob {sha} -->\n\n"
 b=f"\n\n<!-- END 2016_CAUSAL {f} -->"
 assert s.count(a)==s.count(b)==1,f
 return s.split(a,1)[1].split(b,1)[0]
class ChapterFortyOnePatchV2(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=(BASE/OLD).read_text()
  cls.scene=(BASE/SCENE).read_text()
  cls.ch=(BASE/CHAPTER).read_text()
  cls.prev=(BASE/PREV).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.a=rows(cls.prev)
  cls.b=rows(cls.reader)
 def test_01_original_blob(self):self.assertEqual(gitblob(BASE/OLD),OLD_SHA)
 def test_02_scene_blob(self):self.assertEqual(gitblob(BASE/SCENE),SCENE_SHA)
 def test_03_revised_blob(self):self.assertEqual(gitblob(BASE/CHAPTER),CHAPTER_SHA)
 def test_04_prior_reader_unchanged(self):self.assertEqual(gitblob(BASE/PREV),PREV_SHA)
 def test_05_reader_blob(self):self.assertEqual(gitblob(BASE/READER),READER_SHA)
 def test_06_substantial_scene(self):self.assertGreater(len(self.scene.split()),2000)
 def test_07_seven_movements(self):
  self.assertEqual(re.findall(r"^### ([IVX]+)\.",self.ch,re.M),["I","II","III","IV","V","VI","VII"])
 def test_08_six_original_movements_exact(self):
  old=self.old.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  new=self.ch.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  new=new.replace(self.scene.strip()+"\n\n","").replace("### VII. The unpainted space","### VI. The unpainted space")
  self.assertEqual(new,old)
 def test_09_scene_embedded_once(self):self.assertEqual(self.ch.count(self.scene.strip()),1)
 def test_10_manifest_38_and_prefix(self):
  self.assertEqual(len(self.a),37)
  self.assertEqual(len(self.b),38)
  self.assertEqual(self.a,self.b[:37])
  self.assertEqual(self.b[-1],(38,CHAPTER,CHAPTER_SHA,WORDS))
 def test_11_prior_embedded_components_exact(self):
  for _,f,sha,_ in self.a:
   with self.subTest(file=f):self.assertEqual(body(self.reader,f,sha),body(self.prev,f,sha))
 def test_12_38_embedded_sources_exact(self):
  for _,f,sha,w in self.b:
   with self.subTest(file=f):
    self.assertEqual(gitblob(BASE/f),sha)
    self.assertEqual(body(self.reader,f,sha),(BASE/f).read_text().rstrip("\n"))
    self.assertEqual(len((BASE/f).read_text().split()),w)
 def test_13_source_counts(self):
  self.assertEqual(len(self.ch.split()),WORDS)
  self.assertEqual(sum(x[3] for x in self.b),TOTAL)
  self.assertIn(f"Source component words including metadata: {TOTAL}",self.reader)
 def test_14_protected_main_bytes_unchanged(self):
  for p,sha in PROTECTED.items():
   with self.subTest(path=p):self.assertEqual(gitblob(ROOT/p),sha)
 def test_15_historical_archive_unchanged(self):
  self.assertEqual(gitblob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
 def test_16_pov_is_restricted(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.ch)
  for term in ("Edrin thought","Edin knew","Sela thought","Orin wondered","Hessa remembered","The girl knew"):
   self.assertNotIn(term,self.scene)
 def test_17_ground_safety_not_certified(self):
  for term in ("I don't know what it will do in the rain","I sell nails","Sela","Jake"):
   self.assertIn(term,self.scene)
  self.assertNotIn("the ground was safe",self.scene.lower())
 def test_18_private_room_and_apprentice_states(self):
  for term in ("twenty-one nights","Sela","apprentice","six travelers","NO MERGE"):
   self.assertIn(term,self.ch)
 def test_19_no_fabricated_scoring_in_scene(self):
  for term in ("ESPN","Flaim","playoff","championship"):
   self.assertNotIn(term,self.scene)
 def test_20_release_holds(self):
  for term in ("NONCANON","UNAUTHENTICATED","Umpire","NO PUBLICATION","NO CANON PROMOTION"):
   self.assertIn(term,self.reader)

if __name__=="__main__":
 unittest.main()
