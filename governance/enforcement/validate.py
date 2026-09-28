#!/usr/bin/env python3
import argparse
import fnmatch
import json
import re
from datetime import datetime, timezone
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

def _exception_records(root: Path):
    p=root/"governance/enforcement/EXCEPTIONS_V1.json"
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("exceptions",[])

def is_excepted(root: Path, policy_id: str, scope: str):
    for rec in _exception_records(root):
        if rec.get("status")!="ACTIVE" or rec.get("policy_id")!=policy_id:
            continue
        if fnmatch.fnmatch(scope,rec.get("scope_glob","")):
            return True
    return False

def validate_character_canon(root: Path, registry):
    errors=[]
    assertions_path=root/"governance/enforcement/CANON_ASSERTIONS_V1.json"
    if not assertions_path.exists():
        return ["missing CANON_ASSERTIONS_V1.json"]
    assertions=json.loads(assertions_path.read_text())
    lock_path=root/assertions["source_visual_lock"]
    if not lock_path.exists():
        errors.append(f"missing visual canon lock {assertions['source_visual_lock']}")
    else:
        lock=lock_path.read_text(errors="replace")
        if assertions["source_sha256"] not in lock:
            errors.append("visual canon lock checksum mismatch/missing")

    identity_path=root/"living-novel/os/adapters/flaim/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json"
    if not identity_path.exists():
        errors.append("missing active identity registry")
        return errors
    data=json.loads(identity_path.read_text())
    records={rec["owner"]:rec for rec in data.get("records",[])}
    expected=assertions["owners"]
    if set(records)!=set(expected):
        errors.append(f"identity owner set mismatch: expected {sorted(expected)}, got {sorted(records)}")
    for owner,spec in expected.items():
        rec=records.get(owner)
        if not rec:
            continue
        if rec.get("canonical_character")!=spec["title"]:
            errors.append(f"{owner} title mismatch: {rec.get('canonical_character')} != {spec['title']}")
        invariants=set(rec.get("hard_invariants",[]))
        for inv in spec.get("invariants",[]):
            if inv not in invariants:
                errors.append(f"{owner} missing invariant: {inv}")

    master=root/"canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md"
    if not master.exists():
        errors.append("missing master character canon")
    else:
        text=master.read_text(errors="replace")
        for owner,spec in expected.items():
            anchor=f"### {owner} /"
            if anchor not in text:
                errors.append(f"master canon missing owner section: {owner}")
                continue
            section=text.split(anchor,1)[1].split("### ",1)[0]
            if f"**Character:** {spec['title']}." not in section:
                errors.append(f"master canon title mismatch for {owner}")
        jake=text.split("### Jake Kaloper /",1)[1].split("### ",1)[0] if "### Jake Kaloper /" in text else ""
        if "NO CHAMPIONSHIP BELT" not in jake:
            errors.append("Jake NO CHAMPIONSHIP BELT invariant missing from master canon")
        wilson=text.split("### Wilson Look /",1)[1].split("### ",1)[0] if "### Wilson Look /" in text else ""
        if "Arsenal Centaur" not in wilson or "gorilla" not in wilson.lower():
            errors.append("Wilson Arsenal Centaur / never-gorilla invariants incomplete")
    return errors
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
            if not is_excepted(root,"AUTH-001",rel):
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
def validate_temporal_state(root: Path, registry):
    errors=[]
    contract=root/"docs/governance/SUBSYSTEM_TEMPORAL_LINEAGE_CONTRACT_V1.md"
    if not contract.exists():
        errors.append("missing subsystem temporal lineage contract")

    prologue=root/"chronicles/proof-of-concept/prologue"
    historical=[
        "PROLOGUE_MANUSCRIPT_V1.md",
        "PROLOGUE_MANUSCRIPT_V2_AUDITED.md",
        "PROLOGUE_MANUSCRIPT_V3_REBUILD.md",
    ]
    for name in historical:
        p=prologue/name
        if not p.exists():
            errors.append(f"missing historical manuscript {name}")
            continue
        text=p.read_text(errors="replace")
        if "SUPERSEDED HISTORICAL MANUSCRIPT" not in text or "DO NOT USE AS CURRENT PRODUCTION PARENT" not in text:
            errors.append(f"historical manuscript lacks supersession lock: {name}")

    v4=prologue/"PROLOGUE_MANUSCRIPT_V4_CONSULTANT_REVISION.md"
    if not v4.exists():
        errors.append("missing current V4 manuscript parent")
    else:
        text=v4.read_text(errors="replace")
        if "CURRENT PRODUCTION PARENT" not in text:
            errors.append("V4 does not declare CURRENT PRODUCTION PARENT")
        if "current production parent does not mean final published manuscript" not in text:
            errors.append("V4 lacks publication-status distinction")

    mercer=root/"mercer/OPERATING_CONTRACT.md"
    if not mercer.exists():
        errors.append("missing Mercer operating contract")
    else:
        text=mercer.read_text(errors="replace")
        required=[
            "Historical recommendations are decision-journal evidence, not standing instructions",
            "current-state evidence is freshly resolved through the Data Gateway / controlling ledger",
        ]
        for phrase in required:
            if phrase not in text:
                errors.append(f"Mercer temporal rule missing: {phrase}")
    return errors
