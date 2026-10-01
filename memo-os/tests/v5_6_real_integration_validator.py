#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MEMO=ROOT/"memo-os"
TESTS=MEMO/"tests"

errors=[]

def require(path:Path):
    if not path.exists():
        errors.append(f"missing:{path.relative_to(ROOT)}")
    return path

def require_text(path:Path,*needles:str):
    require(path)
    if not path.exists():
        return
    text=path.read_text()
    for n in needles:
        if n not in text:
            errors.append(f"{path.relative_to(ROOT)} missing token: {n}")

# Authority and supersession.
require_text(ROOT/"PROJECT_CONTROL_REGISTRY.md","V5.5 Integrated Preproduction Hardening")
require_text(TESTS/"V5_6_FINAL_ACCEPTANCE_CHECKPOINT.md","SUPERSEDED","V5_6_PROMOTION_EVIDENCE_REGISTER.json")

# Core V5.6 contracts.
for p in [
    MEMO/"PAGE_PRODUCTION_CONTRACT_V1.md",
    MEMO/"MEMO_RELEASE_REGISTRY_SPEC_V1.md",
    MEMO/"CHARACTER_PACKET_GATE_V1.md",
    MEMO/"WORLD_ENCOUNTER_BINDING_V1.md",
    MEMO/"REFERENCE_MOUNT_RECEIPT_V1.md",
    MEMO/"RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md",
    MEMO/"GENERATION_INTENT_FIREWALL_V1.md",
]:
    require(p)

# Real page receipt wiring.
page=MEMO/"week-4"/"WEEK_4_REAL_PAGE_ACCEPTANCE_V1.md"
require_text(page,
    "REAL WEEK 4 PAGE ACCEPTANCE: PASS",
    "27619581-a3b2-4715-b956-e8439e7b5541",
    "97a316c2-aa34-46cc-b088-442d0c6868a4",
    "ec8c514f-98c6-4493-8436-9dfc68020809",
    "140.78",
    "161.05",
)

# Persisted promotion evidence must not self-certify missing evidence.
reg_path=TESTS/"V5_6_PROMOTION_EVIDENCE_REGISTER.json"
require(reg_path)
if reg_path.exists():
    reg=json.loads(reg_path.read_text())
    expected={
      "week4_real_page_acceptance":"FAIL",
      "actual_reference_mount_proof":"PASS",
      "renderer_addressable_exact_bytes":"PARTIAL",
      "week2_controlled_reconstruction":"MISSING",
      "independent_release_audit":"MISSING",
    }
    for key,status in expected.items():
        got=(reg.get(key) or {}).get("status")
        if got!=status:
            errors.append(f"promotion evidence {key}: expected {status}, got {got}")

# No release promotion yet.
project=(ROOT/"PROJECT_CONTROL_REGISTRY.md").read_text()
if "Current controlling build: **V5.6" in project:
    errors.append("premature V5.6 promotion detected")

if errors:
    print("INTEGRATION VALIDATION: FAIL")
    for e in errors:
        print("-",e)
    raise SystemExit(1)

print("INTEGRATION VALIDATION: PASS")
print("Reference mount and technical page wiring are proven; Week 4 publication fidelity intentionally remains FAIL pending a benchmark-grade replacement page.")
