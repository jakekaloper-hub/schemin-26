#!/usr/bin/env python3
"""Source reference verifier for Memo OS local evidence snapshots.

Does not authenticate remote ESPN/NFL claims; validates that supplied evidence
bytes and metadata are internally bound, so synthetic evidence cannot self-pass
as provider-authenticated.
"""
import hashlib,json
from pathlib import Path

def verify_sources(packet, packet_path):
    errors=[]; root=Path(packet_path).resolve().parent
    for index,item in enumerate(packet.get("source_inputs",[]),1):
        label=f"source {index}"
        rel=item.get("path")
        if not isinstance(rel,str) or not rel:
            errors.append(f"{label}: missing evidence path");continue
        path=(root/rel).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f"{label}: inaccessible evidence");continue
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item.get("sha256"):errors.append(f"{label}: evidence hash mismatch")
        if item.get("authentication") != "PROVIDER_VERIFIED":
            errors.append(f"{label}: authenticated source receipt required")
        if not item.get("provider_receipt"):
            errors.append(f"{label}: provider receipt missing")
    if packet.get("requires_live_sources") and not packet.get("source_inputs"):
        errors.append("live source inputs required")
    return errors
