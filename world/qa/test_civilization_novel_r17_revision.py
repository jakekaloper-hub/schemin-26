"""R17 V2 literary-development mechanical smoke tests; not literary acceptance."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
V1=(BASE/"manuscript/THE_SURVEY_LINE_FULL_CAUSAL_MANUSCRIPT_V1_NONCANON.md").read_text()
V2=(BASE/"manuscript/THE_SURVEY_LINE_FULL_CAUSAL_MANUSCRIPT_V2_NONCANON.md").read_text()
D=json.loads((BASE/"R15_SURVEY_LINE_SOURCE_AND_RELEASE_REGISTER_V1.json").read_text())
class TestNovelR17V2Development(unittest.TestCase):
 def test_v1_preserved_and_v2_distinct(self):
  self.assertNotEqual(V1,V2)
  self.assertGreater(len(V2.split()),len(V1.split())+450)
  self.assertIn("NONCANON",V2[:300])
 def test_four_sections_and_two_lawful_owners(self):
  self.assertEqual(re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)",V2),[x["owner"] for x in D["scenes"]])
  self.assertEqual({x["owner"] for x in D["scenes"]},{"CHAR-BOBBY-MITCHELL","CHAR-DAVID-BABB"})
 def test_verified_match_and_source_sites(self):
  self.assertIn("193.73",V2)
  self.assertIn("127.09",V2)
  loc={x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
  for scene in D["scenes"]:self.assertEqual(loc[scene["location"]]["physical_zone_id"],scene["region"])
 def test_new_economic_and_civic_consequences(self):
  for word in ["warehouse","medicine","flour","timber","assessment","damaged support","community"]:
   self.assertIn(word,V2.lower())
  self.assertIn("less money",V2)
  self.assertIn("The elder objected.",V2)
 def test_no_new_canon_or_synthetic_easement(self):
  self.assertEqual(D["promotion"],"HOLD")
  self.assertIn("No land transferred",V2)
  self.assertIn("not a land purchase",V2.lower())
  self.assertNotIn("Edrin Vale",V2)
  self.assertNotIn("ObiWan received the Belt",V2)
if __name__=="__main__": unittest.main()
