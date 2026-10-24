#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTER=ROOT/"memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json"

def load(path):
    return json.loads(Path(path).read_text())

def validate_packet(packet:dict, register=None)->dict:
    reg=register or load(REGISTER)
    by_id={u["story_unit_id"]:u for u in reg.get("story_units",[])}
    sid=packet.get("story_authority_id")
    current=by_id.get(sid)
    errors=[]
    if not current:
        return {"state":"FAIL","code":"STORY_AUTHORITY_MISMATCH","errors":["UNKNOWN_STORY_AUTHORITY_ID"]}

    if packet.get("story_authority_state")!="CURRENT":
        errors.append("STORY_AUTHORITY_STATE_NOT_CURRENT")
    if packet.get("story_authority_hash")!=current.get("story_authority_hash"):
        errors.append("STORY_AUTHORITY_HASH_MISMATCH")
    if packet.get("story_authority_receipt")!="memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json":
        errors.append("STORY_AUTHORITY_RECEIPT_INVALID")

    expected={
      "story_page_role":current.get("page_role"),
      "visual_job":current.get("visual_job"),
      "prose_job":current.get("prose_job"),
      "data_job":current.get("data_job"),
      "transition_job":current.get("transition_job"),
    }
    for field,value in expected.items():
        if packet.get(field)!=value:
            errors.append(f"{field.upper()}_MISMATCH")

    return {
      "state":"FAIL" if errors else "PASS",
      "code":"STORY_AUTHORITY_MISMATCH" if errors else "SEMANTIC_FIDELITY_PASS",
      "errors":errors,
      "story_unit_id":sid
    }

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("packet")
    args=p.parse_args()
    result=validate_packet(load(Path(args.packet)))
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result["state"]!="PASS" else 0)
