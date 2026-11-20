#!/usr/bin/env python3
"""Read-only GitHub inventory; writes a Markdown ledger; never merges or deletes."""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def github_json(url: str, token: str | None = None):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "schemin-visibility/1",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def pages(repo: str, endpoint: str, token: str | None = None) -> list[dict]:
    sep = "&" if "?" in endpoint else "?"
    items: list[dict] = []
    for page in range(1, 21):
        url = f"https://api.github.com/repos/{repo}/{endpoint}{sep}per_page=100&page={page}"
        batch = github_json(url, token)
        if not isinstance(batch, list):
            raise ValueError("Unexpected paginated GitHub response")
        items.extend(batch)
        if len(batch) < 100:
            return items
    raise ValueError("Refusing incomplete pagination above 2000 records")


def clean(value) -> str:
    return str(value).replace("|", " / ").replace("\r", " ").replace("\n", " ").strip()


def local_pr(pr: dict, repo: str) -> bool:
    return ((pr.get("head") or {}).get("repo") or {}).get("full_name") == repo


def state(pr: dict) -> str:
    if pr.get("state") == "open":
        return "DRAFT" if pr.get("draft") else "REVIEW"
    return "MERGED" if pr.get("merged_at") else "CLOSED_UNMERGED"


def snapshot(branches: list[dict], prs: list[dict], repo: str,
             utc_day: str, protected: bool | None = None) -> str:
    names = sorted({b["name"] for b in branches if b.get("name") and b["name"] != "main"})
    open_prs = sorted((p for p in prs if p.get("state") == "open"),
                      key=lambda p: p["number"], reverse=True)
    idx: dict[str, list[dict]] = {}
    for p in prs:
        if local_pr(p, repo):
            idx.setdefault(p["head"]["ref"], []).append(p)
    for matches in idx.values():
        matches.sort(key=lambda p: (p.get("state") == "open",
                                   p.get("merged_at") is not None,
                                   p.get("updated_at") or "", p.get("number", 0)),
                     reverse=True)
    no_pr = [name for name in names if not idx.get(name)]
    stacked = [p for p in open_prs if (p.get("base") or {}).get("ref") != "main"]
    main = next((b for b in branches if b.get("name") == "main"), {})
    sha = (main.get("commit") or {}).get("sha", "unknown")
    protection = "UNKNOWN" if protected is None else ("PROTECTED" if protected else "UNPROTECTED")
    lines = [
        "# Schemin '26 — Repository Visibility Ledger", "",
        f"**Inventory day (UTC):** {utc_day}",
        f"**Repository:** https://github.com/{repo}",
        f"**Main HEAD at inventory:** {sha}",
        f"**Main branch protection:** {protection}", "",
        "> Visibility does not imply canon, approval, merge, or publication. Source, domain authority, "
        "QA and release evidence remain governed by PROJECT_CONTROL_REGISTRY.md.", "",
        "## Summary", "",
        f"- {len(branches)} branches including main; {len(open_prs)} open pull requests",
        f"- {sum(bool(p.get('draft')) for p in open_prs)} draft; "
        f"{sum(not p.get('draft') for p in open_prs)} reviewable",
        f"- {len(stacked)} stacked PRs targeting a non-main base",
        f"- {len(no_pr)} non-main branches without any same-repository PR record", "",
        "## Every open pull request", "",
        "| PR | State | Base | Head | Title |", "|---|---|---|---|---|"
    ]
    for p in open_prs:
        lines.append(f"| [#{p['number']}]({p['html_url']}) | {state(p)} | "
                     f"{clean(p['base']['ref'])} | {clean(p['head']['ref'])} | "
                     f"{clean(p.get('title') or '')} |")
    lines += [
        "", "## Every non-main branch", "",
        "Unlinked branches appear first. No PR does not prove unmerged work; "
        "a branch can survive after an accepted merge.", "",
        "| Branch | Best matching PR | State | Target |", "|---|---|---|---|"
    ]
    for name in sorted(names, key=lambda n: (bool(idx.get(n)), n.lower())):
        matches = idx.get(name, [])
        p = matches[0] if matches else None
        link = f"[#{p['number']}]({p['html_url']})" if p else "No PR"
        status = state(p) if p else "NEEDS TRIAGE"
        base = clean((p.get("base") or {}).get("ref", "")) if p else "—"
        lines.append(f"| [{clean(name)}](https://github.com/{repo}/tree/{name}) | "
                     f"{link} | {status} | {base} |")
    lines += [
        "", "## Checkup protocol", "",
        "1. Read main and PROJECT_CONTROL_REGISTRY.md for approved authority.",
        "2. Refresh this live GitHub inventory and inspect open PR gates.",
        "3. Triage active branches without PRs and stacked dependency chains.",
        "4. Merge only after source/ownership checks, exact-head tests and independent QA.",
        "5. Retain unresolved experimental work in visible draft PRs or HOLD registers.",
        "6. Check branch protection and current CI/deploy checks independently.",
        "", "Special case: data/live is a snapshot-history branch; never wholesale-merge it.",
        "", "Generator: governance/repository-health/visibility.py. The scheduled workflow "
        "updates only this derived Markdown ledger, not canon, publication or source code.", ""
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY",
                                                         "jakekaloper-hub/schemin-26"))
    parser.add_argument("--output", type=Path, default=Path(
        "governance/repository-health/BRANCH_VISIBILITY_LEDGER.md"))
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        parser.error("Expected owner/repo")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    branches = pages(args.repo, "branches", token)
    prs = pages(args.repo, "pulls?state=all&sort=created&direction=desc", token)
    main_branch = github_json(f"https://api.github.com/repos/{args.repo}/branches/main", token)
    content = snapshot(branches, prs, args.repo,
                       datetime.now(timezone.utc).date().isoformat(),
                       protected=bool(main_branch.get("protected", False)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Inventory: {len(branches)} branches; "
          f"{sum(p.get('state') == 'open' for p in prs)} open PRs; output={args.output}")


if __name__ == "__main__":
    main()