def validate_mercer_firewall(root: Path, registry):
    errors=[]
    public_roots=[
        root/"chronicles",
        root/"living-novel/manuscript",
        root/"living-novel/narrative",
        root/"living-novel/art",
        root/"productions",
    ]
    patterns=[
        (re.compile(r"Mercer grade\s+[A-F][+-]?",re.I),"Mercer grade"),
        (re.compile(r"Mercer judged",re.I),"Mercer judged"),
        (re.compile(r"MERCER CALL:",re.I),"MERCER CALL"),
        (re.compile(r"Mercer recommends",re.I),"Mercer recommends"),
        (re.compile(r"Mercer valuation",re.I),"Mercer valuation"),
    ]
    allow_paths={
        "chronicles/proof-of-concept/prologue/PROLOGUE_PRESEASON_EVIDENCE_AND_EMOTIONAL_SPINE.md",
    }
    for base in public_roots:
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            rel=p.relative_to(root).as_posix()
            text=p.read_text(errors="replace")
            for rx,label in patterns:
                for m in rx.finditer(text):
                    if rel in allow_paths:
                        line=text[:m.start()].count("\n")+1
                        line_text=text.splitlines()[line-1] if text.splitlines() else ""
                        if "private" in line_text.lower() or "no private" in line_text.lower():
                            continue
                    if not is_excepted(root,"FIREWALL-001",rel):
                        errors.append(f"public creative Mercer leakage [{label}] at {rel}")
                    break
    return errors
def validate_prompt_governance(root: Path, registry):
    errors=[]
    prompt_name=re.compile(r"(PROMPT|DIRECTIVE|HANDOFF|INITIATION)",re.I)
    forbidden_strings={
        "Frat-Bro Berserker":"retired Slob title",
        "People's Champ? / Blue-Collar Spoiler":"retired Chins title",
        "People's Champ / Blue-Collar Spoiler":"retired Chins title",
        "world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md":"retired canon path",
        "XCODE_CHATGPT_HANDOFF.md":"retired handoff path",
        "XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md":"retired handoff path",
    }
    for p in root.rglob("*.md"):
        rel=p.relative_to(root)
        if "archive" in rel.parts:
            continue
        if not prompt_name.search(p.name):
            continue
        text=p.read_text(errors="replace")
        for needle,reason in forbidden_strings.items():
            if needle in text:
                if not is_excepted(root,"PROMPT-001",rel.as_posix()):
                    errors.append(f"active prompt contamination [{reason}] at {rel}: {needle}")
    return errors
