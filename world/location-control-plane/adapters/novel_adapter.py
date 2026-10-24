#!/usr/bin/env python3
from pathlib import Path
import sys
COMPILER = Path(__file__).resolve().parents[1] / "compiler"
sys.path.insert(0, str(COMPILER))
from location_control_plane import compile_world_packet

def compile_novel_location_packet(location_id, character_ids=None, event_class="NON_MATCHUP", sublocation_handle=None, home_character_id=None):
    packet=compile_world_packet(location_id,character_ids or [],"NOVEL",event_class,sublocation_handle,home_character_id,False)
    if packet.get("status") in {"READY_FOR_SEMANTIC_QA","READY_FOR_RENDER"}:
        packet["novel_adapter"]={
            "hydration_required":True,
            "pov_knowledge_envelope_required":True,
            "ordinary_world_consequence_required_for_major_events":True
        }
    # Additive, read-only civilization context; never elevates semantic QA to publication.
    if packet.get("status") in {"READY_FOR_SEMANTIC_QA", "READY_FOR_RENDER"}:
        from pathlib import Path
        import sys
        root = Path(__file__).resolve().parents[3]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from world.engine.civilization_consumers import resolve_scene_context
        context = resolve_scene_context(location_id, "novel")
        if not context.get("ok"):
            packet["status"] = "HUMAN_REVIEW_REQUIRED"
            packet.setdefault("review_blockers", []).append("CIVILIZATION_CONTEXT_UNRESOLVED")
        else:
            packet["civilization_context"] = context
            packet["civilization_context_status"] = "INTERPRETIVE_NON_PROMOTING"
    return packet
