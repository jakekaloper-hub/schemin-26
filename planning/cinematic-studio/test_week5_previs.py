import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
class PrevisTests(unittest.TestCase):
    def test_previs_not_renderer_authorized(self):
        p=json.loads((ROOT/'planning/cinematic-studio/WEEK5_SLOB_CHINS_PREVIS_CANDIDATE.json').read_text())
        self.assertIsNone(p['venue']['location_id'])
        self.assertFalse(p['publication_authorized'])
        self.assertFalse(p['character_boundary']['per_subject_mount_proof'])
        self.assertEqual(len(p['scene_beats']),3)
    def test_evidence_and_character_ids(self):
        p=json.loads((ROOT/'planning/cinematic-studio/WEEK5_SLOB_CHINS_PREVIS_CANDIDATE.json').read_text())
        self.assertEqual({t['character_id'] for t in p['teams']},{'CHAR-BEN-WHIPPLE','CHAR-JORDAN-HOLLINGSHEAD'})
        for ref in p['source_refs']: self.assertTrue((ROOT/ref).is_file(),ref)
        self.assertTrue(p['fact_boundary']['needs_live_espn_reverification'])
    def test_real_scores(self):
        p=json.loads((ROOT/'planning/cinematic-studio/WEEK5_SLOB_CHINS_PREVIS_CANDIDATE.json').read_text())
        scores={t['team']:t['score'] for t in p['teams']}
        self.assertAlmostEqual(scores['Seven Deadly Chins']-scores['Slob on my Dobb'],35.76)

if __name__=='__main__': unittest.main()
