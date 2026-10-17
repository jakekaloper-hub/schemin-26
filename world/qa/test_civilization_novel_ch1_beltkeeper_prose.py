"""Protect a noncanonical Belt Keeper Chapter I prose pilot against source drift.

This checks historical manuscript witnesses, not ESPN proof, literary merit or independent approval.
"""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"living-novel/production/full-rewrite-2026"

class TestNovelChapterOneBeltKeeperPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet=json.loads((BASE/"R6_CHAPTER_I_S08_SOURCE_AND_PROSE_PACKET_V1.json").read_text())
        cls.prose=(ROOT/cls.packet["source_control"]["new_prose_path"]).read_text()
        cls.historical=(ROOT/cls.packet["source_control"]["historical_witness"]).read_text()
        cls.locations={x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
        cls.settlements={x["id"]:x for x in json.loads((ROOT/"world/data/settlements.json").read_text())["settlements"]}

    def test_source_witness_numbers_and_no_false_provider_attestation(self):
        record=self.packet["scene"]["verified_in_manuscript"]
        self.assertEqual(record["winner"],"ObiWan Jacoby")
        self.assertEqual(record["loser"],"His Majesty's Blood")
        pattern=r"OBIWAN JACOBY — (\d+\.\d{2})\s+HIS MAJESTY'S BLOOD — (\d+\.\d{2})"
        numbers=re.search(pattern,self.historical)
        self.assertIsNotNone(numbers)
        self.assertEqual([float(x) for x in numbers.groups()],
                         [record["winner_points"],record["loser_points"]])
        self.assertEqual(self.packet["source_control"]["historical_evidence_class"],
                         "APPROVED_MANUSCRIPT_WITNESS_NOT_NEW_ESPN_RECEIPT")

    def test_one_canonical_owner_and_belt_not_transferred(self):
        s=self.packet["scene"]
        self.assertEqual(s["pov_character_id"],"CHAR-AUSTIN-BYARS")
        self.assertEqual(s["pov_segment_count"],1)
        self.assertEqual(s["belt_owner_after_match"],"CHAR-AUSTIN-BYARS")
        self.assertEqual(s["story_time_cutoff"],"WEEK_01_POST_RESULT_BEFORE_WEEK_02")
        self.assertIn("**POV:** His Majesty's Blood",self.prose)
        self.assertIn("He had not lost the Belt.",self.prose)
        self.assertNotIn("Edrin Vale",self.prose)
        self.assertNotIn("**POV: ObiWan",self.prose)

    def test_existing_location_not_newly_invented(self):
        scene=self.packet["scene"]
        l=self.locations[scene["location_id"]]
        ctx=self.settlements[scene["world_context_id"]]
        self.assertEqual(l["physical_zone_id"],scene["region_id"])
        self.assertEqual(ctx["physical_zone_id"],scene["region_id"])
        self.assertIn(scene["location_id"],ctx.get("anchor_location_ids",[]))

    def test_explicit_development_firewall(self):
        self.assertEqual(self.packet["status"],"DEVELOPMENT_ONLY_NOT_CANON")
        self.assertEqual(self.packet["scene"]["world_delta_status"],
                         "NO_APPROVED_WORLD_EVOLUTION_TRANSACTION")
        self.assertEqual(self.packet["scene"]["chapter_promotion_status"],"HOLD")
        self.assertIn("NOT CANON",self.prose[:260])
        self.assertGreater(len(self.prose.split()),1800)

    def test_adversarial_score_change_and_location_change(self):
        original=self.packet["scene"]["verified_in_manuscript"]
        self.assertNotEqual(141.71,original["winner_points"])
        wrong_location=self.locations["LOC-TRADE-JEDI-MOUNTAIN-BASE"]
        self.assertNotEqual(wrong_location["physical_zone_id"],
                            self.packet["scene"]["region_id"])
if __name__=="__main__":
    unittest.main()
