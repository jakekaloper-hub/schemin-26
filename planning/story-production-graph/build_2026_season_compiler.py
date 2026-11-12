#!/usr/bin/env python3
"""Closer + Setup Man: one compiler manifest spanning all nine 2026 memo cycles."""
from __future__ import annotations
import json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from adapt_2026_memo_season import compile_season
from build_compiler_manifest import build_manifest

def build():
    season=compile_season()
    manifest=build_manifest(season["events"],season["scenes"],"2026-memos-w01-w09")
    manifest["build_id"]="BUILD-2026-MEMOS-W01-W09"
    manifest["inputs"]["memo_issue_ids"]=[i["issue_id"] for i in season["issues"]]
    for issue in season["issues"]:
        for surface in ("WEB","TIMELINE"):
            jid=f"JOB-{issue['issue_id']}-{surface}"
            manifest["jobs"].append({
              "job_id":jid,"surface":surface,"depends_on":[issue["issue_id"]],
              "render_profile":None,"status":"READY"
            })
            manifest["invalidation"]["dependency_edges"].append({
              "upstream":issue["issue_id"],"downstream":jid,"dependency_class":"BASE"
            })
    return manifest

if __name__=="__main__":
    print(json.dumps(build(),indent=2,ensure_ascii=False))
