"""Development-only adapter to existing Memo assembly and Novel POV contracts.

No writes to published artifacts, no invented POV, no automatic approval.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from world.engine.civilization_hydration import build_central_basin_hydration

ROOT = Path(__file__).resolve().parents[2]


def _load_novel_validator():
    path = ROOT / "living-novel/os/qa/pov_packet_validator.py"
    spec = importlib.util.spec_from_file_location("novel_pov_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_pov_packet


def validate_preproduction_bridge(pov_packet: dict | None = None) -> dict:
    hydration = build_central_basin_hydration()
    if not hydration["ok"]:
        return hydration
    assembly = json.loads((ROOT / "memo-os/week-4/publication-readiness/WEEK_04_ASSEMBLY_MANIFEST.json").read_text())
    memo = {
        "contract": "memo-os/week-4/publication-readiness/WEEK_04_ASSEMBLY_MANIFEST.json",
        "publication_id": assembly["publication_id"],
        "assembly_state": assembly["state"],
        "context": hydration["memo_packet"],
        "can_assemble_page": False,
        "reason": "No verified week-specific event or approved page artifact; development context only",
    }
    novel = {
        "contract": "living-novel/os/qa/pov_packet_validator.py",
        "context": hydration["novel_packet"],
        "can_publish_scene": False,
        "reason": "No approved owner POV, story-time cutoff or verified knowledge for this pilot",
    }
    if pov_packet is not None:
        novel["pov_validation_errors"] = _load_novel_validator()(pov_packet)
        novel["can_publish_scene"] = False
    return {
        "ok": True,
        "status": "CONTRACT_COMPATIBILITY_ONLY_NOT_PRODUCTION_INVOCATION",
        "hydration": hydration,
        "memo": memo,
        "novel": novel,
        "production_gate": "HOLD",
    }
