#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/"memo-os/week-4/publication-readiness"
REGISTER=PACK/"WEEK_04_STORY_AUTHORITY_REGISTER.json"
SUPERSESSION=PACK/"WEEK_04_STORY_SUPERSESSION_MAP.json"
OWNERSHIP=PACK/"WEEK_04_DIRECTOR_OWNERSHIP_MATRIX.json"

def load_json(path): return json.loads(Path(path).read_text())
def git_blob_sha(path):
    p=subprocess.run(["git","hash-object",str(Path(path).relative_to(ROOT))],cwd=ROOT,check=True,capture_output=True,text=True)
    return p.stdout.strip()
def story_hash(unit):
    payload={"role":unit["page_role"],"sources":[s["blob_sha"] for s in unit["current_controlling_sources"]]}
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def validate(register=None):
    doc=register or load_json(REGISTER)
    errors=[]
    units=doc.get("story_units",[])
    by_id={u.get("story_unit_id"):u for u in units}
    required=set(doc.get("required_matchup_story_units",[]))|set(doc.get("required_editorial_modules",[]))
    missing=sorted(required-set(by_id))
    if missing: errors.append({"code":"STORY_AUTHORITY_UNIT_MISSING","units":missing})
    if len(by_id)!=len(units): errors.append({"code":"DUPLICATE_STORY_UNIT_ID"})
    for uid,u in by_id.items():
        if u.get("status")!="CURRENT": errors.append({"code":"NON_CURRENT_STORY_UNIT","unit":uid})
        if not u.get("director_owner") or not u.get("cross_reference_reviewer"): errors.append({"code":"MISSING_OWNER_OR_COUNTERWEIGHT","unit":uid})
        for src in u.get("current_controlling_sources",[]):
            p=ROOT/src["path"]
            if not p.exists():
                errors.append({"code":"CONTROLLING_SOURCE_MISSING","unit":uid,"path":src["path"]}); continue
            actual=git_blob_sha(p)
            if actual!=src["blob_sha"]: errors.append({"code":"STORY_AUTHORITY_SOURCE_STALE","unit":uid,"path":src["path"],"expected":src["blob_sha"],"actual":actual})
        if story_hash(u)!=u.get("story_authority_hash"): errors.append({"code":"STORY_AUTHORITY_HASH_MISMATCH","unit":uid})
    expected_counts={
      "W4-STORY-DK-OBI":4,"W4-STORY-MUD-TDS":3,"W4-STORY-RED-DUCK":3,
      "W4-STORY-SLOB-CHILI":3,"W4-STORY-LLC-HMB":3,"W4-STORY-ELNINO-7DC":3
    }
    for uid,count in expected_counts.items():
        if by_id.get(uid,{}).get("current_page_count")!=count: errors.append({"code":"PAGE_COUNT_MISMATCH","unit":uid,"expected":count,"actual":by_id.get(uid,{}).get("current_page_count")})
    if doc.get("generation_state")!="PRE_ART_LOCKED_WAITING_ON_FLAIM_ONLY": errors.append({"code":"GENERATION_STATE_INVALID"})
    smap=load_json(SUPERSESSION)
    rows=smap.get("classifications",[])
    if not any(r.get("classification")=="SUPERSEDED" and "one-page LLC" in r.get("source","") for r in rows): errors.append({"code":"STALE_LLC_ONE_PAGE_NOT_SUPERSEDED"})
    for forbidden in ("Repair Bridge","Club-Information Bridge","Models/Pressure Bridge"):
        if not any(r.get("classification")=="FORBIDDEN" and r.get("source")==forbidden for r in rows): errors.append({"code":"FORBIDDEN_BRIDGE_NOT_RECORDED","source":forbidden})
    ownership=load_json(OWNERSHIP)
    gates=ownership.get("gates",[])
    if [g.get("gate_id") for g in gates] != [f"G{i}" for i in range(1,13)]: errors.append({"code":"DIRECTOR_GATE_SET_INVALID"})
    for g in gates:
        if not g.get("owner") or not g.get("counterweight") or g.get("control_status")!="PASS": errors.append({"code":"DIRECTOR_GATE_INVALID","gate":g.get("gate_id")})
    return {"state":"FAIL_INTERNAL" if errors else "PASS","errors":errors,"story_units":len(units)}

if __name__=="__main__":
    r=validate(); print(json.dumps(r,indent=2)); raise SystemExit(1 if r["state"]!="PASS" else 0)
