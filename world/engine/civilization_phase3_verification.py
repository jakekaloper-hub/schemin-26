"""Deterministic evidence-backed production preflight, not a manuscript publisher."""
from __future__ import annotations
import hashlib
from pathlib import Path
from world.engine.civilization_phase2_handoff import build_phase2_handoff

ROOT=Path(__file__).resolve().parents[2]
FACT=ROOT/"memo-os/week-3/WEEK_3_FACT_LOCK_V1.md"
NOVEL=ROOT/"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"


def verify_week3_recap_context(location_id: str = "LOC-LEAGUE-CHAMBER") -> dict:
    """Use an existing institutional site only as a proposed recap location, not game venue."""
    fact=FACT.read_text(encoding="utf-8")
    exact="ObiWan Jacoby 136.73 def Three Dreaded Snake 114.50."
    if exact not in fact:
        return {"ok":False,"code":"VERIFIED_FACT_NOT_FOUND"}
    packet=build_phase2_handoff(location_id,2026,3)
    if not packet.get("ok"):
        return {"ok":False,"code":"LOCATION_HANDOFF_FAILED","detail":packet}
    novel_text=NOVEL.read_text(encoding="utf-8")
    if not novel_text.strip():
        return {"ok":False,"code":"MANUSCRIPT_MISSING"}
    shared=packet["shared_context_id"]
    return {
        "ok":True,
        "source_event":{"season":2026,"week":3,"winner":"ObiWan Jacoby","loser":"Three Dreaded Snake",
                        "winner_score":"136.73","loser_score":"114.50",
                        "fact_lock_path":str(FACT.relative_to(ROOT)),
                        "fact_lock_sha256":hashlib.sha256(FACT.read_bytes()).hexdigest()},
        "scene_context":{"location_id":location_id,"context_id":shared,
                         "site_role":"PROPOSED_INSTITUTIONAL_RECAP_SETTING_NOT_MATCH_VENUE",
                         "memo_packet":packet["memo_location_packet"],
                         "novel_packet":packet["novel_location_packet"],
                         "visual_packet":packet["visual_world_packet"],
                         "seasonal_overlay":packet["seasonal_division_overlay"]},
        "existing_manuscript":{"path":str(NOVEL.relative_to(ROOT)),
                               "sha256":hashlib.sha256(NOVEL.read_bytes()).hexdigest(),
                               "status":"READ_ONLY_EXISTING_MANUSCRIPT"},
        "publication_eligible":False,
        "blockers":["ACTIVE_MEMO_PUBLICATION_RUNNER_UNVERIFIED",
                    "ACTIVE_NOVEL_MANUSCRIPT_COMPILER_UNVERIFIED",
                    "CHARACTER_SOURCE_BYTES_AND_RENDER_MOUNT_NOT_VERIFIED",
                    "SCENE_SETTING_NOT_EDITORIALLY_APPROVED",
                    "INDEPENDENT_UMPIRE_NOT_ATTESTED"],
        "verification_kind":"REAL_EXISTING_ADAPTER_EXECUTION_NOT_END_TO_END_PUBLICATION",
    }
