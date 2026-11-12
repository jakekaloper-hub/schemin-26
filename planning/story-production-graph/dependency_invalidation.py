#!/usr/bin/env python3
"""Deterministic dependency invalidation for Story Production Graph V1.

This module computes transitive downstream impact only. It does not rebuild,
render, publish, or mutate canon.
"""
from __future__ import annotations
from collections import defaultdict, deque
from typing import Iterable

def build_adjacency(edges: Iterable[dict]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        upstream=edge["upstream"]; downstream=edge["downstream"]
        graph[upstream].add(downstream)
    return graph

def impacted_nodes(edges: Iterable[dict], changed_nodes: Iterable[str]) -> list[str]:
    graph=build_adjacency(edges)
    seen=set()
    q=deque(changed_nodes)
    while q:
        node=q.popleft()
        for nxt in sorted(graph.get(node, ())):
            if nxt not in seen:
                seen.add(nxt); q.append(nxt)
    return sorted(seen)

def minimal_rebuild_jobs(edges: Iterable[dict], changed_nodes: Iterable[str], jobs: Iterable[dict]) -> list[str]:
    impacted=set(impacted_nodes(edges,changed_nodes))
    return sorted(j["job_id"] for j in jobs if j["job_id"] in impacted)

if __name__=="__main__":
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]
    fixture=json.loads((root/"planning/story-production-graph/fixtures/week9_minimal.json").read_text())
    compiler=fixture["compiler"]
    edges=compiler["invalidation"]["dependency_edges"]
    changed=[fixture["event"]["event_id"]]
    print(json.dumps({
      "changed":changed,
      "impacted":impacted_nodes(edges,changed),
      "rebuild_jobs":minimal_rebuild_jobs(edges,changed,compiler["jobs"])
    },indent=2))
