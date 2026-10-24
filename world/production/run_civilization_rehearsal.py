#!/usr/bin/env python3
"""Run existing Memo QA, Novel OS and Atlas compilers; emit draft artifacts, never publish."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_phase3_verification import verify_week3_recap_context
from world.production.build_visual_world_packet import build_packet

def load(relative,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/relative)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def compile_rehearsal():
    pilot=verify_week3_recap_context()
    if not pilot.get("ok"):
        raise ValueError(f"fact/world preflight failed: {pilot}")
    event=pilot["source_event"]
    loc=pilot["scene_context"]["location_id"]
    memo=load("memo-os/tests/validate_issue.py","civilization_memo_runner").validate_civilization_rehearsal(loc,2026,3,event)
    novel_module=load("living-novel/os/engine/novel_os.py","civilization_novel_runner")
    pov=json.loads((ROOT/"living-novel/production/chapter-03/CHAPTER_03_POV_PACKET_WILSON_V1.json").read_text())
    novel=novel_module.validate_civilization_manuscript_rehearsal(loc,2026,3,pov,event)
    visual=build_packet(loc)
    if not memo.get("ok") or not novel.get("ok"):
        raise ValueError(f"consumer preflight failed: {memo} / {novel}")
    cid=visual["civilization_context"]["context_id"]
    if cid!=memo["context_id"] or cid!=novel["context_id"]:
        raise ValueError("cross-consumer context drift")
    winner,loser=event["winner"],event["loser"]
    score=f'{event["winner_score"]}–{event["loser_score"]}'
    memo_text=(f'# Week 3 Memo — Development-only recap component\n\n'
               f'{winner} defeated {loser}, {score}.\n\n'
               f'Source: {event["fact_lock_path"]}\n'
               f'World context: {cid}\n'
               f'Proposed institutional recap setting: {loc}; not the historical game venue.\n'
               f'Publication: HOLD — no approved page assets, render QA or Umpire receipt.\n')
    novel_text=(f'# Living Novel — Development-only scene planning sheet\n\n'
                f'Historical external event: {winner} defeated {loser}, {score}.\n'
                f'World context: {cid}\n'
                f'Institutional recap setting {loc} is a proposal, not an approved scene.\n'
                f'Existing validated POV packet: {pov["character_id"]}; **not assigned to this event**.\n'
                f'No owner interiority, witnessed knowledge, dialogue, or manuscript scene authorized.\n'
                f'Publication: HOLD pending event-appropriate owner POV and editorial approval.\n')
    return {"manifest":{"status":"DEVELOPMENT_REHEARSAL_ONLY","publication_eligible":False,
                        "event":event,"shared_context_id":cid,
                        "blockers":pilot["blockers"]+["EVENT_APPROPRIATE_OWNER_POV_REQUIRED"],
                        "memo_preflight":memo,"novel_preflight":novel},
            "memo.md":memo_text,"novel.md":novel_text,
            "atlas.json":visual}

def run(output:Path):
    result=compile_rehearsal()
    output.mkdir(parents=True,exist_ok=True)
    for name in ("memo.md","novel.md"):
        (output/name).write_text(result[name],encoding="utf-8")
    (output/"atlas.json").write_text(json.dumps(result["atlas.json"],sort_keys=True,indent=2)+"\n")
    manifest=result["manifest"]
    manifest["artifacts"]={name:hashlib.sha256((output/name).read_bytes()).hexdigest()
                           for name in ("memo.md","novel.md","atlas.json")}
    (output/"manifest.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    return manifest

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.output),indent=2))
