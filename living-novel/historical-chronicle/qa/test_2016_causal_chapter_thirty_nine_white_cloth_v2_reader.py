"""Source-exact chapter XXXIX V2 36-part reading copy test suite — NONCANON."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD="THE_STREET_THAT_TURNED_BLUE_CHAPTER_39_NONCANON.md"
SCENE="THE_WHITE_CLOTH_AT_THE_CORNER_CH39_EPILOGUE_V2_NONCANON.md"
CHAPTER="THE_STREET_THAT_TURNED_BLUE_THE_WHITE_CLOTH_AT_CORNER_CH39_V2_NONCANON.md"
PREV="READING_COPY_2016_CAUSAL_CH01_38_THIRTY_FIVE_PARTS_WINDOWS_NONCANON.md"
READER="READING_COPY_2016_CAUSAL_CH01_39_THIRTY_SIX_PARTS_WHITE_CLOTH_NONCANON.md"
OLD_SHA="529fa222dcd1cbf254d5a7235249f4240e29ba66"
SCENE_SHA="0feea5db656adf3cff347c7bda990b23bb47baf6"
CHAPTER_SHA="6baae4538fcfb6fac43e2bd39107a278e48cfae2"
PREV_SHA="c79ebebde7b238b021b8d0e271bd2303d050fd7b"
READER_SHA="64396b4e7527ba1586737b9b23d9373bd6a98881"
WORDS=9164
TOTAL=268205
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def gitblob(path):
 data=path.read_bytes()
 return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()
def rows(s):
 return [(int(n),f,sha,int(w)) for n,f,sha,w in re.findall(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",s,re.M)]
def body(s,f,sha):
 a=f"<!-- BEGIN 2016_CAUSAL {f} | git_blob {sha} -->\n\n"
 b=f"\n\n<!-- END 2016_CAUSAL {f} -->"
 assert s.count(a)==s.count(b)==1, f
 return s.split(a,1)[1].split(b,1)[0]
class ChapterThirtyNineWhiteCloth(unittest.TestCase):
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
 def test_03_revised_blob(self): self.assertEqual(gitblob(BASE/CHAPTER),CHAPTER_SHA)
 def test_04_previous_reader_preserved(self): self.assertEqual(gitblob(BASE/PREV),PREV_SHA)
 def test_05_assembled_reader_blob(self): self.assertEqual(gitblob(BASE/READER),READER_SHA)
 def test_06_original_six_movements_unchanged(self):
  a=self.old.split("### I.",1)[1].split("\n---\n\n### Editorial handoff",1)[0].strip()
  b=self.ch.split("### I.",1)[1].split("### VII.",1)[0].strip()
  self.assertEqual(a,b)
  self.assertEqual(re.findall(r"^### ([IVX]+)\. ",self.ch,re.M),["I","II","III","IV","V","VI","VII"])
 def test_07_2710_plus_new_words_and_scene_exact(self):
  s=self.scene.split("### VII.",1)[1].split("\n---\n",1)[0].rstrip()
  self.assertGreater(len(s.split()),1800)
  self.assertIn("### VII."+s,self.ch)
 def test_08_36_part_manifest(self):
  self.assertEqual(len(self.a),35);self.assertEqual(len(self.b),36)
  self.assertEqual(self.a,self.b[:35])
  self.assertEqual(self.b[35],(36,CHAPTER,CHAPTER_SHA,WORDS))
 def test_09_every_embedded_part_exact(self):
  for _,f,sha,w in self.b:
   with self.subTest(f=f):
    self.assertEqual(gitblob(BASE/f),sha)
    self.assertEqual(body(self.reader,f,sha),(BASE/f).read_text().rstrip("\n"))
    self.assertEqual(len((BASE/f).read_text().split()),w)
 def test_10_previous_35_embedded_bodies_preserved(self):
  for _,f,sha,_ in self.a:
   self.assertEqual(body(self.previous,f,sha),body(self.reader,f,sha))
 def test_11_all_word_counts(self):
  self.assertEqual(len(self.ch.split()),WORDS)
  self.assertEqual(sum(r[3] for r in self.b),TOTAL)
  self.assertIn(f"Source component words including metadata: {TOTAL}",self.reader)
 def test_12_single_canonical_owner_pov(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.ch)
  for prohibited in ("Edrin thought","Edin knew","Seli thought","Mara knew","Fara wondered","Hessa remembered"):
   self.assertNotIn(prohibited,self.ch)
 def test_13_empty_water_jars_not_water_provision(self):
  self.assertIn("The covered water is still owed",self.ch)
  self.assertIn("two empty storage jars",self.ch)
 def test_14_white_sheet_removal_is_on_page(self):
  self.assertIn("Fara took down the sheet",self.ch)
  self.assertIn("The blue remained after the white cloth was gone",self.ch)
 def test_15_original_causal_incident_remains(self):
  for s in ("The blue was already in the street","### VI. The work that was closed","Eren","Ina"):
   self.assertIn(s,self.ch)
 def test_16_history_archive_preserved(self):
  self.assertEqual(gitblob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
 def test_17_2026_protected_manuscript_identical(self):
  for path,sha in PROTECTED.items(): self.assertEqual(gitblob(ROOT/path),sha)
 def test_18_noncanon_and_room_timeline(self):
  for s in ("NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","UNAUTHENTICATED","Chapter XL"):
   self.assertIn(s,self.reader)
if __name__=="__main__": unittest.main()
