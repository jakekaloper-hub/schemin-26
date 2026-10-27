"""Deterministic, fail-closed Commonwealth Inklings workshop reconciliation.

This module does not invoke models or certify the output as canon. It accepts
independently prepared, source-anchored methodology findings and produces one
bounded creative decision packet for existing Memo/Novel OS consumers.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

VALID_DECISIONS = {"ACCEPT", "ADAPT", "HOLD", "REJECT"}
REQUIRED = {"assignment_id", "production", "evidence_sha", "decision_question", "findings"}
ALLOWED_PRODUCTIONS = {"memo-os", "novel-os"}

class WorkshopError(ValueError):
    pass

def reconcile(assignment: dict, registry: dict, production_bench: dict) -> dict:
    if not isinstance(assignment, dict) or not REQUIRED.issubset(assignment):
        raise WorkshopError("Missing required workshop fields")
    if assignment["production"] not in ALLOWED_PRODUCTIONS:
        raise WorkshopError("Unsupported production")
    for field in ("assignment_id", "evidence_sha", "decision_question"):
        if not isinstance(assignment[field], str) or not assignment[field].strip():
            raise WorkshopError("Invalid " + field)
    if len(assignment["evidence_sha"]) != 64 or any(c not in "0123456789abcdef" for c in assignment["evidence_sha"]):
        raise WorkshopError("Evidence SHA-256 required")
    authors = set(registry["author_council"]["core_eight"])
    specialists = {p["name"] for p in production_bench["profiles"]}
    findings = assignment["findings"]
    if not isinstance(findings, list) or not findings:
        raise WorkshopError("At least one independent finding required")
    per_advisor = {}
    accepted, dissent = [], []
    seen = set()
    for item in findings:
        if not isinstance(item, dict):
            raise WorkshopError("Finding must be object")
        for key in ("id", "advisor", "observation", "source_anchor", "proposal", "decision", "rationale"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise WorkshopError("Missing finding field: " + key)
        if item["id"] in seen:
            raise WorkshopError("Duplicate finding id")
        seen.add(item["id"])
        if item["advisor"] not in authors | specialists:
            raise WorkshopError("Unregistered methodology advisor")
        if item["decision"] not in VALID_DECISIONS:
            raise WorkshopError("Invalid decision")
        per_advisor[item["advisor"]] = per_advisor.get(item["advisor"], 0) + 1
        if per_advisor[item["advisor"]] > 3:
            raise WorkshopError("More than three findings per advisor")
        if item["decision"] in {"ACCEPT", "ADAPT"}:
            accepted.append(item)
        else:
            dissent.append(item)
    if not accepted:
        raise WorkshopError("No accepted or adapted creative direction")
    if not isinstance(assignment.get("synthesis"), str) or not assignment["synthesis"].strip():
        raise WorkshopError("Single creative synthesis required")
    return {
        "status": "CANDIDATE_PENDING_INDEPENDENT_REVIEW",
        "authority": "ADVISORY_ONLY",
        "assignment_id": assignment["assignment_id"],
        "production": assignment["production"],
        "evidence_sha": assignment["evidence_sha"],
        "decision_question": assignment["decision_question"],
        "selected_advisors": sorted(per_advisor),
        "synthesis": assignment["synthesis"],
        "accepted": accepted,
        "dissent": dissent,
        "canon_promoted": False,
        "umpire": "PENDING",
    }

def load_and_reconcile(assignment_path: Path, registry_path: Path, bench_path: Path) -> dict:
    files = [assignment_path, registry_path, bench_path]
    data = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    return reconcile(*data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("assignment", type=Path)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--bench", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(load_and_reconcile(args.assignment, args.registry, args.bench), indent=2))
    except (WorkshopError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        raise SystemExit(2)
