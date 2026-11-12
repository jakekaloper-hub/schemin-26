import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
FIX=json.loads((BASE/"fixtures/week9_minimal.json").read_text())

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

inv=load_module("dependency_invalidation",BASE/"dependency_invalidation.py")
chron=load_module("build_chronicle_projection",BASE/"build_chronicle_projection.py")
val=load_module("validate_story_graph",BASE/"validate_story_graph.py")

class StoryGraphTests(unittest.TestCase):
    def test_fixture_structural_pass(self):
        self.assertEqual(val.validate(FIX),[])

    def test_event_change_invalidates_only_declared_downstream(self):
        c=FIX["compiler"]
        impacted=inv.impacted_nodes(c["invalidation"]["dependency_edges"],[FIX["event"]["event_id"]])
        self.assertEqual(impacted,[
          "JOB-W09-M01-MOTION",
          "JOB-W09-M01-PNG",
          "SCN-W09-M01-LAST-PUTT",
        ])

    def test_minimal_rebuild_jobs(self):
        c=FIX["compiler"]
        jobs=inv.minimal_rebuild_jobs(c["invalidation"]["dependency_edges"],[FIX["event"]["event_id"]],c["jobs"])
        self.assertEqual(jobs,["JOB-W09-M01-MOTION","JOB-W09-M01-PNG"])

    def test_character_projection_is_rebuildable_and_derived(self):
        p=chron.character_timeline([FIX["event"]],"CHAR-OBIWAN","2026-W09-postgame")
        self.assertTrue(p["derived_only"]); self.assertTrue(p["rebuildable"])
        self.assertEqual(p["event_ids"],["EVT-W09-DUCKHOOK-OBIWAN"])

    def test_relationship_projection_requires_both_characters(self):
        p=chron.relationship_history([FIX["event"]],"CHAR-DUCKHOOK","CHAR-OBIWAN","2026-W09-postgame")
        self.assertEqual(len(p["entries"]),1)
        q=chron.relationship_history([FIX["event"]],"CHAR-DUCKHOOK","CHAR-NOT-PRESENT","2026-W09-postgame")
        self.assertEqual(q["entries"],[])

if __name__=="__main__":
    unittest.main()
