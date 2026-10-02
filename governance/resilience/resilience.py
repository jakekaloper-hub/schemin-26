from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_CHECKPOINT_FIELDS = {
    "version","checkpoint_id","project","workflow","stage","owner","source_authority",
    "completed_at","input_fingerprints","outputs","evidence","invalidation_triggers",
}

def load_json(path: Path):
    return json.loads(path.read_text())

def validate_checkpoint(checkpoint: dict, root: Path = ROOT) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_CHECKPOINT_FIELDS - set(checkpoint))
    if missing:
        errors.append("missing checkpoint fields: " + ", ".join(missing))
        return errors
    if checkpoint.get("version") != "1.0.0":
        errors.append("checkpoint version must be 1.0.0")
    source = root / checkpoint["source_authority"]
    if not source.exists():
        errors.append(f"source authority missing: {checkpoint['source_authority']}")
    for field in ("input_fingerprints","outputs"):
        rows = checkpoint.get(field) or []
        if not rows:
            errors.append(f"{field} must be non-empty")
        for i,row in enumerate(rows):
            if not all(row.get(k) for k in ("path","digest_algo","digest")):
                errors.append(f"{field}[{i}] missing path/digest_algo/digest")
            if row.get("digest_algo") not in {"sha256","git_blob"}:
                errors.append(f"{field}[{i}] invalid digest_algo")
    if not checkpoint.get("evidence"):
        errors.append("evidence must be non-empty")
    if not checkpoint.get("invalidation_triggers"):
        errors.append("invalidation_triggers must be non-empty")
    return errors

def checkpoint_inputs_match(checkpoint: dict, current_fingerprints: dict[str,str]) -> bool:
    for item in checkpoint.get("input_fingerprints", []):
        if current_fingerprints.get(item["path"]) != item["digest"]:
            return False
    return True

def latest_valid_checkpoint(checkpoints: list[dict], current_fingerprints: dict[str,str]) -> dict | None:
    valid = [
        cp for cp in checkpoints
        if not validate_checkpoint(cp) and checkpoint_inputs_match(cp, current_fingerprints)
    ]
    if not valid:
        return None
    return sorted(valid, key=lambda cp: cp["completed_at"])[-1]

def resolve_task_by_alias(registry: dict, phrase: str) -> dict | None:
    needle = phrase.strip().lower()
    exact = []
    contains = []
    for task in registry.get("tasks", []):
        aliases = [str(x).lower() for x in task.get("aliases", [])]
        title = str(task.get("title","")).lower()
        if needle in aliases or needle == title:
            exact.append(task)
        elif any(alias in needle or needle in alias for alias in aliases):
            contains.append(task)
    pool = exact or contains
    if not pool:
        return None
    priority = {"IN_PROGRESS":0,"VERIFYING":1,"READY":2,"WAITING_EXTERNAL":3,"NOT_STARTED":4,"BLOCKED":5,"COMPLETE":9}
    return sorted(pool, key=lambda t:(priority.get(t.get("status"),6), t.get("task_id","")))[0]

def validate_conditioning_registry(doc: dict, root: Path = ROOT) -> list[str]:
    errors = []
    systems = doc.get("systems") or []
    if not systems:
        return ["conditioning registry has no systems"]
    seen = set()
    for system in systems:
        sid = system.get("id")
        if not sid:
            errors.append("conditioning system missing id")
            continue
        if sid in seen:
            errors.append(f"duplicate conditioning system {sid}")
        seen.add(sid)
        entry = system.get("entry_point")
        if not entry or not (root / entry).exists():
            errors.append(f"{sid}: missing entry point {entry}")
        layers = system.get("required_layers") or []
        if not layers:
            errors.append(f"{sid}: no required layers")
        for layer in layers:
            authority = layer.get("authority")
            if not authority or not (root / authority).exists():
                errors.append(f"{sid}: missing layer authority {authority}")
        if not system.get("drift_signals"):
            errors.append(f"{sid}: no drift signals")
    return errors
