#!/usr/bin/env python3
"""Atlas board resolution execution gate: scoped reversible preproduction only.

Loads the real PR324 working tree. Optional PR325/PR337/PR322 checkouts are
read-only and pinned to exact Git blobs; no image upload, public release,
canonical source mutation, or made-up coordinates can occur.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
TRIAGE = "SEMANTIC_TRIAGE_ALL_44_PR325_V1.json"
DRYRUN = "LAST_FIELD_SUPERSESSION_DRY_RUN_V1.json"
HANDOFF = "PARALLEL_PHOTO_LIBRARY_HANDOFF_V1.json"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def verify_local(triage, dryrun, handoff, candidates, locations, routes, zones, topology):
    current = {x["id"]: x for x in candidates}
    loc = {x["id"]: x for x in locations}
    region_ids = {x["id"] for x in zones}
    rows = triage["rows"]
    require(len(locations) == len(loc) == 23, "23 live location baseline drift")
    require(len(routes) == 18, "Authoritative road registry changed")
    require(len(zones) == 7, "Seven-regions baseline drift")
    require(len(candidates) == len(current) == 88, "88 candidate source baseline drift")
    require(len(rows) == len({r["pr325_candidate_id"] for r in rows}) == 44,
            "44 independent source proposals not covered uniquely")
    require(triage["total_reviewed"] == 44
            and triage["proposed_live_location_count"] == 0,
            "Unreviewed proposals promoted")
    require(triage["status"] == "COMPLETE_PRELIMINARY_DESK_TRIAGE_NOT_INDEPENDENT_UMPIRE",
            "Editorial status was silently upgraded")
    known = {"CONSOLIDATE_AS_SUBFEATURE", "REVIEW_AS_DISTINCT_CIVIC_FUNCTION",
             "CROSS_PARENT_CONFLICT_REVIEW", "HOLD_PLACEMENT_OR_SAFETY",
             "ISLAND_NODE_SUBFEATURE_HOLD"}
    counts = Counter()
    island_nodes = {x["id"] for x in topology["node_records"]}
    for row in rows:
        id_ = row["pr325_candidate_id"]
        cat = row["editorial_treatment"]
        anchor = row["anchor"]
        ref = row["comparison_candidate_id"]
        counts[cat] += 1
        require(id_.startswith("CAND-XP-") and id_ not in current,
                f"New expansion ID collided with existing canon: {id_}")
        require(cat in known, f"Unsupported semantic category: {id_}")
        require(row.get("human_canon_approval") is False
                and row.get("publication_allowed") is False,
                f"Unapproved site prematurely released: {id_}")
        require(len(row["evidence_rationale"]) >= 40
                and bool(row["source_physical"]) and bool(row["source_civil"])
                and bool(row["source_temporal"]),
                f"Semantic source reasoning missing: {id_}")
        if anchor.startswith("POST-NODE:"):
            require(anchor[10:] in island_nodes
                    and cat == "ISLAND_NODE_SUBFEATURE_HOLD" and ref is None,
                    f"Unapproved island sublocation: {id_}")
        else:
            require(anchor in loc and cat != "ISLAND_NODE_SUBFEATURE_HOLD",
                    f"Invalid mainland parent: {id_}")
        if ref is not None:
            require(ref in current and ref.startswith("CAND-"),
                    f"Comparator missing from candidate source: {id_}")
            same_parent = anchor in current[ref].get("related_active_location_ids", [])
            expected_scope = ("SAME_PARENT" if same_parent
                              else "CROSS_PARENT_OR_NON_MATCHING_ANCHOR")
            require(row["comparison_scope"] == expected_scope,
                    f"Comparison scope/source mismatch: {id_}")
        else:
            require(row["comparison_scope"] == "NO_SPECIFIC_COMPARATOR",
                    f"Comparator should not be inferred: {id_}")
    require(dict(counts) == triage["treatment_counts"],
            "Recommended treatment counts disagree with decisions")
    require(counts["CONSOLIDATE_AS_SUBFEATURE"] == 21
            and counts["REVIEW_AS_DISTINCT_CIVIC_FUNCTION"] == 10
            and counts["CROSS_PARENT_CONFLICT_REVIEW"] == 3
            and counts["HOLD_PLACEMENT_OR_SAFETY"] == 6
            and counts["ISLAND_NODE_SUBFEATURE_HOLD"] == 4,
            "Semantic triage changed without new review evidence")

    lf = current["CAND-CHAMP-LAST-FIELD"]
    migration = dryrun["dry_run_change"]
    before = migration["before"]
    after = migration["intended_after_only_if_approved"]
    require(before == lf, "Last Field source before-record was altered")
    require(before["likely_physical_zone_ids"] == ["REG-CENTRAL-BASIN"],
            "Last Field originally not in Central Basin: unexpected source")
    require(after["likely_physical_zone_ids"] == ["REG-INNER-SEA-LITTORAL"]
            and after["likely_physical_zone_ids"][0] in region_ids,
            "Proposed island region not source-consistent")
    require({k for k in before if before[k] != after.get(k)}
            == set(migration["changed_business_fields"])
            == {"likely_physical_zone_ids", "source_provenance", "canon_notes"},
            "Dry-run modifies fields outside a governed versioned supersession")
    require(after["id"] == lf["id"] and after["lifecycle_status"] == lf["lifecycle_status"]
            and after["event_eligibility"] == ["CHAMPIONSHIP"]
            and after["championship_only"] is True
            and after["activation_trigger"] == lf["activation_trigger"],
            "Last Field identity or championship-only gate lost")
    identity = dryrun["single_venue_identity"]
    require(identity["governing_candidate_id"] == lf["id"]
            and identity["proposed_topology_node_id"] == "LAST_FIELD"
            and identity["proposed_island_stage_id"] == "CAND-POST-LAST-FIELD",
            "Two competing Last Fields or incorrect draft alias")
    require(dryrun["status"].startswith("VALIDATABLE_DRY_RUN")
            and not any(dryrun["executed_changes"].values())
            and migration["live_world_file_writes"] == []
            and migration["media_file_writes"] == [],
            "Reversible preproduction unexpectedly wrote to authoritative data")
    neutrality = dryrun["island_neutrality"]
    require(neutrality["public_gate_owner"] is None
            and neutrality["actual_coastal_survey"] == "UNVERIFIED"
            and neutrality["bridge_length_m"] is None
            and neutrality["access_graph"]["status"] == "PROPOSED_ONLY",
            "False neutral/metric/physical approval for island")
    require(topology["counts"]["nodes"] == 23
            and topology["counts"]["edges"] == 45,
            "Island graph source pin drift")

    folio = handoff["verified_parallel_cinematic_folio"]
    refs = handoff["cinematic_folio_bindings"]
    require(folio["source_pr"] == 337 and
            folio["scope"]["active_LOC_folios"] == 23
            and folio["scope"]["planned_region_establishing_plates"] == 7
            and folio["scope"]["approved_cinematic_masters"] == 0,
            "Parallel source library metadata or authority drift")
    require(len(refs) == len({x["location_id"] for x in refs}) == 23
            and {x["location_id"] for x in refs} == set(loc),
            "Read-only folio bindings missing or duplicated LOC")
    for x in refs:
        item = loc[x["location_id"]]
        require(x["physical_zone_id"] == item["physical_zone_id"]
                and x["cinematic_reference_status"] == "MISSING_APPROVED_CINEMATIC_REFERENCE"
                and x["approved_cinematic_reference_uri"] is None
                and x["per_location_status"] == "SOURCE_INDEX_ONLY",
                f"Unapproved location art has become an approved master: {x['location_id']}")
        require(x["proposed_output_path_only"].startswith(
                "world/environment-references/cinematic-folio/plates/" + x["location_id"] + "/"),
                f"Unsafe/unowned future output path: {x['location_id']}")
    require(handoff["adapter_contract"]["media_file_copying"] is False
            and handoff["adapter_contract"]["automatic_image_authority_upgrade"] is False,
            "Atlas bridge silently copied or promoted photos")
    return {"status": "PASS_PREPRODUCTION_ONLY",
            "triaged_pr325_proposals": len(rows),
            "preliminary_subfeature_treatments": counts["CONSOLIDATE_AS_SUBFEATURE"],
            "distinct_function_candidates_pending_approval": counts["REVIEW_AS_DISTINCT_CIVIC_FUNCTION"],
            "last_field_original_zone_preserved": True,
            "last_field_island_change_committed": False,
            "canonical_locations": len(loc), "canonical_routes": len(routes),
            "parallel_cinematic_folio_references": len(refs),
            "approved_new_cinematic_masters": 0}


def verify_external_sources(triage, dryrun, handoff, pr325=None, pr337=None, pr322=None):
    audited = {}
    if pr325:
        path = Path(pr325) / triage["source"]["pr325"]["path"]
        require(git_blob(path) == triage["source"]["pr325"]["blob_sha"],
                "PR325 source bytes do not match pinned GitHub blob")
        src = load(path)["proposals"]
        rows = triage["rows"]
        require(len(src) == len(rows), "PR325 proposal source changed")
        for a, b in zip(src, rows):
            require(a["id"] == b["pr325_candidate_id"]
                    and a["name"] == b["pr325_name"]
                    and a["anchor"] == b["anchor"]
                    and a["depth_seed"]["physical"] == b["source_physical"]
                    and a["depth_seed"]["civil"] == b["source_civil"]
                    and a["depth_seed"]["historical"] == b["source_temporal"],
                    f"PR325 proposal was altered: {b['pr325_candidate_id']}")
        audited["pr325_exact_source_proposals"] = len(src)
    if pr337:
        meta = handoff["verified_parallel_cinematic_folio"]
        path = Path(pr337) / meta["source_path"]
        require(git_blob(path) == meta["source_blob_sha"],
                "PR337 cinematic-folio manifest changed since source pin")
        src = load(path)
        require(src["scope"]["approved_cinematic_count"] == 0
                and src["reference_samples"]["bytes_in_repo"] is False
                and src["scope"]["base_aspect_ratio"] == "16:9",
                "PR337 source asserts image existence or approval")
        refs = {x["location_id"]: x for x in handoff["cinematic_folio_bindings"]}
        for s in src["location_folios"]:
            linked = refs[s["id"]]
            require(linked["source_card"] == s["source_card"]
                    and linked["structural_reference_uri"] == s["structural_reference_uri"]
                    and linked["proposed_output_path_only"] == s["target_paths"]["render_master"]
                    and linked["cinematic_reference_status"] == s["cinematic_reference_status"],
                    f"PR337 source handoff mismatch: {s['id']}")
        audited["pr337_original_folio_records"] = len(src["location_folios"])
    if pr322:
        path = Path(pr322) / dryrun["source_pins"]["island_supersession"]["path"]
        require(git_blob(path) == dryrun["source_pins"]["island_supersession"]["blob_sha"],
                "PR322 supersession source changed")
        src = load(path)
        require(src["current"]["candidate_id"] == dryrun["single_venue_identity"]["governing_candidate_id"]
                and src["proposed"]["zone_ids"] ==
                dryrun["dry_run_change"]["intended_after_only_if_approved"]["likely_physical_zone_ids"]
                and src["no_mutation"]["location_writeback"] is False,
                "PR322 Last Field source no longer matches approval hold")
        audited["pr322_last_field_packet"] = "PINNED_SOURCE_MATCH"
    return audited


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pr325-root")
    p.add_argument("--pr337-root")
    p.add_argument("--pr322-root")
    args = p.parse_args()
    triage = load(HERE / TRIAGE)
    dryrun = load(HERE / DRYRUN)
    handoff = load(HERE / HANDOFF)
    source = load(ROOT / "world/data/atlas_location_candidates.json")
    live = load(ROOT / "world/data/locations.json")
    roads = load(ROOT / "world/data/routes.json")
    regions = load(ROOT / "world/data/physical_zones.json")
    topology = load(HERE / "ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json")
    print(json.dumps(verify_local(triage, dryrun, handoff, source["candidates"],
                                  live["locations"], roads["routes"],
                                  regions["regions"], topology), sort_keys=True))
    if args.pr325_root or args.pr337_root or args.pr322_root:
        print(json.dumps(verify_external_sources(
            triage, dryrun, handoff, args.pr325_root, args.pr337_root,
            args.pr322_root), sort_keys=True))
