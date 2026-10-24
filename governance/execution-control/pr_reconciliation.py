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

def classify(pr):
    if pr.get("merged_at"):
        return "MERGED"
    if pr.get("state") == "open":
        return "OPEN_UNVERIFIED"
    body = (pr.get("body") or "").lower()
    if any(x in body for x in ("superseded by", "replayed onto", "transplanted", "consolidated", "salvaged")):
        return "CLOSED_REPLACEMENT_CLAIM_UNVERIFIED"
    return "CLOSED_UNMERGED_DISPOSITION_UNVERIFIED"

def collect(prs, task_path=None):
    buckets = collections.defaultdict(list)
    for p in prs:
        buckets[classify(p)].append({"number": p["number"], "title": p["title"],
            "url": p["html_url"], "merged_at": p.get("merged_at")})
    tasks = []
    if task_path and Path(task_path).exists():
        d = json.loads(Path(task_path).read_text())
        tasks = [{"id": t["task_id"], "status": t["status"], "created_at":t.get("created_at")}
                 for t in d["tasks"]]
    return {"generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "repository": REPO, "read_only": True, "proof_level": "METADATA_ONLY",
            "counts": {k:len(v) for k,v in sorted(buckets.items())},
            "prs": dict(buckets), "tasks":tasks,
            "limitations": ["GitHub closed != merged", "Replacement claims need diff/commit evidence",
                            "GitHub PR status != code availability", "Task status != live runtime health"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output", default="")
    p.add_argument("--task-registry", default="governance/execution-control/TASK_REGISTRY_V1.json")
    args=p.parse_args()
    report=collect(fetch_pulls(), args.task_registry)
    raw=json.dumps(report,indent=2)+"\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True,exist_ok=True)
        Path(args.output).write_text(raw)
    print(json.dumps({"counts":report["counts"],"tasks":len(report["tasks"]),
                      "replacement_claims":[p["number"] for p in report["prs"].get("CLOSED_REPLACEMENT_CLAIM_UNVERIFIED",[])]}, indent=2))

if __name__=="__main__":
    main()
