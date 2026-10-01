#!/usr/bin/env python3
"""Schemin '26 Location Control Plane V1.

Derived packet compiler only. Upstream world/character/data sources remain authoritative.
"""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LCP = ROOT / "world" / "location-control-plane"

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())

def _registry(name: str) -> dict[str, Any]:
    return load_json(LCP / "registries" / name)

def _card(path: str) -> dict[str, Any]:
    return load_json(ROOT / path)

def _candidate_ids() -> set[str]:
    p = load_json(ROOT / "world" / "data" / "atlas_location_candidates.json")
    return {x["id"] for x in p["candidates"]}

def _routes() -> list[dict[str, Any]]:
    return load_json(ROOT / "world" / "data" / "routes.json")["routes"]

def resolve_location(location_id: str) -> dict[str, Any]:
    if location_id in _candidate_ids() or location_id.startswith("CAND-"):
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"CANDIDATE_NOT_ACTIVE","query":location_id}
    reg = _registry("LOCATION_CARD_REGISTRY.json")
    row = next((x for x in reg["cards"] if x["location_id"] == location_id), None)
    if not row:
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_LOCATION","query":location_id}
    return {"status":"CURRENT_LOCATION_RESOLVED","location":_card(row["path"])}

def resolve_homeland(character_id: str) -> dict[str, Any]:
    reg = _registry("HOMELAND_CARD_REGISTRY.json")
    row = next((x for x in reg["cards"] if x["character_id"] == character_id), None)
    if not row:
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_CHARACTER_DOMAIN","query":character_id}
    return {"status":"CURRENT_HOMELAND_RESOLVED","homeland":_card(row["path"])}

def resolve_sublocation(handle_id: str) -> dict[str, Any]:
    reg = _registry("PARENT_SUBLOCATION_REGISTRY.json")
    row = next((x for x in reg["handles"] if x["handle_id"] == handle_id), None)
    if not row:
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_SUBLOCATION_HANDLE","query":handle_id}
    return {"status":"CURRENT_FEATURE_HANDLE_RESOLVED","handle":row}

def _graph() -> dict[str,set[str]]:
    g: dict[str,set[str]] = {}
    for r in _routes():
        pts = [r.get("from")] + list(r.get("via_location_ids", []))
        if r.get("via_location_id"):
            pts.append(r["via_location_id"])
        pts.append(r.get("to"))
        pts = [x for x in pts if x]
        for a,b in zip(pts,pts[1:]):
            g.setdefault(a,set()).add(b); g.setdefault(b,set()).add(a)
    return g

def path_exists(a: str, b: str) -> bool:
    if a == b: return True
    g=_graph(); q=deque([a]); seen={a}
    while q:
        cur=q.popleft()
        for nxt in g.get(cur,set()):
            if nxt == b: return True
            if nxt not in seen:
                seen.add(nxt); q.append(nxt)
    return False

def relationship(character_id: str, location: dict[str,Any]) -> dict[str,str]:
    h=resolve_homeland(character_id)
    if h["status"]!="CURRENT_HOMELAND_RESOLVED":
        return {"character_id":character_id,"relationship":"UNKNOWN_RELATIONSHIP"}
    home=h["homeland"]
    lid=location["location_id"]
    if lid == home["primary_location_id"]:
        rel="HOME_PRIMARY"
    elif lid in home.get("shared_location_ids",[]):
        rel="HOME_SHARED"
    elif character_id in location.get("owner_character_ids",[]):
        rel="HOME_ASSOCIATED"
    elif not location.get("owner_character_ids"):
        rel="NEUTRAL"
    elif path_exists(home["primary_location_id"],lid):
        rel="AWAY_REACHABLE"
    else:
        rel="UNKNOWN_RELATIONSHIP"
    return {"character_id":character_id,"relationship":rel}

def _consumer_overlay(consumer: str, character_ids: list[str]) -> dict[str,Any]:
    base={"consumer":consumer,"constraints":[]}
    if consumer=="MEMO":
        base["constraints"]=[
            "Venue/location must be resolved before art prompting.",
            "Visual metaphor may not mutate active geography.",
            "Current world state must persist."
        ]
    elif consumer=="NOVEL":
        base["constraints"]=[
            "Apply POV knowledge envelope.",
            "Memo visual shorthand is not automatically literal world fact.",
            "Travel and ordinary-life causality must be preserved."
        ]
        if "CHAR-MANNING-WELTY" in character_ids:
            base["constraints"].append("Living Novel El Niño overlay: atmospheric/mobile storm; no interior POV or dialogue.")
    elif consumer=="VISUAL":
        base["constraints"]=[
            "Camera/style variables cannot alter geography.",
            "Character visual references are resolved separately.",
            "Generated scenery cannot become canon."
        ]
    return base

def compile_world_packet(
    location_id: str,
    character_ids: list[str] | None = None,
    consumer: str = "MEMO",
    event_class: str = "REGULAR",
    sublocation_handle: str | None = None,
    home_character_id: str | None = None,
    require_visual_reference: bool = False,
) -> dict[str,Any]:
    if consumer not in {"MEMO","NOVEL","VISUAL"}:
        return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_CONSUMER"}
    rr=resolve_location(location_id)
    if rr["status"]!="CURRENT_LOCATION_RESOLVED":
        return rr
    loc=rr["location"]; characters=character_ids or []
    blockers=[]
    if sublocation_handle:
        sr=resolve_sublocation(sublocation_handle)
        if sr["status"]!="CURRENT_FEATURE_HANDLE_RESOLVED":
            return sr
        if sr["handle"]["parent_location_id"] != location_id:
            return {"status":"HUMAN_REVIEW_REQUIRED","reason":"SUBLOCATION_PARENT_MISMATCH"}
    rels=[relationship(cid,loc) for cid in characters]
    if any(x["relationship"]=="UNKNOWN_RELATIONSHIP" for x in rels):
        blockers.append("UNRESOLVED_CHARACTER_LOCATION_RELATIONSHIP")
    ref=loc["reference_status"]
    if require_visual_reference and ref["visual_reference_status"]!="APPROVED_VISUAL_REFERENCE":
        blockers.append("MISSING_APPROVED_VISUAL_REFERENCE")
    packet={
        "status":"HUMAN_REVIEW_REQUIRED" if blockers else "READY_FOR_SEMANTIC_QA",
        "consumer":consumer,
        "event_class":event_class,
        "home_character_id":home_character_id,
        "location":loc,
        "sublocation_handle":sublocation_handle,
        "relationships":rels,
        "consumer_overlay":_consumer_overlay(consumer,characters),
        "reference_status":ref,
        "open_questions":loc.get("open_questions",[]),
        "review_blockers":blockers,
        "prohibited_inventions":loc.get("prohibited_inventions",[]),
        "rule":"Packets compile authority; they do not create canon."
    }
    if consumer=="VISUAL" and not blockers and ref["visual_reference_status"]=="APPROVED_VISUAL_REFERENCE":
        packet["status"]="READY_FOR_RENDER"
    return packet
