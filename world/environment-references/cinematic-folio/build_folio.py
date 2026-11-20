#!/usr/bin/env python3
"""Compile the read-only Commonwealth location Folio Studio, without image generation.

Authority is the existing World Engine. Cross-PR records are source-pinned and
clearly labeled as *unmerged proposals*. Only previously approved STRUCTURAL SVG
reference bytes are copied into the self-contained local frontend bundle.
"""
import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

FOLIO = Path(__file__).resolve().parent
ROOT = FOLIO.parents[2]
SITE = FOLIO / "site"
DATA = SITE / "data" / "world.json"
STRUCT = SITE / "assets" / "structural"

INPUTS = {
    "locations": "world/data/locations.json",
    "regions": "world/data/physical_zones.json",
    "divisions": "world/data/divisions.json",
    "domains": "world/data/owner_domains.json",
    "routes": "world/data/routes.json",
    "candidates": "world/data/atlas_location_candidates.json",
    "states": "world/data/current_world_state.json",
    "events": "world/data/world_state_events.json",
    "settlements": "world/data/settlements.json",
    "references": "world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json",
    "folio": "world/environment-references/cinematic-folio/LOC_FOLIO_MANIFEST.proposal.json",
    "pr_bridge": "world/environment-references/cinematic-folio/bridge/DRAFT_SOURCE_BRIDGE.proposal.json",
}
def read(key):
    return json.loads((ROOT / INPUTS[key]).read_text())
def digest(data):
    return hashlib.sha256(data).hexdigest()
def sha(path):
    return digest(path.read_bytes())
def match(condition, message):
    if not condition:
        raise ValueError(message)
