"""Invoke the real existing Memo QA and Novel engine, plus Atlas compiler."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_phase3_verification import verify_week3_recap_context
from world.production.build_visual_world_packet import build_packet

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m
    spec.loader.exec_module(m)
    return m

MEMO=load("memo-os/tests/validate_issue.py","phase4_memo")
NOVEL=load("living-novel/os/engine/novel_os.py","phase4_novel")
POV=json.loads((ROOT/"living-novel/production/chapter-03/CHAPTER_03_POV_PACKET_WILSON_V1.json").read_text())

class ActivationTests(unittest.TestCase):
    def test_three_existing_entrypoints_share_context(self):
        event=verify_week3_recap_context()["source_event"]
        loc="LOC-LEAGUE-CHAMBER"
        memo=MEMO.validate_civilization_rehearsal(loc,2026,3,event)
        novel=NOVEL.validate_civilization_manuscript_rehearsal(loc,2026,3,POV,event)
        atlas=build_packet(loc)
        self.assertTrue(memo["ok"],memo)
        self.assertTrue(novel["ok"],novel)
        self.assertEqual(memo["context_id"],novel["context_id"])
        self.assertEqual(memo["context_id"],atlas["civilization_context"]["context_id"])
        self.assertFalse(memo["publication_eligible"])
        self.assertFalse(novel["publication_eligible"])

    def test_no_fabricated_pov(self):
        event=verify_week3_recap_context()["source_event"]
        self.assertEqual(NOVEL.validate_civilization_manuscript_rehearsal("LOC-LEAGUE-CHAMBER",2026,3,{},event)["code"],"INVALID_POV_PACKET")

    def test_unverified_event_blocked(self):
        event=verify_week3_recap_context()["source_event"]
        event.pop("fact_lock_sha256")
        self.assertEqual(MEMO.validate_civilization_rehearsal("LOC-LEAGUE-CHAMBER",2026,3,event)["code"],"MEMO_FACT_PROVENANCE_REQUIRED")
        self.assertEqual(NOVEL.validate_civilization_manuscript_rehearsal("LOC-LEAGUE-CHAMBER",2026,3,POV,event)["code"],"NOVEL_FACT_PROVENANCE_REQUIRED")

    def test_reproducible(self):
        event=verify_week3_recap_context()["source_event"]
        self.assertEqual(MEMO.validate_civilization_rehearsal("LOC-LEAGUE-CHAMBER",2026,3,event),
                         MEMO.validate_civilization_rehearsal("LOC-LEAGUE-CHAMBER",2026,3,event))

if __name__=="__main__":
    unittest.main()
