#!/usr/bin/env python3
"""Adversarial regression tests for draft Atlas / photo source handoff."""
import copy
import importlib.util
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("verify_board_bridge", BASE/"verify_board_bridge.py")
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class BoardBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=gate.load(BASE/"CROSS_BRANCH_LOCATION_CONCORDANCE_V1.json")
        cls.p=gate.load(BASE/"PHOTO_LIBRARY_PARALLEL_HANDOFF_V1.json")

    def invalid(self, fn):
        a,p=copy.deepcopy(self.a),copy.deepcopy(self.p)
        fn(a,p)
        with self.assertRaises(ValueError):
            gate.validate(a,p)

    def test_positive_source_bounded_handoff(self):
        s=gate.validate(copy.deepcopy(self.a),copy.deepcopy(self.p))
        self.assertEqual(s["union_unpromoted_handles"],199)
        self.assertEqual(s["approved_environment_master_images"],0)

    def test_never_count_155_plus_147_as_all_new(self):
        self.invalid(lambda a,p:a["exact_id_math"].__setitem__("union_ids",302))

    def test_raw_id_collision_cannot_hide_under_counts(self):
        self.invalid(lambda a,p:a["pr325_only_ids"].__setitem__(0,a["pr324_only_ids"][0]))

    def test_cross_team_dedup_is_not_permitted(self):
        self.invalid(lambda a,p:a["proposed_overlap_review"][0].__setitem__("team_slot_2026",12))

    def test_four_island_proposals_cannot_be_auto_promoted(self):
        def edit(a,p):
            x=next(x for x in a["proposed_overlap_review"] if x["team_slot_2026"] is None)
            x["status"]="APPROVED_ACTIVE_CANON"
        self.invalid(edit)

    def test_no_unreviewed_candidate_merge(self):
        self.invalid(lambda a,p:a["proposed_overlap_review"][0].__setitem__("decision","MERGE_APPROVED"))

    def test_unlisted_photo_location_cannot_appear(self):
        self.invalid(lambda a,p:p["location_bindings"][0].__setitem__("location_id","CAND-POST-LAST-FIELD"))

    def test_missing_location_photo_id_rejected(self):
        self.invalid(lambda a,p:p["location_bindings"].pop())

    def test_render_target_not_proof_of_approved_image(self):
        self.invalid(lambda a,p:p["location_bindings"][0].__setitem__("approved_cinematic_reference_uri","plates/fake.png"))

    def test_character_crops_cannot_become_public(self):
        self.invalid(lambda a,p:p["character_gallery_summary"].__setitem__("all_visibility_internal",False))

    def test_forged_photo_source_metadata_rejected(self):
        self.invalid(lambda a,p:p["source_pins"][0].__setitem__("git_blob_sha","invented"))


if __name__=="__main__":
    unittest.main(verbosity=2)
