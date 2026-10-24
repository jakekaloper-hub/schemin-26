#!/usr/bin/env python3
"""Assemble a read-only review packet from existing Week 3 Memo and Novel texts."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from world.production.run_civilization_rehearsal import run
ROOT=Path(__file__).resolve().parents[2]
FACT=ROOT/"memo-os/week-3/WEEK_3_FACT_LOCK_V1.md"
MEMO=ROOT/"memo-os/week-3/WEEK_3_COMPLETE_MANUSCRIPT_V1.md"
NOVEL=ROOT/"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"
LOCKED="- D0nkey K0ng 172.48 def Mud Dogs 126.86."

def assemble(output:Path)->dict:
    fact=FACT.read_text()
    if LOCKED not in fact:
        raise ValueError("Week 3 source fact changed")
    memo=MEMO.read_text()
    novel=NOVEL.read_text()
    if not memo.strip() or not novel.startswith("# CHAPTER III — THE HILL IS NOT THE KINGDOM"):
        raise ValueError("approved existing editorial source unavailable")
    if "Wilson" not in novel or "Mud Dogs" not in novel:
        raise ValueError("existing manuscript continuity not found")
    manifest=run(output)
    (output/"memo-source.md").write_text(memo)
    (output/"novel-source.md").write_text(novel)
    for filename in ("memo-source.md","novel-source.md"):
        manifest["artifacts"][filename]=hashlib.sha256((output/filename).read_bytes()).hexdigest()
    manifest["existing_editorial_sources"]={
        "memo":"memo-os/week-3/WEEK_3_COMPLETE_MANUSCRIPT_V1.md",
        "novel":"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"}
    manifest["publication_eligible"]=False
    manifest["status"]="SOURCE_BACKED_EDITORIAL_REVIEW_BUNDLE_NOT_PUBLICATION"
    manifest["blockers"]+=["FINAL_PDF_COMPOSITION_AND_ARTWORK_UNVERIFIED",
                            "NOVEL_MANUSCRIPT_APPROVAL_UNVERIFIED",
                            "SIMULATED_UMPIRE_REVIEW_ONLY"]
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    print(json.dumps(assemble(p.parse_args().output),indent=2))
