#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DIR=ROOT/"planning"/"character-native-render"
GAPS=DIR/"PROGRAM_GAP_REGISTER_V1.json"
PLAN=DIR/"PHASE_1_13_EXECUTION_PLANS_V1.md"
MATRIX=DIR/"DIRECTOR_AUTHORITY_COUNTERWEIGHT_MATRIX_V1.md"
NEXT=DIR/"NEXT_GATE_DECISION_V1.md"

REQUIRED_GAP_FIELDS={"id","severity","phase","title","owner","counterweights","blocker_type","acceptance_evidence","status"}

def validate():
    errors=[]
    gaps=json.loads(GAPS.read_text())
    rows=gaps.get("gaps",[])
    phases={x.get("phase") for x in rows}
    if phases != set(range(1,14)):
        errors.append(f"gap phases must cover 1-13 exactly; got {sorted(phases)}")
    ids=[x.get("id") for x in rows]
    if len(ids)!=len(set(ids)):
        errors.append("gap IDs must be unique")
    for row in rows:
        missing=REQUIRED_GAP_FIELDS-set(row)
        if missing:
            errors.append(f"{row.get('id')}: missing {sorted(missing)}")
        if not row.get("counterweights"):
            errors.append(f"{row.get('id')}: counterweights required")
        if row.get("owner") in set(row.get("counterweights",[])):
            errors.append(f"{row.get('id')}: owner cannot self-counterweight")
    plan=PLAN.read_text()
    for n in range(1,14):
        if f"## Phase {n} " not in plan:
            errors.append(f"Phase {n} execution plan missing")
    matrix=MATRIX.read_text()
    for n in range(1,14):
        if f"| {n} " not in matrix:
            errors.append(f"Phase {n} director matrix row missing")
    nxt=NEXT.read_text()
    if "PHASE 1 — EXACT SOURCE-BYTE PORTABILITY" not in nxt:
        errors.append("next gate must be Phase 1")
    return errors

if __name__=="__main__":
    errors=validate()
    print(json.dumps({"valid":not errors,"errors":errors},indent=2))
    raise SystemExit(1 if errors else 0)
