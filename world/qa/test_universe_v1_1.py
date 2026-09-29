#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "world" / "engine" / "validate_world.py"

spec = importlib.util.spec_from_file_location("validate_world", VALIDATOR_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class UniverseV11Tests(unittest.TestCase):
    def payloads(self):
        divisions = mod.load_json("divisions.json")
        locations = mod.load_json("locations.json")
        domains = mod.load_json("owner_domains.json")
        routes = mod.load_json("routes.json")
        ontology = mod.load_json("inhabitant_ontology.json")
        venue = mod.load_json("encounter_venue_policy.json")
        travel = mod.load_repo_json("living-novel/os/geography/world_travel_graph_v1.json")
        return divisions, locations, domains, routes, ontology, venue, travel

    def test_repository_v11_passes(self):
        self.assertEqual(mod.validate_repo(), [])

    def test_exact_2026_division_truth(self):
        divisions, *_ = self.payloads()
        actual = {d["id"]: set(d["member_team_ids_2026"]) for d in divisions["divisions"]}
        self.assertEqual(actual, mod.EXPECTED_DIVISION_MEMBERS)

    def test_wrong_division_membership_fails(self):
        p = list(self.payloads())
        bad = copy.deepcopy(p)
        bad[0]["divisions"][0]["member_team_ids_2026"] = [2, 3, 5, 11]
        errs = mod.validate_universe_extensions(*bad)
        self.assertTrue(any("membership mismatch" in e for e in errs))

    def test_ontology_partition(self):
        *_, ontology, venue, travel = self.payloads()
        flat = []
        for values in ontology["classes"].values():
            flat.extend(values)
        self.assertEqual(len(flat), 12)
        self.assertEqual(len(set(flat)), 12)
        self.assertEqual(
            set(ontology["classes"]["SINGULAR_BEING"]),
            {"CHAR-AUSTIN-BYARS","CHAR-ZACH-WILSON","CHAR-MANNING-WELTY","CHAR-DAVID-BABB"},
        )

    def test_tds_chili_shared_march(self):
        divisions, locations, domains, routes, ontology, venue, travel = self.payloads()
        loc = next(x for x in locations["locations"] if x["id"] == "LOC-TDS-CHILI-SHARED-MARCH")
        self.assertEqual(set(loc["division_presence_ids"]), {"DIV-BURGERS","DIV-WINGS"})
        self.assertEqual(
            set(ontology["shared_cohabitation"]["members"]),
            {"CHAR-PHILLIP-PITTS","CHAR-BRANDON-PRYOR"},
        )

    def test_el_nino_dual_manifestation(self):
        *_, ontology, venue, travel = self.payloads()
        modes = set(ontology["el_nino"]["manifestation_modes"])
        self.assertIn("EMBODIED", modes)
        self.assertIn("ATMOSPHERIC_MANIFESTATION", modes)

    def test_all_twelve_home_venues_resolve(self):
        divisions, locations, domains, routes, ontology, venue, travel = self.payloads()
        self.assertEqual(set(venue["home_venues"]), {str(i) for i in range(1,13)})
        loc_ids = {x["id"] for x in locations["locations"]}
        self.assertTrue(all(v in loc_ids for v in venue["home_venues"].values()))

    def test_major_events_default_neutral(self):
        *_, venue, travel = self.payloads()
        for key in ("GAME_OF_THE_WEEK","PLAYOFF","CHAMPIONSHIP"):
            self.assertEqual(venue["event_rules"][key]["venue_mode"], "NEUTRAL_DEFAULT")

    def test_home_routes_reach_neutral_network(self):
        divisions, locations, domains, routes, ontology, venue, travel = self.payloads()
        g = mod.build_location_graph(routes)
        for home in venue["home_venues"].values():
            self.assertTrue(any(mod.path_exists(g, home, neutral) for neutral in venue["neutral_pool"]), home)

    def test_novel_travel_graph_hydrated(self):
        *_, travel = self.payloads()
        self.assertNotEqual(travel["status"], "SEED_NOT_FULL_MAP")
        self.assertGreater(len(travel["edges"]), 0)

    def test_zero_edge_travel_graph_fails(self):
        p = list(self.payloads())
        bad = copy.deepcopy(p)
        bad[6]["status"] = "SEED_NOT_FULL_MAP"
        bad[6]["edges"] = []
        errs = mod.validate_universe_extensions(*bad)
        self.assertTrue(any("zero approved edges" in e or "SEED_NOT_FULL_MAP" in e for e in errs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
