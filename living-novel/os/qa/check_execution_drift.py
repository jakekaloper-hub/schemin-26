#!/usr/bin/env python3
"""Read-only Novel / Execution Control discrepancy detector.

This is advisory evidence only: repository prose or manuscript existence never
certifies ESPN result finality, completes an execution task, or promotes canon.

Usage:
  python living-novel/os/qa/check_execution_drift.py [repository-root]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Evidence predicates are explicit and source-scoped. Do not interpret a
# historical narrative as authoritative independent league verification.
CHECKS = (
    {
        "task": "MEMO-W4-002",
        "source": "living-novel/whole-book/_INDEX.md",
        "evidence": "D0nkey K0ng's sole-undefeated claim ends",
        "reason": "Week 4 downstream prose exists; check actual league final-result receipt and task authority before changing status.",
    },
    {
        "task": "NOVEL-NEXT-002",
        "source": "living-novel/whole-book/_INDEX.md",
        "evidence": "REVIEWED SOFT MANUSCRIPT",
        "reason": "The Chapter IV index records a reviewed soft manuscript; reconcile task chronology without treating it as hard canon.",
    },
)
IN_REVIEW = frozenset({"VERIFYING", "COMPLETE"})


def inspect(root: str | Path) -> dict:
    root = Path(root)
    registry = root / "governance/execution-control/TASK_REGISTRY_V1.json"
    try:
        document = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        return {"status": "ERROR", "reason": f"TASK_REGISTRY_UNREADABLE: {type(exc).__name__}", "findings": []}

    if not isinstance(document, dict) or not isinstance(document.get("tasks"), list):
        return {"status": "ERROR", "reason": "TASK_REGISTRY_TASKS_NOT_ARRAY", "findings": []}
    tasks = document["tasks"]
    if not all(isinstance(task, dict) and isinstance(task.get("task_id"), str) for task in tasks):
        return {"status": "ERROR", "reason": "TASK_REGISTRY_INVALID_TASK_OBJECT", "findings": []}

    by_id = {task["task_id"]: task for task in tasks}
    findings: list[dict] = []
    for check in CHECKS:
        task = by_id.get(check["task"])
        if task is None:
            findings.append({"task": check["task"], "result": "MISSING_TASK", "source": check["source"]})
            continue
        file = root / check["source"]
        try:
            content = file.read_text(encoding="utf-8")
        except FileNotFoundError:
            findings.append({"task": check["task"], "result": "MISSING_SOURCE", "source": check["source"]})
            continue
        except (OSError, UnicodeError) as exc:
            return {"status": "ERROR", "reason": f"SOURCE_UNREADABLE: {type(exc).__name__}", "findings": []}
        if check["evidence"] in content and task.get("status") not in IN_REVIEW:
            findings.append({
                "task": check["task"], "result": "REVIEW_REQUIRED",
                "recorded_status": task.get("status"), "source": check["source"],
                "reason": check["reason"],
            })

    return {
        "status": "REVIEW_REQUIRED" if findings else "NO_KNOWN_DRIFT",
        "checks": len(CHECKS),
        "findings": findings,
        "authority_effect": "NONE_READ_ONLY_ADVISORY",
    }


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    result = inspect(root)
    print(json.dumps(result, indent=2))
    # REVIEW_REQUIRED is not a test failure. Only an unreadable or malformed
    # source fails CI. Change of authoritative task state requires separate QA.
    return 2 if result["status"] == "ERROR" else 0


if __name__ == "__main__":
    raise SystemExit(main())
