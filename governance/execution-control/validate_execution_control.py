#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "governance" / "execution-control" / "TASK_REGISTRY_V1.json"
STATES = {
    "NOT_STARTED","READY","IN_PROGRESS","BLOCKED","WAITING_EXTERNAL",
    "DEFERRED","VERIFYING","COMPLETE","SUPERSEDED","CANCELLED","REOPENED"
}
PRIORITIES = {"P0","P1","P2","P3"}
TERMINAL = {"COMPLETE","SUPERSEDED","CANCELLED"}

def load_registry(path: Path = REGISTRY) -> dict:
    return json.loads(path.read_text())

def validate_registry(data: dict) -> list[str]:
    errors: list[str] = []
    tasks = data.get("tasks", [])
    if data.get("version") != "1.0.0":
        errors.append("registry version must be 1.0.0")
    ids = [t.get("task_id") for t in tasks]
    if any(not x for x in ids):
        errors.append("all tasks require task_id")
    if len(ids) != len(set(ids)):
        errors.append("duplicate task_id")
    index = {t["task_id"]: t for t in tasks if t.get("task_id")}
    required = [
        "title","project","program","roadmap","phase","workstream","owner",
        "priority","status","source_authority","next_action"
    ]
    array_fields = ["dependencies","blocked_by","blocks","acceptance_criteria","evidence","supersedes"]
    for task in tasks:
        tid = task.get("task_id", "<missing>")
        for field in required:
            if not isinstance(task.get(field), str) or not task[field].strip():
                errors.append(f"{tid}: {field} required")
        if task.get("status") not in STATES:
            errors.append(f"{tid}: invalid status {task.get('status')}")
        if task.get("priority") not in PRIORITIES:
            errors.append(f"{tid}: invalid priority {task.get('priority')}")
        for field in array_fields:
            if not isinstance(task.get(field), list):
                errors.append(f"{tid}: {field} must be array")
        for relation in task.get("dependencies", []) + task.get("blocks", []):
            if relation not in index:
                errors.append(f"{tid}: relation references missing task {relation}")
        if task.get("status") == "COMPLETE":
            evidence = task.get("evidence", [])
            if not task.get("acceptance_criteria"):
                errors.append(f"{tid}: COMPLETE without acceptance criteria")
            if not any(e.get("status") == "PASS" for e in evidence):
                errors.append(f"{tid}: COMPLETE without PASS evidence")
            if any(e.get("status") == "FAIL" for e in evidence):
                errors.append(f"{tid}: COMPLETE contains FAIL evidence")
        source = task.get("source_authority")
        if source and not (ROOT / source).exists():
            errors.append(f"{tid}: source_authority missing: {source}")
        for ev in task.get("evidence", []):
            ref = ev.get("ref")
            if ref and not ref.startswith(("http://","https://","run:","commit:")) and not (ROOT / ref).exists():
                errors.append(f"{tid}: evidence ref missing: {ref}")
    return errors

def dependency_complete(task: dict, index: dict[str, dict]) -> bool:
    return all(index.get(tid, {}).get("status") in {"COMPLETE","SUPERSEDED"} for tid in task.get("dependencies", []))

def executable_tasks(data: dict) -> list[dict]:
    index = {t["task_id"]: t for t in data["tasks"]}
    return [
        t for t in data["tasks"]
        if t["status"] in {"NOT_STARTED","READY","REOPENED"}
        and dependency_complete(t,index)
        and not t.get("blocked_by")
    ]

def priority_score(task: dict, index: dict[str,dict]) -> int:
    base={"P0":400,"P1":300,"P2":200,"P3":100}[task["priority"]]
    state={"READY":50,"REOPENED":45,"NOT_STARTED":20}.get(task["status"],0)
    downstream=sum(1 for t in index.values() if task["task_id"] in t.get("dependencies", []) or task["task_id"] in t.get("blocked_by", []))
    return base + state + downstream*10

def select_next(data: dict) -> dict | None:
    candidates=executable_tasks(data)
    if not candidates:
        return None
    index={t["task_id"]:t for t in data["tasks"]}
    return sorted(candidates,key=lambda t:(-priority_score(t,index),t["task_id"]))[0]

def resolve(request: str, data: dict) -> dict | None:
    text=request.lower()
    tokens=[x for x in __import__("re").split(r"[^a-z0-9]+",text) if len(x)>=3]
    scored=[]
    for task in data["tasks"]:
        hay=" ".join([
            task["task_id"],task["title"],task["project"],task["program"],task["roadmap"],
            task["phase"],task["workstream"],*(task.get("aliases") or [])
        ]).lower()
        score=sum(1 for token in set(tokens) if token in hay)
        if any(alias.lower() in text for alias in task.get("aliases",[])):
            score += 5
        if task["task_id"].lower() in text:
            score += 10
        if score:
            scored.append((score,task["task_id"],task))
    return sorted(scored,key=lambda x:(-x[0],x[1]))[0][2] if scored else None

def rollup(data: dict, project: str | None=None) -> dict:
    tasks=[t for t in data["tasks"] if not project or t["project"]==project]
    accountable=[t for t in tasks if t["status"] not in {"SUPERSEDED","CANCELLED"}]
    complete=sum(1 for t in accountable if t["status"]=="COMPLETE")
    return {
        "total":len(tasks),
        "complete":complete,
        "completion_pct": round((complete/len(accountable))*100,1) if accountable else 0,
        "counts":{state:sum(1 for t in tasks if t["status"]==state) for state in sorted(STATES)}
    }

def main() -> int:
    data=load_registry()
    errors=validate_registry(data)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Execution-control registry valid.")
    nxt=select_next(data)
    print("Next:", nxt["task_id"] if nxt else "NONE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
