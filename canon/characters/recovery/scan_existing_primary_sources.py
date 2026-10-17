#!/usr/bin/env python3
"""Explicit-roots-only local recovery for existing approved character source bytes.

Metadata-only by default. It does not send files over a network, change canon,
approve supplemental assets, or perform rendering. Permission to access each root
must come from the operator controlling the machine. Only sha256-exact bytes stage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "canon/characters/reference_sources_v1.json"
SKIP_DIR_NAMES = frozenset({".git", "node_modules", ".venv", "__pycache__", "venv"})


def digest_path(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def find_exact_sources(
    roots: list[Path],
    source_registry: dict,
    *,
    skip_existing: bool = False,
    repository_root: Path = ROOT,
) -> dict:
    entries = source_registry.get("entries", [])
    if len(entries) != 12 or len({x["character_id"] for x in entries}) != 12:
        raise ValueError("Source registry must have exactly 12 unique character IDs")
    if len({x["expected_sha256"] for x in entries}) != 12:
        raise ValueError("Cannot recover duplicate cross-character hashes")
    candidates: dict[int, list[dict]] = {}
    verified_existing: list[str] = []
    for entry in entries:
        dest = repository_root / entry["repository_path"]
        if skip_existing and dest.is_file():
            if (digest_path(dest) != entry["expected_sha256"]
                    or dest.stat().st_size != entry["observed_library_size_bytes"]):
                raise ValueError(f"Registered primary destination is corrupt: {entry['character_id']}")
            verified_existing.append(entry["character_id"])
            continue
        candidates.setdefault(entry["observed_library_size_bytes"], []).append(entry)
    scanned = 0
    byte_size_matches = 0
    result: dict[str, dict] = {}
    for root in roots:
        root = root.expanduser().resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"Requested authorized root is missing: {root}")
        for folder, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
            for name in files:
                p = Path(folder) / name
                if p.is_symlink():
                    continue
                scanned += 1
                try:
                    size = p.stat().st_size
                except OSError:
                    continue
                eligible = candidates.get(size)
                if not eligible:
                    continue
                byte_size_matches += 1
                try:
                    h = digest_path(p)
                except OSError:
                    continue
                for entry in eligible:
                    if entry["expected_sha256"] == h:
                        cid = entry["character_id"]
                        result.setdefault(cid, {
                            "character_id": cid,
                            "expected_sha256": h,
                            "bytes": size,
                            "repository_path": entry["repository_path"],
                            # Local diagnostics only; do not push source path to GitHub.
                            "local_source_path": str(p),
                        })
    return {
        "state": "LOCAL_EXACT_BYTES_FOUND" if result else "NO_ADDITIONAL_EXACT_BYTES_FOUND",
        "scanned_files": scanned,
        "candidate_size_hits": byte_size_matches,
        "previously_verified_in_repo": sorted(verified_existing),
        "matches": sorted(result.values(), key=lambda e: e["character_id"]),
    }


def stage_results(report: dict, destination_root: Path) -> list[dict]:
    destination_root = destination_root.resolve()
    # Preflight every destination first. Never replace a conflicting file.
    for item in report["matches"]:
        dest = (destination_root / item["repository_path"]).resolve()
        if not dest.is_relative_to(destination_root):
            raise ValueError("Unsafe canonical asset destination")
        if dest.is_file() and digest_path(dest) != item["expected_sha256"]:
            raise ValueError(f"Conflict: refusing overwrite at {dest}")
    staged = []
    for item in report["matches"]:
        dest = destination_root / item["repository_path"]
        if dest.is_file():
            continue
        src = Path(item["local_source_path"])
        if src.stat().st_size != item["bytes"] or digest_path(src) != item["expected_sha256"]:
            raise ValueError("Source bytes changed before staging; stop")
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tempname = tempfile.mkstemp(prefix=".canon-approved-primary-", dir=dest.parent)
        try:
            with os.fdopen(fd, "wb") as out, src.open("rb") as inp:
                shutil.copyfileobj(inp, out)
            if digest_path(Path(tempname)) != item["expected_sha256"]:
                raise ValueError("Source changed during copy; stop")
            os.replace(tempname, dest)
        finally:
            if os.path.exists(tempname):
                os.unlink(tempname)
        staged.append({"character_id": item["character_id"], "repository_path": item["repository_path"]})
    return staged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-root", type=Path, action="append", required=True,
                        help="Explicitly authorized local folder to scan. Repeat as needed.")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--stage", action="store_true", help="Stage exact sources, refusing collisions.")
    args = parser.parse_args()
    root = args.repository_root.resolve()
    registry = json.loads((root / "canon/characters/reference_sources_v1.json").read_text())
    found = find_exact_sources(args.search_root, registry, skip_existing=True, repository_root=root)
    if args.stage:
        found["staged"] = stage_results(found, root)
    # Avoid exposing exact local browser cache, home paths, and filenames to public logs.
    safe = {k:v for k,v in found.items() if k != "matches"}
    safe["matches"] = [{k:v for k,v in m.items() if k != "local_source_path"} for m in found["matches"]]
    print(json.dumps(safe, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
