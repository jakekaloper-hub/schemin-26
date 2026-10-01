#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "world" / "atlas" / "integration" / "validate_publication_convergence.py"

spec = importlib.util.spec_from_file_location("atlas_publication_convergence", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class AtlasPublicationConvergenceTests(unittest.TestCase):
    def payload(self):
        return mod.load_contract()

    def test_repository_contract_passes(self):
        self.assertEqual(mod.validate_repo(), [])

    def test_three_division_kingdom_model_is_rejected(self):
        bad = copy.deepcopy(self.payload())
        bad["binding_principles"]["division_spatial_model"] = "SEALED_TERRITORIES"
        errs = mod.validate_contract(bad)
        self.assertTrue(any("NONEXCLUSIVE_OVERLAY" in e for e in errs))

    def test_image_cannot_promote_world_state(self):
        bad = copy.deepcopy(self.payload())
        bad["binding_principles"]["image_can_mutate_world"] = True
        errs = mod.validate_contract(bad)
        self.assertTrue(any("image_can_mutate_world" in e for e in errs))

    def test_required_cross_os_handoff_cannot_disappear(self):
        bad = copy.deepcopy(self.payload())
        bad["handoffs"] = [
            h for h in bad["handoffs"]
            if not (h["from"] == "location_control_plane" and h["to"] == "novel_os")
        ]
        errs = mod.validate_contract(bad)
        self.assertTrue(any("location_control_plane -> novel_os" in e for e in errs))

    def test_live_counterweight_evidence_requires_changed_decision(self):
        bad = copy.deepcopy(self.payload())
        bad["live_counterweight_evidence"][0]["decision_changed"] = False
        errs = mod.validate_contract(bad)
        self.assertTrue(any("does not prove a changed decision" in e for e in errs))

    def test_all_ten_production_systems_are_declared(self):
        payload = self.payload()
        ids = {x["id"] for x in payload["systems"]}
        self.assertEqual(ids, mod.REQUIRED_SYSTEMS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
