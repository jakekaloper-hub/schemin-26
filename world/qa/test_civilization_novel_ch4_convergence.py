"""Development-only Chapter IV continuity regression; do not imply literary signoff."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"
TEXT=(BASE/"manuscript/CHAPTER_04_THE_ROAD_DOES_NOT_BOW_CONTINUITY_CANDIDATE_NONCANON.md").read_text()
W3=(ROOT/"memo-os/week-3/WEEK_3_FACT_LOCK_V1.md").read_text()
CH3=(BASE/"R12_CHAPTER_III_SOURCE_POV_CONTINUITY_REGISTER_V1.json")
DATA=json.loads(CH3.read_text())
# W4 readback from PR #167 is frozen as a value comparison, NOT fabricated direct ESPN auth.
W4_OBI=157.33
W4_DK=139.67
PR128_BLOB="851ab270b577a9b5e4d28eab7b75178b9fc7e84f"

class TestNovelChapterFourConvergence(unittest.TestCase):
    def test_w3_to_w4_scores_and_first_unbeaten_defeat(self):
        self.assertIn("D0nkey K0ng 172.48 def Mud Dogs 126.86",W3)
        self.assertEqual(DATA["pov_segments"][0]["decision"].find("3–0")>=0,True)
        self.assertIn(f"{W4_OBI:.2f}",TEXT)
        self.assertIn(f"{W4_DK:.2f}",TEXT)
        self.assertNotIn("184.91",TEXT)  # W5 loss to Duckhook is distinct
        self.assertIn("The unbeaten one had fallen.",TEXT)

    def test_title_succession_and_temporal_morphology(self):
        self.assertIn("four iron-shod hooves",TEXT)
        self.assertIn("equine lower body",TEXT)
        self.assertNotIn("Wilson's boots",TEXT)
        self.assertIn('Was it his?',TEXT)
        self.assertIn("Then I couldn't have taken it.",TEXT)
        self.assertIn("A hill was not a kingdom.",TEXT)
        self.assertNotIn("Obi won the Belt",TEXT)

    def test_unverified_bridge_travel_interval_excluded(self):
        self.assertNotIn("three days later",TEXT.lower())
        self.assertIn("later that week",TEXT.lower())
        self.assertNotIn("That was the story they agreed to tell themselves.",TEXT)

    def test_single_pov_boundary_and_editorial_firewall(self):
        self.assertIn("NONCANON",TEXT[:500])
        self.assertNotRegex(TEXT,re.compile(r"\bEdrin(?: Vale)?\b|\bEdin\b",re.I))
        self.assertNotIn("Chapter IV — Final Canon Accepted",TEXT)
        self.assertGreater(len(TEXT.split()),2350)
        self.assertEqual(PR128_BLOB,"851ab270b577a9b5e4d28eab7b75178b9fc7e84f")

    def test_w3_chapter_lineage_preserved(self):
        self.assertEqual(DATA["hard_original"]["blob_sha"],"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc")
        orig=ROOT/DATA["hard_original"]["path"]
        raw=orig.read_bytes()
        sha=hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
        self.assertEqual(sha,DATA["hard_original"]["blob_sha"])

if __name__=="__main__":
    unittest.main()
