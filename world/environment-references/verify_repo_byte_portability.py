#!/usr/bin/env python3
"""Verify Phase 3 structural-reference portability in a fresh repo checkout.

This proves repository-byte resolution and integrity only.
It deliberately does NOT claim external renderer injection.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/"world"/"location-control-plane"/"registries"/"LOCATION_REFERENCE_REGISTRY.json"

def main():
    reg=json.loads(REG.read_text())
    rows=reg["locations"]
    assert len(rows)==23
    receipts=[]
    for row in rows:
        assert row["structural_reference_status"]=="APPROVED_STRUCTURAL_REFERENCE"
        assert row["repo_byte_status"]=="VERIFIED_REPO_PATH"
        assert row["renderer_injection_status"]=="UNPROVEN"
        assert row["renderer_ready"] is False
        uris=row["approved_structural_reference_uris"]
        assert len(uris)==1
        p=ROOT/uris[0]
        assert p.is_file(), uris[0]
        b=p.read_bytes()
        assert b.startswith(b"<svg"), uris[0]
        receipts.append({"location_id":row["location_id"],"uri":uris[0],"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
    print(json.dumps({"status":"PASS_REPO_BYTE_PORTABILITY_ONLY","count":len(receipts),"renderer_injection":"UNPROVEN","references":receipts},indent=2))

if __name__=="__main__":
    main()
