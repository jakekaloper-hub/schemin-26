#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from week4_story_authority import validate as validate_story_authority

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/"memo-os/week-4/publication-readiness"
MANIFEST=PACK/"WEEK_04_PUBLICATION_MANIFEST.json"
PUB_MANIFEST=ROOT/"governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"
CHAR_MATRIX=PACK/"WEEK_04_12_CHARACTER_AUTHORITY_MATRIX.json"
GEN_GATE=PACK/"WEEK_04_PAGE_GENERATION_GATE.md"

def load_json(path): return json.loads(Path(path).read_text())
def file_sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def publication_record():
    doc=load_json(PUB_MANIFEST)
    return next(p for p in doc["publications"] if p["publication_id"]=="memo.2026.week-04")

def validate_internal():
    errors=[]; holds=[]
    manifest=load_json(MANIFEST)
    if manifest.get("issue_length")!=27: errors.append("ISSUE_LENGTH_NOT_27")
    if manifest.get("page_plan_state")!="LOCKED": errors.append("PAGE_PLAN_NOT_LOCKED")
    pages=manifest.get("pages",[])
    if len(pages)!=27: errors.append(f"EXPECTED_27_PAGES_FOUND_{len(pages)}")
    nums=[p.get("page_number") for p in pages]
    if nums!=list(range(1,28)): errors.append("PAGE_ORDER_NOT_1_TO_27")
    if len({p.get("page_id") for p in pages})!=27: errors.append("DUPLICATE_PAGE_ID")
    if manifest.get("external_holds")!=["MNF_ESPN_FLAIM_FINALITY"]: errors.append("NON_FLAIM_PREPRODUCTION_HOLD_PRESENT")
    if not GEN_GATE.exists(): errors.append("PAGE_GENERATION_GATE_MISSING")
    story=validate_story_authority()
    if story.get("state")!="PASS": errors.append({"code":"STORY_AUTHORITY_VALIDATION_FAIL","detail":story.get("errors",[])})
    rows=load_json(CHAR_MATRIX).get("characters",[])
    if len(rows)!=12 or len({x.get("character_id") for x in rows})!=12: errors.append("CHARACTER_MATRIX_NOT_12_UNIQUE")
    for row in rows:
        if len(row.get("expected_sha256",""))!=64 or not row.get("required") or not row.get("reject"): errors.append("CHARACTER_AUTHORITY_ROW_INVALID:"+str(row.get("character_id")))
    pub=publication_record()
    if pub.get("release_state")!="BLOCKED": errors.append("PUBLICATION_PREMATURELY_RELEASED")
    if pub.get("canonical_artifact") is not None: errors.append("CANONICAL_ARTIFACT_EXISTS_PREMATURELY")
    if not errors:
        holds.append({"code":"WAITING_ON_FLAIM_ONLY","detail":"All non-Flaim pre-art controls are locked; final decided-result fields remain open."})
    return {
      "state":"FAIL_INTERNAL" if errors else "HOLD_EXTERNAL",
      "errors":errors,"holds":holds,
      "manifest_sha256":file_sha256(MANIFEST),
      "pages":len(pages),
      "page_plan_state":manifest.get("page_plan_state"),
      "story_authority_state":story.get("state"),
      "only_hold":"MNF_ESPN_FLAIM_FINALITY"
    }

def main():
    r=validate_internal(); print(json.dumps(r,indent=2)); return 1 if r["state"]=="FAIL_INTERNAL" else 2

if __name__=="__main__": raise SystemExit(main())
