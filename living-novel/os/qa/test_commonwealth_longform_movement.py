from pathlib import Path
import unittest,re
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/"living-novel/production/full-rewrite-2026/G07_COMMONWEALTH_LONGFORM_MOVEMENT_THE_PRICE_OF_CERTAINTY_NONCANON.md"
class LongformMovementChecks(unittest.TestCase):
 def test_four_movement_dates_and_noncanon_boundary(self):
  s=P.read_text()
  for h in ("## I. The sign","## II. The price","## III. What fell","## IV. The hill"):
   self.assertIn(h,s)
  self.assertIn("UNREVIEWED NONCANON DRAFT",s)
  self.assertIn("owner UNKNOWN",s)
 def test_not_an_institutional_narrator(self):
  s=P.read_text().split("## Narrative evidence")[0]
  self.assertIsNone(re.search(r"\b(?:edrin|master oren)\b",s,re.I))
 def test_facts_are_present(self):
  s=P.read_text()
  for value in ("116.32","97.96","191.90","100.90","172.48","126.86"):
   self.assertIn(value,s)
 def test_has_substantial_prose(self):
  self.assertGreater(len(P.read_text().split()),1800)
if __name__=="__main__":unittest.main()
