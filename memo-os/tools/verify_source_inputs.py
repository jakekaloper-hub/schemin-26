#!/usr/bin/env python3
"""Verify local evidence bytes AND trusted ingest attestation.

An HMAC proves the receipt was issued by a configured trusted intake process,
NOT that ESPN/NFL content is true. Keys must come from a protected runtime secret.
"""
import hashlib,hmac,json,os
from pathlib import Path

def signature(key, source_sha, provider, provider_receipt):
    payload=json.dumps({"sha256":source_sha,"provider":provider,"provider_receipt":provider_receipt},sort_keys=True,separators=(",",":")).encode()
    return hmac.new(key.encode(),payload,hashlib.sha256).hexdigest()

def verify_sources(packet, packet_path):
    errors=[];root=Path(packet_path).resolve().parent
    inputs=packet.get("source_inputs",[])
    if not isinstance(inputs,list):
        return ["source inputs must be an array"]
    key=os.environ.get("SCHEMIN_MEMO_INGEST_HMAC_KEY","")
    for i,item in enumerate(inputs,1):
        label=f"source {i}"
        if not isinstance(item,dict):
            errors.append(f"{label}: invalid source record");continue
        rel=item.get("path")
        if not isinstance(rel,str) or not rel:
            errors.append(f"{label}: missing evidence path");continue
        source=(root/rel).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            errors.append(f"{label}: inaccessible evidence");continue
        actual=hashlib.sha256(source.read_bytes()).hexdigest()
        if actual!=item.get("sha256"):errors.append(f"{label}: evidence hash mismatch")
        provider=item.get("provider")
        receipt=item.get("provider_receipt")
        if not isinstance(provider,str) or not provider or not isinstance(receipt,str) or not receipt:
            errors.append(f"{label}: provider and intake receipt required");continue
        if len(key)<32:
            errors.append(f"{label}: trusted ingestion verification key unavailable");continue
        expected=signature(key,actual,provider,receipt)
        if not hmac.compare_digest(expected,str(item.get("ingest_attestation",""))):
            errors.append(f"{label}: trusted ingestion attestation mismatch")
    if packet.get("requires_live_sources") and not inputs:
        errors.append("live source inputs required")
    return errors
