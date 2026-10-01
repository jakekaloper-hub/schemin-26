#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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
