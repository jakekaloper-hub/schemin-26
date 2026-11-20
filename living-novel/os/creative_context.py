"""Fail-closed Novel OS creative task context adapter.

This module prepares an authority-ranked context manifest. It never invokes
an LLM, edits manuscripts, or promotes generated text to canon.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROUTER = "living-novel/os/TASK_CONTEXT_MATRIX_V1.json"
AUTHORITY = "living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md"
REGISTRY = "governance/execution-control/TASK_REGISTRY_V1.json"


class ContextError(ValueError):
    """Context could not be assembled safely."""


def resolve_context(root: Path, intent: str) -> dict:
    """Resolve Novel OS routing with authoritative sources pinned first.

    Fail closed when route data or any selected source is absent. This is a
    preparation operation, not authorization to publish or write into canon.
    """
    root = root.resolve()
    if not intent or not intent.strip():
        raise ContextError("Nonempty task intent required")
    router_path = root / ROUTER
    if not router_path.is_file():
        raise ContextError(f"Missing Novel OS router: {ROUTER}")
    try:
        router = json.loads(router_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ContextError("Novel OS router invalid or unreadable") from exc
    routes = router.get("routes")
    if not isinstance(routes, list):
        raise ContextError("Invalid Novel OS routing schema")
    normalized = intent.casefold()
    matches = [
        item for item in routes
        if isinstance(item, dict) and any(
            isinstance(term, str) and term.casefold() in normalized
            for term in item.get("terms", [])
        )
    ]
    exclusive = [item for item in matches if item.get("exclusive")]
    if exclusive:
        matches = exclusive[:1]
    else:
        matches = matches[:router.get("defaults", {}).get("max_matches", 2)]
    if not matches:
        raise ContextError("No authoritative Novel OS route matched intent")
    sources = [AUTHORITY, REGISTRY]
    for route in matches:
        for source in route.get("context_sources", []):
            if not isinstance(source, str) or source.startswith("/") or ".." in Path(source).parts:
                raise ContextError("Unsafe context source path")
            if source not in sources:
                sources.append(source)
    # Do not silently truncate mandatory authority references.
    selected = []
    for source in sources:
        target = (root / source).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ContextError(f"Missing or invalid required source: {source}")
        selected.append({"path": source, "bytes": target.stat().st_size})
    return {
        "status": "CONTEXT_READY_NOT_APPROVED",
        "intent": intent,
        "routes": [r["id"] for r in matches],
        "sources": selected,
        "constraints": [
            "verified_league_truth_precedes_prose",
            "generated_output_has_no_canon_authority",
            "existing_manuscript_release_gates_required",
            "no_new_provider_or_paid_dependency",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve governed Novel OS writing context")
    parser.add_argument("intent", help="Novel OS task request")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    try:
        result = resolve_context(args.root, args.intent)
    except ContextError as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
