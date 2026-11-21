#!/usr/bin/env python3
"""No-render end-to-end proof: source authority -> scene -> job -> render request -> lineage.

No renderer is invoked. The proof is intended to detect authority escalation
at the compiler/render boundary.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from adapt_2026_memo_season import compile_season
from build_compiler_manifest import build_manifest
from render_request_bridge import render_request
from artifact_lineage import planned_receipt

def build_proof():
    season=compile_season()
    # Use a source-backed accepted Week 5 event and Scene. Mark only the copied
    # Scene render-eligible for this no-render contract proof.
    event=next(e for e in season["events"] if e["league_time"]["week"]==5 and e["authority"]["evidence_status"]=="VERIFIED")
    scene=next(s for s in season["scenes"] if s["event_id"]==event["event_id"])
    scene=json.loads(json.dumps(scene))
    scene["qa"]["publication_state"]="RENDER_ELIGIBLE"
    manifest=build_manifest([event],[scene],"audit308-no-render")
    job=next(j for j in manifest["jobs"] if j["surface"]=="PNG")
    req=render_request(job,scene,event=event)
    receipt=planned_receipt(job,scene,manifest["source_snapshot"])
    return {
      "event_id":event["event_id"],
      "scene_id":scene["scene_id"],
      "job_id":job["job_id"],
      "event_authority":event["authority"]["evidence_status"],
      "render_request_evidence_status":req["evidence"]["status"],
      "render_request_freshness":req["evidence"]["freshness"],
      "renderer_execution":receipt["renderer"]["execution_status"],
      "artifact_status":receipt["artifact"]["status"],
      "publication_state":receipt["publication"]["state"],
    }

if __name__=="__main__":
    print(json.dumps(build_proof(),indent=2))
