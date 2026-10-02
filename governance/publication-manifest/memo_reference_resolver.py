#!/usr/bin/env python3
"""Deterministic Weekly Memo reference resolver.

Authority is derived from the Publication Manifest. Search/vector similarity may
locate candidates but must never choose publication authority.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"

class MemoReferenceError(ValueError):
    pass

def _memos(manifest):
    return [p for p in manifest["publications"] if p.get("family") == "weekly_memo"]

def _week(p):
    weeks = p.get("source_interval", {}).get("weeks", [])
    return weeks[0] if len(weeks) == 1 else None

def _released(p):
    return p.get("release_state") == "RELEASED" and bool(p.get("canonical_artifact"))

def load_manifest(path=MANIFEST):
    return json.loads(Path(path).read_text())

def resolve_memo_reference(request, manifest=None):
    manifest = manifest or load_manifest()
    memos = _memos(manifest)
    text = (request or "").strip().lower()

    explicit = re.search(r"\bweek\s*[-_ ]?(\d{1,2})\b", text)
    if explicit:
        week = int(explicit.group(1))
        matches = [p for p in memos if _week(p) == week and _released(p)]
        if len(matches) != 1:
            raise MemoReferenceError(f"REQUESTED_WEEK_ARTIFACT_NOT_VERIFIED: week={week}")
        return matches[0]

    current_terms = ("latest", "current", "benchmark", "most recent", "the memo")
    if not text or any(term in text for term in current_terms):
        current = [p for p in memos if _released(p) and p.get("metadata", {}).get("benchmark_status") == "CURRENT_BENCHMARK"]
        if len(current) != 1:
            raise MemoReferenceError("MEMO_REFERENCE_UNRESOLVED: expected exactly one CURRENT_BENCHMARK")
        latest_week = max(_week(p) for p in memos if _released(p) and _week(p) is not None)
        if _week(current[0]) != latest_week:
            raise MemoReferenceError("STALE_BENCHMARK_AUTHORITY")
        return current[0]

    raise MemoReferenceError("MEMO_REFERENCE_UNRESOLVED")

def authority_packet(request, manifest=None):
    p = resolve_memo_reference(request, manifest)
    return {
        "requested_reference": request,
        "publication_id": p["publication_id"],
        "week": _week(p),
        "canonical_artifact": p["canonical_artifact"],
        "release_state": p["release_state"],
        "benchmark_status": p.get("metadata", {}).get("benchmark_status"),
        "authority_refs": p.get("authority_refs", []),
    }

if __name__ == "__main__":
    import sys
    print(json.dumps(authority_packet(" ".join(sys.argv[1:])), indent=2))
