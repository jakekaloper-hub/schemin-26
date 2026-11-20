#!/usr/bin/env python3
"""Independent *structural* guard for the 2015–2025 playoff slot/Atlas crosswalk.

Source-derived facts here were transcribed from draft postseason PR #322 and
have not been refetched from ESPN by this validator. Verifies the internal
bracket, all twelve slot-year records, Losers' Beach admission semantics,
and the fictional venue / real sports result boundary.

Does NOT ratify fictional venues, historical owners or island publication.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FILE = ROOT / "world/atlas/summits/2026-11-20/SEASON_BY_SEASON_SLOT_GEO_IMPACT_MATRIX_V1.json"
ISLAND = ROOT / "world/atlas/summits/2026-11-20/PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json"


def ensure(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def validate(matrix: dict, island: dict) -> dict:
    field = matrix.get("qualification_field_by_season", [])
    records = matrix.get("slots", [])
    provenance = matrix.get("full_playoff_source", {})
    ensure(provenance.get("repo_pr") == "https://github.com/jakekaloper-hub/schemin-26/pull/322", "Historical qualifier provenance missing")
    ensure("NOT_INDEPENDENTLY_REFETCHED" in provenance.get("evidence_class", ""), "Missing data-origin limitation")
    ensure(len(field) == 11 and len(records) == 12, "Expected eleven source years and twelve slot records")
    ensure({x["season"] for x in field} == set(range(2015, 2026)), "Source-year coverage drift")
    ensure({x["current_2026_team_id"] for x in records} == set(range(1, 13)), "Slot identities duplicated/missing")
    ensure(matrix.get("no_2026_finals") is True, "2026 title outcome must remain unset")

    per_year = {x["season"]: x for x in field}
    row_map = {}
    actual_match_ids = set()
    total_qualifiers = total_byes = total_appearances = 0
    for owner in records:
        slot = owner["current_2026_team_id"]
        years = owner["year_by_year"]
        ensure(len(years) == 11, f"Eleven years missing for slot {slot}")
        ensure({r["season"] for r in years} == set(range(2015, 2026)), f"Slot {slot}: duplicate or missing season")
        ensure(owner.get("timeline_may_not_be_retroassigned_to_current_owner") is True, "Historical owner lineage safeguard lost")
        for row in years:
            key = (row["season"], slot)
            ensure(key not in row_map and row["team_slot"] == slot, f"Duplicate/wrong slot-year {key}")
            row_map[key] = row

    for year in range(2015, 2026):
        src = per_year[year]
        entries = src["qualifier_slot_ids"]
        byes = src["bye_slot_ids"]
        expected = 4 if year <= 2016 else 6 if year <= 2020 else 7
        expected_byes = 0 if year <= 2016 else 2 if year <= 2020 else 1
        ensure(len(entries) == len(set(entries)) == expected, f"{year}: qualifier field size/duplicates")
        ensure(len(byes) == len(set(byes)) == expected_byes, f"{year}: bye count/duplicates")
        ensure(set(byes).issubset(entries), f"{year}: nonqualifier assigned bye")
        ensure(src["champion_slot"] in entries, f"{year}: champion not qualified")
        ensure(len(src["match_ids"]) == len(set(src["match_ids"])) == expected - 1, f"{year}: source fixture ID coverage")
        ensure(all(1 <= s <= 12 for s in entries), f"{year}: slot outside twelve")
        expected_rounds = Counter({"QF": 0 if year <= 2016 else 2 if year <= 2020 else 3, "SF": 2, "FINAL": 1})
        appearances = defaultdict(list)
        fixture_views = defaultdict(list)

        for slot in range(1, 13):
            row = row_map[(year, slot)]
            is_qualified = slot in entries
            is_bye = slot in byes
            games = row["verified_bracket_matchups"]
            ensure(row["playoff_qualified"] is is_qualified and row["earned_bye"] is is_bye, f"{year}/{slot}: participation or bye flag")
            ensure(row["playoff_participation_verified"] == ("YES_PR322_VERIFIED_QUALIFIER" if is_qualified else "NO_PR322_VERIFIED_NONQUALIFIER"), f"{year}/{slot}: evidence label")
            ensure(row["historical_owner_person_identity"] == "NOT_VERIFIED_FROM_PROVIDER", f"{year}/{slot}: fabricated personal owner")
            ensure(row["physical_location_status"] == "NO_2015_2025_EVENT_VENUE_ATTESTED", f"{year}/{slot}: fictional venue promoted")
            ensure(row["domain_evolution_status"] == "NO_SOURCE_PROVES_HISTORIC_BUILDING_CONSTRUCTION_OR_DEMOLITION", f"{year}/{slot}: fabricated historic destruction")
            ensure(not any(g.get("fictional_venue_assignment") != "NOT_FACT" for g in games), f"{year}/{slot}: fictional venue stated as fact")
            expected_beach = ("LOSERS_BEACH_ELIGIBLE_AFTER_QUALIFICATION_LOCK" if not is_qualified else
                              "CHAMPION_NOT_BEACH" if slot == src["champion_slot"] else
                              "LOSERS_BEACH_ELIGIBLE_AFTER_CERTIFIED_ELIMINATION")
            ensure(row["playoff_island_lodging_proposal"] == expected_beach, f"{year}/{slot}: incorrect beach eligibility")
            if not is_qualified:
                ensure(not games and row["bracket_end_state"] == "DID_NOT_QUALIFY", f"{year}/{slot}: nonqualifier received match")
                continue
            total_qualifiers += 1
            total_byes += int(is_bye)
            ensure(bool(games), f"{year}/{slot}: qualifier missing all matches")
            lost = [g for g in games if g["outcome"] == "LOSS"]
            ensure(len(lost) == (0 if slot == src["champion_slot"] else 1), f"{year}/{slot}: elimination cardinality")
            state = "CHAMPION" if not lost else "ELIMINATED_" + lost[0]["round"]
            ensure(row["bracket_end_state"] == state, f"{year}/{slot}: elimination round mismatch")
            ensure(not (is_bye and any(g["round"] == "QF" for g in games)), f"{year}/{slot}: bye team played quarterfinal")
            for g in games:
                ensure(g["round"] in ("QF", "SF", "FINAL"), f"{year}/{slot}: invalid round")
                ensure(g["opponent_team_slot"] in entries and g["opponent_team_slot"] != slot, f"{year}/{slot}: opponent not valid qualifier")
                ensure(g["outcome"] in ("WIN", "LOSS"), f"{year}/{slot}: invalid match outcome")
                ensure(isinstance(g["own_score"], (int, float)) and isinstance(g["opponent_score"], (int, float)), f"{year}/{slot}: invalid score")
                ensure(g["own_score"] != g["opponent_score"], f"{year}/{slot}: tied frozen result")
                ensure((g["own_score"] > g["opponent_score"]) == (g["outcome"] == "WIN"), f"{year}/{slot}: result contradicts points")
                fixture_views[g["match_id"]].append((slot, g))
                appearances[g["round"]].append((slot, g))
                total_appearances += 1

        ensure(set(fixture_views) == set(src["match_ids"]), f"{year}: annual fixture IDs do not reconcile")
        actual_match_ids.update(src["match_ids"])
        round_count = Counter()
        for match_id, sides in fixture_views.items():
            ensure(len(sides) == 2, f"{match_id}: game missing reciprocal opponent record")
            (first, a), (second, b) = sides
            ensure(a["opponent_team_slot"] == second and b["opponent_team_slot"] == first, f"{match_id}: opponent reversal")
            ensure(a["own_score"] == b["opponent_score"] and b["own_score"] == a["opponent_score"], f"{match_id}: reciprocal score drift")
            ensure({a["outcome"], b["outcome"]} == {"WIN", "LOSS"} and a["round"] == b["round"], f"{match_id}: asymmetric outcome")
            round_count[a["round"]] += 1
            if a["round"] == "FINAL":
                winner_slot = first if a["outcome"] == "WIN" else second
                ensure(winner_slot == src["champion_slot"], f"{year}: wrong championship winner")
        ensure(round_count == Counter({k: v for k, v in expected_rounds.items() if v}), f"{year}: fixture round counts")

    source_ids = provenance.get("copied_from_fixture_ids", [])
    ensure(len(source_ids) == len(set(source_ids)) == 56, "Source fixture manifest not 56 unique IDs")
    ensure(set(source_ids) == actual_match_ids, "Historical source fixture IDs disagree with row-level brackets")
    ensure(total_qualifiers == 67 and total_byes == 13 and total_appearances == 112, "League-wide historical totals")
    ensure(matrix["result_counts"]["playoff_qualifier_slot_years"] == total_qualifiers, "Summary qualifier mismatch")
    ensure(matrix["result_counts"]["nonqualifier_slot_years"] == 132 - total_qualifiers, "Summary nonqualifier mismatch")
    ensure(matrix["result_counts"]["first_round_bye_slot_years"] == total_byes, "Summary bye mismatch")
    ensure(matrix["result_counts"]["complete_source_bracket_fixtures"] == 56, "Summary fixtures mismatch")
    ensure(island["counts"]["historical_matches"] == 56, "Island history fixtures different")
    beach = next(x for x in island["three_depth_records"] if x["id"] == "LOSERS_BEACH")
    beach_years = {x["year"]: x for x in beach["layer3"]["historical_beach_years"]}
    ensure(len(beach_years) == 11, "Beach year count")
    for year, src in per_year.items():
        ensure(beach_years[year]["opening_nonqualifier_count"] == 12 - len(src["qualifier_slot_ids"]), f"Beach {year}: opening population")
        ensure(beach_years[year]["postfinal_nonchampion_count"] == 11, f"Beach {year}: postfinal composition")
    return {"status": "PASS_SOURCE_BOUND_NOT_CANON", "slot_year_rows": len(row_map),
            "qualification_records": total_qualifiers, "nonqualifiers": 132 - total_qualifiers,
            "byes": total_byes, "fixture_ids": len(actual_match_ids), "appearance_views": total_appearances,
            "verified_physical_venue_attributions": 0, "independent_ESPN_refetch": False}


if __name__ == "__main__":
    data = json.loads(FILE.read_text(encoding="utf-8"))
    island = json.loads(ISLAND.read_text(encoding="utf-8"))
    print(json.dumps(validate(data, island), sort_keys=True))
