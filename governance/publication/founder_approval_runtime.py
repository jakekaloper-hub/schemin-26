"""Durable fail-closed Memo approval transaction adapter (Issue #184).

This is an adapter for a trusted authenticated caller, not an identity provider.
Never expose MEMO_APPROVAL_SIGNING_KEY to untrusted production agents.
"""
from __future__ import annotations
import copy
import hashlib
import hmac
import json
import os
import tempfile
from pathlib import Path
from typing import Mapping, Any

from governance.publication.founder_approval_gate import evaluate_transition

class GateError(RuntimeError):
    pass

def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def _key() -> bytes:
    key = os.environ.get("MEMO_APPROVAL_SIGNING_KEY", "").encode()
    if len(key) < 32:
        raise GateError("SIGNING_KEY_UNAVAILABLE")
    return key

def _mac(payload: Mapping[str, Any]) -> str:
    return hmac.new(_key(), _canonical(payload), hashlib.sha256).hexdigest()

def _verified(envelope: Any) -> dict:
    if not isinstance(envelope, dict) or set(envelope) != {"payload", "signature"}:
        raise GateError("MALFORMED_ENVELOPE")
    if not isinstance(envelope["payload"], dict) or not isinstance(envelope["signature"], str):
        raise GateError("MALFORMED_ENVELOPE")
    if not hmac.compare_digest(_mac(envelope["payload"]), envelope["signature"]):
        raise GateError("INTEGRITY_FAILURE")
    return copy.deepcopy(envelope["payload"])

def _seal(payload: Mapping[str, Any]) -> dict:
    return {"payload": copy.deepcopy(dict(payload)), "signature": _mac(payload)}

def issue_founder_receipt(*, issue_id: str, gate: str, artifact_sha256: str,
                          receipt_id: str, authenticated_principal: str,
                          verified_by: str) -> dict:
    """Caller must authenticate Founder through an independent trusted identity service.

    A principal string is NOT itself authentication. The trusted verifier ID
    must match the deployment-configured identity-verifier allowlist.
    """
    allowed_verifier = os.environ.get("MEMO_TRUSTED_IDENTITY_VERIFIER", "")
    founder = os.environ.get("MEMO_FOUNDER_PRINCIPAL", "")
    if not allowed_verifier or verified_by != allowed_verifier or not founder or authenticated_principal != founder:
        raise GateError("FOUNDER_IDENTITY_NOT_VERIFIED")
    if gate not in ("CREATIVE_DIRECTION", "FINAL_PUBLICATION"):
        raise GateError("UNKNOWN_GATE")
    if len(artifact_sha256) != 64 or any(c not in "0123456789abcdef" for c in artifact_sha256):
        raise GateError("INVALID_HASH")
    if not issue_id or not receipt_id:
        raise GateError("MISSING_RECEIPT_IDENTITY")
    payload = {"gate": gate, "issue_id": issue_id, "artifact_sha256": artifact_sha256,
               "receipt_id": receipt_id, "approver_role": "FOUNDER", "decision": "APPROVED",
               "authenticated": True, "principal": authenticated_principal, "verified_by": verified_by}
    return _seal(payload)

def verify_receipt(envelope: Any, *, gate: str, issue_id: str, artifact_sha256: str) -> dict:
    receipt = _verified(envelope)
    if (receipt.get("gate") != gate or receipt.get("issue_id") != issue_id
        or receipt.get("artifact_sha256") != artifact_sha256
        or receipt.get("principal") != os.environ.get("MEMO_FOUNDER_PRINCIPAL")
        or receipt.get("verified_by") != os.environ.get("MEMO_TRUSTED_IDENTITY_VERIFIER")):
        raise GateError("RECEIPT_SCOPE_OR_IDENTITY_MISMATCH")
    return receipt

def _read(path: Path) -> dict:
    if not path.exists():
        raise GateError("STATE_NOT_FOUND")
    return _verified(json.loads(path.read_text(encoding="utf-8")))

def initialize(path: str | Path, issue: Mapping[str, Any]) -> None:
    path = Path(path)
    if path.exists():
        raise GateError("STATE_ALREADY_EXISTS")
    if issue.get("state") != "INTAKE" or not issue.get("issue_id"):
        raise GateError("INVALID_INITIAL_STATE")
    _write(path, dict(issue))

def _write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".memo-state-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(_seal(payload), f, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def transition(path: str | Path, target: str, *, approvals: Mapping[str, Any] | None = None) -> dict:
    """Single-process atomic state transition. Deployments need an external lock
    for concurrent writers; no multi-writer guarantee is claimed here.
    """
    path = Path(path)
    issue = _read(path)
    if approvals:
        issue.setdefault("approvals", {})
        for name, envelope in approvals.items():
            if name not in ("creative", "publication"):
                raise GateError("UNKNOWN_APPROVAL_SLOT")
            gate = "CREATIVE_DIRECTION" if name == "creative" else "FINAL_PUBLICATION"
            digest = issue.get("approved_plan_sha256") if name == "creative" else issue.get("final_pdf_sha256")
            issue["approvals"][name] = verify_receipt(envelope, gate=gate, issue_id=str(issue["issue_id"]), artifact_sha256=digest)
    verdict = evaluate_transition(issue, target)
    if verdict.state != "PASS":
        raise GateError("TRANSITION_DENIED:" + ",".join(verdict.errors))
    issue["state"] = target
    _write(path, issue)
    return issue

def inspect(path: str | Path) -> dict:
    return _read(Path(path))
