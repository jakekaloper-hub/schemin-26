#!/usr/bin/env python3
"""Verify that the Atlas summit preserves Playoff Island topology exactly.

The pinned source is a read-only historical dependency from draft PR #322.
Graph validation confers NO canonical route or spatial measurement approval.
"""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(value, reason):
    if not value:
        raise ValueError(reason)


def reachable(node_map, edges, start, target, mode, excluded=None):
    if start not in node_map or target not in node_map:
        return False
    omitted = set(excluded or [])
    seen = {start}
    waiting = deque([start])
    while waiting:
        this = waiting.popleft()
        if this == target:
            return True
        for edge in edges:
            if edge["id"] in omitted or mode not in edge["modes"]:
                continue
            other = edge["to"] if edge["from"] == this else edge["from"] if edge["to"] == this else None
            if other and other not in seen:
                seen.add(other)
                waiting.append(other)
    return False


def validate(source, summit):
    require(source["status"] == "PINNED_PROPOSED_ISLAND_TOPOLOGY_NOT_ACTIVE_WORLD", "Pinned topology promoted or changed status")
    require(summit["status"] == "EDITORIAL_SOURCE_CROSSWALK_NOT_CANON", "Summit topology promoted")
    source_nodes = source["node_records"]
    source_edges = source["edge_records"]
    nodes = {x["id"]: x for x in source_nodes}
    edges = {x["id"]: x for x in source_edges}
    require(len(source_nodes) == len(nodes) == 23, "Source must contain 23 unique island nodes")
    require(len(source_edges) == len(edges) == 45, "Source must contain 45 unique island edges")
    require(source["source_declared_checks"]["node_count"] == 23
            and source["source_declared_checks"]["edge_count"] == 45, "Source PR #322 topology counts not synchronized")
    require(source["source_blob_sha"] == summit["source_topology_blob_sha"], "Summit must pin exact upstream source blob")
    require(summit["pinned_topology_path"].endswith("/ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json"),
            "Source lock not discoverable")
    receipt = summit["known_source_defect"]
    require(receipt["recorded"] == receipt["actual"] == 45
            and receipt["status"] == "RESOLVED_IN_UPSTREAM_PR_322", "Outdated 41-vs-45 source discrepancy or false resolution")
    require(all(n["status"] == "PROPOSED_ONLY" and n["coordinates"] is None
                for n in source_nodes), "An island node incorrectly becomes measured active geography")
    require(all(e["status"] == "PLANNING_ONLY"
                and e["from"] in nodes and e["to"] in nodes and e["from"] != e["to"]
                and bool(e["modes"]) and len(e["modes"]) == len(set(e["modes"]))
                for e in source_edges), "Non-proposed, dangling, self-loop or invalid source edge")

    summit_nodes = {x["id"]: x for x in summit["three_depth_records"] if x["kind"] == "ISLAND_TOPOLOGY_NODE"}
    require(set(summit_nodes) == set(nodes), "Cross-Atlas inspector missing or inventing island nodes")
    for node_id, n in nodes.items():
        d = summit_nodes[node_id]
        require(d["name"] == n["name"] and d["status"] == n["status"],
                f"Stale island name/state: {node_id}")
        require(d["layer1"]["zone"] == n["zone"], f"Stale physical zone: {node_id}")
        require(d["layer2"]["function"] == n["use"], f"Stale civilian function: {node_id}")
        require(d.get("editorial_discoverable") is True, f"Dormant source ID not inspectable: {node_id}")
        for forbidden in ("world_loc_active", "canon_promoted", "public_release"):
            require(d.get(forbidden) is not True, f"Noncanon island unexpectedly published: {node_id}")
        incident = [e for e in source_edges if e["from"] == node_id or e["to"] == node_id]
        require(d["layer1"]["edge_ids"] == [e["id"] for e in incident],
                f"Incident edge ledger incorrect: {node_id}")
        require(d["layer1"]["connected_nodes"] == [
                    e["to"] if e["from"] == node_id else e["from"] for e in incident],
                f"Physical connectivity ledger incorrect: {node_id}")
        require(d["layer1"]["travel_modes"] == [e["modes"] for e in incident],
                f"Travel modes drifted: {node_id}")
        require(d["layer1"]["metric_geometry"] == "NOT_VERIFIED",
                f"Unapproved metric island map: {node_id}")

    # Limited policy checks on the proposed route graph. These are not
    # engineering capacity, tide, crowd or emergency-operability approval.
    require(reachable(nodes, source_edges, "MAINLAND_PUBLIC_LITTORAL", "LOSERS_BEACH", "public"),
            "Beach no longer accessible by public source routes")
    require(not reachable(nodes, source_edges, "MAINLAND_PUBLIC_LITTORAL", "CONTENDER_FORTRESS", "public"),
            "Public foot traffic can enter secured contender residence")
    require(reachable(nodes, source_edges, "CONTENDER_FORTRESS", "LOSERS_BEACH", "post_elimination"),
            "Elimination transition route missing")
    require(reachable(nodes, source_edges, "LOSERS_BEACH", "EMERGENCY_PIER", "emergency"),
            "Beach emergency evacuation route missing")
    require(reachable(nodes, source_edges, "EMERGENCY_PIER", "MAINLAND_PUBLIC_LITTORAL", "emergency"),
            "Beach emergency route to mainland missing")
    for venue in ("IRON_QUARRY", "SALTWIND_STEPS", "BREAKWATER_GROUNDS",
                  "CROWN_STAIR", "GROVE_STANDARDS", "LAST_FIELD"):
        require(reachable(nodes, source_edges, "MAINLAND_PUBLIC_LITTORAL", venue, "public"),
                f"Public spectator route missing: {venue}")
        require(reachable(nodes, source_edges, "CONTENDER_FORTRESS", venue, "contender"),
                f"Contender competition access missing: {venue}")
        require(reachable(nodes, source_edges, "UTILITY_PLANT", venue, "service"),
                f"Site service route missing: {venue}")

    edge_modes = Counter(m for e in source_edges for m in e["modes"])
    return {"status": "PASS_TOPOLOGY_SOURCE_LOCK_NOT_WORLD_CANON",
            "source_nodes": len(nodes), "source_edges": len(edges),
            "summit_nodes_reconciled": len(summit_nodes),
            "losers_beach_source_id": "LOSERS_BEACH",
            "route_mode_counts": dict(sorted(edge_modes.items())),
            "active_world_routes_created": 0, "metric_distances_verified": 0}


if __name__ == "__main__":
    src = load(HERE / "ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json")
    summit = load(HERE / "PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json")
    print(json.dumps(validate(src, summit), sort_keys=True))
