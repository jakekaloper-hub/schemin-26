"""Governed, provider-independent manuscript candidate staging for Novel OS.

No model is invoked. Draft text must be supplied by an actual author/provider.
All artifacts remain candidates until the existing Novel OS release gate accepts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from creative_context import ContextError, resolve_context

SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{2,80}$")
REQUIRED = ("task_id", "intent", "pov", "chapter_job", "dramatic_question",
            "location", "opening_pressure", "turn", "consequence",
            "open_loop", "off_page", "exit_pressure", "source_paths")


def _safe_path(root: Path, path: str) -> Path:
    if not isinstance(path, str) or not path or Path(path).is_absolute() or ".." in Path(path).parts:
        raise ContextError("Unsafe source path")
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ContextError(f"Missing source: {path}")
    return candidate


def prepare(root: Path, spec: dict) -> dict:
    """Build source-verified context package; does not certify content."""
    root = root.resolve()
    if not isinstance(spec, dict):
        raise ContextError("Specification must be an object")
    missing = [key for key in REQUIRED if not spec.get(key)]
    if missing:
        raise ContextError("Missing required fields: " + ", ".join(missing))
    task_id = spec["task_id"]
    if not isinstance(task_id, str) or not SAFE_ID.fullmatch(task_id):
        raise ContextError("Invalid task identifier")
    if not isinstance(spec["source_paths"], list) or not spec["source_paths"]:
        raise ContextError("source_paths must be nonempty list")
    if any(not isinstance(spec[k], str) or not spec[k].strip() for k in REQUIRED if k != "source_paths"):
        raise ContextError("Required prose gate fields must be nonempty strings")
    context = resolve_context(root, spec["intent"])
    sources = []
    for path in spec["source_paths"]:
        target = _safe_path(root, path)
        sources.append({"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    for entry in context["sources"]:
        path = entry["path"]
        if path not in {s["path"] for s in sources}:
            target = _safe_path(root, path)
            sources.append({"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    return {"status": "READY_FOR_DRAFT_NOT_CANON", "task_id": task_id,
            "specification": {k: spec[k] for k in REQUIRED},
            "routes": context["routes"], "sources": sources,
            "instructions": [
                "Historical factual claims must trace to included verified sources.",
                "Write causally; source weeks do not define chapters.",
                "Preserve canonical POV, location and character identity.",
                "Treat the draft as noncanonical until independent release."
            ]}


def stage(root: Path, packet: dict, prose: str, output_dir: Path) -> dict:
    """Stage an actual supplied prose candidate and content-addressed receipt."""
    root = root.resolve()
    if packet.get("status") != "READY_FOR_DRAFT_NOT_CANON":
        raise ContextError("Unapproved or malformed context packet")
    task_id = packet.get("task_id", "")
    if not isinstance(task_id, str) or not SAFE_ID.fullmatch(task_id):
        raise ContextError("Invalid task identifier")
    if not isinstance(prose, str) or len(prose.split()) < 350:
        raise ContextError("Insufficient substantive manuscript prose (minimum 350 words)")
    for entry in packet.get("sources", []):
        target = _safe_path(root, entry["path"])
        if hashlib.sha256(target.read_bytes()).hexdigest() != entry.get("sha256"):
            raise ContextError("Stale source: " + entry["path"])
    dest = output_dir.resolve()
    if not dest.is_relative_to(root) or dest.exists():
        raise ContextError("Output must be a new path inside repository")
    dest.mkdir(parents=True)
    manuscript = dest / "candidate.md"
    manuscript.write_text(prose, encoding="utf-8")
    receipt = {"status": "CANDIDATE_PENDING_INDEPENDENT_REVIEW",
               "task_id": task_id, "created_utc": datetime.now(timezone.utc).isoformat(),
               "manuscript": manuscript.relative_to(root).as_posix(),
               "manuscript_sha256": hashlib.sha256(prose.encode()).hexdigest(),
               "word_count": len(prose.split()), "sources": packet["sources"],
               "release_authority": "NONE", "independent_umpire": "PENDING"}
    (dest / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path, help="JSON dossier with all pre-prose gate fields")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--draft", type=Path, help="Existing, substantive human/provider-authored Markdown")
    parser.add_argument("--out", type=Path, help="New candidate directory inside repository")
    args = parser.parse_args()
    try:
        packet = prepare(args.root, json.loads(args.spec.read_text(encoding="utf-8")))
        if args.draft or args.out:
            if not args.draft or not args.out:
                raise ContextError("--draft and --out must be supplied together")
            receipt = stage(args.root, packet, args.draft.read_text(encoding="utf-8"), args.out)
            print(json.dumps(receipt, indent=2))
        else:
            print(json.dumps(packet, indent=2))
        return 0
    except (ContextError, ValueError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