def validate_publication_release(root: Path, registry):
    errors=[]
    registry_path=root/"governance/enforcement/RELEASE_REGISTRY_V1.json"
    contract=root/"governance/enforcement/RELEASE_MANIFEST_CONTRACT_V1.md"
    if not registry_path.exists():
        return ["missing release registry"]
    if not contract.exists():
        errors.append("missing release manifest contract")
    release_data=json.loads(registry_path.read_text())
    records=release_data.get("releases",[])
    by_path={}
    required={"artifact_path","status","source_commit","released_at","authority","qa_gates"}
    for idx,rec in enumerate(records):
        missing=required-set(rec)
        if missing:
            errors.append(f"release[{idx}] missing {sorted(missing)}")
            continue
        if rec["status"]!="RELEASED":
            errors.append(f"release[{idx}] invalid status {rec['status']}")
        if not isinstance(rec["qa_gates"],list) or not rec["qa_gates"]:
            errors.append(f"release[{idx}] qa_gates must be non-empty")
        if rec["artifact_path"] in by_path:
            errors.append(f"duplicate release record for {rec['artifact_path']}")
        by_path[rec["artifact_path"]]=rec

    marker=re.compile(r"(\*\*Status:\*\*\s*RELEASED|\*\*Publication status:\*\*\s*RELEASED|PUBLICATION_STATUS:\s*RELEASED)",re.I)
    scan_roots=[root/"memo-os",root/"chronicles",root/"living-novel",root/"productions"]
    for base in scan_roots:
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if "archive" in p.parts:
                continue
            text=p.read_text(errors="replace")
            if marker.search(text):
                rel=p.relative_to(root).as_posix()
                rec=by_path.get(rel)
                if not rec:
                    if not is_excepted(root,"PUB-001",f"release:{rel}"):
                        errors.append(f"RELEASED artifact lacks release registry record: {rel}")
    return errors

def validate_data_gateway_dependency(root: Path, registry):
    warnings=[]
    expected=[
        "data-gateway/check_snapshot_health.py",
        "tests/test_data_gateway_snapshot_contract.py",
        ".github/workflows/data-gateway-ci.yml",
    ]
    for rel in expected:
        if not (root/rel).exists():
            warnings.append(f"PR #12 hardening dependency not yet integrated: missing {rel}")
    workflow=root/".github/workflows/espn-cold-standby.yml"
    if workflow.exists():
        text=workflow.read_text(errors="replace")
        if "data/live" not in text:
            warnings.append("ESPN workflow does not yet persist operational state to data/live")
    refresh=root/"data-gateway/refresh_espn_snapshot.py"
    if refresh.exists():
        text=refresh.read_text(errors="replace")
        if "snapshot_age_seconds" not in text:
            warnings.append("refresh_espn_snapshot.py lacks snapshot_age_seconds hardening from PR #12")
    return warnings

def validate_security_scan(root: Path, registry):
    errors=[]
    patterns=[
        (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),"private key"),
        (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),"GitHub classic token"),
        (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),"GitHub fine-grained token"),
        (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),"API secret token"),
        (re.compile(r"\bESPN_S2\s*[:=]\s*['\"]?[^\s'\"]{12,}"),"ESPN_S2 credential"),
        (re.compile(r"\bSWID\s*[:=]\s*['\"]?\{?[A-Fa-f0-9-]{16,}\}?"),"SWID credential"),
    ]
    allowed_ext={".md",".json",".py",".js",".yml",".yaml",".txt"}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in allowed_ext or ".git" in p.parts:
            continue
        text=p.read_text(errors="replace")
        for rx,label in patterns:
            if rx.search(text):
                errors.append(f"credential signature [{label}] in {p.relative_to(root)}")
    return errors

def validate_historical_identity(root: Path, registry):
    errors=[]
    path=root/"world/history/2025/2025_OWNER_TEAM_ALIAS_MAP.md"
    if not path.exists():
        return ["missing 2025 owner/team alias map"]
    text=path.read_text(errors="replace")
    required=[
        "HISTORICAL EVIDENCE / IDENTITY RESOLUTION — TO VERIFY WHERE MARKED",
        "canon/SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md",
        "canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md",
        "TO VERIFY",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"historical alias map missing required guard: {phrase}")
    forbidden=[
        "Master Character Canon v1.1",
        "Frat-Bro Berserker / established Slob",
        "People's Champ? / Blue-Collar Spoiler",
        "Philosopher-Warrior / Arsenal Centaur",
    ]
    for phrase in forbidden:
        if phrase in text and not is_excepted(root,"HIST-001",path.relative_to(root).as_posix()):
            errors.append(f"historical alias map uses retired current-identity authority: {phrase}")
    return errors

