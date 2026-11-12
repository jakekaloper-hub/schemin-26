#!/usr/bin/env python3
"""Architect + Setup Man lane: build compiler jobs from Scene V1 objects.

This creates planning jobs only. It never renders or publishes.
"""
from __future__ import annotations
from collections import defaultdict

def _classify(key):
    if "::RESULT" in key: return "RESULT"
    if key.startswith("CHAR::"): return "CHARACTER"
    if key.startswith("LOC::"): return "LOCATION"
    if key.startswith("COPY::"): return "COPY"
    if key.startswith("AUDIO::"): return "AUDIO"
    if key.startswith("PRESENT::"): return "PRESENTATION"
    return "BASE"

SURFACE_PROFILE={
  "PNG":"CHARACTER_GROUNDED_STATIC",
  "MOTION":"MOTION",
  "WEB":None,
  "NOVEL_CONTEXT":None,
  "AUDIO":"MOTION",
  "TIMELINE":None,
}

def build_manifest(events,scenes,source_snapshot="story-graph-source"):
    jobs=[];edges=[]
    for s in scenes:
        for surface in s["outputs"]:
            jid=f"JOB-{s['scene_id']}-{surface}"
            jobs.append({
              "job_id":jid,
              "surface":"PDF" if surface=="PDF_PAGE" else surface,
              "depends_on":[s["scene_id"]],
              "render_profile":SURFACE_PROFILE.get(surface),
              "status":"BLOCKED" if s["qa"]["publication_state"]=="PLANNED" else "READY",
            })
            edges.append({"upstream":s["scene_id"],"downstream":jid})
        for dep in s.get("dependencies",[]):
            if dep.startswith(("EVT-","CHAR::","LOC::","COPY::","AUDIO::","PRESENT::")):
                edges.append({"upstream":dep,"downstream":s["scene_id"],"dependency_class":_classify(dep)})

    return {
      "schema_version":"1.0",
      "build_id":"BUILD-STORY-GRAPH-V1",
      "source_snapshot":source_snapshot,
      "inputs":{
        "event_ids":[e["event_id"] for e in events],
        "scene_ids":[s["scene_id"] for s in scenes],
        "chronicle_projection_ids":[],
      },
      "jobs":jobs,
      "artifacts":[],
      "invalidation":{"dependency_edges":edges},
      "publication":{"authority_mutation_allowed":False,"auto_publish_allowed":False},
    }
