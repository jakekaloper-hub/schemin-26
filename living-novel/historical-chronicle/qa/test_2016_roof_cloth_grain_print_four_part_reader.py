"""2016 I-VI four-part noncanonical source-exact reader. Mechanical regression checks only."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
READER=BASE/"READING_COPY_2016_CAUSAL_CH01_06_FOUR_PARTS_ROOF_CLOTH_GRAIN_PRINT_NONCANON.md"
PRIOR=BASE/"READING_COPY_2016_CAUSAL_CH01_05_THREE_PARTS_ROOF_CLOTH_GRAIN_NONCANON.md"
SOURCES=[
 ("THE_ROOF_AND_THE_UNCLAIMED_BOWL_2016_CH01_02_CONSOLIDATED_NONCANON.md","011a098cdd760cd820e9fc818ae24097375d3c8e",3564),
 ("THE_CLOTH_AND_THE_LOCK_2016_CH03_04_CONSOLIDATED_NONCANON.md","ccf74ae267e3ffd9ae679c2744c11198e07b7293",7742),
 ("THE_WEIGHT_OF_DRY_GRAIN_CHAPTER_05_NONCANON.md","40d12860e93d9393b18d7771c427061c82e46c8c",4733),
 ("THE_SILENCE_IN_THE_SECOND_PRINTING_CHAPTER_06_NONCANON.md","4e3d655895847e9910b7e8c69349fb2b09c94b4b",4303),
]
READER_SHA="2448e7e1f6a03e1459bc53b0b4be0d418e1e0af7"
PRIOR_SHA="09d5ddd8980cdb12c5641d96914771a10e890477"
WRAP=re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW=re.compile(r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$",re.M)
PROTECTED={
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
def blob(f):
 data=f.read_bytes()
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class FourPartPressReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reading=READER.read_text(encoding="utf-8")
  cls.wraps=WRAP.findall(cls.reading)
  cls.rows=ROW.findall(cls.reading.split("## Part 1 —",1)[0])

 def test_01_new_reader_blob(self):
  self.assertEqual(blob(READER),READER_SHA)

 def test_02_previous_reader_not_replaced(self):
  self.assertEqual(blob(PRIOR),PRIOR_SHA)

 def test_03_four_parts_source_exact_in_order(self):
  self.assertEqual(len(self.wraps),4)
  self.assertEqual(len(self.rows),4)
  for i,((name,sha,words),wrap,row) in enumerate(zip(SOURCES,self.wraps,self.rows),start=1):
   with self.subTest(part=i):
    self.assertEqual([wrap[0],wrap[1],wrap[3]],[name,sha,name])
    self.assertEqual([int(row[0]),row[1],row[2],int(row[3])],[i,name,sha,words])
    source=BASE/name
    self.assertEqual(blob(source),sha)
    self.assertEqual(wrap[2],source.read_text(encoding="utf-8").rstrip("\n"))
    self.assertEqual(len(source.read_text(encoding="utf-8").split()),words)

 def test_04_compression_math(self):
  self.assertEqual(sum(x[2] for x in SOURCES),20342)
  self.assertEqual(21479+4303,25782)
  self.assertEqual(25782-20342,5440)
  self.assertIn("20342 whitespace source words",self.reading)
  self.assertIn("net source reduction **5440**",self.reading)

 def test_05_singer_consent_precedes_unauthorized_print(self):
  ch2=self.wraps[1][2]
  ch4=self.wraps[3][2]
  self.assertIn("Then leave it silent",ch2)
  self.assertIn("I didn't offer it",ch2)
  self.assertIn("the traveling singer's name",ch4)
  self.assertIn("refused the printer's request",ch4)
  self.assertLess(self.reading.index("Then leave it silent"),self.reading.index("By noon a stranger had written"))

 def test_06_distinguish_canvas_and_market_awning(self):
  for phrase in ["canvas was returned","market awning","Grain is not certified safe"]:
   self.assertIn(phrase.lower(),self.reading.lower())

 def test_07_personal_property_and_worker_consent_survive(self):
  for phrase in ["The chest is still in there","reaching frame","two mornings","wheel remained still"]:
   self.assertIn(phrase.lower(),self.reading.lower())

 def test_08_only_one_principal_historical_owner_view(self):
  self.assertIn("CHAR-JAKE-KALOPER",self.reading)
  self.assertIn("not an authenticated manager-account attribution",self.reading)
  self.assertIn("Distinct 2016 Austin-named teams remain separate",self.reading)
  self.assertNotRegex(self.reading,r"(?m)^### (?:Edrin|Edin|Oren)\b")

 def test_09_no_protected_main_changes(self):
  for p,sha in PROTECTED.items():
   with self.subTest(p=p):
    self.assertEqual(blob(ROOT/p),sha)

 def test_10_release_gates_remain_open(self):
  self.assertIn("INDEPENDENT LITERARY/UMPIRE/ATLAS/CHARACTER",self.reading)
  self.assertIn("not a Founder-approved publication",self.reading)
  self.assertIn("Original 72-chapter manuscript remains separate",self.reading)

if __name__=="__main__":
 unittest.main()
