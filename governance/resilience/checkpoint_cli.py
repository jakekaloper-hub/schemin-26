#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from resilience import (
    ROOT,
    build_checkpoint,
    load_workflow_checkpoints,
    latest_valid_checkpoint,
    persist_checkpoint,
)

def emit(args) -> int:
    completed_at=args.completed_at or datetime.now(timezone.utc).isoformat()
    checkpoint=build_checkpoint(
        checkpoint_id=args.checkpoint_id,
        project=args.project,
        workflow=args.workflow,
        stage=args.stage,
        owner=args.owner,
        source_authority=args.source_authority,
        completed_at=completed_at,
        input_paths=args.input,
        output_paths=args.output,
        evidence=args.evidence,
        invalidation_triggers=args.invalidate,
        digest_algo=args.digest_algo,
        root=ROOT,
    )
    path=persist_checkpoint(checkpoint,root=ROOT)
    print(json.dumps({"status":"CHECKPOINT_WRITTEN","path":str(path.relative_to(ROOT)),"checkpoint_id":checkpoint["checkpoint_id"]},indent=2))
    return 0

def resume(args) -> int:
    checkpoints=load_workflow_checkpoints(args.workflow)
    checkpoint=latest_valid_checkpoint(checkpoints,root=ROOT)
    if not checkpoint:
        print(json.dumps({"status":"NO_VALID_CHECKPOINT","workflow":args.workflow},indent=2))
        return 2
    print(json.dumps({"status":"VALID_CHECKPOINT","checkpoint":checkpoint},indent=2))
    return 0

def main() -> int:
    parser=argparse.ArgumentParser(description="Schemin repository-native production checkpoint tool")
    sub=parser.add_subparsers(dest="command",required=True)

    p=sub.add_parser("emit")
    p.add_argument("--checkpoint-id",required=True)
    p.add_argument("--project",required=True)
    p.add_argument("--workflow",required=True)
    p.add_argument("--stage",required=True)
    p.add_argument("--owner",required=True)
    p.add_argument("--source-authority",required=True)
    p.add_argument("--completed-at")
    p.add_argument("--digest-algo",choices=["sha256","git_blob"],default="sha256")
    p.add_argument("--input",action="append",required=True)
    p.add_argument("--output",action="append",required=True)
    p.add_argument("--evidence",action="append",required=True)
    p.add_argument("--invalidate",action="append",required=True)
    p.set_defaults(func=emit)

    p=sub.add_parser("resume")
    p.add_argument("--workflow",required=True)
    p.set_defaults(func=resume)

    args=parser.parse_args()
    return args.func(args)

if __name__=="__main__":
    raise SystemExit(main())
