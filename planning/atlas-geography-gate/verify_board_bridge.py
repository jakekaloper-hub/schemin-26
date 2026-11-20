#!/usr/bin/env python3
"""Fail-closed checks for draft Atlas geography board and photo-library bridge.

This validates two *snapshotted, noncanonical* source joins. It does not verify
uncommitted image bytes, run external source review, or approve world geography.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def need(cond, why):
    if not cond:
        raise ValueError(why)


def validate(crosswalk: dict, photo: dict):
    require_source_pin = lambda x: (x.get("git_blob_sha") or "").isalnum() and len(x["git_blob_sha"]) == 40
    need(crosswalk["status"] == "EVIDENCE_CONCORDANCE_ONLY_NO_CANON_PROMOTION", "Crosswalk source unexpectedly promoted")
    need(photo["status"] == "READ_ONLY_SOURCE_HANDOFF_NO_ASSET_INGESTION_OR_PUBLICATION", "Photo library handoff must remain read-only")
    need(all(require_source_pin(p) for p in crosswalk["source_pins"] + photo["source_pins"]), "Missing exact Git source hash")
    need(len({(x["path"], x["ref"]) for x in crosswalk["source_pins"]}) == len(crosswalk["source_pins"]),
         "Duplicate cross-Atlas source pin")
    calc = crosswalk["exact_id_math"]
    shared = crosswalk["shared_existing_source_ids"]
    only_a = crosswalk["pr324_only_ids"]
    only_b = crosswalk["pr325_only_ids"]
    a_ids, b_ids = set(shared + only_a), set(shared + only_b)
    need(len(shared) == 103 and len(only_a) == 52 and len(only_b) == 44, "Atlas draft ID-set coverage mismatch")
    need(len(a_ids) == 155 and len(b_ids) == 147 and len(a_ids | b_ids) == 199, "Duplicate or missing proposal source identifiers")
    need(not(set(only_a) & set(only_b)) and not(set(shared) & set(only_a + only_b)),
         "Source-exclusive IDs overlap")
    for label, expected in (("pr324_handles",155),("pr325_handles",147),("shared_ids",103),
                            ("only_pr324_ids",52),("only_pr325_ids",44),("union_ids",199)):
        need(calc[label] == expected, "Invalid summary value " + label)
    reviews = crosswalk["proposed_overlap_review"]
    need(len(reviews) == 40 and len({x["candidate_id"] for x in reviews}) == 40,
         "Forty PR324 proposal triage records required")
    need(all(r["candidate_id"] in only_a for r in reviews), "Crosswalk triage record does not belong to PR324-only inventory")
    owner_reviews = [x for x in reviews if x["team_slot_2026"] is not None]
    island_reviews = [x for x in reviews if x["team_slot_2026"] is None]
    need(len(owner_reviews) == 36 and len(island_reviews) == 4, "Current 36 owner + four held Island proposal grouping changed")
    need(Counter(x["team_slot_2026"] for x in owner_reviews) == {k: 3 for k in range(1,13)},
         "Each current team requires exactly three PR324 site comparisons")
    for r in owner_reviews:
        hints = r["possible_equivalents"]
        need(len(hints) == 3 and len({h["id"] for h in hints}) == 3
             and all(h["id"] in only_b for h in hints),
             "Owner proposal must compare to three independent PR325 candidate IDs")
        need(r["comparison_scope"].startswith("SAME_2026_FRANCHISE"), "Cross-franchise geography improperly aliased")
        need(r["decision"] == "MANUAL_ADJUDICATION_REQUIRED_NOT_CANON", "Premature match/promotion")
    for r in island_reviews:
        need(r["candidate_id"].startswith("CAND-PLAYOFF-ISLAND-")
             and r["status"] == "HOLD_FOR_LATER_EVIDENCE"
             and not r["possible_equivalents"]
             and r["existing_island_node_reuse_targets"],
             "Four held Island candidate ideas must reconcile against original topology")
        need(r["decision"] == "MANUAL_ADJUDICATION_REQUIRED_NOT_CANON", "Island candidate promoted")
    need(crosswalk["source_scopes"]["pr324"]["active_loc"] == 23
         and crosswalk["source_scopes"]["pr325"]["active_loc"] == 23,
         "Core world locations must not grow through draft union")
    need(photo["current_known_source_ownership"]["approved_cinematic_images_observed"] == 0
         and photo["current_known_source_ownership"]["photos_committed_during_this_handoff"] == 0,
         "Proposed image targets falsely listed as approved bytes")
    bindings = photo["location_bindings"]
    ids = [b["location_id"] for b in bindings]
    need(len(ids) == len(set(ids)) == 23 and all(i.startswith("LOC-") for i in ids),
         "Photo bridge must bind 23 distinct active LOC references only")
    need(len({b["physical_zone_id"] for b in bindings}) == 7, "Seven actual regions not fully referenced by photo bridge")
    need(all(b["source_status"] == "MISSING_APPROVED_CINEMATIC_REFERENCE"
             and b["approved_cinematic_reference_uri"] is None
             and b["readiness"] == "READ_ONLY_INDEX_ONLY_REQUIRES_BYTES_AND_ART_APPROVAL"
             for b in bindings), "Image path or planning status improperly promoted to approved source")
    need(all(b["source_folio"] == "world/environment-references/cinematic-folio/LOC_FOLIO_MANIFEST.proposal.json"
             and b["reference_card"].endswith("/CARD.json")
             and b["structural_reference_uri"].endswith("/STRUCTURAL_PLATE.svg")
             and b["render_target_proposed_not_existence"].endswith("/MASTER_16x9.png")
             for b in bindings), "Image source/structural fallback/target path authority changed")
    chars = photo["character_gallery_summary"]
    need(chars["records"] == chars["matching_canon_location_ids"] == 12
         and chars["all_visibility_internal"] and chars["all_approval_hold"], "Character reference privacy/approval hold lost")
    need("photo_library" in photo["schema"] or "photo_library" in photo["schema"].replace(".","_"),
         "Photo contract has unexpected type")
    return {"status":"PASS_READONLY_GEO_AND_IMAGE_HANDOFF_NOT_CANON",
            "shared_source_ids":len(shared),"union_unpromoted_handles":len(a_ids | b_ids),
            "proposals_pr324":len(reviews),"proposals_pr325":len(only_b),
            "held_island_dedup":len(island_reviews),"active_world_mutations":0,
            "photo_loc_bindings":len(bindings),"approved_environment_master_images":0,
            "character_sources_internal_hold":12}


if __name__ == "__main__":
    crosswalk = load(HERE / "CROSS_BRANCH_LOCATION_CONCORDANCE_V1.json")
    photo = load(HERE / "PHOTO_LIBRARY_PARALLEL_HANDOFF_V1.json")
    print(json.dumps(validate(crosswalk,photo), sort_keys=True))
