#!/usr/bin/env python3
"""Read-only PR disposition and task freshness inventory. No merge claims inferred."""
import argparse
import collections
import datetime as dt
import json
import os
from pathlib import Path
import urllib.request

REPO = "jakekaloper-hub/schemin-26"
API = f"https://api.github.com/repos/{REPO}/pulls"

def fetch_pulls(fetch=None):
    if fetch is None:
        def fetch(url):
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "schemin-convergence-audit",
                **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.environ.get("GH_TOKEN") else {})
            })
            with urllib.request.urlopen(req, timeout=20) as response:
                return json.load(response)
    result = []
    for page in range(1, 30):
        batch = fetch(f"{API}?state=all&per_page=100&page={page}")
        result.extend(batch)
        if len(batch) < 100:
            return result
    raise RuntimeError("PR pagination exceeded safety bound; audit incomplete")

def fetch_branches(fetch=None):
    """Enumerate all remote branch refs. Branch presence alone is not unmerged-code proof."""
    if fetch is None:
        def fetch(url):
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "schemin-convergence-audit",
                **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.environ.get("GH_TOKEN") else {})
            })
            with urllib.request.urlopen(req, timeout=20) as response:
                return json.load(response)
    result = []
    for page in range(1, 30):
        batch = fetch(f"https://api.github.com/repos/{REPO}/branches?per_page=100&page={page}")
        result.extend(batch)
        if len(batch) < 100:
            return result
    raise RuntimeError("Branch pagination exceeded safety bound; audit incomplete")

def classify(pr):
    if pr.get("merged_at"):
        return "MERGED"
    if pr.get("state") == "open":
        return "OPEN_UNVERIFIED"
    body = (pr.get("body") or "").lower()
    if any(x in body for x in ("superseded by", "replayed onto", "transplanted", "consolidated", "salvaged")):
        return "CLOSED_REPLACEMENT_CLAIM_UNVERIFIED"
    return "CLOSED_UNMERGED_DISPOSITION_UNVERIFIED"

def collect(prs, task_path=None, branches=None):
    buckets = collections.defaultdict(list)
    for p in prs:
        buckets[classify(p)].append({"number": p["number"], "title": p["title"],
            "url": p["html_url"], "merged_at": p.get("merged_at")})
    tasks = []
    if task_path and Path(task_path).exists():
        d = json.loads(Path(task_path).read_text())
        tasks = [{"id": t["task_id"], "status": t["status"], "created_at":t.get("created_at")}
                 for t in d["tasks"]]
    visibility = {"checked": branches is not None,
                  "branch_count": len(branches) if branches is not None else None,
                  "without_open_pr_head_or_base_count": None,
                  "without_open_pr_head_or_base": []}
    if branches is not None:
        tracked = set()
        for p in prs:
            if p.get("state") != "open":
                continue
            for ref in (p.get("head", {}).get("ref"), p.get("base", {}).get("ref")):
                if ref:
                    tracked.add(ref)
        untracked = sorted(b["name"] for b in branches
                           if b["name"] != "main" and b["name"] not in tracked)
        visibility["without_open_pr_head_or_base_count"] = len(untracked)
        visibility["without_open_pr_head_or_base"] = untracked

    return {"generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "repository": REPO, "read_only": True, "proof_level": "METADATA_ONLY",
            "counts": {k:len(v) for k,v in sorted(buckets.items())},
            "prs": dict(buckets), "tasks":tasks, "branch_visibility": visibility,
            "limitations": ["GitHub closed != merged", "Replacement claims need diff/commit evidence",
                            "GitHub PR status != code availability", "Task status != live runtime health", "A branch without an open PR can be a historical merged branch; unique commits not established"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output", default="")
    p.add_argument("--task-registry", default="governance/execution-control/TASK_REGISTRY_V1.json")
    args=p.parse_args()
    report=collect(fetch_pulls(), args.task_registry, fetch_branches())
    raw=json.dumps(report,indent=2)+"\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True,exist_ok=True)
        Path(args.output).write_text(raw)
    print(json.dumps({"counts":report["counts"],"tasks":len(report["tasks"]),
                      "branch_count":report["branch_visibility"]["branch_count"],
                      "branches_without_open_pr":report["branch_visibility"]["without_open_pr_head_or_base_count"],
                      "replacement_claims":[p["number"] for p in report["prs"].get("CLOSED_REPLACEMENT_CLAIM_UNVERIFIED",[])]}, indent=2))

if __name__=="__main__":
    main()
