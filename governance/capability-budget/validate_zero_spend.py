#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/"governance"/"capability-budget"/"ZERO_INCREMENTAL_SPEND_V1.json"

def validate(doc):
    errors=[]
    if doc.get("baseline")!="CHATGPT_PLUS_ONLY":
        errors.append("baseline must be CHATGPT_PLUS_ONLY")
    if doc.get("default_class")!="UNKNOWN_COST_BLOCKED":
        errors.append("default_class must fail closed")
    seen=set()
    for p in doc.get("providers",[]):
        name=p.get("provider")
        if name in seen:
            errors.append(f"duplicate provider: {name}")
        seen.add(name)
        if p.get("class") in {"UNFUNDED_EXTERNAL","UNKNOWN_COST_BLOCKED"} and p.get("critical_path_allowed"):
            errors.append(f"unfunded/unknown provider on critical path: {name}")
    return errors

def main():
    doc=json.loads(REG.read_text())
    errors=validate(doc)
    print(json.dumps({"baseline":doc.get("baseline"),"providers":len(doc.get("providers",[])),"valid":not errors,"errors":errors},indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
