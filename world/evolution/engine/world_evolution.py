#!/usr/bin/env python3
"""Schemin '26 Weekly World Evolution Engine V1.

Dry-run by default. Only verified, approved Class A state/history changes may be applied.
Candidate promotion is planned but never automatically applied here.
"""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/"world"/"data"
EVROOT=ROOT/"world"/"evolution"

def load(path: Path) -> dict[str,Any]:
    return json.loads(path.read_text())

def world_payloads() -> dict[str,Any]:
    return {
        "locations":load(DATA/"locations.json"),
        "routes":load(DATA/"routes.json"),
        "zones":load(DATA/"physical_zones.json"),
        "events":load(DATA/"world_state_events.json"),
        "state":load(DATA/"current_world_state.json"),
        "candidates":load(DATA/"atlas_location_candidates.json"),
        "ledger":load(EVROOT/"WORLD_EVOLUTION_LEDGER.json"),
    }

def finding(code,severity,message):
    return {"code":code,"severity":severity,"message":message}

def validate_request(req: dict[str,Any], payloads: dict[str,Any] | None=None) -> dict[str,Any]:
    p=payloads or world_payloads()
    findings=[]
    loc_ids={x["id"] for x in p["locations"]["locations"]}
    route_ids={x["id"] for x in p["routes"]["routes"]}
    zone_ids={x["id"] for x in p["zones"]["regions"]}
    cand={x["id"]:x for x in p["candidates"]["candidates"]}
    event_ids={x["id"] for x in p["events"]["events"]}
    txn_ids={x["transaction_id"] for x in p["ledger"]["transactions"]}

    required=["transaction_id","week","season","source_release","release_verified","operations","approvals"]
    for key in required:
        if key not in req:
            findings.append(finding("MISSING_FIELD","FATAL",key))
    if findings:
        return _plan(req,findings,False,False,[],[],[],[])

    if req["transaction_id"] in txn_ids:
        findings.append(finding("DUPLICATE_TRANSACTION","FATAL",req["transaction_id"]))
    if not req["source_release"]:
        findings.append(finding("MISSING_SOURCE_RELEASE","FATAL","source_release"))
    approvals=req.get("approvals",{})
    state_ops=[]
    candidate_evidence=[]
    promotion_plans=[]
    new_candidate_plans=[]

    for op in req.get("operations",[]):
        typ=op.get("op")
        if typ=="APPEND_WORLD_STATE_EVENT":
            e=op.get("event",{})
            if e.get("id") in event_ids:
                findings.append(finding("DUPLICATE_EVENT_ID","FATAL",str(e.get("id"))))
            if e.get("location_id") not in loc_ids:
                findings.append(finding("UNKNOWN_LOCATION","FATAL",str(e.get("location_id"))))
            if not e.get("source_provenance"):
                findings.append(finding("EVENT_MISSING_PROVENANCE","FATAL",str(e.get("id"))))
            state_ops.append(op)
        elif typ=="SET_LOCATION_STATE":
            if op.get("location_id") not in loc_ids:
                findings.append(finding("UNKNOWN_LOCATION","FATAL",str(op.get("location_id"))))
            if not isinstance(op.get("state"),list):
                findings.append(finding("INVALID_STATE","FATAL",str(op.get("location_id"))))
            state_ops.append(op)
        elif typ=="REGISTER_CANDIDATE_EVIDENCE":
            if op.get("candidate_id") not in cand:
                findings.append(finding("UNKNOWN_CANDIDATE","FATAL",str(op.get("candidate_id"))))
            if not op.get("evidence_reference"):
                findings.append(finding("CANDIDATE_EVIDENCE_MISSING_SOURCE","FATAL",str(op.get("candidate_id"))))
            candidate_evidence.append(op)
        elif typ=="REQUEST_CANDIDATE_PROMOTION":
            cid=op.get("candidate_id")
            c=cand.get(cid)
            if not c:
                findings.append(finding("UNKNOWN_CANDIDATE","FATAL",str(cid)))
                continue
            ready=bool(approvals.get("umpire") and approvals.get("closer") and approvals.get("commissioner"))
            reasons=[]
            if not ready: reasons.append("TRIPLE_APPROVAL_REQUIRED")
            proposed=op.get("proposed_location",{})
            if not str(proposed.get("id","")).startswith("LOC-"):
                reasons.append("PROPOSED_LOC_ID_REQUIRED")
            if proposed.get("id") in loc_ids:
                reasons.append("PROPOSED_LOC_ID_COLLISION")
            if proposed.get("physical_zone_id") not in zone_ids:
                reasons.append("VALID_ZONE_REQUIRED")
            if op.get("route_resolution")!="RESOLVED":
                reasons.append("ROUTE_RESOLUTION_REQUIRED")
            if c.get("championship_only"):
                if op.get("event_class")!="CHAMPIONSHIP": reasons.append("CHAMPIONSHIP_EVENT_REQUIRED")
                if not op.get("championship_verified"): reasons.append("CHAMPIONSHIP_VERIFICATION_REQUIRED")
                if not op.get("finalists_verified"): reasons.append("FINALISTS_VERIFIED_REQUIRED")
            promotion_plans.append({"candidate_id":cid,"ready_for_separate_location_transaction":not reasons,"blockers":reasons,"proposed_location":proposed})
        elif typ=="REGISTER_NEW_CANDIDATE":
            proposal=op.get("candidate",{})
            if not str(proposal.get("id","")).startswith("CAND-"):
                findings.append(finding("NEW_CANDIDATE_ID_INVALID","FATAL",str(proposal.get("id"))))
            if proposal.get("lifecycle_status")=="APPROVED_ACTIVE_CANON":
                findings.append(finding("NEW_CANDIDATE_CANNOT_START_ACTIVE","FATAL",str(proposal.get("id"))))
            new_candidate_plans.append(op)
        else:
            findings.append(finding("UNKNOWN_OPERATION","FATAL",str(typ)))

    if state_ops and not req.get("release_verified"):
        findings.append(finding("UNVERIFIED_RELEASE","FATAL","state/history mutation requires verified release evidence"))

    fatal=any(x["severity"]=="FATAL" for x in findings)
    state_apply_allowed=bool(state_ops and not fatal and req.get("release_verified") and approvals.get("umpire") and approvals.get("closer"))
    rebuild=[]
    if state_ops:
        rebuild += [
          "world/data/world_state_events.json",
          "world/data/current_world_state.json",
          "world/location-control-plane/",
          "world/environment-references/plates/",
          "world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html",
        ]
    if candidate_evidence or promotion_plans or new_candidate_plans:
        rebuild += ["world/data/atlas_location_candidates.json","world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html"]
    return _plan(req,findings,state_apply_allowed,not fatal,state_ops,candidate_evidence,promotion_plans,new_candidate_plans,rebuild)

