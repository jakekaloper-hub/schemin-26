#!/usr/bin/env python3
"""Validate Phase 1 source-byte portability state from repository truth.

This does not fetch external bytes. It fails closed until every target source
asset exists at its canonical path and matches the approved SHA-256.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
REG=ROOT/"canon"/"characters"/"reference_sources_v1.json"

def inspect():
    doc=json.loads(REG.read_text())
    rows=[]
    for item in doc["entries"]:
        path=ROOT/item["repository_path"]
        row={
            "character_id":item["character_id"],
            "path":item["repository_path"],
            "expected_sha256":item["expected_sha256"],
            "exists":path.exists(),
            "observed_sha256":None,
            "status":"SOURCE_BYTES_REQUIRED",
        }
        if path.exists():
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            row["observed_sha256"]=digest
            row["status"]="PASS" if digest==item["expected_sha256"] else "HASH_MISMATCH"
        rows.append(row)
    return rows

def main():
    rows=inspect()
    passed=sum(r["status"]=="PASS" for r in rows)
    result={"passed":passed,"total":len(rows),"phase_status":"PASS" if passed==len(rows) else "HOLD","rows":rows}
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if passed==len(rows) else 2)

if __name__=="__main__":
    main()
