#!/usr/bin/env python3
"""Fail-closed validation of the 2026-11-20 additive Atlas candidate summit.

This checks evidence structure, not artistic quality or independent canon approval.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def require(condition: bool, explanation: str):
    if not condition:
        raise AssertionError(explanation)

def validate() -> dict:
    active = load("world/data/locations.json")["locations"]
    candidates = load("world/data/atlas_location_candidates.json")["candidates"]
    routes = load("world/data/routes.json")["routes"]
    owner_domains = load("world/data/owner_domains.json")["domains"]
    zones = load("world/data/physical_zones.json")["regions"]
    world_events = load("world/data/world_memory.json")["events"]
    source_history = load("living-novel/history/CHAMPIONSHIP_SUCCESSION_MACHINE_INDEX_2015_2026.json")["seasons"]
    dossier = json.loads((HERE / "THREE_LAYER_LOCATION_DOSSIERS_V1.json").read_text())
    review = json.loads((HERE / "STRUCTURAL_REVIEW_MANIFEST_V1.json").read_text())
    year_matrix = json.loads((HERE / "SEASON_BY_SEASON_SLOT_GEO_IMPACT_MATRIX_V1.json").read_text())
    island = json.loads((HERE / "PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json").read_text())

    ids = [x["id"] for x in active] + [x["id"] for x in candidates]
    require(len(active) == 23, "active LOC baseline changed")
    require(len(candidates) == 88, "candidate registry is not original 48 plus 40")
    require(len(ids) == len(set(ids)), "duplicate registry location ID")
    require(len(world_events) >= 7, "world event source unexpectedly truncated")
    current = [x for x in dossier["active_location_three_layer_dossiers"]]
    proposed = dossier["existing_and_new_candidate_three_layer_dossiers"]
    require(len(current) == 23 and len(proposed) == 88, "dossier coverage does not match registries")
    require({x["location_id"] for x in current} == {x["id"] for x in active}, "live ID missing from dossier")
    require({x["location_id"] for x in proposed} == {x["id"] for x in candidates}, "candidate ID missing from dossier")

    required_levels = ("level_1_physical_and_arrival", "level_2_lived_civilization_and_institution",
                       "level_3_memory_evolution_and_playoffs")
    for item in current + proposed:
        for key in required_levels:
            require(isinstance(item.get(key), dict) and len(item[key]) >= 5,
                    f"three-depth structure absent: {item['location_id']} {key}")
        require(item["location_id"] in review["location_checks"],
                f"missing per-location phase review: {item['location_id']}")
        require(review["location_checks"][item["location_id"]]["independent_umpire"] == "PENDING",
                f"unverified independent approval: {item['location_id']}")

    active_ids = {x["id"] for x in active}
    zone_ids = {x["id"] for x in zones}
    owner_ids = {x["character_id"] for x in owner_domains}
    route_ids = {x["id"] for x in routes}
    for x in active:
        require(x["physical_zone_id"] in zone_ids, f"bad active physical zone: {x['id']}")
        require(all(r in route_ids for r in x["access_route_ids"]), f"unknown active route: {x['id']}")
        require(x.get("owner_character_id") is None or x["owner_character_id"] in owner_ids,
                f"bad active owner: {x['id']}")
    for x in candidates:
        require(x["id"].startswith("CAND-"), f"invalid candidate ID {x['id']}")
        require(x["lifecycle_status"] != "APPROVED_ACTIVE_CANON", f"unauthorized promotion: {x['id']}")
        require(not x.get("promoted_location_id"), f"unauthorized LOC backlink: {x['id']}")
        require(all(z in zone_ids for z in x["likely_physical_zone_ids"]),
                f"candidate has unknown physical zone: {x['id']}")
        require(all(p in active_ids for p in x.get("related_active_location_ids", [])),
                f"candidate parent location missing: {x['id']}")
        require(x.get("technology_translation") in ("NATIVE_PREMODERN", "FUNCTIONAL_ANALOGUE",
                 "REQUIRES_TECH_UNLOCK", "REJECTED_TECH_DRIFT"), f"invalid tech classification: {x['id']}")

    # The three layers must contain source-grounded content, not merely
    # nonempty boilerplate dictionaries. This is still editorial QA, not a
    # fictional-world construction permit.
    active_dossiers = {x["location_id"]: x for x in current}
    candidate_dossiers = {x["location_id"]: x for x in proposed}
    zone_by_id = {x["id"]: x for x in zones}
    route_by_id = {x["id"]: x for x in routes}
    for item in active:
        packet = active_dossiers[item["id"]]
        physical = packet["level_1_physical_and_arrival"]
        society = packet["level_2_lived_civilization_and_institution"]
        history = packet["level_3_memory_evolution_and_playoffs"]
        region = physical["region_grounding"]
        require(len(region) == 1 and region[0]["region_id"] == item["physical_zone_id"],
                f"active zone grounding changed: {item['id']}")
        require(region[0]["terrain_options"] == zone_by_id[item["physical_zone_id"]]["environment"]["terrain"],
                f"active terrain source drift: {item['id']}")
        require({r["route"] for r in physical["movement_bottlenecks"]} == set(item["access_route_ids"]),
                f"active access route dossier drift: {item['id']}")
        require(all(r["constraints"] == route_by_id[r["route"]].get("constraints", [])
                    for r in physical["movement_bottlenecks"]),
                f"active route constraints drift: {item['id']}")
        require(len(society["ordinary_life_development_gate"]) >= 3,
                f"no ordinary-life causal test: {item['id']}")
        source_events = {e["event_id"] for e in world_events if e["location"] == item["id"]}
        require({e["event_id"] for e in history["source_world_memory_evidence"]} == source_events,
                f"source world-event memory omitted or invented: {item['id']}")
        require("never automatically" in history["championship_side_effect_rule"],
                f"playoff win misattributed to territorial power: {item['id']}")

    for item in candidates:
        packet = candidate_dossiers[item["id"]]
        physical = packet["level_1_physical_and_arrival"]
        society = packet["level_2_lived_civilization_and_institution"]
        history = packet["level_3_memory_evolution_and_playoffs"]
        zones_for_item = physical["regional_constraints_from_governing_atlas"]
        require([z["region_id"] for z in zones_for_item] == item["likely_physical_zone_ids"],
                f"candidate geographic hypothesis diverges from source: {item['id']}")
        require(all(z["terrain_options"] == zone_by_id[z["region_id"]]["environment"]["terrain"]
                    and z["movement_constraints"] == zone_by_id[z["region_id"]]["environment"]["movement"]
                    for z in zones_for_item), f"candidate terrain/movement source drift: {item['id']}")
        require(len(physical["material_support_and_logistics_to_prove"]) >= 3,
                f"candidate lacks physical support obligations: {item['id']}")
        require(len(society["civilian_roles_to_verify"]) >= 3,
                f"candidate lacks ordinary inhabitant design: {item['id']}")
        require(society["historical_civil_population"].startswith("UNVERIFIED"),
                f"unverified old settlement silently asserted: {item['id']}")
        require(history["historical_construction_window"].startswith("NOT_ASSIGNED"),
                f"unverified 2015–2025 construction canonized: {item['id']}")
        require(history["venue_use_not_proven_by_historical_scores"] is True,
                f"ESPN sports result falsely used as venue evidence: {item['id']}")
        status = history["eligibility_source_status"]
        require(status["source_lifecycle"] == item["lifecycle_status"]
                and status["event_eligibility"] == item["event_eligibility"],
                f"candidate venue eligibility/lifecycle drift: {item['id']}")
        require(all(x["inheritance"] == "CONTEXT_ONLY_NOT_SUBLOCATION_EVENT"
                    and x["parent"] in item.get("related_active_location_ids", [])
                    for x in history["parent_world_memory_references"]),
                f"candidate inherited parent memory as new event: {item['id']}")

    frozen_ids = load("world/atlas/interactive/FROZEN_EDITORIAL_CANDIDATE_IDS_V1.json")["candidate_ids"]
    require(len(frozen_ids) == len(set(frozen_ids)) == 48, "Phase4 editorial snapshot mutated")
    require(set(frozen_ids).issubset({x["id"] for x in candidates}), "Frozen Phase4 candidate missing")
    require(not any("Founder location-expansion directive 2026-11-20"
                    in next(x for x in candidates if x["id"] == name).get("source_provenance", [])
                    for name in frozen_ids), "New site leaked into frozen legacy catalog")

    vintage = Counter(x["candidate_vintage"] for x in proposed)
    require(vintage == {"PREEXISTING": 48, "NEW_2026_11_20": 40}, "legacy candidate removed or added mix wrong")
    new = [x for x in proposed if x["candidate_vintage"] == "NEW_2026_11_20"]
    count_by_storyline = Counter(x["storyline_owner_character_id"] for x in new)
    require(len(owner_domains) == 12, "twelve-domain baseline mismatch")
    require(all(count_by_storyline[x["character_id"]] == 3 for x in owner_domains),
            "each current owner storyline must have exactly three proposed sublocations")
    require(count_by_storyline[None] == 4, "four unplaced island proposals missing")
    island_ids = [x for x in candidates if x["id"].startswith("CAND-PLAYOFF-ISLAND-")]
    require(len(island_ids) == 4, "missing four island source-gated candidates")
    require(all(not x["likely_physical_zone_ids"] and x.get("rare_use") for x in island_ids),
            "unknown island must not acquire invented zone or open ordinary venue use")
    require(all(x["lifecycle_status"] == "HOLD_FOR_LATER_EVIDENCE" for x in island_ids),
            "duplicate-risk island candidates prematurely activated")

    # Island source PR #322 is an independent editorial atlas with stable handles,
    # not 44 new LOC locations or proof of real-playoff venue geography.
    island_records = island["three_depth_records"]
    require(len(island_records) == 44 and len({x["id"] for x in island_records}) == 44,
            "island source handle count/identity drift")
    require(not ({x["id"] for x in island_records} & set(ids)),
            "island handles must not be silently duplicated as canonical LOC/CAND IDs")
    for x in island_records:
        require(all(isinstance(x.get(depth), dict) and x[depth]
                    for depth in ("layer1", "layer2", "layer3")),
                f"island three-depth record missing: {x['id']}")
        statuses_by_class = {
            "POSTSEASON_ARENA": {"UNPROMOTED"},
            "ISLAND_TOPOLOGY_NODE": {"PROPOSED_ONLY"},
            "DORMANT_HERITAGE": {"STAFF_CLOSED", "BARRIER_LOCKED", "PERMIT_REQUIRED",
                                 "ACCESS_PROHIBITED", "MASONRY_SURVEY_HOLD",
                                 "CLOSED_TEST_RING", "RANGE_CLOSED",
                                 "CLOSED_UNTIL_REFURBISHED"},
            "NEUTRAL_SITING_HYPOTHESIS": {"NOT_LOC"},
        }
        require(x.get("status") in statuses_by_class.get(x.get("kind"), set()),
                f"unexpected island promotion: {x['id']}")
    require(island["counts"]["historical_matches"] == 56, "island historical fixture count mismatch")
    require(island["counts"]["dormant_heritage_sites"] == 9, "dormant island heritage lost")
    require(island["counts"]["edges"] == 45, "island source edge-list count drift")
    require(island["known_source_defect"]["actual"] == island["known_source_defect"]["recorded"] == 45 and
            island["known_source_defect"]["status"] == "RESOLVED_IN_UPSTREAM_PR_322",
            "island source count is not reconciled with the repaired 45-edge PR #322")
    require(island["championship_identity_conflict"]["approval"].startswith("Explicit"),
            "Last Field conflicting locations must require explicit review")
    require(next(x for x in candidates if x["id"] == "CAND-CHAMP-LAST-FIELD")["championship_only"],
            "last-field championship-only lock lost")
    require(next(x for x in candidates if x["id"] == "CAND-STOCKCAR-SPEEDWAY")["lifecycle_status"] == "REJECTED_FOR_DRIFT",
            "modern-stockcar drift guard lost")
    require(next(x for x in candidates if x["id"] == "CAND-MIRE-HILL-CUSTODIAL-OUTPOST")["likely_physical_zone_ids"] == ["REG-CENTRAL-BASIN"],
            "Mire Hill neutral basin drift")
    require(next(x for x in candidates if x["id"] == "CAND-SHARED-MARCH-CUSTOMS-HEARTH")["related_active_location_ids"] == ["LOC-TDS-CHILI-SHARED-MARCH"],
            "shared-March cross-Division inheritance drift")

    yrs = year_matrix["slots"]
    require(len(yrs) == 12 and len(source_history) == 11, "history cardinality mismatch")
    require({y["season"] for x in yrs for y in x["year_by_year"]} == set(range(2015, 2026)),
            "history missing a year")
    require(all(len(x["year_by_year"]) == 11 for x in yrs), "history not eleven years per slot")
    require(all(y["physical_location_status"] == "NO_2015_2025_EVENT_VENUE_ATTESTED"
                and y["historical_owner_person_identity"] == "NOT_VERIFIED_FROM_PROVIDER"
                for x in yrs for y in x["year_by_year"]), "unverified venue/owner silently promoted")
    for season in source_history:
        for finish in ("champion", "runner_up", "third"):
            podium = season[finish]
            row = yrs[podium["team_slot"]-1]["year_by_year"][season["season"]-2015]
            require(row["verified_team_name_from_slot_lineage"] == podium["team_name"] and
                    row["postseason_podium_status"] == finish,
                    f"team lineage/podium mismatch in {season['season']} {finish}")
    require(year_matrix["result_counts"]["source_mismatches"] == 0, "unresolved historical name mismatch")
    return {"status": "PASS_STRUCTURAL_ONLY", "active": len(active), "legacy_candidates": vintage["PREEXISTING"],
            "new_candidates": vintage["NEW_2026_11_20"], "dossiers": len(current)+len(proposed),
            "owner_slots": len(yrs), "historic_slot_years": len(yrs)*11, "podium_checks": len(source_history)*3,
            "island_source_handles": len(island_records), "total_dossiers_and_island_handles": len(current)+len(proposed)+len(island_records),
            "island_source_gate": "HOLD", "umpire": "PENDING"}

if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
