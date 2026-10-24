import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/"governance/cross-os/validate_scene_convergence.py"
spec=importlib.util.spec_from_file_location("scene_checker",PATH)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CONTRACT=json.loads((ROOT/"governance/cross-os/SCENE_CONVERGENCE_CONTRACT_V1.json").read_text())

def candidate():
    core={"character_id":"CHAR-TEST","character_source_ref":"test-ref",
          "location_id":"LOC-TEST","world_state_ref":"test-state",
          "verified_event_ref":"test-evidence"}
    views={}
    for consumer in ("memo_os","novel_os","visual_grounding","interactive_atlas"):
        views[consumer]={**core,"narrative_purpose":consumer+" interprets event differently"}
    return {**core,"views":views}

class SceneConvergenceTests(unittest.TestCase):
    def test_active_authorities_exist(self):
        self.assertEqual(module.validate_contract(CONTRACT),[])
    def test_valid_cross_os_scene(self):
        self.assertEqual(module.validate_scene(candidate(),CONTRACT),[])
    def test_character_drift_fails(self):
        obj=candidate();obj["views"]["novel_os"]["character_id"]="CHAR-WRONG"
        self.assertTrue(any("divergent character_id" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_character_source_ref_drift_fails(self):
        obj=candidate();obj["views"]["memo_os"]["character_source_ref"]="obsolete-image-ref"
        self.assertTrue(any("divergent character_source_ref" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_missing_character_source_ref_in_view_fails(self):
        obj=candidate();del obj["views"]["visual_grounding"]["character_source_ref"]
        self.assertTrue(any("divergent character_source_ref" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_world_state_drift_fails(self):
        obj=candidate();obj["views"]["interactive_atlas"]["world_state_ref"]="old"
        self.assertTrue(any("divergent world_state_ref" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_missing_consumer_fails(self):
        obj=candidate();del obj["views"]["visual_grounding"]
        self.assertTrue(any("missing view visual_grounding" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_mercer_private_leak_fails(self):
        obj=candidate();obj["private_mercer_data"]={"trade":"private"}
        self.assertTrue(any("private data" in x for x in module.validate_scene(obj,CONTRACT)))
    def test_image_world_mutation_fails(self):
        obj=candidate();obj["art_claims_canon"]=True
        self.assertTrue(module.validate_scene(obj,CONTRACT))
    def test_contract_fork_fails(self):
        obj=copy.deepcopy(CONTRACT);obj["parent"]="memo-os/_INDEX.md"
        self.assertTrue(any("existing Atlas" in x for x in module.validate_contract(obj)))

if __name__=="__main__": unittest.main()