def build():
    records = {k: read(k) for k in INPUTS}
    locs = records["locations"]["locations"]
    regions = records["regions"]["regions"]
    divisions = records["divisions"]["divisions"]
    domains = records["domains"]["domains"]
    routes = records["routes"]["routes"]
    candidates = records["candidates"]["candidates"]
    states = records["states"]
    events = records["events"]["events"]
    settlements = records["settlements"]["settlements"]
    refs = records["references"]["locations"]
    master = records["folio"]["location_folios"]
    bridge = records["pr_bridge"]
    loc_ids = {x["id"] for x in locs}
    region_ids = {x["id"] for x in regions}
    div_ids = {x["id"] for x in divisions}
    route_ids = {x["id"] for x in routes}
    ref_by_id = {x["location_id"]: x for x in refs}
    master_by_id = {x["id"]: x for x in master}
    domain_by_id = {x["primary_location_id"]: x for x in domains}
    event_by_loc = {}
    for e in events:
        match(e["location_id"] in loc_ids, "Unknown event location: "+e["location_id"])
        event_by_loc.setdefault(e["location_id"], []).append(e)
    match(len(locs) == len(loc_ids) == len(ref_by_id) == len(master_by_id) == 23, "LOC identity mismatch")
    match(len(regions) == len(region_ids) == 7, "Physical zone count or ID mismatch")
    match(len(divisions) == len(div_ids) == 3, "League division count mismatch")
    match(len(domains) == 12, "Owner-home count mismatch")
    match(len(routes) == len(route_ids) == 18, "Travel-graph count mismatch")
    match(len(set(x["character_id"] for x in domains)) == 12, "Owner identity collision")
    match(len(set(x["team_id"] for x in domains)) == 12, "Team-slot collision")
    match(len(set(domain_by_id)) == 12, "Two owners assigned one primary home")
    match({x["division_id"] for x in domains} == div_ids, "Unexpected home division")
    match(all(x["primary_location_id"] in loc_ids for x in domains), "Missing primary location")
    match(all(x["physical_zone_id"] in region_ids for x in locs), "Unknown location region")
    team_ids = []
    for div in divisions:
        match(len(div["member_team_ids_2026"]) == 4, "Expected four members in "+div["id"])
        team_ids.extend(div["member_team_ids_2026"])
    match(len(set(team_ids)) == 12, "Division overlap across team slots")
    match(set(team_ids) == {x["team_id"] for x in domains}, "Team-slot membership drift")
    for owner in domains:
        div = next(x for x in divisions if x["id"] == owner["division_id"])
        match(owner["team_id"] in div["member_team_ids_2026"], "Owner/Division mapping drift")
    for r in routes:
        for end in (r["from"], r["to"]):
            match(end in loc_ids, "Route dangling location: "+end)
        for via in r.get("via_location_ids", []) + ([r["via_location_id"]] if r.get("via_location_id") else []):
            match(via in loc_ids, "Unknown waypoint: "+via)
    for loc in locs:
        match(loc["id"] in ref_by_id and loc["id"] in master_by_id, "Missing reference: "+loc["id"])
        match(master_by_id[loc["id"]]["physical_zone_id"] == loc["physical_zone_id"], "Folio region drift")
        match(master_by_id[loc["id"]]["requested_render_states"]["establishing_master_16x9"] == "SOURCE_INDEX_ONLY", "False render readiness")
        match(master_by_id[loc["id"]]["approved_cinematic_reference_uri"] is None, "Unreviewed image promoted")
    for l in locs:
        for r in l["access_route_ids"]:
            match(r in route_ids, "Missing route: "+r)
    match(len(candidates) == 48, "Main candidate store changed; explicit review required")
    match(len(bridge["proposals"]) == 199, "Cross-branch union drift")
    match(len(bridge["island"]["nodes"]) == 23 and len(bridge["island"]["edges"]) == 45, "Island topology drift")
    nodes = {x["id"] for x in bridge["island"]["nodes"]}
    match(len(nodes) == 23, "Island node identifier duplication")
    match(all(x["from"] in nodes and x["to"] in nodes for x in bridge["island"]["edges"]), "Island edge endpoint unknown")
    match(len(bridge["island"]["venues"]) == 9, "Island round-venue count drift")
    annual = bridge["island"]["annual_proposed_site_program"]
    match(len(annual) == 11 and [x["year"] for x in annual] == list(range(2015, 2026)),
          "Island year/period source drift")
    venue_ids = {v["id"] for v in bridge["island"]["venues"]}
    for year in annual:
        match(set(year["site_ids"]).issubset(venue_ids), "Island venue not source-known in "+str(year["year"]))
        match(year["site_chronology_truth"] != "verified", "Proposed venue history misrepresented")
    match(len(set(x["id"] for x in bridge["proposals"])) == 199, "Repeated proposal code")
    # Source-pin the *inputs* and the exact bytes of the approved structural refs.
    source_receipts = {k: {"path": v, "sha256": sha(ROOT / v)} for k,v in INPUTS.items()}
    structural = {}
    for loc in locs:
        ref = ref_by_id[loc["id"]]
        match(ref["structural_reference_status"] == "APPROVED_STRUCTURAL_REFERENCE", "Structural reference not approved")
        match(ref["cinematic_reference_status"] == "MISSING_APPROVED_CINEMATIC_REFERENCE", "Unexpected cinematic approval")
        match(not ref["approved_cinematic_reference_uris"], "Unverified cinematic bytes")
        uri = ref["approved_structural_reference_uris"][0]
        path = (ROOT / uri).resolve()
        match(path.is_relative_to(ROOT.resolve()) and path.is_file(), "Missing/unsafe structural plate URI")
        structural[loc["id"]] = {"source_path": uri, "sha256": sha(path),
                                 "local_path": "assets/structural/"+loc["id"]+".svg"}
    enriched = []
    for loc in locs:
        identity = loc["id"]
        dom = domain_by_id.get(identity)
        refs_data = ref_by_id[identity]
        visible_route_ids = [x["id"] for x in routes if identity in (
            [x["from"],x["to"]] + x.get("via_location_ids", []) +
            ([x["via_location_id"]] if x.get("via_location_id") else []))]
        historical = event_by_loc.get(identity, [])
        card_path = "world/location-control-plane/locations/"+identity+"/CARD.json"
        match((ROOT/card_path).is_file(), "Missing source Location Card: "+identity)
        enriched.append({
            **loc,
            "owner_home": bool(dom),
            "home_team": dom["team"] if dom else None,
            "home_character_id": dom["character_id"] if dom else None,
            "home_team_id": dom["team_id"] if dom else None,
            "membership_overlays": sorted(set(([loc["division_id"]] if loc.get("division_id") else []) +
                loc.get("division_presence_ids", []))),
            "full_route_ids": visible_route_ids,
            "current_world_state_as_of": states["as_of"],
            "current_world_state": states["locations"].get(identity, []),
            "historical_events": historical,
            "structural_reference": structural[identity],
            "source_location_card": card_path,
            "source_card_sha256": sha(ROOT/card_path),
            "cinematic_asset": {
                "status": "MISSING_APPROVED_CINEMATIC_REFERENCE",
                "approved_reference_uri": None,
                "candidate_path_not_a_file": master_by_id[identity]["target_paths"]["render_master"],
                "render_preparation_status": "SOURCE_INDEX_ONLY"
            }
        })
    domain_records = []
    portrait_by_char = {x["id"]: x for x in bridge["character_reference_library"]["assets"]}
    for d in domains:
        portrait = portrait_by_char.get(d["character_id"])
        match(portrait is not None and portrait["location_id"] == d["primary_location_id"],
              "Visual library/home source mismatch: "+d["character_id"])
        domain_records.append({**d, "location": next(x["name"] for x in locs if x["id"]==d["primary_location_id"]),
                               "portrait_reference": portrait,
                               "portrait_display_permission": "INTERNAL_REVIEW_ONLY_NOT_BUNDLED"})
    region_records = []
    for reg in regions:
        region_records.append({**reg,
             "location_ids": [x["id"] for x in locs if x["physical_zone_id"] == reg["id"]],
             "settlement_textures": [x for x in settlements if x["physical_zone_id"] == reg["id"]]})
    proposal_records = []
    main_candidates = {x["id"]: x for x in candidates}
    for rec in bridge["proposals"]:
        ident = rec["id"]
        kind = ("ACTIVE_MAIN_LOC" if ident in loc_ids else
                "MAIN_EDITORIAL_CANDIDATE" if ident in main_candidates else
                "UNMERGED_CROSS_PR_PROPOSAL")
        proposal_records.append({**rec, "source_class": kind,
                                 "main_candidate": main_candidates.get(ident),
                                 "is_active_world_location": ident in loc_ids})
    payload = {
        "schema": "schemin.cinematic_folio.studio_dataset.v1",
        "status": "READ_ONLY_CODE_PREVIEW_NO_ART_GENERATION_OR_CANON_PROMOTION",
        "world_version": "World Engine V1.1 / main authoritative geography",
        "world_state_as_of": states["as_of"],
        "world_state_warning": "Current world-state snapshot is end_of_week_3_2026; not verified as a Week 11 present-state snapshot.",
        "division_law": "League divisions are nonexclusive affiliation overlays, not sovereign countries or segregated habitats.",
        "coordinate_law": "Schemin-local-v1 abstract, non-metric; plotted pins/lines are schematic relationships only.",
        "source_sha256": source_receipts,
        "stats": {"divisions":3, "homelands":12, "locations":23, "regions":7,
                  "routes":18, "main_candidates":48, "cross_pr_identifiers":199,
                  "approved_structural_references":23,"approved_cinematic_references":0,
                  "island_nodes_proposed":23, "island_edges_proposed":45, "island_venues_proposed":9},
        "divisions": divisions, "characters": domain_records, "locations":enriched,
        "regions": region_records, "routes": routes, "events": events,
        "main_candidates": candidates, "cross_pr": {
            "concordance": bridge["concordance"], "source_pins": bridge["sources"],
            "proposals": proposal_records, "island": bridge["island"],
            "character_library": {"scope": "12 internal character references; NOT approved location images",
                                  "status": "INTERNAL_REVIEW_RENDERER_QA_HOLD", "count":12},
            "observer_preview": bridge["observer_preview"]
        },
        "rendering_law": "No images are generated. All 23 copied SVGs are previously approved structural diagrams, not cinematic masters."
    }
    return payload, structural
def serialize(data):
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail unless generated artifacts equal source compilation")
    args = ap.parse_args()
    world,structural = build()
    expected = serialize(world)
    if args.check:
        match(DATA.is_file() and DATA.read_text() == expected, "Data JSON not reproducible")
        for ref in structural.values():
            dest = SITE / ref["local_path"]
            match(dest.is_file() and sha(dest) == ref["sha256"], "Structural asset drift: "+ref["source_path"])
        print("PASS 3 divisions, 12 homes, 7 regions, 23 LOC, 18 routes, 48 CAND, 199 cross-PR handles, 23+45 island topology")
        return
    DATA.parent.mkdir(parents=True, exist_ok=True)
    STRUCT.mkdir(parents=True, exist_ok=True)
    DATA.write_text(expected)
    for ref in structural.values():
        shutil.copyfile(ROOT / ref["source_path"], SITE / ref["local_path"])
    print("WROTE",DATA,"and 23 PRE-EXISTING approved structural diagrams (NO new images)")
if __name__ == "__main__":
    main()
