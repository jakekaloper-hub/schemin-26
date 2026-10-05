#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from week4_story_authority import validate as validate_story_authority

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "memo-os/week-4/publication-readiness"
MANIFEST = PACK / "WEEK_04_PUBLICATION_MANIFEST.json"
MATRIX = PACK / "WEEK_04_GATE_ENFORCEMENT_MATRIX.json"
PUB_MANIFEST = ROOT / "governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"
VISUAL_AUTHORITY = ROOT / "canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"
DK_SPEC = ROOT / "canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md"
RELEASE_REGISTRY = ROOT / "governance/release-evidence/registry.json"
STORY_AUTHORITY = PACK / "WEEK_04_STORY_AUTHORITY_REGISTER.json"
CHARACTER_REGISTRY = ROOT / "canon/characters/CHARACTER_REGISTRY.yaml"
CHARACTER_RESOLVER = ROOT / "canon/characters/cccp_resolver.py"

REQUIRED_PACK_FILES = [
    "WEEK_04_PUBLICATION_READINESS_DASHBOARD.md",
    "WEEK_04_FACT_LOCK.md",
    "WEEK_04_PITTYS_BOOK_SETTLEMENT.md",
    "WEEK_04_POWER_RANKINGS_LOCK.md",
    "WEEK_04_STATE_OF_REALM.md",
    "WEEK_04_MATCHUP_CONSEQUENCE_REGISTER.md",
    "WEEK_04_WORLD_STATE_DELTA.md",
    "WEEK_04_PAGE_PACKET_REGISTER.md",
    "WEEK_04_VISUAL_QA_REGISTER.md",
    "WEEK_04_PUBLICATION_DESIGN_QA.md",
    "WEEK_04_CONTINUITY_AUDIT.md",
    "WEEK_04_FINAL_UMPIRE_REPORT.md",
    "WEEK_04_PUBLICATION_RECEIPT.md",
    "WEEK_04_STORY_AUTHORITY_REGISTER.json",
]

DK_REQUIRED = {"ONE BODY", "GORILLA", "FOUR-LEGGED", "ARSENAL"}

def load_json(path: Path):
    return json.loads(path.read_text())

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def publication_record():
    doc = load_json(PUB_MANIFEST)
    return next(p for p in doc["publications"] if p["publication_id"] == "memo.2026.week-04")

def character_production_blockers():
    if not RELEASE_REGISTRY.exists():
        return ["RELEASE_EVIDENCE_REGISTRY_MISSING"]
    reg = load_json(RELEASE_REGISTRY)
    receipts = [r for r in reg.get("receipts", []) if r.get("system_id") == "character-production"]
    if not receipts:
        return ["CHARACTER_PRODUCTION_RECEIPT_MISSING"]
    blocked = [r for r in receipts if r.get("result") == "BLOCKED"]
    if not blocked:
        return []
    return blocked[-1].get("unresolved_blockers", [])

def validate_dk_authority(errors: list[str]):
    authority = load_json(VISUAL_AUTHORITY)
    stale = authority.get("master_lineup", {}).get("stale_for", [])
    row = next((x for x in stale if x.get("character_id") == "CHAR-WILSON-LOOK"), None)
    if not row:
        errors.append("DK_ACTIVE_AUTHORITY_NOT_FOUND")
        return
    arch = str(row.get("canonical_architecture", "")).upper()
    for token in DK_REQUIRED:
        if token not in arch:
            errors.append(f"DK_AUTHORITY_MISSING_{token.replace(' ','_').replace('-','_')}")
    spec = DK_SPEC.read_text().upper()
    for token in DK_REQUIRED:
        if token not in spec:
            errors.append(f"DK_SPEC_MISSING_{token.replace(' ','_').replace('-','_')}")

