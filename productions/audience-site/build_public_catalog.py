#!/usr/bin/env python3
"""Build the Commonwealth audience-site public projection from Story Graph feeds.

Presentation-only adapter. It never promotes publication state, canon, render
eligibility, or world/character authority.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil

BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
DEFAULT_WEB=ROOT/"planning/story-production-graph/generated/2026/web_index.json"
DEFAULT_TIMELINE=ROOT/"planning/story-production-graph/generated/2026/timeline.json"

def _read_json(path):
    return json.loads(pathlib.Path(path).read_text())

def _memo_status(publication_state):
    return "Released edition" if publication_state=="RELEASED" else publication_state.replace("_"," ").title()

def _memo_available(issue):
    # Presence in the graph is not enough for a working public issue reader.
    # Require both released authority and an in-repo binary until an explicit
    # external-artifact adapter is introduced.
    return issue["publication_state"]=="RELEASED" and bool(issue["binary_in_repo"])

def _project_memo(issue):
    return {
      "id":f"week-{issue['week']}",
      "issueId":issue["issue_id"],
      "week":issue["week"],
      "title":f"Week {issue['week']} Dispatch",
      "publicationState":issue["publication_state"],
      "sourceClass":issue["source_class"],
      "coverageState":issue["coverage_state"],
      "binaryInRepo":bool(issue["binary_in_repo"]),
      "canonicalArtifact":issue.get("canonical_artifact"),
      "eventCount":issue["event_count"],
      "encounterCount":issue["encounter_count"],
      "sceneCount":issue["scene_count"],
      "sceneIds":list(issue["scene_ids"]),
      "consumerJobs":list(issue["consumer_jobs"]),
      "available":_memo_available(issue),
      "status":_memo_status(issue["publication_state"]),
    }

def _project_timeline(entry):
    return {
      "eventId":entry["event_id"],
      "week":entry["week"],
      "eventType":entry["event_type"],
      "evidenceStatus":entry["evidence_status"],
      "canonStatus":entry["canon_status"],
      "branchState":entry["branch_state"],
      "participants":list(entry["participants"]),
      "result":entry["result"],
      "sourceReceipts":list(entry["source_receipts"]),
    }

def build_catalog(output=None,render=False,web_index_path=None,timeline_path=None):
    output=pathlib.Path(output or BASE/"dist")
    output.mkdir(parents=True,exist_ok=True)
    web=_read_json(web_index_path or DEFAULT_WEB)
    timeline=_read_json(timeline_path or DEFAULT_TIMELINE)

    if web.get("season")!=timeline.get("season"):
        raise ValueError("Story Graph season mismatch")
    web_fp=web.get("source_fingerprint_sha256")
    timeline_fp=timeline.get("source_fingerprint_sha256")
    if not web_fp:
        raise ValueError("Story Graph web index missing source fingerprint")
    if timeline_fp is not None and timeline_fp!=web_fp:
        raise ValueError("Story Graph consumer fingerprint mismatch")

    data={
      "memos":[_project_memo(x) for x in sorted(web["memo_issues"],key=lambda x:x["week"],reverse=True)],
      "timeline":[_project_timeline(x) for x in timeline["entries"]],
      "meta":{
        "title":"Schemin · The Commonwealth",
        "schemaVersion":2,
        "season":web["season"],
        "storyGraphFingerprint":web_fp,
        "authority":"READ_ONLY_PRESENTATION_PROJECTION",
        "warnings":[
          "Story Graph status is preserved; site presentation cannot promote release or canon.",
          "Unavailable memo artifacts remain unavailable rather than falling back to another week.",
          "Renderer execution is outside the audience-site boundary.",
        ],
      },
    }
    (output/"data.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    source_dir=BASE/"src"
    if source_dir.exists():
        shutil.copytree(source_dir,output,dirs_exist_ok=True)
    return data

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=pathlib.Path,default=BASE/"dist")
    parser.add_argument("--no-render",action="store_true")
    args=parser.parse_args()
    data=build_catalog(args.output,render=not args.no_render)
    print(json.dumps({
      "output":str(args.output),
      "memos":len(data["memos"]),
      "timeline":len(data["timeline"]),
      "storyGraphFingerprint":data["meta"]["storyGraphFingerprint"],
    }))
