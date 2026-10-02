from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_ROOT = ROOT / "governance" / "resilience" / "checkpoints"
REQUIRED_CHECKPOINT_FIELDS = {
    "version","checkpoint_id","project","workflow","stage","owner","source_authority",
    "completed_at","input_fingerprints","outputs","evidence","invalidation_triggers",
}
EVIDENCE_PREFIXES = ("http://","https://","run:","commit:","pr:","test:","receipt:")

def load_json(path: Path):
    return json.loads(path.read_text())

def _digest_bytes(data: bytes, algo: str) -> str:
    if algo == "sha256":
        return hashlib.sha256(data).hexdigest()
    if algo == "git_blob":
        header = f"blob {len(data)}\0".encode()
        return hashlib.sha1(header + data).hexdigest()
    raise ValueError(f"unsupported digest algorithm: {algo}")

def compute_digest(path: Path, algo: str) -> str:
    return _digest_bytes(path.read_bytes(), algo)

def fingerprint(path: str, algo: str = "sha256", root: Path = ROOT) -> dict:
    target = root / path
    if not target.is_file():
        raise FileNotFoundError(path)
    return {"path": path, "digest_algo": algo, "digest": compute_digest(target, algo)}

def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None

def _evidence_ref_valid(ref: str, root: Path) -> bool:
    if ref.startswith(EVIDENCE_PREFIXES):
        return True
    return (root / ref).exists()

def _fingerprint_shape_error(item: dict, label: str) -> str | None:
    if not all(item.get(k) for k in ("path","digest_algo","digest")):
        return f"{label} missing path/digest_algo/digest"
    algo = item.get("digest_algo")
    digest = item.get("digest","")
    if algo == "sha256" and not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        return f"{label} sha256 digest must be 64 hex chars"
    if algo == "git_blob" and not re.fullmatch(r"[0-9a-fA-F]{40}", digest):
        return f"{label} git_blob digest must be 40 hex chars"
    if algo not in {"sha256","git_blob"}:
        return f"{label} invalid digest_algo"
    return None

def validate_checkpoint(checkpoint: dict, root: Path = ROOT, verify_artifacts: bool = True) -> list[str]:
    errors = []
    missing = sorted(REQUIRED_CHECKPOINT_FIELDS - set(checkpoint))
    if missing:
        errors.append("missing checkpoint fields: " + ", ".join(missing))
        return errors
    if checkpoint.get("version") != "1.0.0":
        errors.append("checkpoint version must be 1.0.0")
    if _parse_timestamp(str(checkpoint.get("completed_at",""))) is None:
        errors.append("completed_at must be ISO-8601")

    source = root / checkpoint["source_authority"]
    if not source.exists():
        errors.append(f"source authority missing: {checkpoint['source_authority']}")

    for field in ("input_fingerprints","outputs"):
        rows = checkpoint.get(field) or []
        if not rows:
            errors.append(f"{field} must be non-empty")
        for i,item in enumerate(rows):
            label=f"{field}[{i}]"
            shape_error=_fingerprint_shape_error(item,label)
            if shape_error:
                errors.append(shape_error)
                continue
            if verify_artifacts:
                target=root / item["path"]
                if not target.is_file():
                    errors.append(f"{label} artifact missing: {item['path']}")
                    continue
                actual=compute_digest(target,item["digest_algo"])
                if actual.lower()!=item["digest"].lower():
                    errors.append(f"{label} digest mismatch: {item['path']}")

    evidence=checkpoint.get("evidence") or []
    if not evidence:
        errors.append("evidence must be non-empty")
    else:
        for i,ref in enumerate(evidence):
            if not isinstance(ref,str) or not ref.strip():
                errors.append(f"evidence[{i}] invalid")
            elif verify_artifacts and not _evidence_ref_valid(ref,root):
                errors.append(f"evidence[{i}] missing: {ref}")

    if not checkpoint.get("invalidation_triggers"):
        errors.append("invalidation_triggers must be non-empty")
    return errors

def current_fingerprints(checkpoint: dict, root: Path = ROOT) -> dict[str,str]:
    result={}
    for item in checkpoint.get("input_fingerprints",[]):
        target=root / item["path"]
        if not target.is_file():
            continue
        result[item["path"]]=compute_digest(target,item["digest_algo"])
    return result

def checkpoint_inputs_match(checkpoint: dict, current: dict[str,str] | None = None, root: Path = ROOT) -> bool:
    current = current if current is not None else current_fingerprints(checkpoint,root)
    for item in checkpoint.get("input_fingerprints", []):
        if current.get(item["path"],"").lower() != item["digest"].lower():
            return False
    return True

def latest_valid_checkpoint(checkpoints: list[dict], current: dict[str,str] | None = None, root: Path = ROOT) -> dict | None:
    valid=[]
    for cp in checkpoints:
        if validate_checkpoint(cp,root=root,verify_artifacts=True):
            continue
        if not checkpoint_inputs_match(cp,current=current,root=root):
            continue
        valid.append(cp)
    if not valid:
        return None
    return max(valid,key=lambda cp:_parse_timestamp(cp["completed_at"]))

def build_checkpoint(*, checkpoint_id: str, project: str, workflow: str, stage: str, owner: str,
                     source_authority: str, completed_at: str, input_paths: list[str],
                     output_paths: list[str], evidence: list[str], invalidation_triggers: list[str],
                     digest_algo: str = "sha256", root: Path = ROOT) -> dict:
    checkpoint={
        "version":"1.0.0",
        "checkpoint_id":checkpoint_id,
        "project":project,
        "workflow":workflow,
        "stage":stage,
        "owner":owner,
        "source_authority":source_authority,
        "completed_at":completed_at,
        "input_fingerprints":[fingerprint(path,digest_algo,root) for path in input_paths],
        "outputs":[fingerprint(path,digest_algo,root) for path in output_paths],
        "evidence":evidence,
        "invalidation_triggers":invalidation_triggers,
    }
    errors=validate_checkpoint(checkpoint,root=root,verify_artifacts=True)
    if errors:
        raise ValueError("; ".join(errors))
    return checkpoint

def persist_checkpoint(checkpoint: dict, store_root: Path = CHECKPOINT_ROOT, root: Path = ROOT) -> Path:
    errors=validate_checkpoint(checkpoint,root=root,verify_artifacts=True)
    if errors:
        raise ValueError("; ".join(errors))
    workflow=re.sub(r"[^a-zA-Z0-9_.-]+","-",checkpoint["workflow"]).strip("-")
    cid=re.sub(r"[^a-zA-Z0-9_.-]+","-",checkpoint["checkpoint_id"]).strip("-")
    target=store_root / workflow / f"{cid}.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(checkpoint,indent=2)+"\n")
    return target

def load_workflow_checkpoints(workflow: str, store_root: Path = CHECKPOINT_ROOT) -> list[dict]:
    folder=store_root / re.sub(r"[^a-zA-Z0-9_.-]+","-",workflow).strip("-")
    if not folder.exists():
        return []
    rows=[]
    for path in sorted(folder.glob("*.json")):
        rows.append(load_json(path))
    return rows

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
        layer_ids=set()
        for layer in layers:
            lid=layer.get("id")
            if not lid:
                errors.append(f"{sid}: conditioning layer missing id")
            elif lid in layer_ids:
                errors.append(f"{sid}: duplicate conditioning layer {lid}")
            layer_ids.add(lid)
            authority = layer.get("authority")
            if not authority or not (root / authority).exists():
                errors.append(f"{sid}: missing layer authority {authority}")
        if not system.get("drift_signals"):
            errors.append(f"{sid}: no drift signals")
    return errors