def _plan(req,findings,state_apply_allowed,valid,state_ops,candidate_evidence,promotion_plans,new_candidate_plans,rebuild=None):
    return {
      "transaction_id":req.get("transaction_id"),
      "status":"FATAL" if any(x["severity"]=="FATAL" for x in findings) else ("READY_TO_APPLY_STATE" if state_apply_allowed else "REVIEW_REQUIRED"),
      "valid":valid,
      "state_apply_allowed":state_apply_allowed,
      "findings":findings,
      "state_operations":state_ops,
      "candidate_evidence":candidate_evidence,
      "candidate_promotion_plans":promotion_plans,
      "new_candidate_plans":new_candidate_plans,
      "rebuild_targets":list(dict.fromkeys(rebuild or [])),
      "rule":"Candidate promotion is never auto-applied by Phase 5."
    }

def apply_to_payloads(req: dict[str,Any], payloads: dict[str,Any] | None=None) -> tuple[dict[str,Any],dict[str,Any]]:
    p=copy.deepcopy(payloads or world_payloads())
    plan=validate_request(req,p)
    if not plan["state_apply_allowed"]:
        raise ValueError("STATE_APPLY_NOT_ALLOWED")
    for op in plan["state_operations"]:
        if op["op"]=="APPEND_WORLD_STATE_EVENT":
            p["events"]["events"].append(copy.deepcopy(op["event"]))
        elif op["op"]=="SET_LOCATION_STATE":
            p["state"]["locations"][op["location_id"]]=copy.deepcopy(op["state"])
    p["state"]["as_of"]=f'end_of_week_{req["week"]}_{req["season"]}'
    p["ledger"]["transactions"].append({
      "transaction_id":req["transaction_id"],
      "week":req["week"],
      "season":req["season"],
      "source_release":req["source_release"],
      "operation_count":len(plan["state_operations"]),
      "candidate_promotions_applied":0
    })
    return p,plan

def apply_to_repo(req: dict[str,Any]) -> dict[str,Any]:
    p,plan=apply_to_payloads(req)
    (DATA/"world_state_events.json").write_text(json.dumps(p["events"],indent=2)+"\n")
    (DATA/"current_world_state.json").write_text(json.dumps(p["state"],indent=2)+"\n")
    (EVROOT/"WORLD_EVOLUTION_LEDGER.json").write_text(json.dumps(p["ledger"],indent=2)+"\n")
    return plan

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("request")
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--plan-out")
    args=ap.parse_args()
    req=load(Path(args.request))
    plan=apply_to_repo(req) if args.apply else validate_request(req)
    if args.plan_out: Path(args.plan_out).write_text(json.dumps(plan,indent=2)+"\n")
    print(json.dumps(plan,indent=2))
    raise SystemExit(0 if plan["valid"] else 2)

if __name__=="__main__": main()
