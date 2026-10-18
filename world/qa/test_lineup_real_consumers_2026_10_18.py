"""Real Memo/Novel and visual-world consumer calls, with image-generation denied."""
import unittest
from unittest.mock import patch
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"world/location-control-plane/adapters"))
from memo_adapter import compile_memo_location_packet
from novel_adapter import compile_novel_location_packet
from world.production.build_visual_world_packet import build_packet

class LineupRuntimeConsumersTests(unittest.TestCase):
    def test_real_memo_and_novel_character_context(self):
        for consumer in (compile_memo_location_packet,compile_novel_location_packet):
            for location,cid in (
                ("LOC-TRADE-JEDI-MOUNTAIN-BASE","CHAR-JAKE-KALOPER"),
                ("LOC-ARSENAL-BARBERSHOP","CHAR-WILSON-LOOK"),
                ("LOC-STORM-BOWL","CHAR-MANNING-WELTY"),
            ):
                with self.subTest(consumer=consumer.__name__,cid=cid):
                    x=consumer(location,[cid])
                    self.assertEqual(x["status"],"READY_FOR_SEMANTIC_QA")
                    self.assertEqual(x["character_visual_authority_status"],"VERIFIED_APPEARANCE_ONLY")
                    self.assertFalse(x["character_rendering_eligible"])
                    self.assertEqual(x["visual_render_release_gate"],"C1_T15_T16_AND_PROVIDER_SOURCE_BINDING_HOLD")
                    self.assertEqual(x["character_visual_authority"]["requested_character_ids"],[cid])
                    self.assertFalse(x["character_visual_authority"]["image_generation_eligible"])
                    self.assertTrue(x["character_physical_constraints"][cid]["anatomy_constraints"])
                    self.assertTrue(x["character_spatial_anchors"][cid]["home_location_id"].startswith("LOC-"))

    def test_corrupted_lineup_never_bypasses_memo_novel_adapters(self):
        with patch("canon.characters.runtime.reference_authority.resolve_approved_lineup_presentation",
                   return_value={"state":"GENERATION_BLOCKED","reason":"LINEUP_OWNER_CROP_SHA256_FAILED"}):
            for consumer in (compile_memo_location_packet,compile_novel_location_packet):
                result=consumer("LOC-TRADE-JEDI-MOUNTAIN-BASE",["CHAR-JAKE-KALOPER"])
                self.assertEqual(result["status"],"HUMAN_REVIEW_REQUIRED")
                self.assertIn("CHARACTER_VISUAL_PRESENTATION_UNRESOLVED",result["review_blockers"])
                self.assertEqual(result["character_visual_authority"]["state"],"GENERATION_BLOCKED")
                self.assertNotIn("character_rendering_eligible",result)

    def test_spatial_drift_in_authoritative_character_packet_blocks_memo_novel(self):
        import copy
        from canon.characters.runtime.reference_authority import resolve_approved_lineup_presentation
        wrong=copy.deepcopy(resolve_approved_lineup_presentation(["CHAR-JAKE-KALOPER"]))
        wrong["subjects"][0]["spatial_anchor"]["home_location_id"]="LOC-INVENTED"
        with patch("canon.characters.runtime.reference_authority.resolve_approved_lineup_presentation",
                   return_value=wrong):
            for consumer in (compile_memo_location_packet,compile_novel_location_packet):
                packet=consumer("LOC-TRADE-JEDI-MOUNTAIN-BASE",["CHAR-JAKE-KALOPER"])
                self.assertEqual(packet["status"],"HUMAN_REVIEW_REQUIRED")
                self.assertIn("CHARACTER_PHYSICAL_SPATIAL_CANON_MISMATCH",packet["review_blockers"])
                self.assertEqual(packet["character_visual_authority"]["state"],"GENERATION_BLOCKED")
                self.assertNotIn("character_rendering_eligible",packet)

    def test_existing_visual_world_production_builder_consumes_physical_and_spatial(self):
        for location,cid in (
            ("LOC-TRADE-JEDI-MOUNTAIN-BASE","CHAR-JAKE-KALOPER"),
            ("LOC-ARSENAL-BARBERSHOP","CHAR-WILSON-LOOK"),
        ):
            p=build_packet(location)
            self.assertEqual(p["character"]["principal_character_ids"],[cid])
            self.assertFalse(p["character"]["generation_eligible"])
            self.assertEqual(p["character"]["source_binding_state"],"UNPROVEN_RENDERER_HOLD")
            self.assertTrue(p["character"]["body_locks"][cid]["anatomy_constraints"])
            self.assertTrue(p["character"]["owner_specific_negative_locks"][cid])
            r=p["character"]["visual_authority"]
            self.assertEqual(r["state"],"COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE")
            self.assertEqual(r["T15"],"HOLD")
            self.assertEqual(r["T16"],"HOLD")
            if cid=="CHAR-WILSON-LOOK":
                self.assertIn("four",str(r["subjects"][0]["physical_constraints"]).lower())

    def test_production_world_packet_fails_closed_on_invalid_visual_resolver(self):
        with patch("canon.characters.runtime.reference_authority.resolve_approved_lineup_presentation",
                   return_value={"state":"GENERATION_BLOCKED","reason":"CURRENT_APPROVED_LINEUP_UNAVAILABLE"}):
            with self.assertRaisesRegex(ValueError,"unresolved"):
                build_packet("LOC-TRADE-JEDI-MOUNTAIN-BASE")

    def test_visual_world_builder_rejects_tampered_home_anchor(self):
        import copy
        from canon.characters.runtime.reference_authority import resolve_approved_lineup_presentation
        wrong=copy.deepcopy(resolve_approved_lineup_presentation(["CHAR-JAKE-KALOPER"]))
        wrong["subjects"][0]["spatial_anchor"]["home_location_id"]="LOC-FAKE"
        with patch("canon.characters.runtime.reference_authority.resolve_approved_lineup_presentation",
                   return_value=wrong):
            with self.assertRaisesRegex(ValueError,"physical/spatial canon mismatch"):
                build_packet("LOC-TRADE-JEDI-MOUNTAIN-BASE")

    def test_bad_location_and_unknown_character_are_never_ready(self):
        for consumer in (compile_memo_location_packet,compile_novel_location_packet):
            p=consumer("LOC-NOT-AN-ACTIVE-PLACE",["CHAR-JAKE-KALOPER"])
            self.assertNotIn(p["status"],("READY_FOR_SEMANTIC_QA","READY_FOR_RENDER"))
            bad=consumer("LOC-LEAGUE-CHAMBER",["CHAR-FAKE"])
            self.assertEqual(bad["status"],"HUMAN_REVIEW_REQUIRED")
            self.assertIn("CHARACTER_VISUAL_PRESENTATION_UNRESOLVED",bad["review_blockers"])

if __name__=="__main__":
    unittest.main()
