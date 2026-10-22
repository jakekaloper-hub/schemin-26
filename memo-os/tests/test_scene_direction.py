"""Regression tests for additive scene direction preflight."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("scene_direction", ROOT / "memo-os/scene_direction.py")
sd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd)

def scene():
    return {
        "scene_id": "sandbox-01", "beat_id": "B01", "narrative_objective": "show consequence",
        "scene_type": "aftermath", "intensity": "grounded", "character_intentions": [],
        "reference_receipts": [], "blocking": {"positions":"none","eyelines":"n/a",
          "action_axis":"north","physical_contact":"none","silhouette":"gate"},
        "camera": {"position":"north approach","shot_scale":"wide","motivated_light":"dawn",
          "decisive_instant":"gate opens","focal_hierarchy":"gate first"},
        "costume_state": {}, "environment": {"atlas_location":"LOC-SANDBOX",
          "foreground":"stones","midground":"gate","background":"ridge","visible_landmarks":[]},
        "continuity":{"entering_state":"closed","exiting_state":"open","forbidden_mutations":[]},
        "typography_safe": True,"director_route":{"primary":"Visual Direction Lead",
          "counterweight_plan":{"activated":True,"counterweights":["Umpire"]}},
    }

class SceneDirectionTests(unittest.TestCase):
    def test_provenance_registry_never_claims_collaboration(self):
        import json
        profile_path = ROOT / "memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json"
        doc = json.loads(profile_path.read_text())
        self.assertEqual(len(doc["profiles"]), 12)
        self.assertEqual(doc["authority"], "ADVISORY_ONLY")
        self.assertTrue(all(not p["may_approve_release"] and not p["may_override_canon"] for p in doc["profiles"]))
        self.assertTrue(all(p["source_status"] in {"CREDIT_SOURCE_IDENTIFIED", "SOURCE_RESEARCH_REQUIRED"} for p in doc["profiles"]))

    def test_twelve_profiles(self):
        self.assertEqual(len(sd.SPECIALISTS), 12)

    def test_targeted_routing(self):
        names={x["name"] for x in sd.select_specialists("combat")}
        self.assertIn("Rob Alonzo",names)
        self.assertNotIn("Randy Thom",names)

    def test_valid_previs_never_approves_render(self):
        r=sd.preflight(scene())
        self.assertEqual(r["status"],"PREVIS_READY")
        self.assertFalse(r["can_render"])

    def test_missing_geometry_rejected(self):
        p=scene()
        del p["blocking"]["eyelines"]
        self.assertEqual(sd.preflight(p)["status"],"BLOCK")

    def test_missing_director_rejected(self):
        p=scene();p["director_route"]={}
        self.assertEqual(sd.preflight(p)["status"],"BLOCK")

    def test_counterweight_primary_mismatch(self):
        p=scene()
        p["director_route"]["counterweight_plan"]["primary"]="other"
        self.assertEqual(sd.preflight(p)["status"],"BLOCK")

    def test_character_missing_reference_holds(self):
        p=scene();p["character_intentions"]=[{"character_id":"one","objective":"advance"}]
        self.assertEqual(sd.preflight(p)["status"],"HOLD")

    def test_no_generated_typography(self):
        p=scene();p["typography_safe"]=False
        self.assertEqual(sd.preflight(p)["status"],"BLOCK")

    def test_render_gate_rejects_invalid_optional_stage(self):
        import sys
        sys.path.insert(0, str(ROOT / "governance/publication"))
        from week4_render_eligibility import render_eligibility
        p = scene()
        del p["camera"]["position"]
        result = render_eligibility({"scene_direction": p})
        self.assertEqual(result["reason"], "SCENE_DIRECTION_NOT_READY")

    def test_unknown_scene_rejected(self):
        p=scene();p["scene_type"]="spectacle"
        self.assertEqual(sd.preflight(p)["status"],"BLOCK")

if __name__=="__main__":
    unittest.main()
