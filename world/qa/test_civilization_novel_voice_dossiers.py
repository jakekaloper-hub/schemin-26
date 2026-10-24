"""Fact-and-canon guard for proposed 12-owner Novel voice packets (not prose release)."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BOARD=ROOT/"living-novel/production/full-rewrite-2026"
WORLD=ROOT/"world/data"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def parse_week3_results(text):
    """Exact scoreboard names and numbers, no regex synthesis of hypothetical scores."""
    results={}
    for name,win,opp,lose in re.findall(
        r"(?m)^- (.+?) (\d+\.\d{2}) def (.+?) (\d+\.\d{2})\.$",text
    ):
        if name in results or opp in results:
            raise ValueError("duplicate result pair")
        results[name]={"opponent":opp,"points_for":float(win),"points_against":float(lose),"outcome":"WIN"}
        results[opp]={"opponent":name,"points_for":float(lose),"points_against":float(win),"outcome":"LOSS"}
    return results

class TestNovelVoiceDossiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=load(BOARD/"R2_TWELVE_OWNER_TEMPORAL_VOICE_DOSSIERS_V1.json")
        cls.world=load(WORLD/"owner_domains.json")["domains"]
        cls.locations={x["id"]:x for x in load(WORLD/"locations.json")["locations"]}
        cls.settlements={x["id"]:x for x in load(WORLD/"settlements.json")["settlements"]}
        cls.fact_text=(ROOT/"memo-os/week-3/WEEK_3_FACT_LOCK_V1.md").read_text(encoding="utf-8")
        cls.facts=parse_week3_results(cls.fact_text)
        cls.by_id={x["character_id"]:x for x in cls.doc["paths"]}

    def test_all_twelve_and_verified_six_matches(self):
        self.assertEqual(len(self.doc["paths"]),12)
        self.assertEqual(len(self.by_id),12)
        self.assertEqual(set(self.by_id),{x["character_id"] for x in self.world})
        self.assertEqual(set(self.facts),{x["team"] for x in self.world})
        self.assertEqual(sum(x["outcome"]=="WIN" for x in self.facts.values()),6)

    def test_no_result_fabrication(self):
        for record in self.doc["paths"]:
            with self.subTest(record=record["character_id"]):
                self.assertEqual(record["week3_verified_fact"],self.facts[record["team"]])
                self.assertEqual(record["week3_source"],"memo-os/week-3/WEEK_3_FACT_LOCK_V1.md")
                self.assertEqual(record["temporary_story_time_scope"],"AFTER_WEEK_3_CERTIFICATION_BEFORE_WEEK_4_RESULTS")
        self.assertNotEqual(self.facts["D0nkey K0ng"]["points_for"],999.99)

    def test_owner_home_source_join(self):
        domains={d["character_id"]:d for d in self.world}
        for r in self.doc["paths"]:
            with self.subTest(owner=r["character_id"]):
                domain=domains[r["character_id"]]
                loc=self.locations[domain["primary_location_id"]]
                sett=self.settlements[r["home_world_context_id"]]
                self.assertEqual(r["team"],domain["team"])
                self.assertEqual(r["home_location_id"],domain["primary_location_id"])
                self.assertEqual(r["home_region_id"],loc["physical_zone_id"])
                self.assertEqual(sett["physical_zone_id"],loc["physical_zone_id"])
                self.assertIn(r["home_region_id"],domain["physical_zone_ids"])
                self.assertTrue(r["knowledge_firewall"].strip())
                self.assertTrue(r["real_owner_boundary"].strip())

    def test_unique_elemental_hold(self):
        held=[x for x in self.doc["paths"] if x["narrative_status"]=="ELEMENTAL_POV_ELIGIBILITY_HOLD"]
        self.assertEqual(len(held),1)
        self.assertEqual(held[0]["character_id"],"CHAR-MANNING-WELTY")
        self.assertIn("NO AUTHORISED INTERIOR",held[0]["voice_design"])
        self.assertEqual(
            len([x for x in self.doc["paths"] if x["narrative_status"]=="DEVELOPMENT_ONLY_NOT_PROSE_APPROVED"]),11,
        )

    def test_adversarial_forged_score(self):
        forged=dict(self.by_id["CHAR-WILSON-LOOK"]["week3_verified_fact"],points_for=999.99)
        self.assertNotEqual(forged,self.facts["D0nkey K0ng"])

    def test_adversarial_wrong_team_and_home(self):
        wrong=dict(self.by_id["CHAR-JAKE-KALOPER"],team="D0nkey K0ng")
        self.assertNotEqual(wrong["week3_verified_fact"],self.facts[wrong["team"]])
        wrong_location=dict(self.by_id["CHAR-JAKE-KALOPER"],home_region_id="REG-CENTRAL-BASIN")
        self.assertNotEqual(wrong_location["home_region_id"],self.locations[wrong_location["home_location_id"]]["physical_zone_id"])

if __name__=="__main__":
    unittest.main()
