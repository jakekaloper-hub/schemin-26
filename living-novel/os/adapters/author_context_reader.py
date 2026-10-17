"""Read-only, time-bounded Author Context Packet assembly from existing source rows.

This is a small utility in existing Novel OS; it creates no second memory store.
Input historical evidence MUST have its own source/provenance and verified matchups.
"""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any

class AuthorContextError(ValueError):
    pass

def author_context(*, character_id: str, scene_year: int, scene_week: int,
                   owner_domains: Mapping[str, Any], historical_rows: list[dict],
                   known_identity_links: Mapping[str, list[int]] | None = None) -> dict:
    """Return only scenes a principal could chronologically know (no source-side writes).

    Historic team-slot to 2026 owner mappings are NEVER assumed from matching integers.
    A caller must independently verify such identities and pass them explicitly.
    """
    if not isinstance(scene_year, int) or not isinstance(scene_week, int) or not 1 <= scene_week <= 19:
        raise AuthorContextError("scene_year must be integer and scene_week 1..19")
    domains = owner_domains.get("domains", [])
    owners = [d for d in domains if d.get("character_id") == character_id]
    if len(owners) != 1:
        raise AuthorContextError("character must identify exactly one registered 2026 owner")
    owner = owners[0]
    proven = (known_identity_links or {}).get(character_id, [])
    permitted_team_ids = {int(t) for t in proven}
    is_current_owner_year = scene_year == 2026
    if is_current_owner_year:
        permitted_team_ids.add(int(owner["team_id"]))
    factual = []
    unresolved = []
    for row in historical_rows:
        year, week = row.get("season", 2022), row.get("week")
        if not isinstance(year, int) or not isinstance(week, int) or (year, week) > (scene_year, scene_week):
            continue
        entry = {"season": year, "week": week, "home_team_id": row.get("home_team_id"),
                 "away_team_id": row.get("away_team_id"), "home_points": row.get("home_points"),
                 "away_points": row.get("away_points"), "winner": row.get("winner"),
                 "source_status": "HISTORICAL_MATCHUP_RECORD"}
        involved = {row.get("home_team_id"), row.get("away_team_id")}
        if involved & permitted_team_ids:
            factual.append(entry)
        else:
            unresolved.append(entry)
    factual.sort(key=lambda x: (x["season"], x["week"]))
    return {"character_id": character_id, "scene_year": scene_year, "scene_week": scene_week,
            "current_domain_id": owner.get("primary_location_id"), "current_domain_year": 2026,
            "historical_domain_state": "UNKNOWN" if scene_year != 2026 else "CURRENT_2026",
            "proven_historical_team_ids": sorted(permitted_team_ids),
            "character_matchups": factual, "other_public_matchups": unresolved,
            "evidence_cutoff": [scene_year, scene_week], "historical_owner_identity_unknown": not bool(proven) and scene_year < 2026,
            "memory_mutation": False, "draft_canon_status": "NO_CANON_PROMOTION"}
