#!/usr/bin/env python3
"""Librarian + Groundskeeper: artifact lineage receipt construction."""
from __future__ import annotations

def planned_receipt(job,scene,source_snapshot):
    return {
      "schema_version":"1.0",
      "artifact_id":f"ART::{job['job_id']}",
      "job_id":job["job_id"],
      "surface":job["surface"],
      "source_snapshot":source_snapshot,
      "event_ids":[scene["event_id"]],
      "scene_ids":[scene["scene_id"]],
      "authority_receipts":list(scene["authority"]["source_receipts"]),
      "renderer":{
        "profile":job.get("render_profile"),
        "execution_status":"NOT_EXECUTED",
        "execution_receipt":None,
      },
      "artifact":{
        "status":"PLANNED",
        "path":None,
        "sha256":None,
        "bytes":None,
      },
      "qa":{
        "status":"NOT_RUN",
        "gates":list(scene["qa"]["required_gates"]),
        "receipt":None,
      },
      "publication":{
        "state":"UNPUBLISHED",
        "authority_mutation_allowed":False,
      },
    }

def assert_no_false_execution(receipt):
    if receipt["renderer"]["execution_status"]=="NOT_EXECUTED":
        art=receipt["artifact"]
        if art["status"] in {"CREATED","VERIFIED"} or art["path"] or art["sha256"]:
            raise ValueError("FALSE_ARTIFACT_EXECUTION_CLAIM")
    if receipt["qa"]["status"]=="PASS" and receipt["artifact"]["status"]!="VERIFIED":
        raise ValueError("QA_PASS_WITHOUT_VERIFIED_ARTIFACT")
    if receipt["publication"]["state"]=="ACCEPTED" and receipt["qa"]["status"]!="PASS":
        raise ValueError("PUBLICATION_ACCEPTED_WITHOUT_QA_PASS")
    return True
