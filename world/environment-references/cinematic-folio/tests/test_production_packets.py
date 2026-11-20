"""Third-pass production-packet contract: source-derived metadata, never image generation."""
import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

FOLIO = Path(__file__).resolve().parents[1]
ROOT = FOLIO.parents[2]
PACKETS_PATH = FOLIO / "site" / "data" / "production_packets.json"
WORLD = json.loads((FOLIO / "site" / "data" / "world.json").read_text())
sys.path.insert(0, str(FOLIO))
from production_packets import compile_packets


class ProductionPacketsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(PACKETS_PATH.read_text())

    def test_baseline_complete_and_uniquely_coded(self):
        self.assertEqual(self.payload["status"], "CODE_ONLY_SOURCE_INDEX_NO_IMAGE_GENERATION")
        locs = self.payload["locations"]
        regs = self.payload["regions"]
        self.assertEqual({p["location_id"] for p in locs},
                         {l["id"] for l in WORLD["locations"]})
        self.assertEqual(len(locs), 23)
        self.assertEqual(len({p["packet_id"] for p in locs}), 23)
        self.assertEqual({p["region_id"] for p in regs},
                         {r["id"] for r in WORLD["regions"]})
        self.assertEqual(len(regs), 7)

    def test_location_packs_prohibit_render_or_canon_promotion(self):
        locs = {l["id"]: l for l in WORLD["locations"]}
        for packet in self.payload["locations"]:
            loc = locs[packet["location_id"]]
            self.assertEqual(packet["authority"], "MAIN_WORLD_ENGINE")
            self.assertEqual(packet["current_state_as_of"], "end_of_week_3_2026")
            self.assertFalse(packet["render_permitted"])
            self.assertIsNone(packet["approved_cinematic_uri"])
            self.assertEqual(packet["status"], "SOURCE_INDEX_ONLY")
            self.assertTrue(packet["proposed_output_path"].endswith("/CANDIDATE_MASTER_16x9.png"))
            self.assertEqual(packet["location_id"], loc["id"])
            self.assertEqual(packet["region_id"], loc["physical_zone_id"])
            self.assertEqual(packet["home_character_id"], loc["home_character_id"])
            self.assertEqual(packet["landmarks"], loc["persistent_landmarks"])
            self.assertEqual(packet["access_route_ids"], loc["access_route_ids"])

    def test_source_cards_are_byte_exact_and_constraints_preserved(self):
        for packet in self.payload["locations"]:
            source = ROOT / packet["source_location_card"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                             packet["source_card_sha256"])
            card = json.loads(source.read_text())
            self.assertEqual(card["prohibited_inventions"], packet["prohibited_inventions"])
            self.assertEqual(card["weather_relationships"], packet["weather_relationships"])
            self.assertEqual(card["reference_status"]["visual_reference_status"],
                             "MISSING_APPROVED_VISUAL_REFERENCE")

    def test_draft_island_is_not_an_active_location_packet(self):
        island = self.payload["island"]
        self.assertEqual(island["authority"], "UNMERGED_PR_322_PROPOSAL")
        self.assertFalse(island["render_permitted"])
        self.assertFalse(island["main_world_mutated"])
        self.assertEqual(len(island["node_ids"]), 23)
        self.assertEqual(len(island["venue_ids"]), 9)
        self.assertTrue(set(island["node_ids"]).isdisjoint(
            p["location_id"] for p in self.payload["locations"]))

    def test_period_candidates_are_metadata_not_pictures(self):
        records = self.payload["historical_event_candidates"]
        self.assertEqual(len(records), len(WORLD["events"]))
        self.assertEqual({x["source_event_id"] for x in records},
                         {e["id"] for e in WORLD["events"]})
        for row in records:
            self.assertFalse(row["render_permitted"])
            self.assertIsNone(row["asset_uri"])
            self.assertEqual(row["review_status"], "SOURCE_EVIDENCE_ONLY")

    def test_region_packs_are_not_invented_maps(self):
        zones={r["id"]:r for r in WORLD["regions"]}
        for p in self.payload["regions"]:
            ref=zones[p["region_id"]]
            self.assertEqual(p["physical_terrain"],ref["environment"]["terrain"])
            self.assertEqual(p["climate"],ref["environment"]["climate"])
            self.assertFalse(p["render_permitted"])
            self.assertEqual(p["status"],"SOURCE_INDEX_ONLY")

    def test_rejects_noncanonical_or_escaped_card_paths(self):
        poisoned = copy.deepcopy(WORLD)
        poisoned["locations"][0]["source_location_card"] = "../../../../private/key.json"
        with self.assertRaisesRegex(ValueError, "Noncanonical Location Card path"):
            compile_packets(poisoned, ROOT)
        poisoned = copy.deepcopy(WORLD)
        poisoned["locations"][0]["id"] = "LOC-../../private"
        with self.assertRaisesRegex(ValueError, "Unsafe or malformed location ID"):
            compile_packets(poisoned, ROOT)

    def test_data_output_is_reproducible(self):
        output=subprocess.run([sys.executable,str(FOLIO/"build_folio.py"),"--check"],
                              cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(output.returncode,0,output.stdout+output.stderr)


if __name__=="__main__":
    unittest.main()
