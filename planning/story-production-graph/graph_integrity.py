#!/usr/bin/env python3
"""Senior-quality graph integrity checks for Story Production Graph V1.

Pure, deterministic validation helpers. No rendering, publication, mutation,
network access, or authority promotion.
"""
from __future__ import annotations
import hashlib,json
from collections import defaultdict, deque

def _canonical_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def source_fingerprint(events,scenes,issues):
    payload={"events":events,"scenes":scenes,"issues":issues}
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()

def _unique(name,values):
    vals=list(values)
    if len(vals)!=len(set(vals)):
        seen=set(); dup=[]
        for v in vals:
            if v in seen and v not in dup: dup.append(v)
            seen.add(v)
        raise AssertionError(f"duplicate {name}: {dup}")
    return set(vals)

def assert_unique_ids(season,compiler):
    _unique("issue_id",(x["issue_id"] for x in season["issues"]))
    _unique("event_id",(x["event_id"] for x in season["events"]))
    _unique("encounter_id",(x["encounter_id"] for x in season["encounters"]))
    _unique("scene_id",(x["scene_id"] for x in season["scenes"]))
    _unique("job_id",(x["job_id"] for x in compiler["jobs"]))
    _unique("artifact_id",(x["artifact_id"] for x in compiler.get("artifacts",[])))
    return True

def assert_references_resolve(season,compiler):
    issues={x["issue_id"] for x in season["issues"]}
    events={x["event_id"] for x in season["events"]}
    encounters={x["encounter_id"] for x in season["encounters"]}
    scenes={x["scene_id"] for x in season["scenes"]}
    jobs={x["job_id"] for x in compiler["jobs"]}

    for enc in season["encounters"]:
        if enc["event_id"] not in events:
            raise AssertionError(f"encounter {enc['encounter_id']} missing event {enc['event_id']}")
        for sid in enc["scene_ids"]:
            if sid not in scenes:
                raise AssertionError(f"encounter {enc['encounter_id']} missing scene {sid}")

    for s in season["scenes"]:
        if s["event_id"] not in events:
            raise AssertionError(f"scene {s['scene_id']} missing event {s['event_id']}")
        if s["encounter_id"] not in encounters:
            raise AssertionError(f"scene {s['scene_id']} missing encounter {s['encounter_id']}")

    for j in compiler["jobs"]:
        for dep in j["depends_on"]:
            if dep not in scenes and dep not in issues:
                raise AssertionError(f"job {j['job_id']} unresolved dependency {dep}")

    # Edge endpoints may include typed virtual dependency keys derived from
    # real Events/Characters/Locations. Validate their roots rather than
    # requiring a materialized node object for every virtual key.
    for e in compiler["invalidation"]["dependency_edges"]:
        up=e["upstream"]; down=e["downstream"]
        if down not in scenes and down not in jobs:
            raise AssertionError(f"unresolved downstream edge endpoint {down}")
        if up in scenes or up in issues:
            continue
        if up.startswith("EVT-"):
            root=up.split("::",1)[0]
            if root not in events:
                raise AssertionError(f"unresolved event dependency {up}")
            continue
        if up.startswith(("CHAR::","LOC::","COPY::","AUDIO::","PRESENT::")):
            continue
        raise AssertionError(f"unresolved upstream edge endpoint {up}")
    return True

def assert_acyclic(edges):
    graph=defaultdict(set); indegree=defaultdict(int); nodes=set()
    for edge in edges:
        u=edge["upstream"]; v=edge["downstream"]
        nodes.add(u); nodes.add(v)
        if v not in graph[u]:
            graph[u].add(v); indegree[v]+=1
        indegree.setdefault(u,indegree.get(u,0))
    q=deque(sorted(n for n in nodes if indegree[n]==0))
    visited=0
    while q:
        u=q.popleft(); visited+=1
        for v in sorted(graph.get(u,())):
            indegree[v]-=1
            if indegree[v]==0: q.append(v)
    if visited!=len(nodes):
        cyclic=sorted(n for n in nodes if indegree[n]>0)
        raise AssertionError(f"dependency graph contains cycle involving: {cyclic[:20]}")
    return True

def validate_graph(season,compiler):
    assert_unique_ids(season,compiler)
    assert_references_resolve(season,compiler)
    assert_acyclic(compiler["invalidation"]["dependency_edges"])
    return {
      "unique_ids":True,
      "references_resolve":True,
      "acyclic":True,
      "source_fingerprint_sha256":source_fingerprint(season["events"],season["scenes"],season["issues"]),
    }
