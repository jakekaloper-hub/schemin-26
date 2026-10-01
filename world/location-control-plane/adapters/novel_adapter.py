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
    return packet
