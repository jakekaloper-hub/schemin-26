#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/"memo-os/week-4/publication-readiness"
W4=PACK/"WEEK_04_PUBLICATION_MANIFEST.json"
ASM=PACK/"WEEK_04_ASSEMBLY_MANIFEST.json"
PUB=ROOT/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"

def load(p): return json.loads(Path(p).read_text())

def validate()->dict:
    errors=[]
    w4=load(W4)
    asm=load(ASM)
    pub=load(PUB)
    gates=w4.get("gates",[])
    not_pass=[g.get("gate_id") for g in gates[:11] if g.get("state")!="PASS"]
    if not_pass:
        return {"state":"RELEASE_BLOCKED","reason":"UPSTREAM_GATES_NOT_PASS","gates":not_pass}
    if asm.get("state")!="PASS":
        return {"state":"RELEASE_BLOCKED","reason":"ASSEMBLY_NOT_PASS"}
    if not asm.get("final_pdf") or not asm.get("final_pdf_sha256"):
        return {"state":"RELEASE_BLOCKED","reason":"FINAL_PDF_NOT_BOUND"}
    rec=next(x for x in pub["publications"] if x["publication_id"]=="memo.2026.week-04")
    if rec.get("release_state")=="RELEASED":
        if rec.get("canonical_artifact")!=asm.get("final_pdf"):
            errors.append("CANONICAL_ARTIFACT_MISMATCH")
        if not rec.get("release_receipt_refs"):
            errors.append("MISSING_RELEASE_RECEIPT_REF")
    if errors:
        return {"state":"FAIL_INTERNAL","errors":errors}
    return {"state":"READY_FOR_RELEASE_TRANSACTION","final_pdf":asm["final_pdf"],"sha256":asm["final_pdf_sha256"]}

if __name__=="__main__":
    r=validate()
    print(json.dumps(r,indent=2))
    raise SystemExit(0 if r["state"]=="READY_FOR_RELEASE_TRANSACTION" else 2)
