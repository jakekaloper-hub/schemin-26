#!/usr/bin/env python3
"""Universe OS V1.2 + Atlas Control Plane acceptance suite."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "world" / "engine"))
sys.path.insert(0, str(ROOT / "world" / "location-control-plane" / "compiler"))

from universe_resolver import UniverseResolver  # noqa: E402
from location_control_plane import resolve_location  # noqa: E402


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class UniverseOSV12Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.u = UniverseResolver()
        cls.entities = load("world/data/entities_v2.json")
        cls.domains = load("world/data/domain_profiles_v2.json")
        cls.relationships = load("world/data/location_relationship_graph_v2.json")
        cls.memory = load("world/data/world_memory_v1.json")
        cls.divisions = load("world/data/divisions_v2.json")
        cls.layers = load("world/atlas/ATLAS_LAYER_REGISTRY_V2.json")
        cls.locations = load("world/data/locations.json")
        cls.venue = load("world/data/encounter_venue_policy.json")

    def test_ontology_covers_twelve_principals(self):
        ids = {d["owner_character_id"] for d in self.domains["domains"]}
        self.assertEqual(len(ids), 12)
        self.assertEqual(ids, set(self.u.domains))

    def test_jedi_order_and_obiwan_coexistence(self):
        entity_ids = {e["entity_id"] for e in self.entities["entities"]}
        self.assertIn("ORDER-JEDI", entity_ids)
        pop = self.u.who_lives("LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertIn("ORDER-JEDI", pop.get("communities", []))
        self.assertIn("DO_NOT_MAKE_OBIWAN_ONLY_JEDI", self.u.forbidden("CHAR-JAKE-KALOPER"))

    def test_current_character_locks(self):
        self.assertIn("NO_CHAMPIONSHIP_BELT", self.u.forbidden("CHAR-JAKE-KALOPER"))
        self.assertIn("NO_CENTAUR_ANATOMY", self.u.forbidden("CHAR-WILSON-LOOK"))
        self.assertIn("ONE_BODY_THREE_SERPENT_HEADS", self.u.forbidden("CHAR-PHILLIP-PITTS"))

    def test_singular_principals_do_not_generate_species(self):
        for cid in ("CHAR-AUSTIN-BYARS","CHAR-ZACH-WILSON","CHAR-MANNING-WELTY","CHAR-DAVID-BABB"):
            home = self.u.where_is(cid)["location_id"]
            pop = self.u.who_lives(home)
            self.assertTrue(pop.get("singular_principal"))
            self.assertIn("Mixed ordinary", pop["population_status"])

    def test_wings_is_chicken_wings(self):
        culture = self.u.division_culture("DIV-WINGS")
        self.assertEqual(culture["food_referent"], "chicken_wings")
        forbidden = " ".join(culture["culture_v2"]["forbidden"]).lower()
        self.assertIn("angel", forbidden)
        self.assertIn("bird", forbidden)

    def test_tds_chili_shared_march(self):
        loc = next(x for x in self.locations["locations"] if x["id"]=="LOC-TDS-CHILI-SHARED-MARCH")
        self.assertEqual(set(loc["division_presence_ids"]), {"DIV-BURGERS","DIV-WINGS"})
        shared_edges = [
            e for e in self.relationships["edges"]
            if e["relationship"]=="SHARES_POPULATION_WITH" and "LOC-TDS-CHILI-SHARED-MARCH" in (e["from"], e["to"])
        ]
        self.assertGreaterEqual(len(shared_edges), 2)

    def test_all_home_domains_reach_neutral_network(self):
        neutral = self.venue["neutral_pool"]
        self.assertTrue(neutral)
        for lid in self.venue["home_venues"].values():
            self.assertTrue(any(self._can_route(lid, n) for n in neutral), lid)

    def _can_route(self, a, b):
        try:
            self.u.how_to_travel(a, b)
            return True
        except (KeyError, ValueError):
            return False

    def test_atlas_has_nine_governing_layers(self):
        ids = [x["id"] for x in self.layers["governing_layers"]]
        self.assertEqual(len(ids), 9)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("LAYER-CIVIL", ids)
        self.assertIn("LAYER-ENCOUNTERS", ids)
        self.assertIn("LAYER-HORIZON", ids)

    def test_candidate_layer_not_active_geography(self):
        active_ids = {x["id"] for x in self.locations["locations"]}
        self.assertFalse(any(x.startswith("CAND-") for x in active_ids))
        editorial = self.layers["editorial_layers"][0]
        self.assertEqual(editorial["authority"], "EDITORIAL_ONLY_NOT_ACTIVE_GEOGRAPHY")
        self.assertFalse(editorial["default_visible"])

    def test_world_memory_country_club(self):
        rows = [m for m in self.memory["memories"] if m.get("location_id")=="LOC-COUNTRY-CLUB-JACKSON"]
        self.assertTrue(rows)
        classes = {c for m in rows for c in m["memory_class"]}
        self.assertIn("HISTORICAL", classes)
        self.assertIn("TEMPORARY", classes)

    def test_existing_location_control_plane_resolves_same_ids(self):
        for loc in self.locations["locations"]:
            result = resolve_location(loc["id"])
            self.assertEqual(result["status"], "CURRENT_LOCATION_RESOLVED")
            self.assertEqual(result["location"]["location_id"], loc["id"])

    def test_domain_profiles_do_not_claim_sovereignty(self):
        for d in self.domains["domains"]:
            self.assertIn("OWNER_DOMAIN_IS_NOT_SOVEREIGN_COUNTRY", d["forbidden_drift"])

    def test_no_renderer_owned_truth(self):
        rules = " ".join(self.layers["rules"]).lower()
        self.assertIn("views over universe data", rules)
        self.assertIn("no layer may mutate", rules)

    def test_el_nino_dual_manifestation(self):
        modes = set(self.u.ontology["el_nino"]["manifestation_modes"])
        self.assertIn("EMBODIED", modes)
        self.assertIn("ATMOSPHERIC_MANIFESTATION", modes)

    def test_memo_novel_art_share_ids(self):
        obiwan = self.u.where_is("CHAR-JAKE-KALOPER")
        self.assertEqual(obiwan["location_id"], "LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertEqual(resolve_location(obiwan["location_id"])["location"]["location_id"], obiwan["location_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
