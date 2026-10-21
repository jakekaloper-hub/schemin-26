#!/usr/bin/env python3
"""Memo OS PNG-first production entrypoint; refuses unverified preflight.
Candidate artifact only: no self-certification, no PDF, no character mounting.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from render_editorial_page import render
from validate_editorial_preflight import validate_atlas,validate_sports,validate_story
from verify_source_inputs import verify_sources

def run(packet_path, output):
    path=Path(packet_path).resolve()
    data=json.loads(path.read_text(encoding="utf-8"))
    errors=verify_sources(data,path)
    if data.get("format")!="schemin-memo-production-v1":
        errors.append("invalid Memo OS production packet format")
    if data.get("production_kind") not in ("SPORTS_DESK","NARRATIVE","FACTUAL_EDITORIAL"):
        errors.append("unsupported production kind")
    atlas=data.get("atlas")
    if atlas is not None:
        errors.extend(validate_atlas(atlas))
    elif data.get("production_kind")=="NARRATIVE":
        errors.append("narrative Atlas preflight required")
    if data.get("production_kind")=="SPORTS_DESK":
        errors.extend(validate_sports(data.get("sports",{})))
    if data.get("production_kind")=="NARRATIVE":
        errors.extend(validate_story(data.get("story",{})))
    if data.get("production_kind") == "SPORTS_DESK" and not data.get("source_inputs"):
        errors.append("Sports Desk authenticated source inputs required")
    if data.get("character_ids"):
        errors.append("BLOCKED_BY_CHARACTER_REFERENCE_PIPELINE: authenticated input receipts required")
    if not data.get("editorial_approval_reference"):
        errors.append("approved editorial reference required")
    src=data.get("page_spec")
    if not isinstance(src,str) or not src:
        errors.append("page spec path required")
    else:
        spec_path=(path.parent/src).resolve()
        if not spec_path.is_relative_to(path.parent):
            errors.append("unsafe page spec path")
        elif not spec_path.is_file():
            errors.append("page spec missing")
        elif data.get("page_spec_sha256") != hashlib.sha256(spec_path.read_bytes()).hexdigest():
            errors.append("page spec SHA-256 mismatch")
    if errors:
        return {"status":"BLOCKED","errors":errors,"render_invoked":False}
    receipt=render(spec_path,output)
    result={"status":"CANDIDATE_NOT_APPROVED","errors":[],"render_invoked":True,
            "packet_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "artifact_sha256":receipt["output_sha256"],"renderer_receipt":receipt,
            "independent_approval":False}
    report=Path(output).with_suffix(".production.json")
    report.write_text(json.dumps(result,indent=2),encoding="utf-8")
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("packet");parser.add_argument("output")
    args=parser.parse_args()
    try:result=run(args.packet,args.output)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        result={"status":"BLOCKED","errors":[str(exc)],"render_invoked":False}
    print(json.dumps(result,indent=2))
    return int(result["status"]=="BLOCKED")

if __name__=="__main__":
    sys.exit(main())
