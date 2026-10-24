from pathlib import Path
import re,unittest
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/"living-novel/production/full-rewrite-2026/G07_RECONSTRUCTED_OPENING_PROLOGUE_CH01_CH02_NONCANON.md"
class Opening(unittest.TestCase):
 def test_three_consecutive_sections(self):
  s=P.read_text()
  for t in ("# PROLOGUE — THE KEEPING OF NAMES","# CHAPTER I — THE FIRST ANSWER","# CHAPTER II — WHAT COMES BACK"):
   self.assertIn(t,s)
 def test_no_removed_institutional_narrator(self):
  prose=P.read_text().split("## Reconstruction transaction status")[0]
  self.assertIsNone(re.search(r"\b(?:Edrin|Oren)\b",prose,re.I))
 def test_source_facts_and_no_belt_theft(self):
  prose=P.read_text().split("## Reconstruction transaction status")[0]
  for v in ("191.90","100.90","Dark Horse","Belt","barber","swamp"):
   self.assertIn(v,prose)
  self.assertNotIn("Jake wore the Belt",prose)
 def test_not_canon_promotion(self):
  s=P.read_text();self.assertIn("Developmental continuous-manuscript candidate",s)
  self.assertIn("not canon-approved",s)
if __name__=="__main__":unittest.main()
