"""Deterministic routing for the active Novel Author Consulting Program V2."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT.parent / "ADVISOR_REGISTRY_V1.json"

AUTHOR_ALIASES = {
    "jrr_tolkien": ("tolkien", "j.r.r. tolkien", "jrr tolkien"),
    "george_rr_martin": ("george r.r. martin", "george rr martin", "grrm", "martin"),
    "jk_rowling": ("j.k. rowling", "jk rowling", "rowling"),
    "john_grisham": ("john grisham", "grisham"),
    "ursula_k_le_guin": ("ursula k. le guin", "ursula le guin", "le guin", "leguin"),
    "brandon_sanderson": ("brandon sanderson", "sanderson"),
    "joe_abercrombie": ("joe abercrombie", "abercrombie"),
}

FULL_COUNCIL_TERMS = (
    "full seven",
    "full council",
    "author council",
    "all seven",
    "all consultants",
    "entire council",
)

FULL_COUNCIL_PROBLEMS = (
    "book architecture",
    "rewrite the book",
    "major rewrite",
    "narrator constitution",
    "week to chapter",
    "week→chapter",
    "new novel os doctrine",
)

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("’", "'")).strip()

def load_registry(path: str | Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def core_seven(registry: dict[str, Any] | None = None) -> list[str]:
    registry = registry or load_registry()
    return list(registry["author_council"]["core_seven"])

def _dedupe(ids: list[str]) -> list[str]:
    out = []
    seen = set()
    for advisor_id in ids:
        if advisor_id not in seen:
            out.append(advisor_id)
            seen.add(advisor_id)
    return out

def select_consultants(command: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = registry or load_registry()
    council = registry["author_council"]
    panels = council["panels"]
    panel_aliases = council["panel_aliases"]
    text = _norm(command)

    explicit = []
    for advisor_id, aliases in AUTHOR_ALIASES.items():
        if any(alias in text for alias in aliases):
            explicit.append(advisor_id)
    if explicit:
        return {
            "consultation_type": "TARGETED_PANEL",
            "selection_mode": "EXPLICIT_AUTHORS",
            "panel": None,
            "advisors": _dedupe(explicit),
            "reason": "Explicit named-author request.",
        }

    if any(term in text for term in FULL_COUNCIL_TERMS) or any(term in text for term in FULL_COUNCIL_PROBLEMS):
        return {
            "consultation_type": "FULL_COUNCIL",
            "selection_mode": "FULL_COUNCIL_TRIGGER",
            "panel": "full_seven",
            "advisors": core_seven(registry),
            "reason": "Cross-cutting or explicit full-council request.",
        }

    for panel, aliases in panel_aliases.items():
        if any(alias in text for alias in aliases):
            return {
                "consultation_type": "TARGETED_PANEL",
                "selection_mode": "NAMED_PANEL",
                "panel": panel,
                "advisors": list(panels[panel]),
                "reason": f"Matched canonical {panel} panel.",
            }

    problem_rules = [
        (("pov", "viewpoint", "narrative distance", "voice"), "pov_character"),
        (("pacing", "slow", "drag", "page turn", "chapter ending", "chapter opening"), "pacing_readability"),
        (("worldbuilding", "world depth", "history", "culture", "geography"), "world_depth"),
        (("chapter architecture", "ensemble", "structure", "chapter order", "recap"), "story_architecture"),
        (("rules", "system", "magic", "contest mechanics", "limitations"), "fantasy_logic"),
        (("battle", "action", "epic action", "spectacle"), "epic_fantasy_integrity"),
    ]
    for terms, panel in problem_rules:
        if any(term in text for term in terms):
            return {
                "consultation_type": "TARGETED_PANEL",
                "selection_mode": "PROBLEM_ROUTING",
                "panel": panel,
                "advisors": list(panels[panel]),
                "reason": f"Problem routed to canonical {panel} panel.",
            }

    return {
        "consultation_type": "TARGETED_PANEL",
        "selection_mode": "DEFAULT_CHAPTER_TRIAGE",
        "panel": council["default_panel"],
        "advisors": list(panels[council["default_panel"]]),
        "reason": "No narrower signal found; use smallest general literary triage panel.",
    }

def build_engagement_manifest(
    command: str,
    *,
    engagement_id: str,
    evidence_commit_sha: str,
    temporal_cutoff: str,
    decision_question: str,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selection = select_consultants(command, registry=registry)
    return {
        "version": "1.0",
        "status": "FROZEN",
        "engagement_id": engagement_id,
        "evidence_cutoff": {
            "commit_sha": evidence_commit_sha,
            "temporal_cutoff": temporal_cutoff,
        },
        "decision_question": decision_question,
        "consultation_type": selection["consultation_type"],
        "selection_mode": selection["selection_mode"],
        "panel": selection["panel"],
        "selected_consultants": selection["advisors"],
        "selection_reason": selection["reason"],
        "independence": {
            "same_internal_evidence": True,
            "cross_reading_before_lock": False,
            "source_provenance_required": True,
        },
        "rounds": [
            {"round": 1, "purpose": "diagnostic"},
            {"round": 2, "purpose": "deep_dive_after_implementation"},
            {"round": 3, "purpose": "adversarial_re_review"},
            {"round": 4, "purpose": "final_synthesis"},
        ],
    }

def validate_engagement_manifest(manifest: dict[str, Any], registry: dict[str, Any] | None = None) -> list[str]:
    registry = registry or load_registry()
    valid_ids = {a["id"] for a in registry["advisors"]}
    errors = []
    if manifest.get("status") != "FROZEN":
        errors.append("ENGAGEMENT_NOT_FROZEN")
    cutoff = manifest.get("evidence_cutoff") or {}
    if not cutoff.get("commit_sha"):
        errors.append("MISSING_EVIDENCE_COMMIT")
    if not cutoff.get("temporal_cutoff"):
        errors.append("MISSING_TEMPORAL_CUTOFF")
    if not manifest.get("decision_question"):
        errors.append("MISSING_DECISION_QUESTION")
    selected = manifest.get("selected_consultants") or []
    if not selected:
        errors.append("NO_CONSULTANTS_SELECTED")
    unknown = [advisor_id for advisor_id in selected if advisor_id not in valid_ids]
    if unknown:
        errors.append("UNKNOWN_CONSULTANT:" + ",".join(sorted(unknown)))
    if manifest.get("consultation_type") == "FULL_COUNCIL" and selected != core_seven(registry):
        errors.append("FULL_COUNCIL_NOT_CORE_SEVEN")
    independence = manifest.get("independence") or {}
    if independence.get("cross_reading_before_lock") is not False:
        errors.append("INDEPENDENCE_VIOLATION")
    return errors
