"""2016 causal Chapter XXXI source-exact reader checks; not independent editorial approval."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_HORSE_THAT_CAME_WITHOUT_A_CART_CHAPTER_31_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_31_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_30_NONCANON.md"
CHAPTER_SHA = "057de527cd24fc09a81e689f60c0dac834622791"
READER_SHA = "61df63802ae7000c06dde9efaf1ff1856f99d312"
PREVIOUS_SHA = "48eb9453b05b4ce30fb948badedefdf79c91d8d6"
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
 return [(int(n),name,sha,int(words)) for n,name,sha,words in re.findall(
  r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",text,re.M)]

def passage(text,name,sha):
 start=f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
 end=f"<!-- END 2016_CAUSAL {name} -->"
 assert text.count(start)==1 and text.count(end)==1
 return text.split(start,1)[1].split(end,1)[0].strip()

class ThirtyOneChapterReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=(BASE/CHAPTER).read_text()
  cls.reader=(BASE/READER).read_text()
  cls.old=(BASE/PREVIOUS).read_text()
  cls.manifest=rows(cls.reader)
  cls.old_manifest=rows(cls.old)
  cls.prose=cls.chapter.split("### I.",1)[1].split("\n---\n",1)[0]

 def test_01_manifest_complete_and_ordered(self):
  self.assertEqual([n for n,_,_,_ in self.manifest],list(range(1,32)))
  self.assertEqual(self.manifest[-1],(31,CHAPTER,CHAPTER_SHA,len(self.chapter.split())))

 def test_02_balanced_exact_markers(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "),31)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "),31)
  self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"),1)

 def test_03_all_source_passages_exact(self):
  for n,name,sha,words in self.manifest:
   with self.subTest(chapter=n):
    source=(BASE/name).read_text()
    self.assertEqual(passage(self.reader,name,sha),source.strip())
    self.assertEqual(len(source.split()),words)

 def test_04_manifest_git_hashes(self):
  for n,name,sha,_ in self.manifest:
   with self.subTest(chapter=n): self.assertEqual(blob(BASE/name),sha)

 def test_05_30_chapter_reader_preserved(self):
  self.assertEqual(blob(BASE/PREVIOUS),PREVIOUS_SHA)
  self.assertEqual(self.manifest[:-1],self.old_manifest)

 def test_06_sufficient_narrative_volume(self):
  self.assertEqual(len(re.findall(r"^### [IVX]+\.",self.chapter,re.M)),5)
  self.assertGreaterEqual(len(self.chapter.split()),5000)
  self.assertGreaterEqual(len(self.reader.split()),168000)

 def test_07_exclusive_owner_pov_and_boundary(self):
  self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER",self.chapter)
  self.assertIn("His identification with any historical 2016 league scoring slot remains UNAUTHENTICATED",self.chapter)
  self.assertNotIn("Edrin",self.prose)
  self.assertNotIn("Edin",self.prose)
  self.assertNotIn("Oren",self.prose)

 def test_08_eren_painting_contract_resolved_but_not_fitting(self):
  for phrase in ("Eren counted them herself","That's a new job", "accepted and paid for"):
   self.assertIn(phrase,self.prose)

 def test_09_animal_incident_is_only_fiction(self):
  for phrase in ("She had no cart","a clean diagonal line through it","Someone had cut it with a blade"):
   self.assertIn(phrase,self.prose)
  self.assertIn("invented secondary-world fiction",self.chapter)

 def test_10_carrier_claim_not_ratified(self):
  for phrase in ("I stood surety for no one", "He did not sign in my presence", "I will not pay for a story"):
   self.assertIn(phrase,self.prose)

 def test_11_ina_and_eren_act_independently(self):
  for phrase in ("I'll go with you", "Come at first light", "The guide started up the higher path"):
   self.assertIn(phrase,self.prose)

 def test_12_uncertainty_not_prematurely_closed(self):
  self.assertIn("Pell, the driver, the other horse and the missing freight remain unlocated",self.chapter)
  self.assertIn("No one had returned from the orchard road",self.prose)
  self.assertIn("no verified delivery or reply",self.chapter)
  self.assertIn("the stoneworks kiln passage is sealed",self.chapter)

 def test_13_historical_evidence_untouched(self):
  self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),ARCHIVE_SHA)

 def test_14_protected_main_artifacts_untouched(self):
  for path,sha in PROTECTED.items():
   with self.subTest(path=path):self.assertEqual(blob(ROOT/path),sha)

 def test_15_readback_hashes_and_editorial_hold(self):
  self.assertEqual(blob(BASE/CHAPTER),CHAPTER_SHA)
  self.assertEqual(blob(BASE/READER),READER_SHA)
  self.assertIn("Thirty-one fully assembled",self.reader)
  self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD",self.chapter)
  self.assertIn("No Authors Council, Character Canon/Atlas, Librarian, Umpire or Founder accepted",self.chapter)

if __name__=="__main__":
 unittest.main()
