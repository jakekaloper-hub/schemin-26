#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ASSEMBLY=ROOT/"memo-os/week-4/publication-readiness/WEEK_04_ASSEMBLY_MANIFEST.json"

def load(path=ASSEMBLY):
    return json.loads(Path(path).read_text())

def validate(doc:dict)->dict:
    errors=[]
    page_plan_state=doc.get("page_plan_state")
    pages=doc.get("pages",[])
    nums=[p.get("page_number") for p in pages]
    ids=[p.get("page_id") for p in pages]

    if page_plan_state!="LOCKED":
        if pages:
            errors.append("ACTIVE_PAGES_PRESENT_BEFORE_STORY_LOCK")
        if errors:
            return {"state":"FAIL_INTERNAL","errors":errors,"unresolved_pages":[]}
        return {"state":"HOLD_EXTERNAL","errors":[],"reason":"WAITING_ON_STORY_LOCK","unresolved_pages":[]}

    if not pages:
        errors.append("LOCKED_PAGE_PLAN_EMPTY")
    if nums != list(range(1,len(pages)+1)):
        errors.append("PAGE_ORDER_NOT_CONTIGUOUS")
    if len(ids)!=len(set(ids)):
        errors.append("DUPLICATE_PAGE_ID")

    unresolved=[]
    for p in pages:
        if not p.get("artifact") or not p.get("sha256") or p.get("page_lock")!="PASS":
            unresolved.append(p.get("page_id"))

    if errors:
        return {"state":"FAIL_INTERNAL","errors":errors,"unresolved_pages":unresolved}
    if unresolved or not doc.get("final_pdf") or not doc.get("final_pdf_sha256") or not doc.get("umpire_receipt"):
        return {"state":"HOLD_EXTERNAL","errors":[],"unresolved_pages":unresolved}
    return {"state":"PASS","errors":[],"unresolved_pages":[]}

if __name__=="__main__":
    r=validate(load())
    print(json.dumps(r,indent=2))
    raise SystemExit(1 if r["state"]=="FAIL_INTERNAL" else (2 if r["state"]=="HOLD_EXTERNAL" else 0))
