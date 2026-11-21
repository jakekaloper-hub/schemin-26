import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"

def load(name):
    p=BASE/f"{name}.py"
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

w9=load("adapt_week9_matchups")
scenes_mod=load("adapt_week9_scenes")
prov=load("provenance_graph")
metrics=load("production_metrics")
sec=load("security_policy")
comp=load("build_compiler_manifest")
inv=load("dependency_invalidation")

class DirectorLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week=w9.compile_week9(release_accepted=False)
        cls.events=cls.week["events"]
        cls.encounters=cls.week["encounters"]
        cls.scenes=scenes_mod.compile_scenes()
        cls.manifest=comp.build_manifest(cls.events,cls.scenes,"week9-source-hold")

    def test_beat_writer_scene_coverage(self):
        self.assertGreaterEqual(len(self.scenes),18)
        self.assertEqual({s["event_id"] for s in self.scenes},{e["event_id"] for e in self.events})

    def test_architect_scene_source_mapping_is_explicit(self):
        for s in self.scenes:
            self.assertIn("source_mapping",s)
            self.assertTrue(s["source_mapping"]["source_beat_ids"])

    def test_scout_librarian_provenance_has_no_escalation(self):
        graph=prov.provenance_nodes(self.events,self.encounters,self.scenes,self.manifest)
        self.assertEqual(prov.authority_escalations(graph),[])

    def test_analyst_metrics_expose_hold_risk(self):
        report=metrics.report(self.events,self.encounters,self.scenes)
        self.assertEqual(report["coverage"]["events"],6)
        self.assertEqual(report["coverage"]["event_to_scene_coverage"],1.0)
        self.assertEqual(report["risk"]["provisional_events"],6)
        self.assertEqual(report["risk"]["world_writeback_enabled"],0)

    def test_warden_blocks_private_intelligence(self):
        self.assertTrue(sec.enforce_public_story_boundary({"copy":"public matchup text"}))
        with self.assertRaises(ValueError):
            sec.enforce_public_story_boundary({"copy":"Mercer-private trade strategy"})

    def test_setup_man_jobs_are_blocked_until_scene_gate(self):
        self.assertTrue(self.manifest["jobs"])
        self.assertTrue(all(j["status"]=="BLOCKED" for j in self.manifest["jobs"]))

    def test_umpire_partial_recompile_is_selective(self):
        first=self.scenes[0]
        impacted=inv.impacted_nodes(self.manifest["invalidation"]["dependency_edges"],[first["scene_id"]])
        expected={j["job_id"] for j in self.manifest["jobs"] if j["depends_on"]==[first["scene_id"]]}
        self.assertEqual(set(impacted),expected)
        unrelated={j["job_id"] for j in self.manifest["jobs"] if j["depends_on"]!=[first["scene_id"]]}
        self.assertTrue(unrelated.isdisjoint(set(impacted)))

if __name__=="__main__":
    unittest.main()
