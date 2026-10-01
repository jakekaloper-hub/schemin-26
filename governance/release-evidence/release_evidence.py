#!/usr/bin/env python3
"""SHA- and subsystem-bound release evidence resolver.

A historical PASS may remain useful evidence, but it cannot become current
merely because a Markdown receipt exists. Current applicability requires:
1) unchanged subsystem anchor bytes, and
2) no required check recorded as non-success.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PASS_RESULTS = {"PASS", "PASS_WITH_BLOCK"}
HISTORICAL_RESULTS = {"HISTORICAL_PASS"}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _red_checks(receipt: dict) -> list[str]:
    return [
        check["name"]
        for check in receipt.get("required_checks", [])
        if check.get("conclusion") not in {"success", "neutral", "skipped"}
    ]


def classify_receipt(receipt: dict, *, current_head_sha: str, current_anchor_blob_sha: str | None) -> dict:
    red = _red_checks(receipt)
    result = receipt.get("result")

    if result == "BLOCKED" or red:
        return {
            "state": "BLOCKED_CURRENT_EVIDENCE",
            "applies_to_repo_head_exactly": receipt.get("tested_commit_sha") == current_head_sha,
            "red_checks": red,
            "unresolved_blockers": receipt.get("unresolved_blockers", []),
        }

    if result in HISTORICAL_RESULTS:
        return {
            "state": "HISTORICAL_ONLY",
            "applies_to_repo_head_exactly": False,
            "red_checks": [],
            "unresolved_blockers": receipt.get("unresolved_blockers", []),
        }

    if result not in PASS_RESULTS:
        return {
            "state": "NOT_PROVEN",
            "applies_to_repo_head_exactly": False,
            "red_checks": red,
            "unresolved_blockers": receipt.get("unresolved_blockers", []),
        }

    expected = receipt.get("anchor_blob_sha")
    if not expected or not current_anchor_blob_sha:
        return {
            "state": "NOT_PROVEN_NO_SUBSYSTEM_DIGEST",
            "applies_to_repo_head_exactly": False,
            "red_checks": [],
            "unresolved_blockers": receipt.get("unresolved_blockers", []),
        }

    if expected != current_anchor_blob_sha:
        return {
            "state": "HISTORICAL_ONLY_CHANGED_SUBSYSTEM",
            "applies_to_repo_head_exactly": False,
            "red_checks": [],
            "unresolved_blockers": receipt.get("unresolved_blockers", []),
        }

    if receipt.get("tested_commit_sha") == current_head_sha:
        state = "CURRENT_HEAD_PASS"
        exact = True
    else:
        state = "CURRENT_SUBSYSTEM_PASS"
        exact = False

    return {
        "state": state,
        "applies_to_repo_head_exactly": exact,
        "red_checks": [],
        "unresolved_blockers": receipt.get("unresolved_blockers", []),
    }


def validate_registry(registry: dict, repo_root: Path, current_head_sha: str) -> list[dict]:
    findings = []
    receipts = {r["receipt_id"]: r for r in registry.get("receipts", [])}

    for system in registry.get("systems", []):
        rid = system.get("current_receipt_id")
        receipt = receipts.get(rid)
        if receipt is None:
            findings.append({
                "severity": "FATAL",
                "system_id": system.get("system_id"),
                "reason": "CURRENT_RECEIPT_NOT_FOUND",
                "receipt_id": rid,
            })
            continue

        anchor = system.get("anchor_path")
        current_blob = None
        if anchor:
            path = repo_root / anchor
            if path.exists():
                current_blob = git_blob_sha(path)
            elif not system.get("external_ref"):
                findings.append({
                    "severity": "FATAL",
                    "system_id": system.get("system_id"),
                    "reason": "CURRENT_ANCHOR_NOT_FOUND",
                    "anchor_path": anchor,
                })
                continue

        classification = classify_receipt(
            receipt,
            current_head_sha=current_head_sha,
            current_anchor_blob_sha=current_blob,
        )

        declared = system.get("authority_state")
        if declared in {"ACTIVE", "ACTIVE_SAFETY_BOUNDARY", "RELEASED_ACTIVE"}:
            if classification["state"] not in {"CURRENT_HEAD_PASS", "CURRENT_SUBSYSTEM_PASS"}:
                findings.append({
                    "severity": "FATAL",
                    "system_id": system["system_id"],
                    "reason": "DECLARED_ACTIVE_WITHOUT_CURRENT_APPLICABLE_PASS",
                    "classification": classification,
                })

        if declared == "BLOCKED" and receipt.get("result") != "BLOCKED":
            findings.append({
                "severity": "FATAL",
                "system_id": system["system_id"],
                "reason": "DECLARED_BLOCKED_WITHOUT_BLOCK_RECEIPT",
            })

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="governance/release-evidence/registry.json")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--head-sha", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    registry = json.loads((root / args.registry).read_text())
    findings = validate_registry(registry, root, args.head_sha)
    if findings:
        print(json.dumps({"state": "FAIL", "findings": findings}, indent=2))
        return 1
    print(json.dumps({"state": "PASS", "systems": len(registry.get("systems", []))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
