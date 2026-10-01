#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"governance"/"publication-manifest"/"PUBLICATION_MANIFEST_V1.json"

RELEASE_STATES={"DRAFT","CANDIDATE","BLOCKED","RELEASED","CANON_CLOSED","HISTORICAL","SUPERSEDED"}
RELATION_TYPES={"precedes","follows","companion","interprets_same_source_interval","shares_archive_collection"}
SYMMETRIC={"companion","interprets_same_source_interval","shares_archive_collection"}

def load_manifest(path:Path=MANIFEST)->dict:
    return json.loads(path.read_text())

def validate_manifest(doc:dict)->list[str]:
    errors=[]
    if doc.get("schema_version")!="1.0.0":
        errors.append("schema_version must be 1.0.0")
    if doc.get("project")!="schemin-26":
        errors.append("project must be schemin-26")
    if doc.get("manifest_role")!="derived_release_identity_index":
        errors.append("manifest_role must be derived_release_identity_index")
    if not str(doc.get("authority_rule") or "").strip():
        errors.append("authority_rule is required")

    pubs=doc.get("publications")
    if not isinstance(pubs,list) or not pubs:
        return errors+["publications must be a non-empty list"]

    by_id={}
    slugs=set()
    for i,p in enumerate(pubs):
        pid=p.get("publication_id")
        if not isinstance(pid,str) or not pid:
            errors.append(f"publications[{i}] publication_id required")
            continue
        if pid in by_id:
            errors.append(f"duplicate publication_id: {pid}")
        by_id[pid]=p

        slug=p.get("slug")
        if not isinstance(slug,str) or not slug:
            errors.append(f"{pid}: slug required")
        elif slug in slugs:
            errors.append(f"duplicate slug: {slug}")
        slugs.add(slug)

        state=p.get("release_state")
        if state not in RELEASE_STATES:
            errors.append(f"{pid}: invalid release_state {state}")

        refs=p.get("authority_refs")
        if not isinstance(refs,list) or not refs:
            errors.append(f"{pid}: authority_refs must be non-empty")
        else:
            for ref in refs:
                if not isinstance(ref,str) or not ref:
                    errors.append(f"{pid}: invalid authority ref")
                    continue
                if not (ROOT/ref).exists():
                    errors.append(f"{pid}: missing authority ref {ref}")

        for field in ("release_receipt_refs","fact_refs","canon_refs","world_refs","world_evolution_refs","archive_collections","supersedes"):
            value=p.get(field)
            if not isinstance(value,list):
                errors.append(f"{pid}: {field} must be a list")

        artifact=p.get("canonical_artifact")
        release_refs=p.get("release_receipt_refs") or []
        if state in {"RELEASED","CANON_CLOSED"}:
            if not isinstance(artifact,str) or not artifact:
                errors.append(f"{pid}: {state} requires canonical_artifact")
            if not release_refs:
                errors.append(f"{pid}: {state} requires release_receipt_refs")
        if state=="BLOCKED":
            if artifact is not None:
                errors.append(f"{pid}: BLOCKED publication cannot claim canonical_artifact")
            if p.get("publication_date") is not None:
                errors.append(f"{pid}: BLOCKED publication cannot claim publication_date")

        family=p.get("family")
        source=(p.get("source_interval") or {})
        if family=="living_novel" and source.get("kind")=="week":
            errors.append(f"{pid}: Living Novel cannot encode a source week as automatic chapter identity")

        relations=p.get("relations")
        if not isinstance(relations,list):
            errors.append(f"{pid}: relations must be a list")
        else:
            for rel in relations:
                if not isinstance(rel,dict):
                    errors.append(f"{pid}: relation must be object")
                    continue
                if rel.get("type") not in RELATION_TYPES:
                    errors.append(f"{pid}: invalid relation type {rel.get('type')}")
                target=rel.get("publication_id")
                if not isinstance(target,str) or not target:
                    errors.append(f"{pid}: relation target required")
                if target==pid:
                    errors.append(f"{pid}: self relation not allowed")

    # Referential integrity and relation reciprocity
    for pid,p in by_id.items():
        for rel in p.get("relations") or []:
            target=rel.get("publication_id")
            rtype=rel.get("type")
            if target not in by_id:
                errors.append(f"{pid}: relation target missing {target}")
                continue
            target_rels=by_id[target].get("relations") or []
            if rtype=="precedes":
                if not any(x.get("type")=="follows" and x.get("publication_id")==pid for x in target_rels):
                    errors.append(f"{pid}: precedes {target} without reciprocal follows")
            elif rtype=="follows":
                if not any(x.get("type")=="precedes" and x.get("publication_id")==pid for x in target_rels):
                    errors.append(f"{pid}: follows {target} without reciprocal precedes")
            elif rtype in SYMMETRIC:
                if not any(x.get("type")==rtype and x.get("publication_id")==pid for x in target_rels):
                    errors.append(f"{pid}: {rtype} {target} lacks reciprocal relation")

        for prior in p.get("supersedes") or []:
            if prior not in by_id:
                errors.append(f"{pid}: supersedes missing publication {prior}")
            if prior==pid:
                errors.append(f"{pid}: cannot supersede itself")
        superseded_by=p.get("superseded_by")
        if superseded_by is not None:
            if superseded_by not in by_id:
                errors.append(f"{pid}: superseded_by missing publication {superseded_by}")
            elif pid not in (by_id[superseded_by].get("supersedes") or []):
                errors.append(f"{pid}: superseded_by is not reciprocal")

    # Hard anti-fork / current-state invariants
    w2=by_id.get("memo.2026.week-02")
    if w2 and w2.get("canonical_artifact")!="Week 2 memo.pdf":
        errors.append("Week 2 canonical publication identity drifted")
    w3=by_id.get("memo.2026.week-03")
    if w3 and w3.get("canonical_artifact")!="Pro_Schemin_Week_3_Memo_Final.pdf":
        errors.append("Week 3 canonical publication identity drifted")
    w4=by_id.get("memo.2026.week-04")
    if w4 and w4.get("release_state")!="BLOCKED":
        errors.append("Week 4 publication cannot be promoted by manifest while release gate is blocked")
    ch3=by_id.get("novel.2026.chapter-03")
    if ch3:
        required_artifact="living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"
        required_gate="living-novel/qa/CHAPTER_03_FINAL_CANON_GATE_V1.md"
        required_receipt="living-novel/qa/CHAPTER_03_CANON_RELEASE_RECEIPT_V1.md"
        if (
            ch3.get("release_state")!="CANON_CLOSED"
            or ch3.get("canonical_artifact")!=required_artifact
            or required_gate not in (ch3.get("authority_refs") or [])
            or required_receipt not in (ch3.get("release_receipt_refs") or [])
            or not (ROOT/required_gate).exists()
            or not (ROOT/required_receipt).exists()
        ):
            errors.append("Chapter III requires independent Novel canon/release evidence before manifest indexing")

    return errors

def main():
    doc=load_manifest()
    errors=validate_manifest(doc)
    result={"manifest":str(MANIFEST.relative_to(ROOT)),"publications":len(doc.get("publications") or []),"valid":not errors,"errors":errors}
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
