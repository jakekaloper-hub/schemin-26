#!/usr/bin/env python3
"""Schemin '26 Weekly World Evolution Engine V1.1.

Dry-run by default. Enforces the published request schema, applies only governed
state/history + candidate-evidence mutations, and executes deterministic rebuild
fanout after accepted active-state changes.
"""
from __future__ import annotations
import argparse, copy, json, os, re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/"world"/"data"
EVROOT=ROOT/"world"/"evolution"
SCHEMA_PATH=EVROOT/"schemas"/"world-evolution-request.schema.json"
EVIDENCE_LEDGER=EVROOT/"CANDIDATE_EVIDENCE_LEDGER.json"

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
        "candidate_evidence":load(EVIDENCE_LEDGER),
    }

def finding(code,severity,message):
    return {"code":code,"severity":severity,"message":message}

def _type_ok(value,typ):
    if typ=="object": return isinstance(value,dict)
    if typ=="array": return isinstance(value,list)
    if typ=="string": return isinstance(value,str)
    if typ=="integer": return isinstance(value,int) and not isinstance(value,bool)
    if typ=="boolean": return isinstance(value,bool)
    return True

def _schema_errors(value,schema,path="$"):
    errors=[]
    typ=schema.get("type")
    if typ and not _type_ok(value,typ):
        return [f"{path}: expected {typ}"]
    if "const" in schema and value!=schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    if isinstance(value,str):
        if "minLength" in schema and len(value)<schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength")
        if "pattern" in schema and not re.fullmatch(schema["pattern"],value):
            errors.append(f"{path}: pattern mismatch")
    if isinstance(value,int) and not isinstance(value,bool):
        if "minimum" in schema and value<schema["minimum"]: errors.append(f"{path}: below minimum")
        if "maximum" in schema and value>schema["maximum"]: errors.append(f"{path}: above maximum")
    if isinstance(value,dict):
        for k in schema.get("required",[]):
            if k not in value: errors.append(f"{path}: missing required property {k}")
        props=schema.get("properties",{})
        if schema.get("additionalProperties") is False:
            for k in value:
                if k not in props: errors.append(f"{path}: unexpected property {k}")
        for k,v in value.items():
            if k in props: errors.extend(_schema_errors(v,props[k],f"{path}.{k}"))
    if isinstance(value,list) and "items" in schema:
        for i,v in enumerate(value):
            errors.extend(_schema_errors(v,schema["items"],f"{path}[{i}]"))
    return errors

def validate_against_published_schema(req):
    schema=load(SCHEMA_PATH)
    return _schema_errors(req,schema)

