"""Chapter XLIV V2: scene, source-exact 41-part reader, invariants and holds."""
import unittest, re, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
ORIGINAL="THE_FLOOR_THAT_COULD_BE_LIFTED_CHAPTER_44_NONCANON.md"
SCENE="THE_FLOOR_THAT_COULD_BE_LIFTED_BOOT_AT_THE_THRESHOLD_CH44_V2_SCENE_NONCANON.md"
CHAPTER="THE_FLOOR_THAT_COULD_BE_LIFTED_BOOT_AT_THE_THRESHOLD_CH44_V2_NONCANON.md"
PRIOR="READING_COPY_2016_CAUSAL_CH01_43_FORTY_PARTS_THREAD_NO_DIRECTION_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_44_FORTY_ONE_PARTS_BOOT_THRESHOLD_NONCANON.md"
SHAS={ORIGINAL:"e3250efd8dbc4df8a1dceba6b663d1f45159aaf3",SCENE:"cfff217578f1504f203d4161ebe7cb3e9387828f",CHAPTER:"d450ee2b725201f6d1660613b5880450f63c62d6",PRIOR:"0519fc6ef7f81787acb2a239fc9072c5dfb62beb",READER:"b8ea32a932cfeeebc0f5f359ed90eed0a776918d"}
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def gitblob(p):
 b=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\0"+b).hexdigest()
def rows(s):
 pat=r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$"
 return [(int(i),name,sha,int(words)) for i,name,sha,words in re.findall(pat,s,re.M)]
def block(doc,name,sha):
 a="<!-- BEGIN 2016_CAUSAL "+name+" | git_blob "+sha+" -->"
 b="<!-- END 2016_CAUSAL "+name+" -->"
 assert doc.count(a)==1 and doc.count(b)==1
 return doc.split(a+"\n\n",1)[1].split("\n\n"+b,1)[0]
class TestFortyFourBootV2(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=(BASE/ORIGINAL).read_text()
  cls.scene=(BASE/SCENE).read_text().rstrip("\n")
  cls.chapter=(BASE/CHAPTER).read_text()
  cls.prior=(BASE/PRIOR).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.prev=rows(cls.prior)
  cls.current=rows(cls.reader)
 def test_01_pinned_blobs(self):
  for n,h in SHAS.items():
   with self.subTest(n=n): self.assertEqual(gitblob(BASE/n),h)
 def test_02_substantial_original_scene(self): self.assertGreaterEqual(len(self.scene.split()),1800)
 def test_03_seven_movements(self):
  self.assertEqual(re.findall(r"^### ([IVX]+)\.",self.chapter,re.M),["I","II","III","IV","V","VI","VII"])
 def test_04_original_six_movement_body_exact(self):
  def narrative(s): return s.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  restored=narrative(self.chapter).replace(self.scene+"\n\n","")
  for new,old in [("### V. What an account could not carry","### IV. What an account could not carry"),("### VI. The person who knew where to hold","### V. The person who knew where to hold"),("### VII. A place without his name","### VI. A place without his name")]: restored=restored.replace(new,old)
  self.assertEqual(restored,narrative(self.src))
 def test_05_scene_inserted_once(self): self.assertEqual(self.chapter.count(self.scene),1)
 def test_06_reader_manifest_41(self):
  self.assertEqual(len(self.prev),40)
  self.assertEqual(len(self.current),41)
  self.assertEqual(self.current[:40],self.prev)
  self.assertEqual(self.current[40],(41,CHAPTER,SHAS[CHAPTER],8545))
 def test_07_prior_40_embeds_identical(self):
  for _,n,h,_ in self.prev:
   with self.subTest(n=n): self.assertEqual(block(self.reader,n,h),block(self.prior,n,h))
 def test_08_all_41_sources_exact(self):
  for _,n,h,w in self.current:
   with self.subTest(n=n):
    data=(BASE/n).read_text().rstrip("\n")
    self.assertEqual(gitblob(BASE/n),h)
    self.assertEqual(block(self.reader,n,h),data)
    self.assertEqual(len(data.split()),w)
 def test_09_chapter_count(self): self.assertEqual(len(self.chapter.split()),8545)
 def test_10_total_count(self): self.assertEqual(sum(x[3] for x in self.current),316215)
 def test_11_reader_wrapper_count(self): self.assertIn("Source component words including metadata: 316215",self.reader)
 def test_12_reader_markers(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),41)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),41)
 def test_13_owner_pov(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
 def test_14_no_supporting_interior_in_new_scene(self):
  for x in ("Sela thought","Nella knew","Tam remembered","Meric wondered","Fara realized","Edrin","Edin"):
   self.assertNotIn(x,self.scene)
 def test_15_self_contained_family_scene(self):
  for x in ("Sela","Nella","Tam","Meric","boot","cart","Jake"):
   self.assertIn(x,self.scene)
 def test_16_necessary_consequences_preserved(self):
  for x in ("four coins","Pell","Hessa","correction","second horse","twenty-one"):
   self.assertIn(x,self.chapter.lower() if x=="four coins" else self.chapter)
 def test_17_protected_hard_canon_unchanged(self):
  for n,h in PROTECTED.items():
   with self.subTest(n=n): self.assertEqual(gitblob(ROOT/n),h)
 def test_18_evidence_bytes_unchanged(self):
  p=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
  self.assertEqual(gitblob(p),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
 def test_19_hold_explicit(self):
  for x in ("NONCANON","UNAUTHENTICATED","NO MERGE","NO PUBLICATION","NO CANON PROMOTION"):
   self.assertIn(x,self.chapter)
   self.assertIn(x,self.reader)
 def test_20_no_unsupported_competitive_event_in_scene(self):
  for x in ("ESPN","Flaim","standings","playoff","championship"):
   self.assertNotIn(x,self.scene)
if __name__=="__main__": unittest.main()
