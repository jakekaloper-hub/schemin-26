import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.production.assemble_existing_week3_story_unit import assemble
class AssemblyTests(unittest.TestCase):
    def test_real_editorial_sources_copied_with_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            m=assemble(Path(d))
            self.assertFalse(m["publication_eligible"])
            self.assertTrue((Path(d)/"memo-source.md").stat().st_size>1000)
            self.assertTrue((Path(d)/"novel-source.md").stat().st_size>1000)
            self.assertEqual(len(m["artifacts"]),5)
    def test_repeatability(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            self.assertEqual(assemble(Path(a)),assemble(Path(b)))
    def test_cannot_claim_final_acceptance(self):
        with tempfile.TemporaryDirectory() as d:
            m=assemble(Path(d))
            self.assertIn("SIMULATED_UMPIRE_REVIEW_ONLY",m["blockers"])
if __name__=="__main__":
    unittest.main()