def validate_request(req: dict[str,Any], payloads: dict[str,Any] | None=None) -> dict[str,Any]:
    p=payloads or world_payloads()
    findings=[finding("SCHEMA_VALIDATION","FATAL",e) for e in validate_against_published_schema(req)]
    if findings:
        return _plan(req,findings,False,False,False,[],[],[],[])

    loc_ids={x["id"] for x in p["locations"]["locations"]}
    zone_ids={x["id"] for x in p["zones"]["regions"]}
    cand={x["id"]:x for x in p["candidates"]["candidates"]}
    event_ids={x["id"] for x in p["events"]["events"]}
    txn_ids={x["transaction_id"] for x in p["ledger"]["transactions"]}

    if req["transaction_id"] in txn_ids:
        findings.append(finding("DUPLICATE_TRANSACTION","FATAL",req["transaction_id"]))
    approvals=req["approvals"]
    state_ops=[]; candidate_evidence=[]; promotion_plans=[]; new_candidate_plans=[]

    for op in req["operations"]:
        typ=op.get("op")
        if typ=="APPEND_WORLD_STATE_EVENT":
            e=op.get("event",{})
            required={"id","week","location_id","event_type","classification","entering_state","continuity_out","source_provenance"}
            missing=sorted(required-set(e))
            if missing: findings.append(finding("EVENT_FIELDS_MISSING","FATAL",",".join(missing)))
            if e.get("id") in event_ids: findings.append(finding("DUPLICATE_EVENT_ID","FATAL",str(e.get("id"))))
            if e.get("location_id") not in loc_ids: findings.append(finding("UNKNOWN_LOCATION","FATAL",str(e.get("location_id"))))
            if not e.get("source_provenance"): findings.append(finding("EVENT_MISSING_PROVENANCE","FATAL",str(e.get("id"))))
            state_ops.append(op)

        elif typ=="SET_LOCATION_STATE":
            if op.get("location_id") not in loc_ids: findings.append(finding("UNKNOWN_LOCATION","FATAL",str(op.get("location_id"))))
            if not isinstance(op.get("state"),list): findings.append(finding("INVALID_STATE","FATAL",str(op.get("location_id"))))
            state_ops.append(op)

        elif typ=="REGISTER_CANDIDATE_EVIDENCE":
            cid=op.get("candidate_id")
            if cid not in cand: findings.append(finding("UNKNOWN_CANDIDATE","FATAL",str(cid)))
            if not op.get("evidence_reference"): findings.append(finding("CANDIDATE_EVIDENCE_MISSING_SOURCE","FATAL",str(cid)))
            candidate_evidence.append(op)

        elif typ=="REQUEST_CANDIDATE_PROMOTION":
            cid=op.get("candidate_id"); c=cand.get(cid)
            if not c:
                findings.append(finding("UNKNOWN_CANDIDATE","FATAL",str(cid))); continue
            reasons=[]
            if not (approvals["umpire"] and approvals["closer"] and approvals["commissioner"]):
                reasons.append("TRIPLE_APPROVAL_REQUIRED")
            if c.get("lifecycle_status") not in {"FUTURE_UNLOCK_CANDIDATE","RARE_NEUTRAL_CANDIDATE","PROVISIONAL_CANON"}:
                reasons.append(f"CANDIDATE_STATUS_NOT_PROMOTABLE:{c.get('lifecycle_status')}")
            if c.get("rejection_reason"):
                reasons.append("CANDIDATE_HAS_REJECTION_REASON")
            event_class=op.get("event_class")
            eligibility=c.get("event_eligibility") or []
            if eligibility and event_class not in eligibility:
                reasons.append("EVENT_CLASS_NOT_ELIGIBLE")
            tech=c.get("technology_translation")
            if tech=="REJECTED_TECH_DRIFT":
                reasons.append("TECHNOLOGY_REJECTED")
            if tech=="REQUIRES_TECH_UNLOCK" and not op.get("technology_unlock_verified"):
                reasons.append("TECHNOLOGY_UNLOCK_REQUIRED")
            if c.get("prerequisites") and not op.get("prerequisites_resolved"):
                reasons.append("PREREQUISITES_UNRESOLVED")
            proposed=op.get("proposed_location",{})
            if not str(proposed.get("id","")).startswith("LOC-"): reasons.append("PROPOSED_LOC_ID_REQUIRED")
            if proposed.get("id") in loc_ids: reasons.append("PROPOSED_LOC_ID_COLLISION")
            if proposed.get("physical_zone_id") not in zone_ids: reasons.append("VALID_ZONE_REQUIRED")
            if op.get("route_resolution")!="RESOLVED": reasons.append("ROUTE_RESOLUTION_REQUIRED")
            if c.get("championship_only"):
                if event_class!="CHAMPIONSHIP": reasons.append("CHAMPIONSHIP_EVENT_REQUIRED")
                if not op.get("championship_verified"): reasons.append("CHAMPIONSHIP_VERIFICATION_REQUIRED")
                if not op.get("finalists_verified"): reasons.append("FINALISTS_VERIFIED_REQUIRED")
            promotion_plans.append({"candidate_id":cid,"ready_for_separate_location_transaction":not reasons,"blockers":reasons,"proposed_location":proposed})

        elif typ=="REGISTER_NEW_CANDIDATE":
            proposal=op.get("candidate",{})
            if not str(proposal.get("id","")).startswith("CAND-"): findings.append(finding("NEW_CANDIDATE_ID_INVALID","FATAL",str(proposal.get("id"))))
            if proposal.get("lifecycle_status")=="APPROVED_ACTIVE_CANON": findings.append(finding("NEW_CANDIDATE_CANNOT_START_ACTIVE","FATAL",str(proposal.get("id"))))
            new_candidate_plans.append(op)

    if state_ops and not req["release_verified"]:
        findings.append(finding("UNVERIFIED_RELEASE","FATAL","state/history mutation requires verified release evidence"))
    if candidate_evidence and not req["release_verified"]:
        findings.append(finding("UNVERIFIED_RELEASE","FATAL","candidate evidence persistence requires verified release evidence"))

    fatal=any(x["severity"]=="FATAL" for x in findings)
    state_apply_allowed=bool(state_ops and not fatal and req["release_verified"] and approvals["umpire"] and approvals["closer"])
    evidence_apply_allowed=bool(candidate_evidence and not fatal and req["release_verified"] and approvals["umpire"] and approvals["closer"])
    valid=not fatal
    rebuild=[]
    if state_ops:
        rebuild += [
          "world/data/world_state_events.json","world/data/current_world_state.json",
          "world/location-control-plane/","world/environment-references/plates/",
          "world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html",
        ]
    if candidate_evidence:
        rebuild += ["world/evolution/CANDIDATE_EVIDENCE_LEDGER.json"]
    return _plan(req,findings,state_apply_allowed,evidence_apply_allowed,valid,state_ops,candidate_evidence,promotion_plans,new_candidate_plans,rebuild)

