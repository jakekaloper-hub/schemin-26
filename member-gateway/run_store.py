"""Minimal durable run ledger with idempotency protection.

JSON persistence is intentionally simple for the Phase 1 vertical slice.
It proves state semantics without introducing a database platform prematurely.
"""
from pathlib import Path
from typing import Any, Dict
import json

class RunConflictError(RuntimeError):
    pass

class RunStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def _read(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def _write(self, state: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        tmp.replace(self.path)

    def begin(self, run_id: str, request_id: str, capability: str) -> Dict[str, Any]:
        state = self._read()
        if run_id in state:
            return {"created":False, "run":state[run_id]}
        state[run_id] = {
            "run_id":run_id, "first_request_id":request_id,
            "capability":capability, "workflow_state":"RECEIVED",
            "delivery_state":"NOT_DELIVERED"
        }
        self._write(state)
        return {"created":True, "run":state[run_id]}

    def transition(self, run_id: str, workflow_state: str) -> Dict[str, Any]:
        state = self._read()
        if run_id not in state:
            raise RunConflictError("RUN_UNKNOWN")
        state[run_id]["workflow_state"] = workflow_state
        self._write(state)
        return state[run_id]

    def mark_delivered(self, run_id: str) -> Dict[str, Any]:
        state = self._read()
        if run_id not in state:
            raise RunConflictError("RUN_UNKNOWN")
        state[run_id]["delivery_state"] = "DELIVERED"
        self._write(state)
        return state[run_id]
