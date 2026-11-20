#!/usr/bin/env python3
"""One-time pinned draft-source reader. This does not promote any World Engine data.

Run in an authorized checkout with the six draft source refs fetched as described
in the folio README. A generated compact index is checked in for offline builds.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEST = Path(__file__).with_name("DRAFT_SOURCE_BRIDGE.proposal.json")
SOURCES = {
    "postseason_topology": ("b32ecbc46e82133f7197fc8802a85e6b59abc44a", 322, "planning/postseason/ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json"),
    "postseason_venues": ("b32ecbc46e82133f7197fc8802a85e6b59abc44a", 322, "planning/postseason/ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json"),
    "pr324_atlas": ("8b7ee0f8e5ed8f57c7efb88c4dff15601e883323", 324, "world/atlas/summits/2026-11-20/THREE_LAYER_LOCATION_DOSSIERS_V1.json"),
    "pr324_island": ("8b7ee0f8e5ed8f57c7efb88c4dff15601e883323", 324, "world/atlas/summits/2026-11-20/PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json"),
    "pr325_atlas": ("b7bee20d0fc49aa8c04426545fb25de16eee09c2", 325, "planning/atlas-expansion/ATLAS_THREE_LAYER_DOSSIERS_V1.json"),
    "pr339_concordance": ("ea0b84624b034edceed836890aabe965bf5be3ab", 339, "planning/atlas-geography-gate/CROSS_BRANCH_LOCATION_CONCORDANCE_V1.json"),
    "pr253_character_library": ("1e0089170ee6d4ac9cd829ad1f10a70472147904", 253, "docs/visual/manifest.json"),
}

def main():
    data = {}
    provenance = {}
    for key, (sha, pr, path) in SOURCES.items():
        raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{sha}:{path}"])
        data[key] = json.loads(raw)
        provenance[key] = {
            "pr": pr, "commit": sha, "path": path, "sha256_bytes": hashlib.sha256(raw).hexdigest(),
            "authority": "UNMERGED_DRAFT_SOURCE", "url": f"https://github.com/jakekaloper-hub/schemin-26/pull/{pr}"
        }
    atlas324 = data["pr324_atlas"]
    island324 = data["pr324_island"]
    atlas325 = data["pr325_atlas"]
    concordance = data["pr339_concordance"]
    items = {}
    def add(identifier, name, source, namespace, zone=None, anchor=None):
        item = items.setdefault(identifier, {"id": identifier, "name": name or identifier,
                     "source_prs": [], "namespaces": [], "zone_hypothesis": None,
                     "anchor": None, "production_access": "DRAFT_ONLY_NO_CANON_PROMOTION"})
        item["source_prs"].append(source)
        item["namespaces"].append(namespace)
        if zone and not item["zone_hypothesis"]:
            item["zone_hypothesis"] = zone
        if anchor and not item["anchor"]:
            item["anchor"] = anchor
    for rec in atlas324["active_location_three_layer_dossiers"]:
        add(rec["location_id"], rec.get("name"), 324, "MAIN_ACTIVE_LOC",
            rec.get("level_1_physical_and_arrival", {}).get("physical_zone_id"))
    for rec in atlas324["existing_and_new_candidate_three_layer_dossiers"]:
        layer = rec.get("level_1_physical_and_arrival", {})
        z = layer.get("zone_hypotheses") or []
        add(rec["location_id"], rec.get("name"), 324, "PR324_EDITORIAL_CAND",
            z[0] if z else None)
    for rec in island324["three_depth_records"]:
        add(rec["id"], rec.get("name"), 324, rec.get("kind", "PR324_ISLAND_HANDLE"),
            rec.get("layer1", {}).get("region"))
    for rec in atlas325["records"]:
        add(rec["id"], rec.get("name"), 325, rec.get("namespace","PR325_PROPOSAL"),
            rec.get("zone_id"), rec.get("anchor"))
    proposed324 = {rec["location_id"] for rec in atlas324["active_location_three_layer_dossiers"] +
                   atlas324["existing_and_new_candidate_three_layer_dossiers"]}
    proposed324.update(x["id"] for x in island324["three_depth_records"])
    proposed325 = {x["id"] for x in atlas325["records"]}
    assert len(proposed324) == 155, len(proposed324)
    assert len(proposed325) == 147, len(proposed325)
    assert len(proposed324 & proposed325) == 103
    assert len(items) == 199
    assert proposed324 - proposed325 == set(concordance["pr324_only_ids"])
    assert proposed325 - proposed324 == set(concordance["pr325_only_ids"])
    topo = data["postseason_topology"]
    sites = data["postseason_venues"]
    assert len(topo["nodes"]) == 23 and len(topo["edges"]) == 45
    node_ids = {x["id"] for x in topo["nodes"]}
    assert all(edge["from"] in node_ids and edge["to"] in node_ids for edge in topo["edges"])
    assert len(sites["sites"]) == 9
    refs = data["pr253_character_library"]
    assert len(refs["assets"]) == 12
    bridge = {
        "schema": "schemin.cinematic_folio.cross_pr_preview.v1",
        "status": "SOURCE_PINNED_READONLY_PROPOSAL_NOT_MAIN_CANON",
        "sources": provenance,
        "concordance": {
            "pr324_ids": 155, "pr325_ids": 147, "shared_ids": 103,
            "pr324_only_ids": 52, "pr325_only_ids": 44, "union_ids": 199,
            "note": "199 coded source handles; NOT 199 proven places or active LOCs."
        },
        "proposals": [items[k] for k in sorted(items)],
        "island": {
            "status": topo["status"],
            "geographic_affiliation": topo["island_location"],
            "physical_law": topo["physical_law"],
            "nodes": topo["nodes"], "edges": topo["edges"],
            "venues": [{"id": x["id"], "name": x["name"],
                        "zone": x.get("zone"), "morphology": x.get("morphology"),
                        "round_assignment": x.get("round_assignment"), "categories": x.get("categories")}
                       for x in sites["sites"]],
            "historical_season_count": len(sites["annual"]),
            "annual_proposed_site_program": [
                {"year": y["year"], "era": y["era"], "site_ids": y["site_ids"],
                 "round_counts": y["round_counts"], "historical_event_truth": y["historical_event_truth"],
                 "site_chronology_truth": y["site_chronology_truth"],
                 "media_hardware_state": y["media_hardware_state"]}
                for y in sites["annual"]],
            "source_reported_edge_count": topo.get("checks",{}).get("edge_count"),
            "actual_edge_count": len(topo["edges"]),
            "holds": topo.get("holds",[]),
            "unresolved": "Previous Central Basin championship candidate vs proposed Inner Sea offshore Last Field; mainland causeway anchor unselected.",
            "main_world_mutated": False
        },
        "character_reference_library": {
            "source_pr": 253, "status": "INTERNAL_REVIEW_RENDERER_QA_HOLD",
            "approved_environment_pngs": 0,
            "assets": [{"id": a["id"], "location_id": a["location_id"], "team": a["title"],
                        "source_asset_path": a["asset_path"], "expected_sha256": a["expected_sha256"],
                        "approval": a["approval"], "visibility": a["visibility"]}
                       for a in refs["assets"]]
        },
        "observer_preview": {
            "pr": 314, "commit": "cd5814904fba3bb0d6f51490b30eb854684ffdd8",
            "scope": "23 location environment model candidates in Commonwealth audience-site viewer",
            "approval": "CANDIDATE_NOT_APPROVED",
            "published_or_live_location_assertion": False
        },
    }
    text = json.dumps(bridge, indent=2, ensure_ascii=False) + "\n"
    DEST.write_text(text)
    print(f"CREATED {DEST} proposals={len(items)} island_nodes={len(topo['nodes'])} edges={len(topo['edges'])}")

if __name__ == "__main__":
    main()
