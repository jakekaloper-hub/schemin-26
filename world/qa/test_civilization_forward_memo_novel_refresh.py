import importlib.util
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod
MEMO=load("memo-os/tests/validate_issue.py","memo_forward")
NOVEL=load("living-novel/os/qa/twelve_owner_rewrite_gate.py","novel_rewrite")

class ForwardControls(unittest.TestCase):
    def test_twelve_owner_registry(self):
        self.assertEqual(len(NOVEL.canonical_owner_ids()),12)
    def test_reject_edrin_and_nonowner(self):
        errors=NOVEL.validate_rewrite_scene({"pov_character_id":"EDRIN","pov_class":"ARCHIVE_POV",
          "source_event_ids":["W3"],"world_context_id":"CTX","story_time_cutoff":"W3",
          "real_owner_boundary_note":"fiction","manuscript_text":"Edrin knew."})
        self.assertIn("NON_OWNER_POV_FORBIDDEN",errors)
        self.assertIn("RETIRED_INSTITUTIONAL_CHARACTER_IN_MANUSCRIPT",errors)
    def test_owner_scene_valid(self):
        scene={"pov_character_id":"CHAR-JAKE-KALOPER","pov_class":"PRINCIPAL_CHARACTER",
          "source_event_ids":["EVT-W3"],"world_context_id":"SETCTX-CENTRAL-BASIN",
          "story_time_cutoff":"AFTER_WEEK_3","real_owner_boundary_note":"fictional only",
          "manuscript_text":"The Trade Jedi studied the verified result."}
        self.assertEqual(NOVEL.validate_rewrite_scene(scene),[])
    def test_future_memo_hold(self):
        result=MEMO.validate_future_week_world_gate(season=2026,week=6,location_id="LOC-LEAGUE-CHAMBER",
          fact_lock_sha256="a"*64,character_reference_verified=False,final_artifact_verified=False)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["blockers"]),2)
    def test_invalid_week_rejected(self):
        result=MEMO.validate_future_week_world_gate(season=2026,week=99,location_id="LOC-LEAGUE-CHAMBER",
          fact_lock_sha256="a"*64,character_reference_verified=True,final_artifact_verified=True)
        self.assertFalse(result["ok"])
if __name__=="__main__":
    unittest.main()
