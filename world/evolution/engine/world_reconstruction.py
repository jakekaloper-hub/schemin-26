from __future__ import annotations
import copy, hashlib, json
from typing import Any
from engine.world_evolution import apply_to_payloads

CONTRACT_VERSION="1.0"
SUPPORTED_SOURCE_SCHEMA="1.0"

def canonical_bytes(value:Any)->bytes:
    return (json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode("utf-8")

def digest(value:Any)->str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def make_envelope(payloads:dict[str,Any],transactions:list[dict[str,Any]])->dict[str,Any]:
    base={k:copy.deepcopy(payloads[k]) for k in ("state","events","ledger")}
    return {
      "contract_version":CONTRACT_VERSION,
      "state_schema_version":base["state"].get("schema_version"),
      "events_schema_version":base["events"].get("schema_version"),
      "ledger_schema_version":base["ledger"].get("schema_version"),
      "base_state":base["state"],"base_events":base["events"],"base_ledger":base["ledger"],
      "source_hashes":{k:digest(v) for k,v in base.items()},
      "transactions":copy.deepcopy(transactions)
    }

def validate_envelope(env:dict[str,Any])->None:
    if env.get("contract_version")!=CONTRACT_VERSION:
        raise ValueError("UNSUPPORTED_RECONSTRUCTION_CONTRACT_VERSION")
    for key in ("state_schema_version","events_schema_version","ledger_schema_version"):
        if env.get(key)!=SUPPORTED_SOURCE_SCHEMA:
            raise ValueError("UNSUPPORTED_SOURCE_SCHEMA_VERSION")
    mapping={"state":"base_state","events":"base_events","ledger":"base_ledger"}
    for key,field in mapping.items():
        expected=(env.get("source_hashes") or {}).get(key)
        if not expected or digest(env.get(field))!=expected:
            raise ValueError(f"SOURCE_HASH_MISMATCH:{key}")
    if not isinstance(env.get("transactions"),list):
        raise ValueError("INVALID_TRANSACTION_SEQUENCE")

def reconstruct(env:dict[str,Any],static_payloads:dict[str,Any])->dict[str,Any]:
    validate_envelope(env)
    p=copy.deepcopy(static_payloads)
    p["state"]=copy.deepcopy(env["base_state"])
    p["events"]=copy.deepcopy(env["base_events"])
    p["ledger"]=copy.deepcopy(env["base_ledger"])
    for req in env["transactions"]:
        p,_=apply_to_payloads(req,p)
    return p
