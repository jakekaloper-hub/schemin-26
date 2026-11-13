import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
OUT=BASE/"generated/2026"
sys.path.insert(0,str(BASE))

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

consumer=load("build_downstream_consumers") if (BASE/"build_downstream_consumers.py").exists() else None
season_mod=load("adapt_2026_memo_season")
compiler_mod=load("build_2026_season_compiler")

class DownstreamConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.season=season_mod.compile_season()
        cls.compiler=compiler_mod.build()

    def test_consumer_builder_exists(self):
        self.assertIsNotNone(consumer,"build_downstream_consumers.py required")

    def test_web_index_has_all_nine_memos_and_source_status(self):
        data=consumer.build_web_index(self.season,self.compiler)
        self.assertEqual([x["week"] for x in data["memo_issues"]],list(range(1,10)))
        self.assertTrue(all("publication_state" in x for x in data["memo_issues"]))
        self.assertTrue(all("scene_count" in x for x in data["memo_issues"]))

    def test_timeline_is_deterministic_and_chronological(self):
        a=consumer.build_timeline(self.season)
        b=consumer.build_timeline(self.season)
        self.assertEqual(a,b)
        keys=[(x["week"],x["event_id"]) for x in a["entries"]]
        self.assertEqual(keys,sorted(keys))
        self.assertEqual(len(a["entries"]),42)

    def test_timeline_preserves_authority_without_promotion(self):
        data=consumer.build_timeline(self.season)
        by_id={e["event_id"]:e for e in self.season["events"]}
        for row in data["entries"]:
            self.assertEqual(row["evidence_status"],by_id[row["event_id"]]["authority"]["evidence_status"])
            self.assertEqual(row["canon_status"],by_id[row["event_id"]]["authority"]["canon_status"])

    def test_render_queue_contains_no_blocked_jobs_as_ready_requests(self):
        q=consumer.build_render_queue(self.season,self.compiler)
        self.assertEqual(q["ready_count"],0)
        self.assertEqual(q["ready_requests"],[])
        self.assertGreater(q["blocked_count"],0)
        self.assertEqual(q["blocked_count"],len(q["blocked_jobs"]))

    def test_blocked_render_queue_explains_why(self):
        q=consumer.build_render_queue(self.season,self.compiler)
        self.assertTrue(all(x["reason"] for x in q["blocked_jobs"]))

    def test_consumer_outputs_are_persisted_and_match_live_build(self):
        self.assertIsNotNone(consumer)
        expected={
            "web_index.json":consumer.build_web_index(self.season,self.compiler),
            "timeline.json":consumer.build_timeline(self.season),
            "render_queue.json":consumer.build_render_queue(self.season,self.compiler),
        }
        for name,obj in expected.items():
            path=OUT/name
            self.assertTrue(path.is_file(),name)
            self.assertEqual(json.loads(path.read_text()),obj,name)

    def test_web_index_links_only_existing_scene_ids(self):
        data=consumer.build_web_index(self.season,self.compiler)
        scenes={s["scene_id"] for s in self.season["scenes"]}
        for issue in data["memo_issues"]:
            self.assertTrue(set(issue["scene_ids"]).issubset(scenes))

if __name__=="__main__":
    unittest.main()
