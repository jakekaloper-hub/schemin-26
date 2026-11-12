#!/usr/bin/env python3
"""Warden + Umpire lane: fail-closed public-story security checks."""
from __future__ import annotations

FORBIDDEN_PUBLIC_TOKENS=(
  "mercer-private",
  "private trade strategy",
  "private negotiation note",
  "confidential roster strategy",
  "commissioner secret",
)

def scan_text(value, path="$"):
    problems=[]
    if isinstance(value,str):
        low=value.lower()
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in low:
                problems.append({"path":path,"token":token,"reason":"PRIVATE_INTELLIGENCE_LEAK"})
    elif isinstance(value,dict):
        for k,v in value.items():
            problems.extend(scan_text(v,f"{path}.{k}"))
    elif isinstance(value,list):
        for i,v in enumerate(value):
            problems.extend(scan_text(v,f"{path}[{i}]"))
    return problems

def enforce_public_story_boundary(payload):
    problems=scan_text(payload)
    if problems:
        raise ValueError(f"PUBLIC_STORY_BOUNDARY_FAIL: {problems}")
    return True
