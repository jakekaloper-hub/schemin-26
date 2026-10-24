import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.production.run_civilization_rehearsal import compile_rehearsal,run

class EndToEndDevelopmentTests(unittest.TestCase):
    def test_real_artifact_emission_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest=run(Path(tmp))
            self.assertFalse(manifest["publication_eligible"])
            self.assertEqual(set(manifest["artifacts"]),{"memo.md","novel.md","atlas.json"})
            for filename in manifest["artifacts"]:
                self.assertTrue((Path(tmp)/filename).stat().st_size>0)
            self.assertEqual(json.loads((Path(tmp)/"atlas.json").read_text())["civilization_context"]["context_id"],manifest["shared_context_id"])
            self.assertIn("136.73–114.50",(Path(tmp)/"memo.md").read_text())
            self.assertIn("not assigned to this event",(Path(tmp)/"novel.md").read_text())
    def test_deterministic_hashes(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            self.assertEqual(run(Path(a)),run(Path(b)))
    def test_no_publication_or_character_art(self):
        result=compile_rehearsal()
        self.assertFalse(result["manifest"]["publication_eligible"])
        self.assertNotIn("image.png",result)
        self.assertIn("EVENT_APPROPRIATE_OWNER_POV_REQUIRED",result["manifest"]["blockers"])

if __name__=="__main__":
    unittest.main()
