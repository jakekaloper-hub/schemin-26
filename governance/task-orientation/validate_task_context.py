#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def _term_hit(text: str, term: str) -> bool:
    pattern = r"(?:^|[^a-z0-9])" + re.escape(term.lower()).replace(r"\ ", r"\s+") + r"(?:$|[^a-z0-9])"
    return re.search(pattern, text.lower()) is not None

def route_task(task: str, matrix: dict) -> dict:
    scored = []
    for route in matrix.get("routes", []):
        hits = [term for term in route.get("terms", []) if _term_hit(task, term)]
        score = sum(3 if " " in term else 1 for term in hits)
        if score:
            scored.append((score, route["id"], hits, route))
    scored.sort(key=lambda item: (-item[0], item[1]))
    max_matches = int(matrix.get("defaults", {}).get("max_matches", 2))
    max_sources = int(matrix.get("defaults", {}).get("max_context_sources", 4))
    selected = scored[:max_matches]
    sources = []
    for _, _, _, route in selected:
        for source in route.get("context_sources", []):
            if source not in sources:
                sources.append(source)
    for source in matrix.get("defaults", {}).get("context_sources", []):
        if source not in sources:
            sources.append(source)
    return {
        "routes": [item[1] for item in selected],
        "hits": {item[1]: item[2] for item in selected},
        "context_sources": sources[:max_sources],
    }

MATRICES = [
    ROOT / "governance" / "task-orientation" / "TASK_CONTEXT_MATRIX_V1.json",
    ROOT / "living-novel" / "os" / "TASK_CONTEXT_MATRIX_V1.json",
]

def validate_matrix(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text())
    defaults = data.get("defaults", {})
    max_sources = int(defaults.get("max_context_sources", 4))
    if max_sources > 4:
        errors.append(f"{path}: max_context_sources exceeds Schemin context-economy ceiling")
    seen: set[str] = set()
    for route in data.get("routes", []):
        rid = route.get("id")
        if not rid:
            errors.append(f"{path}: route missing id")
            continue
        if rid in seen:
            errors.append(f"{path}: duplicate route id {rid}")
        seen.add(rid)
        if not route.get("terms"):
            errors.append(f"{path}: route {rid} has no terms")
        sources = route.get("context_sources", [])
        if not sources:
            errors.append(f"{path}: route {rid} has no context sources")
        if len(sources) > max_sources:
            errors.append(f"{path}: route {rid} exceeds {max_sources} context sources")
        for source in sources:
            if not (ROOT / source).exists():
                errors.append(f"{path}: route {rid} references missing source {source}")
    for source in defaults.get("context_sources", []):
        if not (ROOT / source).exists():
            errors.append(f"{path}: default references missing source {source}")
    return errors

def main() -> int:
    errors = []
    for path in MATRICES:
        errors.extend(validate_matrix(path))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Task context matrices valid.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
