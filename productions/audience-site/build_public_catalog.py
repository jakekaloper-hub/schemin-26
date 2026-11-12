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
import hashlib
import subprocess
import urllib.parse

BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
DEFAULT_WEB=ROOT/"planning/story-production-graph/generated/2026/web_index.json"
DEFAULT_TIMELINE=ROOT/"planning/story-production-graph/generated/2026/timeline.json"
REVISION=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
REPO=f"https://github.com/jakekaloper-hub/schemin-26/blob/{REVISION}/"
MEDIA=f"https://media.githubusercontent.com/media/jakekaloper-hub/schemin-26/{REVISION}/"

def _read_json(path):
    return json.loads(pathlib.Path(path).read_text())

def _sha256(path):
    digest=hashlib.sha256()
    with pathlib.Path(path).open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return digest.hexdigest()

def _repo_url(path):
    return REPO+urllib.parse.quote(str(path))

def _media_url(path):
    return MEDIA+urllib.parse.quote(str(path))

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
      "source":"planning/story-production-graph/generated/2026/web_index.json",
      "sourceUrl":_repo_url("planning/story-production-graph/generated/2026/web_index.json"),
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


def _build_characters():
    lineup_path="canon/characters/APPROVED_LINEUP_2026_10_18.json"
    lineup=_read_json(ROOT/lineup_path)
    out=[]
    for person in lineup["individuals"]:
        appearance=_read_json(ROOT/person["appearance_delta"])
        assertions=appearance.get("approved_visual_assertions",{})
        description=assertions.get("subject_morphology") or person["display_title"]
        out.append({
          "id":person["character_id"],
          "owner":person["owner"],
          "name":person["display_title"],
          "team":person["team"],
          "locationId":person["home_location_id"],
          "description":description,
          "details":assertions.get("recognizable_props",[]),
          "image":_media_url(person["crop"]),
          "sha256":person["crop_sha256"],
          "source":person["appearance_delta"],
          "sourceUrl":_repo_url(person["appearance_delta"]),
        })
    return out,lineup

def _build_world():
    location_path="world/data/locations.json"
    route_path="world/data/routes.json"
    zone_path="world/data/physical_zones.json"
    locations=_read_json(ROOT/location_path)["locations"]
    projected=[]
    for location in locations:
        x,y=location["abstract_position"]
        projected.append({
          **location,
          "x":x,
          "y":y,
          "zone":location["physical_zone_id"],
          "description":", ".join(location.get("persistent_landmarks",[])),
          "source":location_path,
          "sourceUrl":_repo_url(location_path),
        })
    routes=_read_json(ROOT/route_path)["routes"]
    zones=_read_json(ROOT/zone_path)["regions"]
    return projected,routes,zones

def _build_chapters():
    manifest_path="governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"
    manifest=_read_json(ROOT/manifest_path)
    out=[]
    for publication in manifest["publications"]:
        if publication["family"]!="living_novel" or publication["release_state"]!="CANON_CLOSED":
            continue
        source=publication["canonical_artifact"]
        if not source or not (ROOT/source).is_file():
            raise ValueError(f"CANON_CLOSED manuscript missing source: {publication['publication_id']}")
        out.append({
          "id":publication["slug"],
          "publicationId":publication["publication_id"],
          "title":publication["title"],
          "text":(ROOT/source).read_text(),
          "source":source,
          "sourceUrl":_repo_url(source),
          "sha256":_sha256(ROOT/source),
          "status":"Archive edition",
          "releaseState":publication["release_state"],
          "note":"Accepted archive manuscript; presentation does not alter manuscript authority.",
        })
    return out

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

    characters,lineup=_build_characters()
    locations,routes,zones=_build_world()
    chapters=_build_chapters()
    data={
      "characters":characters,
      "locations":locations,
      "routes":routes,
      "zones":zones,
      "chapters":chapters,
      "memos":[_project_memo(x) for x in sorted(web["memo_issues"],key=lambda x:x["week"],reverse=True)],
      "timeline":[_project_timeline(x) for x in timeline["entries"]],
      "meta":{
        "title":"Schemin · The Commonwealth",
        "schemaVersion":2,
        "season":web["season"],
        "storyGraphFingerprint":web_fp,
        "authority":"READ_ONLY_PRESENTATION_PROJECTION",
        "sourceRevision":REVISION,
        "hero":_media_url(lineup["stored_repository_path"]),
        "heroSource":"Commissioner-approved 2026 character lineup",
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
