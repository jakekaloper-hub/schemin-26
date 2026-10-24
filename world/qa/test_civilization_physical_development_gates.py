#!/usr/bin/env python3
"""G1/G2/G3 physical-development guardrails; editorial data cannot create canon."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/"planning/connected-commonwealth/editorial/TRADE_JEDI_SITE_OPTIONS_G2_2026-10-15.json"

def load(path):
    return json.loads((ROOT/path).read_text())

class CommonwealthPhysicalDevelopmentGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site=json.loads(SITE.read_text())
        cls.locations=load("world/data/locations.json")["locations"]
        cls.routes=load("world/data/routes.json")["routes"]
        cls.zones=load("world/data/physical_zones.json")["regions"]
        cls.owners=load("world/data/owner_domains.json")["domains"]
        cls.candidates=load("world/data/atlas_location_candidates.json")["candidates"]
        cls.handles=load("world/location-control-plane/registries/PARENT_SUBLOCATION_REGISTRY.json")["handles"]

    def test_g1_abstract_position_is_not_metric_measurement(self):
        regions=load("world/data/physical_zones.json")
        self.assertIn("non-metric",regions["coordinate_space"])
        self.assertEqual(self.site["metric_frame_status"],"NOT_SELECTED")
        for key in ("parcel_area_m2","parcel_boundary_m","elevation_datum"):
            self.assertIsNone(self.site[key],key)

    def test_g2_site_uses_existing_canon_sources_only(self):
        active={x["id"]:x for x in self.locations}
        route_ids={x["id"] for x in self.routes}
        handle_ids={x["handle_id"] for x in self.handles}
        owner_ids={x["character_id"] for x in self.owners}
        s=self.site
        self.assertEqual(s["lifecycle_status"],"EDITORIAL_ONLY_NOT_ACTIVE_WORLD_GEOGRAPHY")
        self.assertEqual(s["origin_location_id"],"LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertEqual(s["owner_character_id"],active[s["origin_location_id"]]["owner_character_id"])
        self.assertIn(s["owner_character_id"],owner_ids)
        self.assertEqual(s["physical_zone_id"],active[s["origin_location_id"]]["physical_zone_id"])
        self.assertEqual(s["canonical_abstract_position"],active[s["origin_location_id"]]["abstract_position"])
        self.assertIn(s["related_existing_location_id"],active)
        self.assertIn(s["canonical_access_route_id"],route_ids)
        self.assertTrue(set(s["canonical_feature_handle_ids"]).issubset(handle_ids))
        self.assertEqual(len(s["site_alternatives"]),3)
        self.assertIsNone(s["commissioner_selected_site_id"])
        self.assertEqual(s["reviewer_signoffs"],[])
        self.assertEqual(s["approved_cinematic_reference_ids"],[])

    def test_g2_no_canonical_location_or_property_created(self):
        loc_ids={x["id"] for x in self.locations}
        cand_ids={x["id"] for x in self.candidates}
        all_opts=self.site["site_alternatives"]
        self.assertEqual(len({x["id"] for x in all_opts}),len(all_opts))
        for opt in all_opts:
            with self.subTest(option=opt["id"]):
                self.assertTrue(opt["id"].startswith("SITE-OPT-"))
                self.assertNotIn(opt["id"],loc_ids|cand_ids)
                self.assertTrue(opt["proposal_only"])
                self.assertTrue(opt["ridge_overlook_preserved"])
                self.assertFalse(opt["lake_view_proven"])
                self.assertIsNone(opt["metric_area_m2"])
                self.assertEqual(opt["fictional_building_plan"],"NOT_AUTHORIZED")
                self.assertEqual(opt["site_placement"],"UNRESOLVED")
                self.assertTrue(set(opt["source_feature_handles"]).issubset(self.site["canonical_feature_handle_ids"]))

    def test_g4_exactly_twelve_primary_owner_anchors(self):
        ids={x["id"] for x in self.locations}
        self.assertEqual(len(self.owners),12)
        self.assertEqual(len({x["character_id"] for x in self.owners}),12)
        for d in self.owners:
            with self.subTest(character=d["character_id"]):
                self.assertIn(d["primary_location_id"],ids)

    def test_no_production_authorization_from_site_candidate(self):
        self.assertEqual(self.site["buildings"],[])
        self.assertGreaterEqual(len(self.site["do_not_promote_without"]),5)
        self.assertIn("COMMISSIONER_SITE_SELECTION",self.site["do_not_promote_without"])
        self.assertIn("INDEPENDENT_UMPIRE",self.site["do_not_promote_without"])

if __name__=="__main__":
    unittest.main(verbosity=2)
