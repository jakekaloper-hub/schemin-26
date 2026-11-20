#!/usr/bin/env python3
"""Adversarial source-integrity tests for proposed Championship Island topology."""
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = HERE / "validate_island_topology_pin.py"
spec = importlib.util.spec_from_file_location("validate_island_topology_pin", MOD)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class IslandTopologyGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((HERE / "ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json").read_text())
        cls.summit = json.loads((HERE / "PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json").read_text())

    def dataset(self):
        return copy.deepcopy(self.source), copy.deepcopy(self.summit)

    def reject(self, mutate):
        src, summit = self.dataset()
        mutate(src, summit)
        with self.assertRaises(ValueError):
            guard.validate(src, summit)

    @staticmethod
    def source_edge(src, edge_id):
        return next(e for e in src["edge_records"] if e["id"] == edge_id)

    @staticmethod
    def dossier_node(summit, node_id):
        return next(n for n in summit["three_depth_records"] if n["id"] == node_id)

    def test_unmodified_source_and_dossier_pass(self):
        self.assertEqual(guard.validate(*self.dataset())["status"], "PASS_TOPOLOGY_SOURCE_LOCK_NOT_WORLD_CANON")

    def test_stale_declared_41_links_rejected(self):
        self.reject(lambda src, summit: src["source_declared_checks"].__setitem__("edge_count", 41))

    def test_removed_beach_emergency_link_rejected(self):
        self.reject(lambda src, summit: src["edge_records"].__setitem__(
            slice(None), [e for e in src["edge_records"] if e["id"] != "CAND-ISL-EDGE-043"]))

    def test_forged_extra_link_rejected(self):
        def mutation(src, summit):
            fake = copy.deepcopy(src["edge_records"][0])
            fake["id"] = "CAND-ISL-EDGE-046"
            src["edge_records"].append(fake)
        self.reject(mutation)

    def test_public_cannot_enter_secured_contender_venue(self):
        def mutation(src, summit):
            self.source_edge(src, "CAND-ISL-EDGE-026")["modes"].append("public")
            self.dossier_node(summit, "ISLAND_ENTRY_CHECK")["layer1"]["travel_modes"][
                self.dossier_node(summit, "ISLAND_ENTRY_CHECK")["layer1"]["edge_ids"].index("CAND-ISL-EDGE-026")
            ].append("public")
            self.dossier_node(summit, "CONTENDER_FORTRESS")["layer1"]["travel_modes"][
                self.dossier_node(summit, "CONTENDER_FORTRESS")["layer1"]["edge_ids"].index("CAND-ISL-EDGE-026")
            ].append("public")
        self.reject(mutation)

    def test_mismatched_source_edge_mode_rejected(self):
        self.reject(lambda src, summit:
                    self.source_edge(src, "CAND-ISL-EDGE-042")["modes"].remove("post_elimination"))

    def test_direct_source_beach_evacuation_missing_rejected(self):
        def mutation(src, summit):
            self.source_edge(src, "CAND-ISL-EDGE-043")["modes"] = ["service"]
        self.reject(mutation)

    def test_summit_beach_entry_cannot_drift(self):
        self.reject(lambda src, summit:
                    self.dossier_node(summit, "LOSERS_BEACH")["layer1"]["connected_nodes"].remove("EMERGENCY_PIER"))

    def test_summit_beach_site_status_cannot_promote(self):
        self.reject(lambda src, summit: self.dossier_node(summit, "LOSERS_BEACH").__setitem__("status", "PERMANENT_CANON"))

    def test_summit_beach_cannot_be_marked_publicly_released(self):
        self.reject(lambda src, summit: self.dossier_node(summit, "LOSERS_BEACH").__setitem__("public_release", True))

    def test_forged_metric_coordinates_rejected(self):
        self.reject(lambda src, summit: src["node_records"][0].__setitem__("coordinates", [12, 34]))

    def test_bogus_edge_endpoint_rejected(self):
        self.reject(lambda src, summit: self.source_edge(src, "CAND-ISL-EDGE-007").__setitem__("to", "FAKE_NODE"))

    def test_island_zone_cannot_mutate_cross_atlas(self):
        self.reject(lambda src, summit:
                    self.dossier_node(summit, "LOSERS_BEACH")["layer1"].__setitem__("zone", "island_south"))

    def test_explicit_blob_lock_cannot_drift(self):
        self.reject(lambda src, summit: summit.__setitem__("source_topology_blob_sha", "unverified"))

    def test_fewer_nodes_rejected(self):
        self.reject(lambda src, summit: src["node_records"].pop())


if __name__ == "__main__":
    unittest.main(verbosity=2)