def _plan(req,findings,state_apply_allowed,evidence_apply_allowed,valid,state_ops,candidate_evidence,promotion_plans,new_candidate_plans,rebuild=None):
    apply_allowed=state_apply_allowed or evidence_apply_allowed
    return {
      "transaction_id":req.get("transaction_id"),
      "status":"FATAL" if any(x["severity"]=="FATAL" for x in findings) else ("READY_TO_APPLY" if apply_allowed else "REVIEW_REQUIRED"),
      "valid":valid,"state_apply_allowed":state_apply_allowed,"candidate_evidence_apply_allowed":evidence_apply_allowed,
      "findings":findings,"state_operations":state_ops,"candidate_evidence":candidate_evidence,
      "candidate_promotion_plans":promotion_plans,"new_candidate_plans":new_candidate_plans,
      "rebuild_targets":list(dict.fromkeys(rebuild or [])),
      "rule":"Candidate promotion is never auto-applied by Phase 5."
    }

def apply_to_payloads(req: dict[str,Any], payloads: dict[str,Any] | None=None):
    p=copy.deepcopy(payloads or world_payloads())
    plan=validate_request(req,p)
    if not (plan["state_apply_allowed"] or plan["candidate_evidence_apply_allowed"]):
        raise ValueError("APPLY_NOT_ALLOWED")
    for op in plan["state_operations"]:
        if op["op"]=="APPEND_WORLD_STATE_EVENT":
            p["events"]["events"].append(copy.deepcopy(op["event"]))
        elif op["op"]=="SET_LOCATION_STATE":
            p["state"]["locations"][op["location_id"]]=copy.deepcopy(op["state"])
    if plan["state_apply_allowed"]:
        p["state"]["as_of"]=f'end_of_week_{req["week"]}_{req["season"]}'
    for op in plan["candidate_evidence"]:
        p["candidate_evidence"]["records"].append({
          "transaction_id":req["transaction_id"],"week":req["week"],"season":req["season"],
          "candidate_id":op["candidate_id"],"evidence_reference":op["evidence_reference"],
          "source_release":req["source_release"]
        })
    p["ledger"]["transactions"].append({
      "transaction_id":req["transaction_id"],"week":req["week"],"season":req["season"],
      "source_release":req["source_release"],"state_operation_count":len(plan["state_operations"]),
      "candidate_evidence_count":len(plan["candidate_evidence"]),"candidate_promotions_applied":0
    })
    return p,plan

def _atomic_write_json(path,obj):
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2)+"\n")
    os.replace(tmp,path)

def apply_to_repo(req: dict[str,Any]) -> dict[str,Any]:
    from rebuild_world_derivatives import rebuild_state_derivatives
    paths={
      "events":DATA/"world_state_events.json","state":DATA/"current_world_state.json",
      "ledger":EVROOT/"WORLD_EVOLUTION_LEDGER.json","candidate_evidence":EVIDENCE_LEDGER
    }
    backups={k:p.read_text() for k,p in paths.items()}
    p,plan=apply_to_payloads(req)
    try:
        _atomic_write_json(paths["events"],p["events"])
        _atomic_write_json(paths["state"],p["state"])
        _atomic_write_json(paths["ledger"],p["ledger"])
        _atomic_write_json(paths["candidate_evidence"],p["candidate_evidence"])
        rebuild_receipt=None
        if plan["state_apply_allowed"]:
            rebuild_receipt=rebuild_state_derivatives()
        receipt={"schema_version":"1.0","transaction_id":req["transaction_id"],"status":"APPLIED","state_rebuilt":bool(rebuild_receipt),"rebuild_receipt":rebuild_receipt}
        _atomic_write_json(EVROOT/"LAST_APPLY_RECEIPT.json",receipt)
        return plan
    except Exception:
        for k,path in paths.items():
            path.write_text(backups[k])
        if plan.get("state_apply_allowed"):
            try: rebuild_state_derivatives()
            except Exception: pass
        raise

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("request"); ap.add_argument("--apply",action="store_true"); ap.add_argument("--plan-out")
    args=ap.parse_args(); req=load(Path(args.request))
    plan=apply_to_repo(req) if args.apply else validate_request(req)
    if args.plan_out: Path(args.plan_out).write_text(json.dumps(plan,indent=2)+"\n")
    print(json.dumps(plan,indent=2)); raise SystemExit(0 if plan["valid"] else 2)

if __name__=="__main__": main()
