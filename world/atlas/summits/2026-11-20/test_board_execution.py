#!/usr/bin/env python3
"""Adversarial regression: forbid premature Last Field/asset/site publication."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("preproduction",HERE/"validate_board_execution.py")
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class BoardResolutionExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=[
            v.load(HERE/v.TRIAGE),
            v.load(HERE/v.DRYRUN),
            v.load(HERE/v.HANDOFF),
            v.load(v.ROOT/"world/data/atlas_location_candidates.json")["candidates"],
            v.load(v.ROOT/"world/data/locations.json")["locations"],
            v.load(v.ROOT/"world/data/routes.json")["routes"],
            v.load(v.ROOT/"world/data/physical_zones.json")["regions"],
            v.load(HERE/"ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json"),
        ]

    def run_check(self,change=None):
        args=copy.deepcopy(self.inputs)
        if change:
            change(*args)
        return v.verify_local(*args)

    def rejected(self,change):
        with self.assertRaises(ValueError):
            self.run_check(change)

    def test_valid_current_preproduction(self):
        out=self.run_check()
        self.assertEqual(out["triaged_pr325_proposals"],44)
        self.assertIs(out["last_field_island_change_committed"],False)

    def test_44_review_entries_must_not_decrease(self):
        self.rejected(lambda triage,*unused:triage["rows"].pop())

    def test_review_cannot_silently_approve(self):
        self.rejected(lambda triage,*unused:triage["rows"][0].__setitem__("human_canon_approval",True))

    def test_publication_cannot_sneak_into_review(self):
        self.rejected(lambda triage,*unused:triage["rows"][0].__setitem__("publication_allowed",True))

    def test_duplicate_new_proposal_id_rejected(self):
        self.rejected(lambda triage,*unused:triage["rows"][1].__setitem__(
            "pr325_candidate_id",triage["rows"][0]["pr325_candidate_id"]))

    def test_comparator_missing_rejected(self):
        self.rejected(lambda triage,*unused:triage["rows"][1].__setitem__(
            "comparison_candidate_id","CAND-DOES-NOT-EXIST"))

    def test_source_comparison_scope_rejected(self):
        self.rejected(lambda triage,*unused:triage["rows"][1].__setitem__(
            "comparison_scope","CROSS_PARENT_OR_NON_MATCHING_ANCHOR"))

    def test_island_site_cannot_become_mainland(self):
        def edit(triage,*unused):
            row=next(x for x in triage["rows"] if x["anchor"].startswith("POST-NODE:"))
            row["anchor"]="LOC-TRADE-JEDI-MOUNTAIN-BASE"
        self.rejected(edit)

    def test_last_field_source_cannot_be_overwritten(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["dry_run_change"]["before"].__setitem__(
            "likely_physical_zone_ids",["REG-INNER-SEA-LITTORAL"]))

    def test_last_field_after_status_cannot_auto_activate(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["dry_run_change"][
            "intended_after_only_if_approved"].__setitem__("lifecycle_status","APPROVED_ACTIVE_CANON"))

    def test_last_field_cannot_gain_unapproved_third_change(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["dry_run_change"][
            "intended_after_only_if_approved"].__setitem__("activation_trigger","ANY_MATCHUP"))

    def test_no_live_location_writeback(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["executed_changes"].__setitem__(
            "active_locations_mutated",True))

    def test_neutral_gate_cannot_become_llc_property(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["island_neutrality"].__setitem__(
            "public_gate_owner","CHAR-DAVID-BABB"))

    def test_island_causeway_cannot_claim_metric_length(self):
        self.rejected(lambda triage,dryrun,*unused:dryrun["island_neutrality"].__setitem__(
            "bridge_length_m",2700))

    def test_photo_folio_cannot_gain_unapproved_image(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["cinematic_folio_bindings"][0].__setitem__(
            "cinematic_reference_status","APPROVED_CINEMATIC_REFERENCE"))

    def test_photo_folio_cannot_gain_approved_uri(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["cinematic_folio_bindings"][0].__setitem__(
            "approved_cinematic_reference_uri","unverified.png"))

    def test_photo_folio_cannot_claim_approved_masters(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["verified_parallel_cinematic_folio"][
            "scope"].__setitem__("approved_cinematic_masters",1))

    def test_photo_folio_missing_loc_rejected(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["cinematic_folio_bindings"].pop())

    def test_photo_byte_copying_forbidden(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["adapter_contract"].__setitem__(
            "media_file_copying",True))

    def test_region_change_without_source_rejected(self):
        self.rejected(lambda triage,dryrun,handoff,*unused:handoff["cinematic_folio_bindings"][0].__setitem__(
            "physical_zone_id","REG-CENTRAL-BASIN"))


if __name__=="__main__":
    unittest.main(verbosity=2)
