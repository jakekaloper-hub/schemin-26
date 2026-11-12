import importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
sys.path.insert(0,str(BASE))

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

season_mod=load("adapt_2026_memo_season")
compiler_mod=load("build_2026_season_compiler")
integrity=load("graph_integrity") if (BASE/"graph_integrity.py").exists() else None

class SeniorQualityTimLensTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s1=season_mod.compile_season()
        cls.s2=season_mod.compile_season()
        cls.c1=compiler_mod.build()
        cls.c2=compiler_mod.build()

    def test_repeated_build_is_byte_deterministic(self):
        a=json.dumps({"season":self.s1,"compiler":self.c1},sort_keys=True,separators=(",",":"))
        b=json.dumps({"season":self.s2,"compiler":self.c2},sort_keys=True,separators=(",",":"))
        self.assertEqual(a,b)

    def test_all_primary_ids_are_unique(self):
        self.assertIsNotNone(integrity,"graph_integrity.py required")
        integrity.assert_unique_ids(self.s1,self.c1)

    def test_all_graph_references_resolve(self):
        self.assertIsNotNone(integrity,"graph_integrity.py required")
        integrity.assert_references_resolve(self.s1,self.c1)

    def test_dependency_graph_is_acyclic(self):
        self.assertIsNotNone(integrity,"graph_integrity.py required")
        integrity.assert_acyclic(self.c1["invalidation"]["dependency_edges"])

    def test_compiler_fingerprint_is_sha256_and_stable(self):
        self.assertIn("source_fingerprint_sha256",self.c1)
        fp=self.c1["source_fingerprint_sha256"]
        self.assertRegex(fp,r"^[a-f0-9]{64}$")
        self.assertEqual(fp,self.c2["source_fingerprint_sha256"])

    def test_input_mutation_changes_compiler_fingerprint(self):
        self.assertIsNotNone(integrity,"graph_integrity.py required")
        original=self.c1["source_fingerprint_sha256"]
        season=json.loads(json.dumps(self.s1))
        season["events"][0]["notes"].append("synthetic mutation")
        mutated=integrity.source_fingerprint(season["events"],season["scenes"],season["issues"])
        self.assertNotEqual(original,mutated)

    def test_event_source_receipts_are_in_render_request_provenance_contract(self):
        bridge=load("render_request_bridge")
        event=next(e for e in self.s1["events"] if e["authority"]["evidence_status"]=="VERIFIED")
        scene=next(s for s in self.s1["scenes"] if s["event_id"]==event["event_id"])
        scene=json.loads(json.dumps(scene)); scene["qa"]["publication_state"]="RENDER_ELIGIBLE"
        job={"job_id":"JOB-SENIOR","surface":"PNG","render_profile":"CHARACTER_GROUNDED_STATIC","status":"READY"}
        req=bridge.render_request(job,scene,event=event)
        for receipt in event["authority"]["source_receipts"]:
            self.assertIn(receipt,req["evidence"]["receipts"])

if __name__=="__main__":
    unittest.main()