def validate_current_character_semantics(errors: list[str]):
    registry = CHARACTER_REGISTRY.read_text()
    resolver = CHARACTER_RESOLVER.read_text()

    required = [
        "Frat Star",
        "Arsenal Gorilla Centaur Warrior",
        "FOUR-LEGGED CENTAUR LOWER BODY",
    ]
    for token in required:
        if token not in registry and token not in resolver:
            errors.append(f"ACTIVE_CHARACTER_SEMANTICS_MISSING:{token}")

    forbidden_active = [
        'aliases: ["Fart Star"',
        '"aliases":["Fart Star"',
        'hard_reject: ["centaur anatomy"',
        '"equine lower body","mounted-human substitute"',
    ]
    active_text = registry + "\n" + resolver
    for token in forbidden_active:
        if token in active_text:
            errors.append(f"STALE_ACTIVE_CHARACTER_SEMANTICS:{token}")


def validate_internal() -> dict:
    errors, holds = [], []

    for name in REQUIRED_PACK_FILES:
        if not (PACK / name).exists():
            errors.append(f"MISSING_REQUIRED_ARTIFACT:{name}")

    if not MANIFEST.exists():
        errors.append("WEEK4_MANIFEST_MISSING")
        return {"state":"FAIL_INTERNAL","errors":errors,"holds":holds}
    if not MATRIX.exists():
        errors.append("GATE_MATRIX_MISSING")

    manifest = load_json(MANIFEST)
    gates = manifest.get("gates", [])
    if len(gates) != 12:
        errors.append(f"EXPECTED_12_GATES_FOUND_{len(gates)}")
    ids = [g.get("gate_id") for g in gates]
    if ids != [f"G{i}" for i in range(1,13)]:
        errors.append("GATE_IDS_NOT_G1_TO_G12_IN_ORDER")

    pages = manifest.get("pages", [])
    page_plan_state = manifest.get("page_plan_state")
    if page_plan_state != "LOCKED":
        if pages:
            errors.append("ACTIVE_PAGE_PLAN_PRESENT_BEFORE_STORY_LOCK")
    else:
        nums = [p.get("page_number") for p in pages]
        if not pages or nums != list(range(1, len(pages)+1)):
            errors.append("LOCKED_PAGE_PLAN_INVALID")
        if len({p.get("page_id") for p in pages}) != len(pages):
            errors.append("DUPLICATE_PAGE_ID")

    story_result = validate_story_authority()
    if story_result.get("state") != "PASS":
        errors.append({"code":"STORY_AUTHORITY_VALIDATION_FAIL","detail":story_result.get("errors",[])})
    validate_dk_authority(errors)
    validate_current_character_semantics(errors)

    pub = publication_record()
    if pub.get("release_state") != "BLOCKED":
        errors.append("WEEK4_PUBLICATION_PREMATURELY_PROMOTED")
    if pub.get("canonical_artifact") is not None:
        errors.append("BLOCKED_WEEK4_HAS_CANONICAL_ARTIFACT")

    ext = set(manifest.get("external_holds", []))
    if "MNF_ESPN_FLAIM_FINALITY" not in ext:
        errors.append("MNF_HOLD_NOT_DECLARED")
    blockers = character_production_blockers()
    if blockers:
        holds.append({"code":"CHARACTER_PROVIDER_CAPABILITY_UNPROVEN","detail":blockers})
    else:
        errors.append("CHARACTER_RENDER_HOLD_EXPECTED_BUT_NOT_FOUND")

    for g in gates:
        if g.get("state") == "PASS":
            errors.append(f"PREMATURE_PASS:{g.get('gate_id')}")

    if errors:
        state = "FAIL_INTERNAL"
    elif holds or any(g.get("state") == "HOLD_EXTERNAL" for g in gates):
        state = "HOLD_EXTERNAL"
    else:
        state = "PASS"
    return {
        "state": state,
        "errors": errors,
        "holds": holds,
        "manifest_sha256": file_sha256(MANIFEST),
        "pages": len(pages),
        "page_plan_state": page_plan_state,
        "story_authority_state": story_result.get("state"),
        "gates": len(gates),
    }

def main() -> int:
    result = validate_internal()
    print(json.dumps(result, indent=2))
    if result["state"] == "FAIL_INTERNAL":
        return 1
    if result["state"] == "HOLD_EXTERNAL":
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
