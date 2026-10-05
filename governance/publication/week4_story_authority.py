#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "memo-os/week-4/publication-readiness"
REGISTER = PACK / "WEEK_04_STORY_AUTHORITY_REGISTER.json"

def load_json(path: Path):
    return json.loads(path.read_text())

def git_blob_sha(path: Path) -> str:
    proc = subprocess.run(
        ["git","hash-object",str(path.relative_to(ROOT))],
        cwd=ROOT, check=True, capture_output=True, text=True
    )
    return proc.stdout.strip()

def story_hash(unit: dict) -> str:
    payload = {
        "role": unit["page_role"],
        "sources": [s["blob_sha"] for s in unit["current_controlling_sources"]],
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",",":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def validate(register=None) -> dict:
    doc = register or load_json(REGISTER)
    errors=[]
    units=doc.get("story_units",[])
    by_id={u.get("story_unit_id"):u for u in units}

    required_matchups=set(doc.get("required_matchup_story_units",[]))
    required_modules=set(doc.get("required_editorial_modules",[]))
    missing=[x for x in sorted(required_matchups|required_modules) if x not in by_id]
    if missing:
        errors.append({"code":"STORY_AUTHORITY_UNIT_MISSING","units":missing})

    if len(by_id)!=len(units):
        errors.append({"code":"DUPLICATE_STORY_UNIT_ID"})

    for uid,u in by_id.items():
        if u.get("status")!="CURRENT":
            errors.append({"code":"NON_CURRENT_STORY_UNIT","unit":uid,"state":u.get("status")})
        if not u.get("director_owner") or not u.get("cross_reference_reviewer"):
            errors.append({"code":"MISSING_OWNER_OR_COUNTERWEIGHT","unit":uid})
        if not u.get("current_controlling_sources"):
            errors.append({"code":"MISSING_CONTROLLING_SOURCE","unit":uid})
            continue
        for src in u["current_controlling_sources"]:
            p=ROOT/src["path"]
            if not p.exists():
                errors.append({"code":"CONTROLLING_SOURCE_MISSING","unit":uid,"path":src["path"]})
                continue
            actual=git_blob_sha(p)
            if actual!=src["blob_sha"]:
                errors.append({
                    "code":"STORY_AUTHORITY_SOURCE_STALE",
                    "unit":uid,"path":src["path"],
                    "expected":src["blob_sha"],"actual":actual
                })
        expected=story_hash(u)
        if expected!=u.get("story_authority_hash"):
            errors.append({
                "code":"STORY_AUTHORITY_HASH_MISMATCH",
                "unit":uid,
                "expected":expected,
                "supplied":u.get("story_authority_hash")
            })

    # Exact regression against the rehearsal failure.
    llc=by_id.get("W4-STORY-LLC-HMB")
    if llc:
        rejects=" | ".join(llc.get("superseded_sources",[])).lower()
        combined=" ".join([
            llc.get("page_role",""), llc.get("headline_direction",""),
            llc.get("visual_job",""), llc.get("prose_job",""),
            llc.get("data_job",""), llc.get("transition_job",""), rejects
        ]).lower()
        required_tokens=[
            "one substantial matchup page",
            "the house gets beat",
            "$100",
            "achane",
            "darnold $15",
            "ledger",
            "barometer",
            "three-page"
        ]
        for token in required_tokens:
            if token not in combined:
                errors.append({"code":"LLC_HMB_CURRENT_TREATMENT_INCOMPLETE","missing":token})
        if llc.get("current_page_count")!=1:
            errors.append({"code":"LLC_HMB_STALE_PAGE_COUNT","actual":llc.get("current_page_count")})

    # No artwork while the register itself says no generation.
    if doc.get("generation_state")!="NO_ART_GENERATION_AUTHORIZED":
        errors.append({"code":"GENERATION_STATE_NOT_FAIL_CLOSED"})

    return {
        "state":"FAIL_INTERNAL" if errors else "PASS",
        "errors":errors,
        "story_units":len(units),
        "required_matchups":len(required_matchups),
        "required_modules":len(required_modules)
    }

if __name__=="__main__":
    result=validate()
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result["state"]!="PASS" else 0)