def validate_index_integrity(root: Path, registry):
    errors=[]
    required=[
        "archive/_INDEX.md",
        "canon/_INDEX.md",
        "memo-os/_INDEX.md",
        "data-gateway/_INDEX.md",
        "mercer/_INDEX.md",
    ]
    retired=[
        "world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md",
        "XCODE_CHATGPT_HANDOFF.md",
        "XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md",
        "living-novel/os/adapters/flaim/registries/PRO_SCHEMIN_IDENTITY_RESOLUTION_V1.json",
    ]
    for rel in required:
        p=root/rel
        if not p.exists():
            errors.append(f"missing active index: {rel}")
            continue
        text=p.read_text(errors="replace")
        for old in retired:
            if old in text and not is_excepted(root,"INDEX-001",rel):
                errors.append(f"active index {rel} references retired authority {old}")
    canon=root/"canon/_INDEX.md"
    if canon.exists():
        text=canon.read_text(errors="replace")
        if "SCHEMIN_26_MASTER_VISUAL_CANON_REFERENCE_LOCK_V1.md" not in text:
            errors.append("canon index does not load visual canon lock")
    return errors

def validate_exceptions(root: Path, registry):
    errors=[]
    path=root/"governance/enforcement/EXCEPTIONS_V1.json"
    if not path.exists():
        return ["missing exception registry"]
    data=json.loads(path.read_text())
    records=data.get("exceptions",[])
    policies={p["policy_id"]:p for p in registry.get("policies",[])}
    seen=set()
    now=datetime.now(timezone.utc)
    for idx,rec in enumerate(records):
        required={"exception_id","policy_id","scope_glob","reason","approved_by","approved_at","status"}
        missing=required-set(rec)
        if missing:
            errors.append(f"exception[{idx}] missing {sorted(missing)}")
            continue
        eid=rec["exception_id"]
        if eid in seen:
            errors.append(f"duplicate exception_id {eid}")
        seen.add(eid)
        policy=policies.get(rec["policy_id"])
        if not policy:
            errors.append(f"{eid} references unknown policy {rec['policy_id']}")
            continue
        if policy.get("exception_policy")=="NONE":
            errors.append(f"{eid} attempts exception on non-exceptable policy {rec['policy_id']}")
        if rec["status"]!="ACTIVE":
            errors.append(f"{eid} invalid status {rec['status']}")
        if not isinstance(rec["approved_by"],list) or not rec["approved_by"]:
            errors.append(f"{eid} approved_by must be non-empty list")
        if len(str(rec["reason"]).strip())<12:
            errors.append(f"{eid} reason too short")
        if not rec.get("expires_at") and not rec.get("review_trigger"):
            errors.append(f"{eid} requires expires_at or review_trigger")
        try:
            datetime.fromisoformat(str(rec["approved_at"]).replace("Z","+00:00"))
        except Exception:
            errors.append(f"{eid} invalid approved_at")
        if rec.get("expires_at"):
            try:
                exp=datetime.fromisoformat(str(rec["expires_at"]).replace("Z","+00:00"))
                if exp.tzinfo is None:
                    exp=exp.replace(tzinfo=timezone.utc)
                if exp<=now:
                    errors.append(f"{eid} is expired")
            except Exception:
                errors.append(f"{eid} invalid expires_at")
        rule=policy.get("exception_policy")
        approvers=set(rec.get("approved_by",[]))
        if rule in {"EXPLICIT_COMMISSIONER_ONLY","COMMISSIONER_RELEASE_OVERRIDE"} and "Jake / Commissioner" not in approvers:
            errors.append(f"{eid} requires Jake / Commissioner approval")
        if rule=="DECLASSIFICATION_REQUIRED" and not {"Warden","Jake / Commissioner"}.issubset(approvers):
            errors.append(f"{eid} requires Warden + Jake / Commissioner approval")
    return errors

def run(root: Path, mode="MERGE"):
    registry=load_registry(root)
    validate_registry(root,registry)
    failures=[]
    warnings=[]

    def should_run(policy):
        if policy["policy_id"]=="SYS-001":
            return False
        if mode=="MERGE":
            return policy["enforcement"] in {"MERGE","AUDIT"}
        if mode=="RELEASE":
            return policy["enforcement"] in {"MERGE","RELEASE","AUDIT"}
        return True

    for policy in registry["policies"]:
        if not should_run(policy):
            continue
        fn=globals()[policy["validator"]]
        result=fn(root,registry) or []
        for item in result:
            msg=f"{policy['policy_id']}: {item}"
            severity=policy["severity"]
            if severity=="WARN":
                warnings.append(msg)
            elif severity=="RELEASE_BLOCK" and mode!="RELEASE":
                warnings.append(msg)
            else:
                failures.append(msg)

    for warning in warnings:
        print(f"WARNING: {warning}")
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
