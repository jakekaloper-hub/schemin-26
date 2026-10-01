#!/usr/bin/env python3
"""Validate the Schemin '26 canonical project mission contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISSION = ROOT / "SCHEMIN_26_PROJECT_MISSION.md"
CONTRACT = ROOT / "governance" / "SCHEMIN_26_PROJECT_MISSION_CONTRACT.json"
REGISTRY = ROOT / "PROJECT_CONTROL_REGISTRY.md"
README = ROOT / "README.md"

EXPECTED_LOOP = [
    "REAL_FANTASY_FOOTBALL_EVENT",
    "VERIFIED_LEAGUE_EVIDENCE",
    "CHARACTER_CONSEQUENCE",
    "WORLD_TRANSLATION",
    "STORY_ARCHITECTURE",
    "WEEKLY_MEMO_PUBLICATION",
    "LIVING_NOVEL_NARRATIVE",
    "SHARED_VISUAL_PRODUCTION",
    "GOVERNED_WORLD_STATE_EVOLUTION",
    "FUTURE_CONTINUITY",
]

EXPECTED_SURFACES = {
    "WEEKLY_MEMO",
    "LIVING_NOVEL",
    "UNIVERSE_ATLAS",
    "VISUAL_SYSTEM",
}


def validate() -> list[str]:
    errors: list[str] = []

    for path in (MISSION, CONTRACT, REGISTRY, README):
        if not path.exists():
            errors.append(f"missing required mission authority file: {path.relative_to(ROOT)}")
    if errors:
        return errors

    mission = MISSION.read_text(encoding="utf-8")
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    registry = REGISTRY.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    if payload.get("status") != "CANONICAL_NORTH_STAR":
        errors.append("mission contract status must be CANONICAL_NORTH_STAR")
    if payload.get("operating_loop") != EXPECTED_LOOP:
        errors.append("mission operating loop drifted")
    if set(payload.get("publication_surfaces", [])) != EXPECTED_SURFACES:
        errors.append("publication surface coverage drifted")

    laws = payload.get("laws", {})
    required_true = [
        "one_persistent_fictional_reality",
        "cross_surface_contradiction_is_failure",
        "future_continuity_required",
        "real_league_events_drive_story",
    ]
    for key in required_true:
        if laws.get(key) is not True:
            errors.append(f"mission law must remain true: {key}")
    if laws.get("weekly_reset_allowed") is not False:
        errors.append("weekly_reset_allowed must remain false")
    if laws.get("publication_surfaces_may_independently_rewrite_reality") is not False:
        errors.append("publication surfaces may not independently rewrite reality")

    required_phrases = [
        "Week 4 and every future week",
        "same persistent fictional reality",
        "Nothing resets merely because a new week begins.",
        "Locations remember.",
        "Characters remember.",
        "Institutions remember.",
        "Visual environments remember.",
        "week after week, season after season.",
    ]
    for phrase in required_phrases:
        if phrase not in mission:
            errors.append(f"mission text missing north-star phrase: {phrase}")

    if "SCHEMIN_26_PROJECT_MISSION.md" not in registry:
        errors.append("Project Control Registry does not reference canonical mission")
    if "SCHEMIN_26_PROJECT_MISSION.md" not in readme:
        errors.append("README does not route new work through canonical mission")

    return errors


if __name__ == "__main__":
    errs = validate()
    if errs:
        for err in errs:
            print(f"FAIL: {err}")
        raise SystemExit(1)
    print("PASS: Schemin '26 canonical project mission")
