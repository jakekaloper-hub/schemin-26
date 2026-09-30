"""Durable Phase-1 run ledger with explicit completion/replay invariants.

A run is replayable only when complete() has durably persisted both the
governed response packet and COMPLETED state in the same atomic file replace.
Delivery is deliberately separate from execution completion.
"""
from pathlib import Path
from typing import Any, Dict
import json

class RunConflictError(RuntimeError): pass

LEDGER_VERSION=3
TERMINAL_REPLAYABLE_STATE="COMPLETED"

class RunStore:
    def __init__(self,path:Path): self.path=Path(path)
    def _read(self)->Dict[str,Any]:
        if not self.path.exists(): return {}
        return json.loads(self.path.read_text())
    def _write(self,state:Dict[str,Any])->None:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        tmp=self.path.with_suffix(self.path.suffix+".tmp")
        tmp.write_text(json.dumps(state,indent=2,sort_keys=True)+"\n")
        tmp.replace(self.path)
    def get(self,run_id:str)->Dict[str,Any]:
        state=self._read()
        if run_id not in state: raise RunConflictError("RUN_UNKNOWN")
        return state[run_id]
    def begin(self,run_id:str,request_id:str,capability:str)->Dict[str,Any]:
        state=self._read()
        if run_id in state: return {"created":False,"run":state[run_id]}
        state[run_id]={"run_id":run_id,"first_request_id":request_id,
          "capability":capability,"workflow_state":"RECEIVED",
          "delivery_state":"NOT_DELIVERED","ledger_version":LEDGER_VERSION,
          "response_state":"ABSENT"}
        self._write(state); return {"created":True,"run":state[run_id]}
    def transition(self,run_id:str,workflow_state:str)->Dict[str,Any]:
        if workflow_state in {"PASSED","COMPLETED"}:
            raise RunConflictError("USE_COMPLETE_FOR_TERMINAL_SUCCESS")
        state=self._read()
        if run_id not in state: raise RunConflictError("RUN_UNKNOWN")
        state[run_id]["workflow_state"]=workflow_state
        self._write(state); return state[run_id]
    def complete(self,run_id:str,response_packet:Dict[str,Any])->Dict[str,Any]:
        if not isinstance(response_packet,dict): raise RunConflictError("INVALID_RESPONSE_PACKET")
        state=self._read()
        if run_id not in state: raise RunConflictError("RUN_UNKNOWN")
        row=state[run_id]
        if row.get("workflow_state")=="COMPLETED":
            raise RunConflictError("RUN_ALREADY_COMPLETED")
        row["response_packet"]=response_packet
        row["response_state"]="STORED"
        row["ledger_version"]=LEDGER_VERSION
        row["workflow_state"]="COMPLETED"
        self._write(state)
        return state[run_id]
    def mark_delivered(self,run_id:str)->Dict[str,Any]:
        state=self._read()
        if run_id not in state: raise RunConflictError("RUN_UNKNOWN")
        row=state[run_id]
        if row.get("workflow_state")!="COMPLETED" or row.get("response_state")!="STORED":
            raise RunConflictError("RUN_NOT_REPLAYABLE")
        row["delivery_state"]="DELIVERED"
        self._write(state); return state[run_id]
