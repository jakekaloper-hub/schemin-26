import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/"planning"/"render-adapter"
spec=importlib.util.spec_from_file_location("render_contract_validator",BASE/"contract_validator.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def base_request(profile):
    return {
        "schema_version":"1.0",
        "request_id":"TEST-1",
        "profile":profile,
        "authority":{
            "project_control_receipt":"PROJECT_CONTROL_REGISTRY.md",
            "character_authority":"ACTIVE_CHARACTER_CANON_AT_EXECUTION",
            "world_authority":"World Engine V1.1",
            "publication_authority":"Memo OS V5.5"
        },
        "evidence":{"status":"VERIFIED","freshness":"LOCKED_RELEASE","receipts":["fixture:locked"]},
        "inputs":{},
        "render_directive":{},
        "output_contract":{"artifact_type":"test","provenance_required":True,"qa_gates":["fact","authority"]},
        "safety":{"authority_mutation_allowed":False,"dependency_installation_allowed":False,"external_dependency":"NONE"}
    }

class RenderAdapterCandidateTests(unittest.TestCase):
    def test_candidate_is_not_active(self):
        text=(BASE/"_INDEX.md").read_text()
        self.assertIn("RESEARCH_CANDIDATE / NOT ACTIVE",text)
        self.assertIn("does **not** install",text)

    def test_profiles_keep_external_dependencies_uninstalled(self):
        profiles=json.loads((BASE/"adapter_profiles_v1.json").read_text())
        for profile in profiles["profiles"].values():
            for ext in profile.get("external_research",[]):
                self.assertEqual(ext["dependency_status"],"NOT_INSTALLED")

    def test_character_grounding_passes_with_active_portable_reference(self):
        req=base_request("CHARACTER_GROUNDED_STATIC")
        req["inputs"]={
            "publication_packet":"W4-PAGE-TEST",
            "location_bearing":True,
            "world_packet":"LOC-TEST",
            "character_packets":[{"character_id":"CHAR-TEST","authority_state":"ACTIVE","source_integrity_state":"PASS","render_ready":True,"reference_assets":["repo://canon/test.png"],"mount_receipts":["mount-1"],"capability_receipt_id":"cap-1","execution_receipt_required":True}]
        }
        self.assertEqual(mod.validate_render_request(req),[])

    def test_character_grounding_fails_without_reference(self):
        req=base_request("CHARACTER_GROUNDED_STATIC")
        req["inputs"]={"publication_packet":"P","location_bearing":False,"character_packets":[{"character_id":"X","authority_state":"ACTIVE","source_integrity_state":"SOURCE_BYTES_REQUIRED","render_ready":False,"reference_assets":[],"mount_receipts":[],"capability_receipt_id":None,"execution_receipt_required":False}]}
        errors=mod.validate_render_request(req)
        self.assertTrue(any("render_ready" in e for e in errors))
        self.assertTrue(any("reference_assets" in e for e in errors))
        self.assertTrue(any("source integrity" in e for e in errors))
        self.assertTrue(any("mount_receipts" in e for e in errors))
        self.assertTrue(any("capability receipt" in e for e in errors))
        self.assertTrue(any("execution receipt" in e for e in errors))

    def test_data_story_requires_read_only_verified_sources(self):
        req=base_request("DATA_STORY")
        req["inputs"]={
            "deterministic_data":{"mutation_policy":"READ_ONLY","missing_values_policy":"DO_NOT_INFER","source_receipts":["league:locked"]},
            "data_definitions":{"score":"fantasy points"}
        }
        self.assertEqual(mod.validate_render_request(req),[])
        req["inputs"]["deterministic_data"]["mutation_policy"]="WRITE_BACK"
        self.assertTrue(any("READ_ONLY" in e for e in mod.validate_render_request(req)))

    def test_motion_requires_storyboard_session_and_output_verification(self):
        req=base_request("MOTION")
        req["inputs"]={
            "storyboard_packet_ref":"W4-ISSUE-PREVIS:P1",
            "source_artifacts":["repo://render/source.png"],
            "session":{"session_id":"motion-test","revision":1,"output_verification_required":True}
        }
        self.assertEqual(mod.validate_render_request(req),[])
        req["inputs"]["session"]["output_verification_required"]=False
        self.assertTrue(any("output verification" in e for e in mod.validate_render_request(req)))

    def test_candidate_rejects_dependency_installation_or_authority_mutation(self):
        req=base_request("DATA_STORY")
        req["inputs"]={"deterministic_data":{"mutation_policy":"READ_ONLY","missing_values_policy":"DO_NOT_INFER","source_receipts":["x"]},"data_definitions":{"x":"x"}}
        req["safety"]["external_dependency"]="vizzu"
        req["safety"]["dependency_installation_allowed"]=True
        req["safety"]["authority_mutation_allowed"]=True
        errors=mod.validate_render_request(req)
        self.assertTrue(any("authority mutation" in e for e in errors))
        self.assertTrue(any("dependency installation" in e for e in errors))
        self.assertTrue(any("external dependency" in e for e in errors))

if __name__=="__main__":
    unittest.main()
