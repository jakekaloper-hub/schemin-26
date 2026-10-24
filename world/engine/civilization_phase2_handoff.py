"""Production-oriented read-only handoff through existing Memo/Novel/Atlas entrypoints."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from world.engine.civilization_temporal import resolve_seasonal_division_overlay
from world.production.build_visual_world_packet import build_packet

ROOT = Path(__file__).resolve().parents[2]


def _load_adapter(name: str):
    path = ROOT / "world/location-control-plane/adapters" / f"{name}_adapter.py"
    spec = importlib.util.spec_from_file_location(f"phase2_{name}_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, f"compile_{name}_location_packet")


def build_phase2_handoff(location_id: str, season: int, week: int) -> dict:
    memo = _load_adapter("memo")(location_id)
    novel = _load_adapter("novel")(location_id)
    if memo.get("status") not in {"READY_FOR_SEMANTIC_QA", "READY_FOR_RENDER"} or novel.get("status") not in {"READY_FOR_SEMANTIC_QA", "READY_FOR_RENDER"}:
        return {"ok": False, "code": "LOCATION_PACKET_NOT_READY", "memo_status": memo.get("status"), "novel_status": novel.get("status")}
    cm, cn = memo.get("civilization_context"), novel.get("civilization_context")
    if not cm or not cn or cm["context_id"] != cn["context_id"] or cm["region_id"] != cn["region_id"]:
        return {"ok": False, "code": "CROSS_PUBLICATION_CONTEXT_DRIFT"}
    overlay = resolve_seasonal_division_overlay(cm["region_id"], season, week)
    if not overlay["ok"]:
        return {"ok": False, "code": overlay["code"]}
    visual = build_packet(location_id)
    cv = visual["civilization_context"]
    if cv["context_id"] != cm["context_id"] or cv["region_id"] != cm["region_id"]:
        return {"ok": False, "code": "VISUAL_CONTEXT_DRIFT"}
    return {
        "ok": True, "location_id": location_id, "season": season, "week": week,
        "memo_location_packet": memo, "novel_location_packet": novel,
        "visual_world_packet": visual, "seasonal_division_overlay": overlay,
        "shared_context_id": cm["context_id"],
        "verified_event_status": "REQUIRES_SEPARATE_LEAGUE_FACT_LOCK",
        "pov_status": "REQUIRES_SEPARATE_APPROVED_OWNER_POV",
        "publication_eligible": False, "canon_mutation_allowed": False,
    }
