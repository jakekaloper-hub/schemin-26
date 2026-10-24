"""Fail-closed season-scoped division overlay; no history extrapolation."""
from __future__ import annotations
import json
from pathlib import Path

DIVISIONS = Path(__file__).resolve().parents[1] / "data" / "divisions.json"


def resolve_seasonal_division_overlay(region_id: str, season: int | None, week: int | None = None) -> dict:
    if type(season) is not int or type(week) is not int or not (1 <= week <= 18):
        return {"ok": False, "code": "SEASON_AND_WEEK_REQUIRED"}
    data = json.loads(DIVISIONS.read_text(encoding="utf-8"))
    if season != data["season"]:
        return {"ok": False, "code": "UNVERIFIED_SEASON", "available_season": data["season"]}
    matching = [d for d in data["divisions"] if region_id in d["physical_zone_ids"]]
    if not matching:
        return {"ok": False, "code": "NO_DIVISION_PRESENCE", "region_id": region_id}
    if len({d["id"] for d in matching}) != len(matching):
        return {"ok": False, "code": "DUPLICATE_DIVISION_ID"}
    if any(d.get("spatial_model") != "LEAGUE_JURISDICTION_OVERLAY_NONEXCLUSIVE"
           or d.get("cohabitation_allowed") is not True for d in matching):
        return {"ok": False, "code": "DIVISION_ONTOLOGY_DRIFT"}
    return {
        "ok": True,
        "season": season,
        "week": week,
        "region_id": region_id,
        "division_ids": [d["id"] for d in matching],
        "membership_status": "SEASON_2026_ONLY",
        "week_specific_event_status": "NOT_INFERRED",
        "spatial_model": "NONEXCLUSIVE_JURISDICTION",
        "provenance": ["world/data/divisions.json"],
        "canon_mutation_allowed": False,
    }
