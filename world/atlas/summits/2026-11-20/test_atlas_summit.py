#!/usr/bin/env python3
"""Atlas Summit 2026-11-20: read-only reconciliation gates.

Reads the working branch's mainland World Engine and cross-branch island
source snapshot. Does not fetch the network, write to canon, or ratify PR #322.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SUMMIT = ROOT / "world/atlas/summits/2026-11-20"


def load(relative: str):
    with (ROOT / relative).open(encoding="utf-8") as stream:
        return json.load(stream)


def check():
    live = load("world/data/locations.json")["locations"]
    routes = load("world/data/routes.json")["routes"]
    candidate = load("world/data/atlas_location_candidates.json")["candidates"]
    domains = load("world/data/owner_domains.json")["domains"]
    dossier = load("world/atlas/summits/2026-11-20/THREE_LAYER_LOCATION_DOSSIERS_V1.json")
    island = load("world/atlas/summits/2026-11-20/PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json")
    mainland = dossier["active_location_three_layer_dossiers"]
    proposals = dossier["existing_and_new_candidate_three_layer_dossiers"]
    island_records = island["three_depth_records"]
    all_ids = [s["id"] for s in live] + [s["id"] for s in candidate] + [s["id"] for s in island_records]

    assert len(live) == len(mainland) == 23, "Existing World Engine count must remain 23"
    assert len(routes) == 18, "Do not silently invent a live mainland route"
    assert len(candidate) == len(proposals) == 88
    assert len(island_records) == 44
    assert len(all_ids) == len(set(all_ids)) == 155, "All cross-Atlas source handles must remain distinct"

    for rec in mainland:
        assert rec["location_id"] in {x["id"] for x in live}
        for layer in ("level_1_physical_and_arrival", "level_2_lived_civilization_and_institution", "level_3_memory_evolution_and_playoffs"):
            assert rec[layer], (rec["location_id"], layer)
    for rec in proposals:
        assert rec["location_id"] in {x["id"] for x in candidate}
        for layer in ("level_1_physical_and_arrival", "level_2_lived_civilization_and_institution", "level_3_memory_evolution_and_playoffs"):
            assert rec[layer], (rec["location_id"], layer)
    for rec in island_records:
        for layer in ("layer1", "layer2", "layer3"):
            assert rec[layer], (rec["id"], layer)
        assert rec["editorial_discoverable"] and not rec.get("world_loc_active", False)

    assert len(domains) == 12
    home_ids = {d["primary_location_id"] for d in domains}
    assert home_ids <= {x["id"] for x in live}, "All current owners must bind to existing world locations"

    founder = [c for c in candidate if "Founder location-expansion directive 2026-11-20" in c.get("source_provenance", [])]
    assert len(founder) == 40
    assert len(candidate) - len(founder) == 48
    overlap = {c["id"] for c in founder if c["id"].startswith("CAND-PLAYOFF-ISLAND-")}
    assert len(overlap) == 4
    assert all(c["lifecycle_status"] == "HOLD_FOR_LATER_EVIDENCE" for c in founder if c["id"] in overlap)
    assert len(founder) - len(overlap) == 36, "36 independent owner-region expansions eligible for further review"

    categories = Counter(r["kind"] for r in island_records)
    assert categories == Counter({"POSTSEASON_ARENA": 9, "ISLAND_TOPOLOGY_NODE": 23, "DORMANT_HERITAGE": 9, "NEUTRAL_SITING_HYPOTHESIS": 3}), categories
    beach = next(r for r in island_records if r["id"] == "LOSERS_BEACH")
    counts = {r["year"]: r for r in beach["layer3"]["historical_beach_years"]}
    assert len(counts) == 11
    assert [counts[y]["opening_nonqualifier_count"] for y in (2015, 2017, 2021)] == [8, 6, 5]
    assert all(x["postfinal_nonchampion_count"] == 11 for x in counts.values())
    assert island["counts"]["historical_matches"] == island["counts"]["proposed_physical_traces"] == 56

    edge = island["known_source_defect"]
    assert edge["recorded"] == 41 and edge["actual"] == 45, "Preserve and flag upstream stale count until PR #322 is fixed"
    assert island["championship_identity_conflict"]["existing_candidate"] == "CAND-CHAMP-LAST-FIELD"
    assert island["championship_identity_conflict"]["new_proposed_arena"] == "CAND-POST-LAST-FIELD"
    assert all(row["year"] in range(2015, 2026) for row in island["annual_stadium_status"])
    assert len(island["annual_stadium_status"]) == 11

    return {"status": "PASS_WITH_UPSTREAM_HOLD", "live_locations": 23, "live_routes": 18, "older_candidates": 48, "new_proposals": 40, "held_duplicate_proposals": 4, "new_nonduplicate_proposals": 36, "island_handles": 44, "total_handles": 155, "historical_matches_source_bound": 56, "source_defect": "PR322 edge_count 41 -> actual 45", "canonical_promotions": 0}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
