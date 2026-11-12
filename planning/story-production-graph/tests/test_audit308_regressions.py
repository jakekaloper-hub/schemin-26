import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
sys.path.insert(0,str(BASE))

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

season_mod=load("adapt_2026_memo_season")
compiler_mod=load("build_compiler_manifest")
season_compiler_mod=load("build_2026_season_compiler")
bridge=load("render_request_bridge")
schema_mod=load("schema_contract_validator") if (BASE/"schema_contract_validator.py").exists() else None

class Audit308RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.season=season_mod.compile_season()
        cls.by_event={e["event_id"]:e for e in cls.season["events"]}
        cls.by_scene={s["scene_id"]:s for s in cls.season["scenes"]}
        cls.manifest=season_compiler_mod.build()

    def test_w1_authority_remains_unresolved_without_release_receipt(self):
        w1=next(i for i in self.season["issues"] if i["week"]==1)
        self.assertNotIn("CANONICAL",w1["publication_state"])
        self.assertIsNone(w1["canonical_artifact"])

    def test_w3_w4_winner_first_sources_do_not_fake_home_away(self):
        for week in (3,4):
            rows=[e for e in self.season["events"] if e["league_time"]["week"]==week]
            self.assertTrue(rows)
            for e in rows:
                r=e["result"]
                self.assertNotIn("home_name",r)
                self.assertNotIn("away_name",r)
                self.assertIn("winner",r)
                self.assertIn("loser",r)

    def test_issue_jobs_fail_closed_on_unreleased_or_external_source(self):
        issue_state={i["issue_id"]:i["publication_state"] for i in self.season["issues"]}
        for job in self.manifest["jobs"]:
            if not job["job_id"].startswith("JOB-MEMO-2026-"):
                continue
            issue_id=job["depends_on"][0]
            state=issue_state[issue_id]
            if state!="RELEASED":
                self.assertEqual(job["status"],"BLOCKED",(issue_id,state,job))

    def test_scene_job_readiness_requires_render_eligible_state_only(self):
        scene=json.loads(json.dumps(self.season["scenes"][0]))
        expected={
            "PLANNED":"BLOCKED","RENDER_ELIGIBLE":"READY","RENDERED":"BLOCKED",
            "QA_PENDING":"BLOCKED","ACCEPTED":"BLOCKED","REJECTED":"BLOCKED",
        }
        for state,want in expected.items():
            scene["qa"]["publication_state"]=state
            m=compiler_mod.build_manifest([], [scene], "test")
            got={j["status"] for j in m["jobs"]}
            self.assertEqual(got,{want},(state,got))

    def test_every_compiler_edge_has_dependency_class(self):
        for edge in self.manifest["invalidation"]["dependency_edges"]:
            self.assertIn("dependency_class",edge,edge)

    def test_week6_encounters_reference_their_scene(self):
        scenes_by_enc={}
        for s in self.season["scenes"]:
            scenes_by_enc.setdefault(s["encounter_id"],[]).append(s["scene_id"])
        for enc in self.season["encounters"]:
            if enc["encounter_id"].startswith("ENC-2026-W06-"):
                self.assertTrue(enc["scene_ids"],enc)
                self.assertEqual(sorted(enc["scene_ids"]),sorted(scenes_by_enc.get(enc["encounter_id"],[])))

    def test_render_request_never_upgrades_provisional_event(self):
        scene=next(s for s in self.season["scenes"] if self.by_event[s["event_id"]]["authority"]["evidence_status"]=="PROVISIONAL")
        event=self.by_event[scene["event_id"]]
        job={"job_id":"JOB-TEST","surface":"PNG","render_profile":"CHARACTER_GROUNDED_STATIC","status":"READY"}
        req=bridge.render_request(job,scene,event=event)
        self.assertEqual(req["evidence"]["status"],"PROVISIONAL")
        self.assertNotEqual(req["evidence"]["freshness"],"LOCKED_RELEASE")

    def test_all_generated_objects_validate_against_declared_schemas(self):
        self.assertIsNotNone(schema_mod,"schema_contract_validator.py required")
        schema_mod.validate_season_graph(self.season,self.manifest)

    def test_persisted_scene_and_chronicle_corpus_exists(self):
        self.assertTrue((BASE/"generated/2026/scenes.json").is_file())
        self.assertTrue((BASE/"generated/2026/chronicle.json").is_file())
        scenes=json.loads((BASE/"generated/2026/scenes.json").read_text())
        chron=json.loads((BASE/"generated/2026/chronicle.json").read_text())
        self.assertEqual(len(scenes["scenes"]),len(self.season["scenes"]))
        self.assertEqual(len(chron["character_timelines"]),12)

    def test_no_render_end_to_end_fixture_preserves_authority(self):
        path=BASE/"fixtures/no_render_e2e.json"
        self.assertTrue(path.is_file())
        d=json.loads(path.read_text())
        self.assertEqual(d["event_authority"],d["render_request_evidence_status"])
        self.assertEqual(d["renderer_execution"],"NOT_EXECUTED")
        self.assertEqual(d["publication_state"],"UNPUBLISHED")

if __name__=="__main__":
    unittest.main()
