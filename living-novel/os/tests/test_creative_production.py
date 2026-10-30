"""Fail-closed creative manuscript staging tests."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from creative_production import prepare, stage, ContextError
from creative_context import ROUTER, AUTHORITY, REGISTRY

class CandidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        docs = {ROUTER: json.dumps({"defaults":{"max_matches":2},
                     "routes":[{"id":"chapter","terms":["chapter"],"context_sources":["src.md"]}]}),
                AUTHORITY: "authoritative", REGISTRY:"{}", "src.md":"verified"}
        for path, content in docs.items():
            p=self.root/path; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        self.spec={"task_id":"historical-scene-001","intent":"chapter",
                   "pov":"Canonical POV owner", "chapter_job":"Consequences",
                   "dramatic_question":"What changes?", "location":"Verified place",
                   "opening_pressure":"Risk", "turn":"Reversal", "consequence":"Loss",
                   "open_loop":"Debt", "off_page":"Other league event",
                   "exit_pressure":"Conflict", "source_paths":["src.md"]}
        self.prose=("A causally connected scene unfolds with characters who must choose "
                    "between loyalty and survival. ")*43

    def test_candidate_is_noncanonical(self):
        packet=prepare(self.root,self.spec)
        receipt=stage(self.root,packet,self.prose,self.root/"productions"/"candidate-001")
        self.assertEqual(receipt["release_authority"],"NONE")
        self.assertEqual(receipt["independent_umpire"],"PENDING")
        self.assertTrue((self.root/"productions/candidate-001/candidate.md").exists())

    def test_requires_dossier(self):
        del self.spec["pov"]
        with self.assertRaises(ContextError):prepare(self.root,self.spec)

    def test_rejects_traversal(self):
        self.spec["source_paths"]=["../private"]
        with self.assertRaises(ContextError):prepare(self.root,self.spec)

    def test_rejects_stale_source(self):
        packet=prepare(self.root,self.spec)
        (self.root/"src.md").write_text("changed")
        with self.assertRaises(ContextError):
            stage(self.root,packet,self.prose,self.root/"productions/candidate-001")

    def test_rejects_short_manuscript(self):
        packet=prepare(self.root,self.spec)
        with self.assertRaises(ContextError):
            stage(self.root,packet,"short",self.root/"productions/candidate-001")

    def test_prevents_candidate_overwrite(self):
        packet=prepare(self.root,self.spec)
        path=self.root/"productions/candidate-001"
        stage(self.root,packet,self.prose,path)
        with self.assertRaises(ContextError):stage(self.root,packet,self.prose,path)

if __name__=="__main__":unittest.main()
