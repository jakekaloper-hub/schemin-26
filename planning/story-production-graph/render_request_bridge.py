#!/usr/bin/env python3
"""Pitching Coach + Architect lane: bridge compiler jobs to existing Render Adapter requests.

Planning-only. This module emits request payloads but never calls a renderer.
"""
from __future__ import annotations

def render_request(job,scene,event=None,project_control_receipt="PROJECT_CONTROL_UNPROMOTED"):
    profile=job.get("render_profile")
    if profile not in {"CHARACTER_GROUNDED_STATIC","DATA_STORY","MOTION"}:
        raise ValueError(f"NO_RENDER_ADAPTER_PROFILE: {job['surface']}")
    if job["status"]!="READY":
        raise ValueError(f"JOB_NOT_READY: {job['job_id']} status={job['status']}")
    if event is None:
        raise ValueError("EVENT_REQUIRED_FOR_RENDER_AUTHORITY")
    evidence_status=event["authority"]["evidence_status"]
    canon_status=event["authority"]["canon_status"]
    freshness="LOCKED_RELEASE" if evidence_status=="VERIFIED" and canon_status=="ACCEPTED" else "NOT_RELEASE_LOCKED"
    return {
      "schema_version":"1.0",
      "request_id":f"RR::{job['job_id']}",
      "profile":profile,
      "authority":{
        "project_control_receipt":project_control_receipt,
        "character_authority":scene["authority"]["character_authority"],
        "world_authority":scene["authority"]["world_authority"],
        "publication_authority":"existing Schemin publication gates",
      },
      "evidence":{
        "status":evidence_status,
        "freshness":freshness,
        "receipts":list(dict.fromkeys(list(event["authority"]["source_receipts"])+list(scene["authority"]["source_receipts"]))),
      },
      "inputs":{
        "scene_id":scene["scene_id"],
        "event_id":scene["event_id"],
        "cast":scene["cast"],
        "location":scene["location"],
        "source_mapping":scene.get("source_mapping",{}),
      },
      "render_directive":{
        "surface":job["surface"],
        "narrative":scene["narrative"],
        "visual":scene["visual"],
        "sound":scene.get("sound",{}),
      },
      "output_contract":{
        "artifact_type":job["surface"],
        "provenance_required":True,
        "qa_gates":list(scene["qa"]["required_gates"]),
      },
      "safety":{
        "authority_mutation_allowed":False,
        "dependency_installation_allowed":False,
        "external_dependency":"NONE",
      },
    }
