#!/usr/bin/env python3
"""Build deterministic downstream consumer artifacts from Story Production Graph.

These consumers are read-only projections. They do not mutate canon, render
media, publish artifacts, or promote blocked authority.
"""
from __future__ import annotations
import argparse,json,sys
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parent
OUT=BASE/"generated/2026"
sys.path.insert(0,str(BASE))

from adapt_2026_memo_season import compile_season
from build_2026_season_compiler import build as build_compiler
from graph_integrity import source_fingerprint

def _week_from_event_id(event_id):
    return int(event_id.split("-W",1)[1][:2])

def _scene_groups(season):
    by_week=defaultdict(list)
    for scene in season["scenes"]:
        by_week[_week_from_event_id(scene["event_id"])].append(scene["scene_id"])
    return {k:sorted(v) for k,v in by_week.items()}

def build_web_index(season,compiler):
    scene_groups=_scene_groups(season)
    event_counts=Counter(e["league_time"]["week"] for e in season["events"])
    encounter_counts=Counter(int(e["encounter_id"].split("-W",1)[1][:2]) for e in season["encounters"])
    jobs_by_issue=defaultdict(list)
    for job in compiler["jobs"]:
        for dep in job["depends_on"]:
            if dep.startswith("MEMO-2026-"):
                jobs_by_issue[dep].append({"job_id":job["job_id"],"surface":job["surface"],"status":job["status"]})
    issues=[]
    for issue in sorted(season["issues"],key=lambda x:x["week"]):
        week=issue["week"]
        issues.append({
          "issue_id":issue["issue_id"],
          "week":week,
          "publication_state":issue["publication_state"],
          "source_class":issue["source_class"],
          "coverage_state":issue["coverage_state"],
          "binary_in_repo":issue["binary_in_repo"],
          "canonical_artifact":issue.get("canonical_artifact"),
          "event_count":event_counts.get(week,0),
          "encounter_count":encounter_counts.get(week,0),
          "scene_count":len(scene_groups.get(week,[])),
          "scene_ids":scene_groups.get(week,[]),
          "consumer_jobs":sorted(jobs_by_issue.get(issue["issue_id"],[]),key=lambda x:x["job_id"]),
        })
    return {
      "schema_version":"1.0",
      "season":2026,
      "source_fingerprint_sha256":compiler["source_fingerprint_sha256"],
      "memo_issues":issues,
      "authority":"READ_ONLY_CONSUMER_PROJECTION",
    }

def build_timeline(season):
    entries=[]
    for event in season["events"]:
        r=event.get("result") or {}
        entries.append({
          "week":event["league_time"]["week"],
          "event_id":event["event_id"],
          "event_type":event["event_type"],
          "evidence_status":event["authority"]["evidence_status"],
          "canon_status":event["authority"]["canon_status"],
          "branch_state":event["state"]["branch_state"],
          "participants":[p["entity_id"] for p in event["participants"] if p["entity_type"]=="CHARACTER"],
          "result":r,
          "source_receipts":list(event["authority"]["source_receipts"]),
        })
    entries.sort(key=lambda x:(x["week"],x["event_id"]))
    return {
      "schema_version":"1.0",
      "season":2026,
      "entry_count":len(entries),
      "entries":entries,
      "authority":"READ_ONLY_EVENT_TIMELINE",
    }

def _blocked_reason(job,season):
    dep=job["depends_on"][0] if job["depends_on"] else None
    if dep and dep.startswith("SCN-"):
        scene=next((s for s in season["scenes"] if s["scene_id"]==dep),None)
        if scene:
            return f"scene_publication_state={scene['qa']['publication_state']}"
        return "scene_dependency_missing"
    if dep and dep.startswith("MEMO-"):
        issue=next((i for i in season["issues"] if i["issue_id"]==dep),None)
        if issue:
            return f"memo_publication_state={issue['publication_state']};binary_in_repo={str(issue['binary_in_repo']).lower()}"
        return "memo_dependency_missing"
    return "job_not_ready"

def build_render_queue(season,compiler):
    ready=[]; blocked=[]
    for job in sorted(compiler["jobs"],key=lambda x:x["job_id"]):
        if job["render_profile"] is None:
            # Non-render consumers remain visible in blocked/ready job accounting,
            # but are never converted into renderer requests.
            if job["status"]!="READY":
                blocked.append({"job_id":job["job_id"],"surface":job["surface"],"reason":_blocked_reason(job,season)})
            continue
        if job["status"]=="READY":
            ready.append({
              "job_id":job["job_id"],
              "surface":job["surface"],
              "render_profile":job["render_profile"],
              "depends_on":list(job["depends_on"]),
            })
        else:
            blocked.append({
              "job_id":job["job_id"],
              "surface":job["surface"],
              "render_profile":job["render_profile"],
              "reason":_blocked_reason(job,season),
            })
    return {
      "schema_version":"1.0",
      "season":2026,
      "source_fingerprint_sha256":compiler["source_fingerprint_sha256"],
      "ready_count":len(ready),
      "blocked_count":len(blocked),
      "ready_requests":ready,
      "blocked_jobs":blocked,
      "renderer_execution":"NOT_EXECUTED",
      "authority":"READ_ONLY_GOVERNED_RENDER_QUEUE",
    }

def build_all():
    season=compile_season()
    compiler=build_compiler()
    return {
      "web_index.json":build_web_index(season,compiler),
      "timeline.json":build_timeline(season),
      "render_queue.json":build_render_queue(season,compiler),
    }

def canonical(obj):
    return json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+"\n"

def check():
    expected=build_all()
    problems=[]
    for name,obj in expected.items():
        path=OUT/name
        if not path.is_file(): problems.append(f"MISSING:{path}")
        elif path.read_text()!=canonical(obj): problems.append(f"DRIFT:{path}")
    if problems: raise AssertionError(problems)
    print("DOWNSTREAM_CONSUMERS_PASS "+ " ".join(f"{name}={len(canonical(obj))}" for name,obj in expected.items()))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stdout",action="store_true")
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    outputs=build_all()
    if args.stdout:
        for name,obj in outputs.items():
            marker=name.upper().replace(".","_")
            print(f"{marker}_BEGIN")
            print(canonical(obj),end="")
            print(f"{marker}_END")
        return
    if args.check:
        check(); return
    raise SystemExit("choose --stdout or --check")

if __name__=="__main__": main()
