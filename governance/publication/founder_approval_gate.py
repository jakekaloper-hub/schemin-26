"""Fail-closed issue-level founder approval guard for the existing Memo OS.

This is an additive release guard, not a replacement for the V5.5 page or issue state machines.
Approval receipts must be durable, independently authenticated by the caller, and bound
to immutable production hashes. This module never claims to authenticate a person.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

ISSUE_STATES = frozenset({"INTAKE", "SOURCE_LOCK", "PREPRODUCTION", "PAGE_PRODUCTION", "BLOCKED", "ASSEMBLY", "RELEASE_CANDIDATE", "CORRECTION_REQUIRED", "RELEASED"})
REQUIRED_QA = ("source_lock", "fact_qa", "story_qa", "originality_qa", "character_qa", "art_qa", "design_qa", "mobile_qa", "copy_qa", "assembly_qa", "release_audit")
BLOCKING_FLAGS = ("character_reference_verified", "subject_binding_verified", "venue_verified", "finality_verified", "page_manifest_locked", "final_pdf_inspected", "independent_auditor_verified")

@dataclass(frozen=True)
class Decision:
    state: str
    errors: tuple[str, ...]

def _approval_valid(receipt: Any, *, gate: str, issue_id: str, expected_hash: str) -> bool:
    if not isinstance(receipt, Mapping):
        return False
    return (receipt.get("gate") == gate
            and receipt.get("issue_id") == issue_id
            and receipt.get("artifact_sha256") == expected_hash
            and receipt.get("decision") == "APPROVED"
            and receipt.get("authenticated") is True
            and receipt.get("approver_role") == "FOUNDER"
            and isinstance(receipt.get("receipt_id"), str)
            and bool(receipt["receipt_id"].strip()))

def evaluate_transition(issue: Mapping[str, Any], target: str) -> Decision:
    """Validate an attempted issue-state transition; caller must persist approved state atomically."""
    errors: list[str] = []
    source = issue.get("state")
    if source not in ISSUE_STATES or target not in ISSUE_STATES:
        return Decision("HOLD", ("INVALID_STATE",))
    if source == "RELEASED" and target != "RELEASED":
        return Decision("HOLD", ("RELEASED_IMMUTABLE",))
    if target in {"PAGE_PRODUCTION", "ASSEMBLY", "RELEASE_CANDIDATE", "RELEASED"}:
        plan_hash = issue.get("approved_plan_sha256")
        if not isinstance(plan_hash, str) or len(plan_hash) != 64:
            errors.append("MISSING_PLAN_HASH")
        if not _approval_valid(issue.get("approvals", {}).get("creative") if isinstance(issue.get("approvals"), Mapping) else None, gate="CREATIVE_DIRECTION", issue_id=str(issue.get("issue_id")), expected_hash=plan_hash):
            errors.append("FOUNDER_CREATIVE_APPROVAL_MISSING_OR_STALE")
    if target in {"RELEASE_CANDIDATE", "RELEASED"}:
        for flag in BLOCKING_FLAGS:
            if issue.get(flag) is not True:
                errors.append("REQUIRED_PROOF_MISSING:" + flag)
        qa = issue.get("qa")
        for name in REQUIRED_QA:
            if not isinstance(qa, Mapping) or qa.get(name) != "PASS":
                errors.append("QA_NOT_PASS:" + name)
        if issue.get("open_critical_defects") != 0:
            errors.append("CRITICAL_DEFECTS_NOT_ZERO")
        if not isinstance(issue.get("final_pdf_sha256"), str) or len(issue["final_pdf_sha256"]) != 64:
            errors.append("MISSING_FINAL_PDF_HASH")
    if target == "RELEASED":
        if source != "RELEASE_CANDIDATE":
            errors.append("INVALID_RELEASE_TRANSITION")
        if not _approval_valid(issue.get("approvals", {}).get("publication") if isinstance(issue.get("approvals"), Mapping) else None, gate="FINAL_PUBLICATION", issue_id=str(issue.get("issue_id")), expected_hash=issue.get("final_pdf_sha256")):
            errors.append("FOUNDER_PUBLICATION_APPROVAL_MISSING_OR_STALE")
    return Decision("HOLD" if errors else "PASS", tuple(errors))
