"""Read-only Novel OS / execution-control drift detection.

Reports potentially stale task statuses. Does not promote evidence or mutate state.
Usage: python living-novel/os/qa/check_execution_drift.py [repository-root]
"""
import json
import sys
from pathlib import Path

CHECKS = (
    {
        "task": "MEMO-W4-002",
        "source": "living-novel/whole-book/_INDEX.md",
        "evidence": "D0nkey K0ng's sole-undefeated claim ends",
        "message": "Week 4 downstream narrative exists; revalidate final-result gate and registry status.",
    },
    {
        "task": "NOVEL-NEXT-002",
        "source": "living-novel/whole-book/_INDEX.md",
        "evidence": "REVIEWED SOFT MANUSCRIPT",
        "message": "A reviewed Chapter IV soft manuscript is indexed; reconcile next-story selection task.",
    },
)

def inspect(root):
    root = Path(root)
    registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
    try:
        tasks = json.loads(registry.read_text(encoding="utf-8"))["tasks"]
    except (OSError, ValueError, KeyError) as exc:
        return {"status": "ERROR", "reason": str(exc), "findings": []}
    by_id = {task.get("task_id"): task for task in tasks}
    findings = []
    for check in CHECKS:
        task = by_id.get(check["task"])
        if task is None:
            findings.append({"task": check["task"], "result": "MISSING_TASK"})
            continue
        source = root / check["source"]
        if not source.is_file():
            findings.append({"task": check["task"], "result": "MISSING_SOURCE", "source": check["source"]})
            continue
        content = source.read_text(encoding="utf-8")
        if check["evidence"] in content and task.get("status") not in {"COMPLETE", "VERIFYING"}:
            findings.append({
                "task": check["task"], "result": "REVIEW_REQUIRED",
                "recorded_status": task.get("status"), "source": check["source"],
                "reason": check["message"]
            })
    return {"status": "REVIEW_REQUIRED" if findings else "NO_KNOWN_DRIFT", "findings": findings}

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    print(json.dumps(inspect(root), indent=2))
    sys.exit(2 if inspect(root)["status"] == "ERROR" else 0)
