#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from week4_story_authority import validate as validate_story_authority

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/"memo-os/week-4/publication-readiness"
DATA=PACK/"WEEK_04_DETERMINISTIC_DATA.json"
MANIFEST=PACK/"WEEK_04_PUBLICATION_MANIFEST.json"

def load(path):
    return json.loads(Path(path).read_text())

def validate(data=None, manifest=None):
    data=data or load(DATA)
    manifest=manifest or load(MANIFEST)
    errors=[]

    story_result=validate_story_authority()
    if story_result.get("state")!="PASS":
        errors.append("STORY_AUTHORITY_NOT_PASS")

    rows=data.get("matchups",[])
    if len(rows)!=6:
        errors.append("EXPECTED_SIX_MATCHUPS")

    if manifest.get("page_plan_state")!="LOCKED" and manifest.get("pages"):
        errors.append("ACTIVE_PAGE_PLAN_PRESENT_BEFORE_STORY_LOCK")

    if not data.get("finality"):
        if data.get("final_records") is not None:
            errors.append("FINAL_RECORDS_PRESENT_BEFORE_FINALITY")
        if data.get("standings") is not None:
            errors.append("STANDINGS_PRESENT_BEFORE_FINALITY")
        if data.get("release_safe"):
            errors.append("RELEASE_SAFE_BEFORE_FINALITY")
        for gate_id in ("G1","G3","G4","G5","G6"):
            gate=next(x for x in manifest["gates"] if x["gate_id"]==gate_id)
            if gate.get("state")=="PASS":
                errors.append("PREMATURE_"+gate_id)

    return {
      "state":"FAIL_INTERNAL" if errors else ("HOLD_EXTERNAL" if not data.get("finality") else "PASS"),
      "errors":errors
    }

if __name__=="__main__":
    result=validate()
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result["state"]=="FAIL_INTERNAL" else (2 if result["state"]=="HOLD_EXTERNAL" else 0))
