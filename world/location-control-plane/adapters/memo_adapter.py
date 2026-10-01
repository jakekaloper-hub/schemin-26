#!/usr/bin/env python3
from pathlib import Path
import sys
COMPILER = Path(__file__).resolve().parents[1] / "compiler"
sys.path.insert(0, str(COMPILER))
from location_control_plane import compile_world_packet

def compile_memo_location_packet(location_id, character_ids=None, event_class="REGULAR", sublocation_handle=None, home_character_id=None):
    packet=compile_world_packet(location_id,character_ids or [],"MEMO",event_class,sublocation_handle,home_character_id,False)
    if packet.get("status") in {"READY_FOR_SEMANTIC_QA","READY_FOR_RENDER"}:
        packet["memo_adapter"]={
            "venue_lock_required":True,
            "world_state_lock_required":True,
            "post_release_writeback":"Scout/Librarian/Architect classification required for any new evidence."
        }
    return packet
