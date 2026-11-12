#!/usr/bin/env python3
"""Librarian + Scout lane: source/provenance graph for Story Production Graph V1."""
from __future__ import annotations
from collections import defaultdict

AUTHORITY_ORDER={
  "LEAGUE_EVIDENCE":0,
  "CHARACTER_CANON":1,
  "WORLD_ATLAS":1,
  "MEMO_OS":2,
  "CHRONICLE_PROJECTION":3,
  "RENDER_ARTIFACT":4,
}

def provenance_nodes(events, encounters, scenes, compiler=None):
    nodes={}
    edges=[]
    for e in events:
        nodes[e["event_id"]]={"kind":"EVENT","authority":"MEMO_OS","status":e["authority"]["canon_status"]}
        for src in e["authority"]["source_receipts"]:
            sid=f"SRC::{src}"
            nodes.setdefault(sid,{"kind":"SOURCE","authority":"LEAGUE_EVIDENCE"})
            edges.append({"from":sid,"to":e["event_id"],"relation":"SUPPORTS"})
    for enc in encounters:
        nodes[enc["encounter_id"]]={"kind":"ENCOUNTER","authority":"MEMO_OS"}
        edges.append({"from":enc["event_id"],"to":enc["encounter_id"],"relation":"HYDRATES"})
        for src in enc["authority"]["source_receipts"]:
            sid=f"SRC::{src}"; nodes.setdefault(sid,{"kind":"SOURCE","authority":"MEMO_OS"})
            edges.append({"from":sid,"to":enc["encounter_id"],"relation":"GROUNDS"})
    for s in scenes:
        nodes[s["scene_id"]]={"kind":"SCENE","authority":"MEMO_OS","publication_state":s["qa"]["publication_state"]}
        edges.append({"from":s["event_id"],"to":s["scene_id"],"relation":"CAUSES"})
        edges.append({"from":s["encounter_id"],"to":s["scene_id"],"relation":"INHERITS"})
        for src in s["authority"]["source_receipts"]:
            sid=f"SRC::{src}"; nodes.setdefault(sid,{"kind":"SOURCE","authority":"MEMO_OS"})
            edges.append({"from":sid,"to":s["scene_id"],"relation":"GROUNDS"})
    if compiler:
        for job in compiler.get("jobs",[]):
            nodes[job["job_id"]]={"kind":"JOB","authority":"RENDER_ARTIFACT","status":job["status"]}
            for dep in job["depends_on"]:
                edges.append({"from":dep,"to":job["job_id"],"relation":"BUILDS"})
    return {"nodes":nodes,"edges":edges}

def authority_escalations(graph):
    """Flag downstream nodes that claim stronger authority than their inputs."""
    problems=[]
    for edge in graph["edges"]:
        a=graph["nodes"].get(edge["from"]); b=graph["nodes"].get(edge["to"])
        if not a or not b: continue
        aa=AUTHORITY_ORDER.get(a.get("authority"),99)
        bb=AUTHORITY_ORDER.get(b.get("authority"),99)
        if b.get("kind") in {"SCENE","JOB"} and bb < aa:
            problems.append({"edge":edge,"reason":"DOWNSTREAM_AUTHORITY_ESCALATION"})
    return problems
