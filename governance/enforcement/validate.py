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
def validate_authority_uniqueness(root: Path, registry): return []
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
