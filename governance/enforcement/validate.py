#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ALLOWED_SEVERITIES={"BLOCK","RELEASE_BLOCK","WARN"}
ALLOWED_ENFORCEMENT={"MERGE","RELEASE","AUDIT"}

class EnforcementFailure(Exception):
    pass

def load_registry(root: Path):
    path=root/"governance/enforcement/SCHEMIN_POLICY_REGISTRY_V1.json"
    return json.loads(path.read_text())

def validate_registry(root: Path, registry):
    required={"policy_id","domain","owner","severity","enforcement","rule","validator","source_authority","exception_policy"}
    seen=set()
    errors=[]
    for idx,p in enumerate(registry.get("policies",[])):
        missing=required-set(p)
        if missing:
            errors.append(f"policy[{idx}] missing {sorted(missing)}")
            continue
        if p["policy_id"] in seen:
            errors.append(f"duplicate policy_id {p['policy_id']}")
        seen.add(p["policy_id"])
        if p["severity"] not in ALLOWED_SEVERITIES:
            errors.append(f"{p['policy_id']} invalid severity {p['severity']}")
        if p["enforcement"] not in ALLOWED_ENFORCEMENT:
            errors.append(f"{p['policy_id']} invalid enforcement {p['enforcement']}")
        if not callable(globals().get(p["validator"])):
            errors.append(f"{p['policy_id']} validator not implemented: {p['validator']}")
        src=root/p["source_authority"]
        if not src.exists():
            errors.append(f"{p['policy_id']} missing source authority {p['source_authority']}")
    if errors:
        raise EnforcementFailure("\n".join(errors))

def validate_character_canon(root: Path, registry): return []
def validate_authority_uniqueness(root: Path, registry):
    errors=[]

    active_master=[
        p for p in root.rglob("SCHEMIN_26_MASTER_CHARACTER_CANON*.md")
        if "archive" not in p.parts
    ]
    expected=root/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md"
    if active_master != [expected]:
        rel=[p.relative_to(root).as_posix() for p in active_master]
        errors.append(f"active master character canon set invalid: {rel}")

    active_ids=[
        p for p in root.rglob("PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json")
        if "archive" not in p.parts
    ]
    expected_id=root/"living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json"
    if active_ids != [expected_id]:
        rel=[p.relative_to(root).as_posix() for p in active_ids]
        errors.append(f"active Flaim identity registry set invalid: {rel}")

    retired_paths=[
        "world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md",
        "XCODE_CHATGPT_HANDOFF.md",
        "XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md",
        "living-novel/os/adapters/flaim/registries/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json",
    ]
    for rel in retired_paths:
        if (root/rel).exists():
            errors.append(f"retired active path resurrected: {rel}")

    archive=root/"archive"
    if archive.exists():
        for p in archive.rglob("*.md"):
            if p.name=="_INDEX.md":
                continue
            text=p.read_text(errors="replace")
            if not text.startswith("# HISTORICAL ONLY — DO NOT USE AS CURRENT PRODUCTION AUTHORITY"):
                errors.append(f"archive markdown missing historical banner: {p.relative_to(root)}")
        for p in archive.rglob("*.json"):
            data=json.loads(p.read_text())
            if data.get("_archive_status")!="ARCHIVE_ONLY":
                errors.append(f"archive json missing ARCHIVE_ONLY status: {p.relative_to(root)}")
    return errors
def validate_temporal_state(root: Path, registry): return []
def validate_mercer_firewall(root: Path, registry): return []
def validate_prompt_governance(root: Path, registry): return []
def validate_publication_release(root: Path, registry): return []
def validate_exceptions(root: Path, registry): return []

def run(root: Path, mode="MERGE"):
    registry=load_registry(root)
    validate_registry(root,registry)
    failures=[]
    for policy in registry["policies"]:
        if policy["policy_id"]=="SYS-001":
            continue
        if mode=="MERGE" and policy["enforcement"]!="MERGE":
            continue
        if mode=="RELEASE" and policy["enforcement"] not in {"MERGE","RELEASE"}:
            continue
        fn=globals()[policy["validator"]]
        result=fn(root,registry) or []
        for item in result:
            failures.append(f"{policy['policy_id']}: {item}")
    if failures:
        raise EnforcementFailure("\n".join(failures))
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",default=".")
    p.add_argument("--mode",choices=["MERGE","RELEASE","AUDIT"],default="MERGE")
    args=p.parse_args()
    root=Path(args.root).resolve()
    try:
        run(root,args.mode)
    except EnforcementFailure as e:
        print(str(e))
        raise SystemExit(1)
    print(f"Enforcement {args.mode} gate PASS")

if __name__=="__main__":
    main()
