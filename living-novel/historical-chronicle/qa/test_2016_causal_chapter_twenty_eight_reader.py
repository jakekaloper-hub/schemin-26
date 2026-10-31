"""2016 Chapter XXVIII NONCANON source-exact reader and continuity regression checks.
Mechanical evidence only: no Authors Council, Umpire, period Character Canon or canon approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_SLEEVE_LEFT_UNSTITCHED_CHAPTER_28_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_28_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_27_NONCANON.md"
CHAPTER_SHA = "47a8475c2029f5b5b8222adfc72d2a4d17760da0"
READER_SHA = "d273d050f1554a087119df4141e340dd795fed9b"
PREVIOUS_SHA = "41115b3f158e95d423befba4127063480c60e70b"
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
 return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
     r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M)]

def passage(text, name, sha):
 start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
 end = f"<!-- END 2016_CAUSAL {name} -->"
 assert text.count(start) == 1 and text.count(end) == 1, name
 return text.split(start, 1)[1].split(end, 1)[0].strip()

class TwentyEightChapterReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
  cls.reader = (BASE / READER).read_text(encoding="utf-8")
  cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
  cls.manifest = rows(cls.reader)
  cls.old_manifest = rows(cls.old)
  cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

 def test_01_manifest_order_and_final_row(self):
  self.assertEqual([i for i, _, _, _ in self.manifest], list(range(1, 29)))
  self.assertEqual(self.manifest[-1], (28, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

 def test_02_balanced_assembly_markers(self):
  self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 28)
  self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 28)

 def test_03_full_source_exact_reading_copy(self):
  for n, name, sha, words in self.manifest:
   with self.subTest(chapter=n):
    src = (BASE / name).read_text(encoding="utf-8")
    self.assertEqual(passage(self.reader, name, sha), src.strip())
    self.assertEqual(len(src.split()), words)

 def test_04_all_component_blobs_match_manifest(self):
  for n, name, sha, _ in self.manifest:
   with self.subTest(chapter=n):
    self.assertEqual(blob(BASE / name), sha)

 def test_05_prior_reader_immutable(self):
  self.assertEqual(blob(BASE / PREVIOUS), PREVIOUS_SHA)
  self.assertEqual(self.manifest[:27], self.old_manifest)

 def test_06_prior_prose_exactly_preserved(self):
  for _, name, sha, _ in self.old_manifest:
   with self.subTest(path=name):
    self.assertEqual(passage(self.reader, name, sha), passage(self.old, name, sha))

 def test_07_substantial_five_movement_fiction(self):
  self.assertGreaterEqual(len(self.chapter.split()), 5600)
  self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 5)
  self.assertIn("### Editorial handoff", self.chapter)

 def test_08_twelve_owner_pov_boundary(self):
  self.assertIn("Sole limited interior viewpoint", self.chapter)
  self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
  self.assertIn("NOT an authenticated historical ESPN owner-slot association", self.chapter)
  for forbidden in ("Edrin", "Edin", "Oren"):
   self.assertNotIn(forbidden, self.prose)

 def test_09_the_asked_lie_is_not_certified(self):
  self.assertIn("tell her I've been put on the passage", self.prose)
  self.assertIn("He asked me to say he'd been given work. I can't say that", self.prose)
  self.assertIn("I haven't seen him on one today", self.prose)

 def test_10_ina_independent_trade(self):
  self.assertIn("I came to sell cloth", self.prose)
  self.assertIn("I sold it", self.prose)
  self.assertIn("I will hire another pair of hands and go on selling blue", self.prose)

 def test_11_pell_uncertain_alternative(self):
  self.assertIn("They offered hauling for three days", self.prose)
  self.assertIn("After that I don't know", self.prose)
  self.assertIn("Then I'll look for another place", self.prose)

 def test_12_eren_separate_paid_commission(self):
  self.assertIn("She gave me a price. She has given me half", self.prose) if False else self.assertIn("I've given her a price. She has given me half", self.prose)
  self.assertIn("She paid me for knowing how", self.prose)
  self.assertIn("Eren's cart-mark order is partially paid", self.chapter)

 def test_13_2016_historical_source_unchanged(self):
  self.assertEqual(blob(ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"), ARCHIVE_SHA)

 def test_14_hard_canon_protected(self):
  for path, sha in PROTECTED.items():
   with self.subTest(path=path):
    self.assertEqual(blob(ROOT / path), sha)

 def test_15_reader_blob_and_hold(self):
  self.assertEqual(blob(BASE / CHAPTER), CHAPTER_SHA)
  self.assertEqual(blob(BASE / READER), READER_SHA)
  self.assertGreaterEqual(len(self.reader.split()), 151000)
  self.assertIn("Twenty-eight fully assembled", self.reader)
  self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
  self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
  self.assertIn("No author-room or Umpire approval", self.chapter)

if __name__ == "__main__":
 unittest.main()
