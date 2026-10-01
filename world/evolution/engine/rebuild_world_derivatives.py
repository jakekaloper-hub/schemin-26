#!/usr/bin/env python3
"""Rebuild deterministic world derivatives after accepted state/history evolution."""
from __future__ import annotations
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
RECEIPT=ROOT/"world"/"evolution"/"LAST_REBUILD_RECEIPT.json"

COMMANDS=[
 [sys.executable,"world/history/build_world_memory.py","--write"],
 [sys.executable,"world/history/build_world_memory.py","--check"],
 [sys.executable,"world/location-control-plane/compiler/generate_cards.py","--write"],
 [sys.executable,"world/location-control-plane/compiler/generate_cards.py","--check"],
 [sys.executable,"world/environment-references/render_structural_plates.py"],
 [sys.executable,"world/atlas/interactive/build_interactive_atlas.py"],
]

def rebuild_state_derivatives(write_receipt=True):
    results=[]
    for cmd in COMMANDS:
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        results.append({"command":cmd,"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]})
        if p.returncode!=0:
            raise RuntimeError(f"DERIVATIVE_REBUILD_FAILED: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    receipt={
      "schema_version":"1.0",
      "status":"PASS",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "commands":results,
      "consumer_hydration":"Memo OS, Novel OS, Universe Resolver and Visual World Packet read rebuilt state/memory/cards on demand; no separate hydration cache exists."
    }
    if write_receipt:
        RECEIPT.write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt

if __name__=="__main__":
    print(json.dumps(rebuild_state_derivatives(),indent=2))
