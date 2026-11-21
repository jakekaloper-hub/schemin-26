import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

w9=load("adapt_week9_matchups")
sc=load("adapt_week9_scenes")
comp=load("build_compiler_manifest")
inv=load("dependency_invalidation")
chron=load("chronicle_views")
bridge=load("render_request_bridge")

class SelectiveInvalidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week=w9.compile_week9(False)
        cls.scenes=sc.compile_scenes()
        cls.manifest=comp.build_manifest(cls.week["events"],cls.scenes,"week9-hold")
        cls.by_scene={s["scene_id"]:s for s in cls.scenes}

    def test_result_change_does_not_invalidate_setup_scenes(self):
        event=self.week["events"][0]["event_id"]
        impacted=set(inv.impacted_nodes(self.manifest["invalidation"]["dependency_edges"],[f"{event}::RESULT"]))
        result_scenes={s["scene_id"] for s in self.scenes if s["event_id"]==event and f"{event}::RESULT" in s["dependencies"]}
        setup_scenes={s["scene_id"] for s in self.scenes if s["event_id"]==event and f"{event}::RESULT" not in s["dependencies"]}
        self.assertTrue(result_scenes)
        self.assertTrue(result_scenes.issubset(impacted))
        self.assertTrue(setup_scenes.isdisjoint(impacted))

    def test_character_change_targets_only_scenes_with_character(self):
        char=self.week["events"][0]["participants"][0]["entity_id"]
        impacted=set(inv.impacted_nodes(self.manifest["invalidation"]["dependency_edges"],[f"CHAR::{char}"]))
        expected={s["scene_id"] for s in self.scenes if any(c["character_id"]==char for c in s["cast"])}
        self.assertTrue(expected.issubset(impacted))
        unrelated={s["scene_id"] for s in self.scenes if all(c["character_id"]!=char for c in s["cast"])}
        self.assertTrue(unrelated.isdisjoint(impacted))

    def test_full_week9_chronicle_views(self):
        views=chron.character_timelines(self.week["events"],"2026-W09")
        self.assertEqual(len(views),12)
        rel=chron.relationship_histories(self.week["events"],"2026-W09")
        self.assertEqual(len(rel),6)
        place=chron.place_memory(self.week["events"],self.scenes,"2026-W09")
        self.assertEqual(len(place),6)
        artifacts=chron.artifact_custody(self.week["events"],"2026-W09")
        self.assertEqual(artifacts,{})

    def test_render_bridge_fails_closed_for_blocked_job(self):
        job=self.manifest["jobs"][0]; scene=self.by_scene[job["depends_on"][0]]
        self.assertEqual(job["status"],"BLOCKED")
        with self.assertRaises(ValueError):
            bridge.render_request(job,scene)

if __name__=="__main__":
    unittest.main()
