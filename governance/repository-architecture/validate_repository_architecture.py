#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "governance" / "repository-architecture" / "FOLDER_DOMAIN_REGISTRY_V2.json"
SCENARIOS = ROOT / "governance" / "repository-architecture" / "NAVIGATION_SCENARIOS_V2.json"

IGNORED_ROOT_DIRS = {".git", ".pytest_cache", "__pycache__"}

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text())

def top_level_dirs(root: Path = ROOT) -> set[str]:
    return {
        p.name for p in root.iterdir()
        if p.is_dir() and p.name not in IGNORED_ROOT_DIRS
    }

def validate_registry(root: Path = ROOT, registry: dict | None = None) -> list[str]:
    data = registry or load_registry()
    errors: list[str] = []
    domains = data.get("domains", [])
    declared = [d.get("path") for d in domains]
    if len(declared) != len(set(declared)):
        errors.append("duplicate top-level domain registration")
    actual = top_level_dirs(root)
    missing = sorted(set(declared) - actual)
    unexpected = sorted(actual - set(declared))
    if missing:
        errors.append("registered top-level directories missing: " + ", ".join(missing))
    if unexpected:
        errors.append("unauthorized top-level directories: " + ", ".join(unexpected))
    for domain in domains:
        path = domain.get("path")
        if not path:
            errors.append("domain path is required")
            continue
        if not domain.get("owner"):
            errors.append(f"{path}: owner is required")
        if domain.get("entrypoint_required"):
            entry = domain.get("canonical_entrypoint")
            if not entry:
                errors.append(f"{path}: canonical entrypoint is required")
            elif not (root / entry).exists():
                errors.append(f"{path}: canonical entrypoint missing: {entry}")
        allowed = domain.get("allowed")
        prohibited = domain.get("prohibited")
        if not isinstance(allowed, list) or not allowed:
            errors.append(f"{path}: allowed artifact classes required")
        if not isinstance(prohibited, list):
            errors.append(f"{path}: prohibited artifact classes must be an array")
    return errors

def validate_central_navigation(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    requirements = {
        "README.md": ["REPOSITORY_ARCHITECTURE_V2.md", "FOLDER_DOMAIN_REGISTRY_V2.json"],
        "PROJECT_CONTROL_REGISTRY.md": ["REPOSITORY_ARCHITECTURE_V2.md", "TASK_REGISTRY_V1.json"],
        "docs/CATALOG.md": ["REPOSITORY_ARCHITECTURE_V2.md", "FOLDER_DOMAIN_REGISTRY_V2.json", "TASK_REGISTRY_V1.json"],
        "docs/INVENTORY.md": ["REPOSITORY_ARCHITECTURE_V2.md", "FOLDER_DOMAIN_REGISTRY_V2.json", "TASK_REGISTRY_V1.json"],
        "docs/SESSION_CONTEXT.md": ["REPOSITORY_ARCHITECTURE_V2.md", "FOLDER_DOMAIN_REGISTRY_V2.json", "FILE_PLACEMENT_STANDARD_V1.md"],
    }
    for rel, needles in requirements.items():
        path = root / rel
        if not path.exists():
            errors.append(f"central navigation file missing: {rel}")
            continue
        text = path.read_text()
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing architecture reference {needle}")
    return errors

def validate_legacy_pointer(root: Path = ROOT) -> list[str]:
    path = root / "docs" / "architecture" / "REPOSITORY_ARCHITECTURE.md"
    if not path.exists():
        return ["legacy architecture pointer missing"]
    text = path.read_text()
    if "SUPERSEDED" not in text or "REPOSITORY_ARCHITECTURE_V2.md" not in text:
        return ["legacy architecture file must explicitly point to V2"]
    return []

def validate_navigation_scenarios(root: Path = ROOT) -> list[str]:
    if not SCENARIOS.exists():
        return ["navigation scenarios registry missing"]
    data = json.loads(SCENARIOS.read_text())
    errors: list[str] = []
    for scenario in data.get("scenarios", []):
        for rel in scenario.get("required_paths", []):
            if not (root / rel).exists():
                errors.append(f"{scenario.get('id')}: missing required path {rel}")
    return errors

def validate(root: Path = ROOT) -> list[str]:
    return (
        validate_registry(root)
        + validate_central_navigation(root)
        + validate_legacy_pointer(root)
        + validate_navigation_scenarios(root)
    )

def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Repository Architecture V2 validation PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
