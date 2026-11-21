import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"planning/story-production-graph"
sys.path.insert(0,str(BASE))

def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/f"{name}.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

w9=load("adapt_week9_matchups")
sc=load("adapt_week9_scenes")
comp=load("build_compiler_manifest")
mut=load("mutation_exercise")
lineage=load("artifact_lineage")

class ArtifactMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week=w9.compile_week9(False)
        cls.scenes=sc.compile_scenes()
        cls.manifest=comp.build_manifest(cls.week["events"],cls.scenes,"week9-hold")
        cls.by_scene={s["scene_id"]:s for s in cls.scenes}

    def test_real_mutation_exercise(self):
        out=mut.exercise()
        self.assertEqual(out["state"],"SELECTIVE_INVALIDATION_PASS")
        self.assertTrue(all(out["assertions"].values()))

    def test_planned_lineage_does_not_claim_execution(self):
        job=self.manifest["jobs"][0]
        scene=self.by_scene[job["depends_on"][0]]
        receipt=lineage.planned_receipt(job,scene,self.manifest["source_snapshot"])
        self.assertTrue(lineage.assert_no_false_execution(receipt))
        self.assertEqual(receipt["renderer"]["execution_status"],"NOT_EXECUTED")
        self.assertEqual(receipt["artifact"]["status"],"PLANNED")

    def test_false_artifact_claim_is_rejected(self):
        job=self.manifest["jobs"][0]
        scene=self.by_scene[job["depends_on"][0]]
        receipt=lineage.planned_receipt(job,scene,self.manifest["source_snapshot"])
        receipt["artifact"]["status"]="CREATED"
        receipt["artifact"]["path"]="fake.png"
        with self.assertRaises(ValueError):
            lineage.assert_no_false_execution(receipt)

if __name__=="__main__":
    unittest.main()
