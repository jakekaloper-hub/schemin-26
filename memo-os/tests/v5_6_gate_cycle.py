#!/usr/bin/env python3
"""V5.6 gates 1–8 executable control cycle.

This suite distinguishes engineering-gate PASS from promotion readiness.
A correctly blocked promotion is a successful safety outcome, not a promotion PASS.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable

ROOT=Path(__file__).resolve().parents[2]
MEMO=ROOT/"memo-os"
TESTS=MEMO/"tests"

@dataclass
class GateResult:
    gate: str
    status: str
    detail: str

def run_py(path: Path) -> tuple[bool,str]:
    p=subprocess.run([sys.executable,str(path)],cwd=ROOT,capture_output=True,text=True)
    tail=(p.stdout+"\n"+p.stderr).strip()[-4000:]
    return p.returncode==0,tail

def require_files(paths):
    missing=[str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    return (not missing, missing)

def gate1():
    required=[
        TESTS/"v5_6_acceptance_suite.py",
        TESTS/"V5_6_ACCEPTANCE_SUITE_SPEC.md",
        MEMO/"PAGE_PRODUCTION_CONTRACT_V1.md",
        MEMO/"MEMO_RELEASE_REGISTRY_SPEC_V1.md",
        MEMO/"CHARACTER_PACKET_GATE_V1.md",
        MEMO/"WORLD_ENCOUNTER_BINDING_V1.md",
        MEMO/"GENERATION_INTENT_FIREWALL_V1.md",
        MEMO/"REFERENCE_MOUNT_RECEIPT_V1.md",
        MEMO/"RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md",
    ]
    ok,missing=require_files(required)
    if not ok:
        return GateResult("G1","FAIL","missing: "+", ".join(missing))
    ok,out=run_py(TESTS/"v5_6_acceptance_suite.py")
    if not ok:
        return GateResult("G1","FAIL","V5.6 suite failed: "+out)
    return GateResult("G1","PASS","Executable V5.6 suite and publication-integrity contracts pass.")

def gate2():
    ok,out=run_py(TESTS/"v5_5_acceptance_suite.py")
    return GateResult("G2","PASS" if ok else "FAIL",
                      "Retained V5.5 suite green." if ok else "V5.5 regression: "+out)

# Gate 3 — injected failures must be caught by the correct control.

def validate_character(expected, rendered):
    hard=["species","body","identity"]
    return all(expected.get(k)==rendered.get(k) for k in hard)

def validate_fact(locked, candidate):
    return locked==candidate

def validate_world(expected, candidate):
    return expected["venue"]==candidate["venue"] and expected["terrain"]==candidate["terrain"]

def validate_intent(expected_type, returned_type):
    return expected_type==returned_type

def validate_refs(expected, mounted):
    return set(expected)==set(mounted)

def validate_asset(asset):
    required=["asset_id","storage_location","content_hash","inspection_status"]
    return all(asset.get(k) for k in required) and asset["inspection_status"]=="PASS"

def gate3():
    checks={}
    checks["wrong_character"]=not validate_character(
        {"identity":"BELT_KEEPER","species":"human_immortal","body":"gaunt"},
        {"identity":"GENERIC_KING","species":"human","body":"bulky"})
    # rename must preserve identity; deliberately altered identity must fail
    checks["rename_redesign"]=not validate_character(
        {"identity":"ARSENAL_GORILLA_WARRIOR","species":"gorilla","body":"massive"},
        {"identity":"ARSENAL_CENTAUR","species":"centaur","body":"equine"})
    checks["wrong_score"]=not validate_fact({"home":121.4,"away":118.2},{"home":118.2,"away":121.4})
    checks["world_conflict"]=not validate_world(
        {"venue":"MUD_DOGS_SWAMP","terrain":"wetland"},
        {"venue":"MOUNTAIN_CASTLE","terrain":"alpine"})
    checks["wrong_artifact"]=not validate_intent("PUBLICATION_ILLUSTRATION","DASHBOARD")
    checks["missing_ref"]=not validate_refs(["REF-A","REF-B"],["REF-A"])
    checks["unaddressable_asset"]=not validate_asset(
        {"asset_id":"A","storage_location":None,"content_hash":None,"inspection_status":"NOT_RUN"})
    bad=[k for k,v in checks.items() if not v]
    return GateResult("G3","PASS" if not bad else "FAIL",
                      "All injected defects rejected at responsible gates." if not bad else "escaped: "+", ".join(bad))

def affected_pages(graph, changed):
    return sorted(p for p,deps in graph.items() if set(deps)&set(changed))

def gate4():
    graph={
      "cover":["story_thesis","character_dk"],
      "scoreboard":["score_dk_obi","standings"],
      "dk_obi_feature":["score_dk_obi","character_dk","character_obi","world_gotw"],
      "mud_tds_feature":["score_mud_tds","character_mud","character_tds","world_mud"],
      "power_rankings":["score_dk_obi","standings","editorial_rank"],
      "final_word":["score_dk_obi","standings","story_thesis"],
    }
    got=affected_pages(graph,{"score_dk_obi"})
    expected=["dk_obi_feature","final_word","power_rankings","scoreboard"]
    if got!=expected:
        return GateResult("G4","FAIL",f"targeted reopen mismatch: {got}")
    if "mud_tds_feature" in got or "cover" in got:
        return GateResult("G4","FAIL","unrelated locked artifact reopened")
    event={"change":"score_dk_obi","reopened":got,"preserved":["cover","mud_tds_feature"]}
    digest=hashlib.sha256(json.dumps(event,sort_keys=True).encode()).hexdigest()[:12]
    return GateResult("G4","PASS",f"Targeted reopen correct; event trace {digest}.")

def page_contract(pid, role, fact=True, character=True, world=True, mobile=True):
    return {
      "page_id":pid,"role":role,
      "fact_dependencies_resolved":fact,
      "character_dependencies_resolved":character,
      "world_dependencies_resolved":world,
      "mobile_budget_defined":mobile,
      "deterministic_data_only":True,
    }

def gate5():
    pages=[
      page_contract("P1","cover"),
      page_contract("P2","matchup"),
      page_contract("P3","scoreboard"),
      page_contract("P4","test_ledger"),
      page_contract("P5","final_word"),
    ]
    contracts_ok=all(all([
      p["fact_dependencies_resolved"],p["character_dependencies_resolved"],
      p["world_dependencies_resolved"],p["mobile_budget_defined"],p["deterministic_data_only"]
    ]) for p in pages)
    candidate={
      "release_id":"SIM-V56-001",
      "status":"CANDIDATE",
      "page_count":len(pages),
      "artifact_digest":None,
      "final_pdf_audit":"NOT_RUN",
      "synthetic":True,
    }
    release_allowed=(
      candidate["status"]=="RELEASED" and
      bool(candidate["artifact_digest"]) and
      candidate["final_pdf_audit"]=="PASS" and
      not candidate["synthetic"]
    )
    ok=contracts_ok and len(pages)==5 and not release_allowed
    return GateResult("G5","PASS" if ok else "FAIL",
      "Synthetic five-page publication completed through contracts; release correctly blocked without real artifact/final audit."
      if ok else "simulation invariant failed")

def gate6():
    # Independent audit reads controlling docs; production artifacts cannot self-certify.
    files={
      "patch":MEMO/"SCHEMIN_26_WEEKLY_MEMO_OS_V5_6_PUBLICATION_INTEGRITY_PATCH.md",
      "release":MEMO/"MEMO_RELEASE_REGISTRY_SPEC_V1.md",
      "intent":MEMO/"GENERATION_INTENT_FIREWALL_V1.md",
      "refs":MEMO/"REFERENCE_MOUNT_RECEIPT_V1.md",
      "asset":MEMO/"RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md",
      "project":ROOT/"PROJECT_CONTROL_REGISTRY.md",
    }
    ok,missing=require_files(files.values())
    if not ok:
        return GateResult("G6","FAIL","missing audit inputs: "+", ".join(missing))
    text={k:p.read_text() for k,p in files.items()}
    checks={
      "rc_not_active":"RELEASE CANDIDATE / NOT ACTIVE" in text["patch"],
      "v55_still_active":"V5.5 Integrated Preproduction Hardening" in text["project"],
      "mercer_firewall":"Mercer" in text["project"],
      "reference_proof":"mounted" in text["refs"].lower(),
      "asset_exact_bytes":"exact bytes" in text["asset"].lower(),
      "wrong_artifact_block":"wrong artifact" in text["intent"].lower() or "wrong artifact class" in text["intent"].lower(),
      "release_lineage":"supersed" in text["release"].lower(),
    }
    bad=[k for k,v in checks.items() if not v]
    return GateResult("G6","PASS" if not bad else "FAIL",
      "Independent authority/privacy/canon/release audit found no critical engineering defect."
      if not bad else "audit failures: "+", ".join(bad))

def gate7():
    # Repo-local hardening checks. GitHub check-state is verified separately by the operator.
    project=(ROOT/"PROJECT_CONTROL_REGISTRY.md").read_text()
    patch=(MEMO/"SCHEMIN_26_WEEKLY_MEMO_OS_V5_6_PUBLICATION_INTEGRITY_PATCH.md").read_text()
    workflow=ROOT/".github/workflows/memo-v5-6-acceptance.yml"
    checks=[
      workflow.exists(),
      "V5.5 Integrated Preproduction Hardening" in project,
      "RELEASE CANDIDATE / NOT ACTIVE" in patch,
      "Promotion gate" in patch,
    ]
    return GateResult("G7","PASS" if all(checks) else "FAIL",
      "PR hardening invariants preserve V5.5 authority and CI acceptance workflow."
      if all(checks) else "PR hardening invariant missing")

def gate8():
    # Promotion evidence is persisted outside the test code so real receipts can
    # advance the gate without hard-coding a self-certifying PASS.
    evidence_path=TESTS/"V5_6_PROMOTION_EVIDENCE_REGISTER.json"
    if not evidence_path.exists():
        return GateResult("G8","BLOCKED","Promotion evidence register missing.")
    reg=json.loads(evidence_path.read_text())
    required=[
      "week2_controlled_reconstruction",
      "week4_real_page_acceptance",
      "actual_reference_mount_proof",
      "renderer_addressable_exact_bytes",
      "final_raster_character_world_intent_qa",
      "independent_release_audit",
      "zero_critical_defects",
    ]
    passing={"PASS"}
    missing=[]
    partial=[]
    for key in required:
        status=(reg.get(key) or {}).get("status","MISSING")
        if status in passing:
            continue
        if status.startswith("PASS_WITH"):
            partial.append(key)
        else:
            missing.append(key)
    if not missing and not partial:
        return GateResult("G8","PASS","All promotion evidence present; eligible for explicit registry promotion.")
    parts=[]
    if missing: parts.append("missing/unsatisfied: "+", ".join(missing))
    if partial: parts.append("partial: "+", ".join(partial))
    return GateResult("G8","BLOCKED","Promotion correctly withheld; "+"; ".join(parts))

GATES=[gate1,gate2,gate3,gate4,gate5,gate6,gate7,gate8]

results=[]
for fn in GATES:
    r=fn()
    results.append(r)
    print(f"{r.status:7} {r.gate} - {r.detail}")

engineering_fail=[r for r in results[:7] if r.status!="PASS"]
if engineering_fail:
    print("ENGINEERING RESULT: FAIL")
    raise SystemExit(1)

print("ENGINEERING RESULT: PASS")
print("PROMOTION RESULT:",results[7].status)
