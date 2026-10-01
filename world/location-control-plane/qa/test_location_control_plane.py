#!/usr/bin/env python3
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"world"/"location-control-plane"/"compiler"))
from location_control_plane import resolve_location, resolve_homeland, resolve_sublocation, compile_world_packet, relationship

class LocationControlPlaneTests(unittest.TestCase):
    def load(self,p):
        return json.loads((ROOT/p).read_text())

    def test_card_counts(self):
        h=self.load("world/location-control-plane/registries/HOMELAND_CARD_REGISTRY.json")
        l=self.load("world/location-control-plane/registries/LOCATION_CARD_REGISTRY.json")
        self.assertEqual(h["count"],12)
        self.assertEqual(l["count"],23)

    def test_all_active_locations_resolve(self):
        src=self.load("world/data/locations.json")
        self.assertEqual(len(src["locations"]),23)
        for loc in src["locations"]:
            self.assertEqual(resolve_location(loc["id"])["status"],"CURRENT_LOCATION_RESOLVED")

    def test_all_homelands_resolve(self):
        src=self.load("world/data/owner_domains.json")
        self.assertEqual(len(src["domains"]),12)
        for d in src["domains"]:
            self.assertEqual(resolve_homeland(d["character_id"])["status"],"CURRENT_HOMELAND_RESOLVED")

    def test_candidate_firewall(self):
        x=resolve_location("CAND-CHAMP-LAST-FIELD")
        self.assertEqual(x["status"],"HUMAN_REVIEW_REQUIRED")
        self.assertEqual(x["reason"],"CANDIDATE_NOT_ACTIVE")

    def test_unknown_location_blocks(self):
        self.assertEqual(resolve_location("LOC-NOT-REAL")["status"],"HUMAN_REVIEW_REQUIRED")

    def test_home_and_away_relationships(self):
        mud=resolve_location("LOC-MUD-DOGS-SWAMP")["location"]
        self.assertEqual(relationship("CHAR-BOBBY-MITCHELL",mud)["relationship"],"HOME_PRIMARY")
        self.assertEqual(relationship("CHAR-JAKE-KALOPER",mud)["relationship"],"AWAY_REACHABLE")

    def test_associated_location_relationship(self):
        shop=resolve_location("LOC-ARSENAL-BARBERSHOP")["location"]
        self.assertEqual(relationship("CHAR-WILSON-LOOK",shop)["relationship"],"HOME_ASSOCIATED")

    def test_country_club_state_hydrated(self):
        cc=resolve_location("LOC-COUNTRY-CLUB-JACKSON")["location"]
        joined=" ".join(cc["current_world_state"]).lower()
        self.assertIn("chili",joined)
        self.assertIn("cleanup",joined)

    def test_sublocation_handle_inherits_parent(self):
        cc=resolve_location("LOC-COUNTRY-CLUB-JACKSON")["location"]
        handle=next(x["handle_id"] for x in cc["addressable_feature_handles"] if x["name"]=="clubhouse")
        sr=resolve_sublocation(handle)
        self.assertEqual(sr["status"],"CURRENT_FEATURE_HANDLE_RESOLVED")
        self.assertEqual(sr["handle"]["parent_location_id"],"LOC-COUNTRY-CLUB-JACKSON")

    def test_visual_reference_required_blocks(self):
        p=compile_world_packet("LOC-COUNTRY-CLUB-JACKSON",["CHAR-ZACH-WILSON"],"VISUAL",require_visual_reference=True)
        self.assertEqual(p["status"],"HUMAN_REVIEW_REQUIRED")
        self.assertIn("MISSING_APPROVED_VISUAL_REFERENCE",p["review_blockers"])

    def test_memo_semantic_packet_ready(self):
        p=compile_world_packet("LOC-TRADE-JEDI-MOUNTAIN-BASE",["CHAR-JAKE-KALOPER"],"MEMO")
        self.assertEqual(p["status"],"READY_FOR_SEMANTIC_QA")

    def test_novel_el_nino_overlay(self):
        p=compile_world_packet("LOC-STORM-BOWL",["CHAR-MANNING-WELTY"],"NOVEL")
        self.assertEqual(p["status"],"READY_FOR_SEMANTIC_QA")
        text=" ".join(p["consumer_overlay"]["constraints"])
        self.assertIn("no interior POV",text)

    def test_no_candidate_cards_in_active_registry(self):
        reg=self.load("world/location-control-plane/registries/LOCATION_CARD_REGISTRY.json")
        self.assertFalse(any(x["location_id"].startswith("CAND-") for x in reg["cards"]))

    def test_phase2_does_not_mutate_candidate_count(self):
        c=self.load("world/data/atlas_location_candidates.json")
        self.assertEqual(len(c["candidates"]),48)

    def test_reference_registry_explicit(self):
        r=self.load("world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json")
        self.assertEqual(len(r["locations"]),23)
        self.assertTrue(all("visual_reference_status" in x for x in r["locations"]))

if __name__=="__main__":
    unittest.main(verbosity=2)
