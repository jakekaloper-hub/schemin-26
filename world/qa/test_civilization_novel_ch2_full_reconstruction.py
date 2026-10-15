"""Fail-closed developmental acceptance suite for Chapter II manuscript reconstruction.

Passing asserts source-consistency, not literary quality, league-provider finality,
live director participation, or canon/publication acceptance.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT / "living-novel" / "production" / "full-rewrite-2026"
REGISTER = json.loads((PRODUCTION / "R9_CHAPTER_II_TEN_CARD_CAUSAL_CONTINUITY_REGISTER_V1.json").read_text())
CHAPTER = (ROOT / REGISTER["manuscript_path"]).read_text()
LEGACY = (ROOT / REGISTER["old_hard_manuscript_path"]).read_text()
LOC = {x["id"]:x for x in json.loads((ROOT/"world/data/locations.json").read_text())["locations"]}
CONTEXT = {x["id"]:x for x in json.loads((ROOT/"world/data/settlements.json").read_text())["settlements"]}


def git_blob_sha(source):
    content = source.read_bytes()
    return hashlib.sha1(f"blob {len(content)}\0".encode()+content).hexdigest()


def scene_has_valid_source_location(scene):
    if not scene["location_id"]:
        return False
    loc = LOC.get(scene["location_id"])
    ctx = CONTEXT.get(scene["context_id"])
    return bool(loc and ctx and
                loc["physical_zone_id"]==scene["region_id"] and
                ctx["physical_zone_id"]==scene["region_id"] and
                scene["location_id"] in ctx.get("anchor_location_ids",[]))


class TestChapterTwoFullReconstruction(unittest.TestCase):
    def test_original_chapter_is_bit_exact_and_new_draft_noncanonical(self):
        self.assertEqual(git_blob_sha(ROOT/REGISTER["old_hard_manuscript_path"]),REGISTER["old_hard_blob_sha"])
        self.assertNotEqual(CHAPTER,LEGACY)
        self.assertEqual(REGISTER["status"],"FULL_LENGTH_DEVELOPMENT_CANDIDATE_NOT_CANON")
        self.assertIn("NOT CANON",CHAPTER[:360])
        self.assertGreater(len(CHAPTER.split()),5300)

    def test_exactly_four_separate_pov_sections_three_unique_owners(self):
        markers=re.findall(r"(?m)^\*\*POV: (CHAR-[A-Z-]+)\b",CHAPTER)
        self.assertEqual(markers,[scene["owner"] for scene in REGISTER["pov_sequence"]])
        self.assertEqual(markers,[
            "CHAR-BRANDON-PRYOR","CHAR-BOBBY-MITCHELL",
            "CHAR-PHILLIP-PITTS","CHAR-BRANDON-PRYOR"
        ])
        self.assertEqual(len(set(markers)),3)
        self.assertNotRegex(CHAPTER,re.compile(r"\bEdrin(?: Vale)?\b|\bEdin\b",re.I))

    def test_all_ten_existing_migration_cards_accounted(self):
        self.assertEqual(REGISTER["migration_totals"]["full_source_scene_count"],19)
        self.assertEqual(REGISTER["migration_totals"]["source_chapter_i"],9)
        self.assertEqual(REGISTER["migration_totals"]["source_chapter_ii"],10)
        cards=REGISTER["card_disposition"]
        self.assertEqual(len(cards),10)
        self.assertEqual({x["id"] for x in cards},{f"CHAPTER_02_S{i:02d}" for i in range(1,11)})
        self.assertEqual({x["state"] for x in cards if x["id"]=="CHAPTER_02_S10"},{"DEFERRED_EXPLICITLY"})
        self.assertEqual(REGISTER["prologue_candidate"]["status"],"UNCHANGED_NONCANON_DEVELOPMENT_BASE")

    def test_all_six_week_two_scores_match_hard_chapter_witness(self):
        self.assertEqual(len(REGISTER["score_witnesses"]),6)
        for entry in REGISTER["score_witnesses"]:
            for value in ("winner_score","loser_score"):
                number=f'{entry[value]:.2f}'
                with self.subTest(team=entry["winner"],number=number):
                    self.assertIn(number,LEGACY)
                    self.assertIn(number,CHAPTER)
            self.assertIn(entry["winner"].lower(),LEGACY.lower())
            self.assertIn(entry["loser"].lower(),LEGACY.lower())
        red=REGISTER["score_witnesses"][0]
        self.assertEqual([red["winner"],red["winner_score"],red["loser_score"]],
                         ["Red Leopards",191.9,100.9])
        self.assertEqual(REGISTER["source_authority"],
                         "APPROVED_MANUSCRIPT_WITNESS_NOT_FRESH_PROVIDER_FACT_TRANSACTION")

    def test_geography_two_anchors_valid_two_venues_blocked(self):
        rows=REGISTER["pov_sequence"]
        self.assertEqual(len([r for r in rows if r["location_id"] is None]),2)
        for row in rows:
            if row["location_id"] is None:
                self.assertFalse(scene_has_valid_source_location(row))
                self.assertIn("UNRESOLVED",row["location_status"])
            else:
                self.assertTrue(scene_has_valid_source_location(row),row["section"])
        altered=dict(rows[1],region_id="REG-UPPER-VALLEYS")
        self.assertFalse(scene_has_valid_source_location(altered))
        altered=dict(rows[2],location_id="LOC-FICTIONAL-BARBER")
        self.assertFalse(scene_has_valid_source_location(altered))

    def test_material_character_and_time_canon(self):
        self.assertIn("By the time he set them down, the familiar dreadlocks were gone.",CHAPTER)
        self.assertIn("three, joined to one serpentine body",CHAPTER)
        self.assertIn("four iron-shod equine legs",CHAPTER)
        self.assertIn("D0nkey K0ng.",CHAPTER)
        self.assertIn("Mud Dogs.",CHAPTER)
        self.assertIn("Belt",CHAPTER)
        self.assertNotIn("Sonic chili dog",CHAPTER)
        self.assertNotIn("Week Three",CHAPTER)
        self.assertNotIn("3–0",CHAPTER)

    def test_release_gate_and_no_forged_event(self):
        self.assertEqual(REGISTER["approval"]["canon_transaction"],"HOLD")
        self.assertEqual(REGISTER["approval"]["founder_approval"],"HOLD")
        self.assertEqual(REGISTER["approval"]["independent_editor"],"HOLD")
        self.assertEqual(REGISTER["approval"]["atlas_exact_places"],"TWO_UNRESOLVED")
        self.assertNotEqual(REGISTER["approval"]["technical_validation"],"PASSED_INDEPENDENT_CANON_RELEASE")
        self.assertNotIn("CANON_ACCEPTED",CHAPTER[:250])


if __name__=="__main__":
    unittest.main()
