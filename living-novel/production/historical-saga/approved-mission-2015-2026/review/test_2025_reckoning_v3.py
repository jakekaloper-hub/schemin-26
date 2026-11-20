"""2025 historical reading collection V3: source, assembly, owner, and hard-canon firewall.

This is deterministic quality control, not a human literary/Umpire review,
not fresh ESPN data, and not authorization to publish a four-POV causal chapter.
"""
from __future__ import annotations
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "SCHEMIN_26_PROJECT_MISSION.md").exists())
BASE = ROOT / "living-novel/production/historical-saga/approved-mission-2015-2026/manuscript/2025-reckoning"
ORIGINAL = BASE / "THE_PLACE_LEFT_EMPTY.md"
V2 = BASE / "THE_PLACE_LEFT_EMPTY_EXPANDED_V2_NONCANON.md"
NEW = BASE / "THE_LINE_HE_LEFT_VISIBLE_DUCKHOOK_NONCANON.md"
V3 = BASE / "THE_PLACE_LEFT_EMPTY_EXPANDED_V3_NONCANON.md"
REGISTER = BASE / "SCENE_REGISTER_V3.json"
SOURCE = ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
HARD_CH1 = ROOT / "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md"
HARD_CH1_BLOB_SHA = "26a17f05eb0565e7648c29add03ee9580ec933c3"
OWNERS = ["CHAR-JAKE-KALOPER", "CHAR-AUSTIN-BYARS", "CHAR-ZACH-WILSON",
          "CHAR-PHILLIP-PITTS", "CHAR-JAKE-KALOPER", "CHAR-AUSTIN-BYARS",
          "CHAR-JAKE-KALOPER", "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER"]
POV_NAMES = ["Jake", "Austin", "Zach", "Phillip", "Jake", "Austin", "Jake", "Austin", "Jake"]


def sections(text):
    positions = list(re.finditer(r"^## ([IVX]+)\. (.+)$", text, re.M))
    return [(m.group(1), m.group(2),
             text[m.end():positions[i+1].start() if i + 1 < len(positions) else None].strip())
            for i, m in enumerate(positions)]


def sha_blob(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()


class Historical2025DuckhookV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v2 = V2.read_text()
        cls.v3 = V3.read_text()
        cls.insert = NEW.read_text()
        cls.old = sections(cls.v2)
        cls.new = sections(cls.v3)
        cls.register = json.loads(REGISTER.read_text())
        cls.events = {x["id"]: x for x in json.loads(SOURCE.read_text())["matchups"]}

    def test_nine_sequential_scene_labels(self):
        self.assertEqual(len(self.old), 8)
        self.assertEqual(len(self.new), 9)
        self.assertEqual([x[0] for x in self.new], ["I","II","III","IV","V","VI","VII","VIII","IX"])
        self.assertEqual([x[1].rsplit(" — ", 1)[-1] for x in self.new], POV_NAMES)

    def test_old_v2_bodies_exactly_preserved(self):
        for i, old in enumerate(self.old):
            with self.subTest(scene=i):
                self.assertEqual(old[2], self.new[i if i < 2 else i+1][2])

    def test_duckhook_insert_exact_prose(self):
        self.assertIn("\n---\n", self.insert)
        independent_body = self.insert.split("\n---\n",1)[1].strip()
        self.assertEqual(independent_body,self.new[2][2])
        self.assertGreaterEqual(len(independent_body.split()),1800)
        self.assertGreaterEqual(len(self.v3.split()),9000)

    def test_2025_event_receipts_match_source(self):
        expected = {
            "HIST-2025-SEMIFINAL-1":("ObiWan Jacoby",174.38,"Three Dreaded Snake",153.20),
            "HIST-2025-SEMIFINAL-2":("The Immortal",152.20,"Dr. Duckhook",151.80),
            "HIST-2025-CHAMPIONSHIP-1":("The Immortal",161.07,"ObiWan Jacoby",109.56),
        }
        for event_id,(winner,score,loser,other) in expected.items():
            with self.subTest(event_id=event_id):
                row=self.events[event_id]
                self.assertEqual((row["winner"],float(row["winner_score"]),row["loser"],float(row["loser_score"])),(winner,score,loser,other))
                for n in (score,other):
                    self.assertIn(f"{n:.2f}",self.v3)

    def test_duckhook_lacks_future_knowledge(self):
        self.assertNotRegex(self.new[2][2], r"\b(?:161\.07|109\.56|2026)\b")
        self.assertIn("before the season's final",self.insert)

    def test_preserve_exclusive_principal_pov(self):
        self.assertEqual([x["pov_character_id"] for x in self.register["scenes"]],OWNERS)
        self.assertEqual(len(self.register["scenes"]),9)
        self.assertEqual(len(set(OWNERS)),4)
        self.assertNotRegex(self.v3,r"\b(?:Edrin|Edin|Master Oren)\b")
        self.assertIn("four canonical principal POVs",self.v3)

    def test_four_pov_exception_unapproved(self):
        self.assertEqual(self.register["status"],"HISTORICAL_DRAFT_NONCANON_REVIEW_HOLD")
        self.assertIn("NOT_REQUESTED_OR_APPROVED",self.register["primary_pov_exception_status"])
        self.assertIn("not",self.register["collection_kind"].lower())
        self.assertIn("NOT",self.v3.split("---",1)[0])
        self.assertEqual(self.register["independent_umpire"],"NOT_ACCEPTED")

    def test_raw_owner_and_historical_venue_remain_unknown(self):
        self.assertEqual(self.register["historical_geography"],"PROPOSED_UNAPPROVED")
        self.assertIn("UNKNOWN",self.register["source_ownership_warning"])
        self.assertIn("UNKNOWN",self.v3)
        self.assertIn("PROPOSED_UNAPPROVED",self.v3)
        for scene in self.register["scenes"]:
            self.assertEqual(scene["raw_human_owner_binding"],"UNKNOWN")
            self.assertEqual(scene["historical_venue_status"],"PROPOSED_UNAPPROVED")

    def test_retain_protected_hard_ch1_blob(self):
        self.assertEqual(sha_blob(HARD_CH1.read_bytes()),HARD_CH1_BLOB_SHA)

    def test_new_scene_metadata_does_not_claim_release(self):
        self.assertIn("NONCANON",self.insert)
        self.assertIn("not",self.insert.lower())
        self.assertIn("NOT",self.v3.split("---",1)[0])
        self.assertFalse(self.register["active_schema_replacement"])
        self.assertEqual(self.register["founder_promotions"],"NOT_AUTHORIZED")


if __name__ == "__main__":
    unittest.main()
