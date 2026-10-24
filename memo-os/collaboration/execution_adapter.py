"""V5.2 collaboration gate for the canonical execution-control task registry.

Fail closed on invalid handoffs and unresolved task dependencies. This adapter
uses the existing registry, not a second scheduler or release authority.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ec = _load(ROOT / "governance/execution-control/validate_execution_control.py", "execution_control")
contract = _load(ROOT / "memo-os/collaboration/v52_contract.py", "v52_contract")

def evaluate_assignment(task_id: str, handoff: dict, registry: dict | None = None) -> dict:
    data = registry if registry is not None else ec.load_registry()
    errors = ec.validate_registry(data)
    if errors:
        return {"status": "BLOCKED", "reason": "INVALID_REGISTRY", "details": errors}
    index = {task["task_id"]: task for task in data["tasks"]}
    task = index.get(task_id)
    if task is None:
        return {"status": "BLOCKED", "reason": "UNKNOWN_ASSIGNMENT"}
    if task["status"] in {"COMPLETE", "SUPERSEDED", "CANCELLED", "BLOCKED", "WAITING_EXTERNAL", "DEFERRED"}:
        return {"status": "BLOCKED", "reason": "INVALID_STATE"}
    if task.get("blocked_by") or not ec.dependency_complete(task, index):
        return {"status": "BLOCKED", "reason": "MISSING_DEPENDENCY"}
    if handoff.get("assignment_id") != task_id:
        return {"status": "BLOCKED", "reason": "CONTRACT_VIOLATION"}
    result = contract.handoff(handoff)
    if result != "VALID":
        return {"status": "BLOCKED", "reason": result}
    if not contract.acknowledged(handoff.get("ack_state")):
        return {"status": "BLOCKED", "reason": "ACK_MISSING"}
    return {"status": "READY", "reason": "VALIDATED", "task_id": task_id}
