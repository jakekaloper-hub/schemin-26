"""Development-only source, POV, geography and succession regression for Chapter III."""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/"living-novel/production/full-rewrite-2026"
PACKET=json.loads((PROD/"R12_CHAPTER_III_SOURCE_POV_CONTINUITY_REGISTER_V1.json").read_text())
CHAPTER=(ROOT/PACKET["manuscript_path"]).read_text()
ORIGINAL=ROOT/PACKET["hard_original"]["path"]
FACTS=ROOT/PACKET["week3_fact_lock"]["path"]
LOCATION={x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
CONTEXT={x["id"]:x for x in json.loads((ROOT/"world/data/settlements.json").read_text())["settlements"]}


def git_blob(path):
    b=path.read_bytes()
    return hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()


def parse_locked_results(text):
    matches=re.findall(
        r"(?m)^- (.+?) (\d+\.\d{2}) def (.+?) (\d+\.\d{2})\.$",text
    )
    return [{
        "winner":winner,"winner_points":float(w_score),
        "loser":loser,"loser_points":float(l_score),
    } for winner,w_score,loser,l_score in matches]


def validate_location(s):
    l=LOCATION.get(s["location_id"]);ctx=CONTEXT.get(s["context_id"])
    return bool(
        l and ctx and s["region_id"]==l["physical_zone_id"]
        and s["region_id"]==ctx["physical_zone_id"]
        and s["location_id"] in ctx.get("anchor_location_ids",[])
        and s["site_canon_status"]==l["canon_status"]
    )


class ChapterThreeReconstructionAcceptance(unittest.TestCase):
    def test_hard_original_and_fact_lock_bytes_unchanged(self):
        self.assertEqual(git_blob(ORIGINAL),PACKET["hard_original"]["blob_sha"])
        self.assertEqual(git_blob(FACTS),PACKET["week3_fact_lock"]["blob_sha"])

    def test_full_length_new_prose_and_release_firewall(self):
        self.assertEqual(PACKET["status"],"FULL_LENGTH_DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertGreater(len(CHAPTER.split()),4900)
        self.assertNotEqual(CHAPTER,ORIGINAL.read_text())
        self.assertIn("NONCANON",CHAPTER[:300])
        self.assertEqual(PACKET["approval"]["canon_promotion"],"HOLD")
        self.assertEqual(PACKET["approval"]["literary_human_review"],"NOT_DONE")

    def test_three_distinct_principal_pov_sections_only(self):
        owners=re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)\b",CHAPTER)
        self.assertEqual(owners,["CHAR-WILSON-LOOK","CHAR-JAKE-KALOPER","CHAR-AUSTIN-BYARS"])
        self.assertEqual(owners,[s["character_id"] for s in PACKET["pov_segments"]])
        self.assertNotRegex(CHAPTER,re.compile(r"\bEdrin(?: Vale)?\b|\bEdin\b",re.I))

    def test_all_six_exact_weekthree_approved_scores(self):
        facts=parse_locked_results(FACTS.read_text())
        self.assertEqual(len(facts),6)
        wanted=[{k:s[k] for k in ("winner","winner_points","loser","loser_points")}
                for s in PACKET["score_witness"]]
        self.assertEqual(facts,wanted)
        for item in wanted:
            self.assertIn(f'{item["winner_points"]:.2f}',CHAPTER)
            self.assertIn(f'{item["loser_points"]:.2f}',CHAPTER)
        self.assertEqual({s["event_id"] for s in PACKET["score_witness"]},
                         {"2026-W03-OBI-TDS","2026-W03-DK-MUD",
                          "2026-W03-CHILI-DUCKHOOK","2026-W03-RED-SLOB",
                          "2026-W03-BYARS-CHINS","2026-W03-LLC-ELNINO"})

    def test_wilson_body_hair_and_noncoronation(self):
        self.assertIn("four-legged equine body",CHAPTER)
        self.assertIn("four iron-shod hooves",CHAPTER)
        self.assertNotIn("beneath one boot",CHAPTER)
        self.assertIn("Below the top.",CHAPTER)
        self.assertIn("Did I buy it?",CHAPTER)
        self.assertIn("They had not given him the Belt.",CHAPTER)
        self.assertIn("hair grow back",CHAPTER)  # negative image: a misleading drawing
        self.assertIn("barber disagreed",CHAPTER)
        self.assertNotIn("Snake had grown his dreadlocks back",CHAPTER)

    def test_source_joined_scene_geography_and_negative_cases(self):
        for s in PACKET["pov_segments"]:
            with self.subTest(s=s["segment"]):
                self.assertTrue(validate_location(s))
        changed=dict(PACKET["pov_segments"][0],region_id="REG-UPPER-VALLEYS")
        self.assertFalse(validate_location(changed))
        fabricated=dict(PACKET["pov_segments"][1],location_id="LOC-FABRICATED-LAKE-CITY")
        self.assertFalse(validate_location(fabricated))
        fakepermanent=dict(PACKET["pov_segments"][2],site_canon_status="PERMANENT_CANON")
        self.assertFalse(validate_location(fakepermanent))

    def test_fact_lock_separates_keeper_and_chili_wager_stories(self):
        self.assertIn("Achane",CHAPTER)
        self.assertIn("SECONDARY_STORY_EVIDENCE_NEEDS_ROSTER_TRANSACTION_VETTING",
                      PACKET["pov_segments"][2]["keeper_achane_claim"])
        self.assertNotIn("Achane",FACTS.read_text())
        names={o["object"] for o in PACKET["development_story_objects"]}
        self.assertIn("Sonic chili dog",names)
        self.assertIn("white flag / $100 wager receipt",names)
        self.assertNotIn("Sonic chili dog",ORIGINAL.read_text())

    def test_temporal_week2_to_week3_invariants(self):
        prev=PACKET["previous_opening"]
        c2=(ROOT/prev["chapter_02"]).read_text()
        self.assertIn("two names remained unbeaten",c2)
        self.assertIn("the familiar dreadlocks were gone",c2)
        self.assertNotIn("172.48",c2)
        self.assertIn("Three and zero",CHAPTER)
        self.assertNotIn("Week Four",CHAPTER)
        self.assertNotIn("157.33",CHAPTER)

    def test_adversarial_forged_result_or_status(self):
        falsified=dict(PACKET["score_witness"][1],winner_points=172.49)
        source=parse_locked_results(FACTS.read_text())[1]
        self.assertNotEqual(falsified["winner_points"],source["winner_points"])
        self.assertNotEqual("PUBLISHED",PACKET["status"])
        self.assertEqual(PACKET["approval"]["scoring"],"WEEK3_LOCK_PRESENT_FINAL_PUBLISHER_CHECK_OUTSTANDING")


if __name__=="__main__":
    unittest.main()
