import json
import re
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import importlib.util
spec=importlib.util.spec_from_file_location("rewrite_gate",ROOT/"living-novel/os/qa/twelve_owner_rewrite_gate.py")
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
canonical_owner_ids=gate.canonical_owner_ids
validate_rewrite_scene=gate.validate_rewrite_scene
BASE=ROOT/"living-novel/production/full-rewrite-2026"
class RewriteCandidateTests(unittest.TestCase):
    def test_four_manuscripts_and_pov_markers(self):
        register=json.loads((BASE/"SCENE_REGISTER.json").read_text())
        self.assertEqual(len(register["scenes"]),4)
        for scene in register["scenes"]:
            text=(BASE/"manuscript"/scene["file"]).read_text()
            self.assertGreater(len(text.split()),300)
            self.assertTrue(re.search(r"\*\*POV:",text))
            self.assertEqual(validate_rewrite_scene({**scene,"manuscript_text":text}),[])
            for match in re.findall(r"CHAR-[A-Z-]+",text):
                self.assertIn(match,canonical_owner_ids())
    def test_chapter_three_has_three_distinct_owner_povs(self):
        text=(BASE/"manuscript/CHAPTER_03_REWRITE_CANDIDATE.md").read_text()
        self.assertEqual(text.count("**POV:"),3)
        self.assertIn("CHAR-WILSON-LOOK",text)
        self.assertIn("CHAR-JAKE-KALOPER",text)
        self.assertIn("CHAR-AUSTIN-BYARS",text)
    def test_legacy_is_not_overwritten(self):
        self.assertTrue((ROOT/"living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
        self.assertNotEqual((BASE/"manuscript/PROLOGUE_REWRITE_CANDIDATE.md").read_text(),
                            (ROOT/"living-novel/manuscript/PROLOGUE_DRAFT_V1.md").read_text())
if __name__=="__main__":
    unittest.main()
