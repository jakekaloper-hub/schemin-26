"""Chapter XXXVIII V2: 35 source-exact parts, six archived movements, and prelude provenance."""
import hashlib, re, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD="THE_HAND_THAT_CUT_THE_LEATHER_CHAPTER_38_NONCANON.md"
SCENE="THE_WINDOWS_THAT_WOULD_NOT_STAY_STILL_CH38_PRELUDE_V2_NONCANON.md"
CHAPTER="THE_HAND_THAT_CUT_THE_LEATHER_WINDOWS_THAT_WOULD_NOT_STAY_STILL_CH38_V2_NONCANON.md"
PREV="READING_COPY_2016_CAUSAL_CH01_37_THIRTY_FOUR_PARTS_EMPTY_SECOND_TABLE_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_38_THIRTY_FIVE_PARTS_WINDOWS_NONCANON.md"
OLD_SHA="a6f7f737d2ce79542489094be374f3084f24d657"
SCENE_SHA="b5ac322faf20a108ba4bb495c15d8f7d9e54f61d"
CHAPTER_SHA="e25b7799e18672ba2cffb666d25d7c9b1323ff3d"
PREV_SHA="63d9fcbc3f5fb76438882ca26b5da8b8f821a575"
READER_SHA="c79ebebde7b238b021b8d0e271bd2303d050fd7b"
WORDS=8101
TOTAL=259041
PROTECTED={
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
def gitblob(path):
  b=path.read_bytes()
  return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(s):
  return [(int(n),f,sha,int(w)) for n,f,sha,w in re.findall(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",s,re.M)]
def body(s,f,sha):
  a=f"<!-- BEGIN 2016_CAUSAL {f} | git_blob {sha} -->\n\n"
  b=f"\n\n<!-- END 2016_CAUSAL {f} -->"
  assert s.count(a)==s.count(b)==1,f
  return s.split(a,1)[1].split(b,1)[0]
class ChapterThirtyEightWindows(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=(BASE/OLD).read_text()
  cls.scene=(BASE/SCENE).read_text()
  cls.ch=(BASE/CHAPTER).read_text()
  cls.previous=(BASE/PREV).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.a=rows(cls.previous);cls.b=rows(cls.reader)
 def test_01_original_blob(self): self.assertEqual(gitblob(BASE/OLD),OLD_SHA)
 def test_02_scene_blob(self): self.assertEqual(gitblob(BASE/SCENE),SCENE_SHA)
 def test_03_integrated_blob(self): self.assertEqual(gitblob(BASE/CHAPTER),CHAPTER_SHA)
 def test_04_previous_reader_preserved(self): self.assertEqual(gitblob(BASE/PREV),PREV_SHA)
 def test_05_reader_blob(self): self.assertEqual(gitblob(BASE/READER),READER_SHA)
 def test_06_six_archived_movements_preserved(self):
  a=self.old.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0]
  self.assertIn("### I."+a,self.ch)
  self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.ch,re.M),["I","II","III","IV","V","VI"])
 def test_07_scene_embedded(self):
  part=self.scene.split("### Prelude —",1)[1].split("\n---\n",1)[0].rstrip()
  self.assertIn("### Prelude —"+part,self.ch)
  self.assertLess(self.ch.index("### Prelude —"),self.ch.index("### I."))
  self.assertGreaterEqual(len(part.split()),1700)
 def test_08_manifest_extension(self):
  self.assertEqual(len(self.a),34);self.assertEqual(len(self.b),35)
  self.assertEqual(self.a,self.b[:34])
  self.assertEqual(self.b[34],(35,CHAPTER,CHAPTER_SHA,WORDS))
 def test_09_source_exact_embedded_parts(self):
  for _,f,sha,w in self.b:
   with self.subTest(f=f):
    self.assertEqual(gitblob(BASE/f),sha)
    self.assertEqual(body(self.reader,f,sha),(BASE/f).read_text().rstrip("\n"))
    self.assertEqual(len((BASE/f).read_text().split()),w)
 def test_10_old_embedded_bodies_unchanged(self):
  for _,f,sha,_ in self.a: self.assertEqual(body(self.previous,f,sha),body(self.reader,f,sha))
 def test_11_count_and_words(self):
  self.assertEqual(len(self.ch.split()),WORDS)
  self.assertEqual(sum(r[3] for r in self.b),TOTAL)
  self.assertIn(f"Source component words including metadata: {TOTAL}",self.reader)
 def test_12_bounded_pov(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.ch)
  for prohibited in ("Edrin thought","Edin knew","Seli thought","Mara knew","Fara wondered"):
   self.assertNotIn(prohibited,self.ch)
 def test_13_household_and_letter_not_resolved(self):
  for phrase in ("Seli","Mara","cracked blue bowl","Mev","no word had returned"):
   self.assertIn(phrase,self.ch)
 def test_14_mael_six_movement_event_stays(self):
  for s in ("Mael.","I cut this.","The second cart","The cut on the table"):
   self.assertIn(s,self.ch)
 def test_15_stable_historical_archive(self):
  self.assertEqual(gitblob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
 def test_16_protected_2026(self):
  for p,sha in PROTECTED.items(): self.assertEqual(gitblob(ROOT/p),sha)
 def test_17_release_hold(self):
  for s in ("NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","UNAUTHENTICATED"):
   self.assertIn(s,self.reader)
if __name__=="__main__": unittest.main()
