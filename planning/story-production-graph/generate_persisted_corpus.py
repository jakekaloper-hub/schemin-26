#!/usr/bin/env python3
"""Generate/check durable 2026 Story Graph Scene and Chronicle snapshots."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE/"generated/2026"
sys.path.insert(0,str(BASE))
from adapt_2026_memo_season import compile_season
from build_2026_chronicle import build as build_chronicle
from schema_contract_validator import load_schema,validate

def payloads():
    season=compile_season()
    scenes={"schema_version":"1.0","season":2026,"source":"adapt_2026_memo_season.compile_season","scenes":season["scenes"]}
    chron=build_chronicle()
    return scenes,chron

def canonical(obj):
    return json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+"\n"

def check():
    scenes,chron=payloads()
    expected={"scenes.json":canonical(scenes),"chronicle.json":canonical(chron)}
    problems=[]
    for name,want in expected.items():
        path=OUT/name
        if not path.is_file(): problems.append(f"MISSING:{path}")
        elif path.read_text()!=want: problems.append(f"DRIFT:{path}")
    if problems: raise AssertionError(problems)
    for i,s in enumerate(scenes["scenes"]):
        validate(s,load_schema("scene"),f"persisted.scenes[{i}]")
    print(f"PERSISTED_CORPUS_PASS scenes={len(scenes['scenes'])} characters={len(chron['character_timelines'])}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stdout",action="store_true")
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    scenes,chron=payloads()
    if args.stdout:
        print("SCENES_JSON_BEGIN")
        print(canonical(scenes),end="")
        print("SCENES_JSON_END")
        print("CHRONICLE_JSON_BEGIN")
        print(canonical(chron),end="")
        print("CHRONICLE_JSON_END")
        return
    if args.check:
        check(); return
    raise SystemExit("choose --stdout or --check")

if __name__=="__main__": main()
