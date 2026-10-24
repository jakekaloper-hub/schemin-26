"""Build Bullpen-contract memory entries from Novel evidence without mutating the store."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

def export_memories(packet: dict[str,Any], *, observed_at: str, owner: str = "Schemin Novel OS") -> list[dict]:
    datetime.fromisoformat(observed_at.replace("Z","+00:00"))
    if not owner: raise ValueError("owner required")
    scope="schemin-26"
    result=[]
    for item in packet.get("world_memory_events_as_of_scene",[]):
        if item.get("status")!="WORLD_SOURCE_RECORD_NOT_CHARACTER_PERSONAL_KNOWLEDGE":
            continue
        if not item.get("source"):
            continue
        result.append({"id":f"novel-world-{item['id']}","key":f"world-event:{item['id']}",
            "scope":scope,"source":item["source"],"owner":owner,"observed_at":observed_at,
            "confidence":1.0,"supersedes":[],
            "status":"active","value":{"event_id":item["id"],"season":item["season"],
            "week":item["week"],"location_id":item.get("location_id"),"classification":"WORLD_EVENT_NOT_PERSONAL_MEMORY"}})
    return result
