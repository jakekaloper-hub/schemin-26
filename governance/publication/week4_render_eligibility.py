#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTH = ROOT / "canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"
SPEC = ROOT / "canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md"
RELEASE = ROOT / "governance/release-evidence/registry.json"
CHAR_MATRIX = ROOT / "memo-os/week-4/publication-readiness/WEEK_04_12_CHARACTER_AUTHORITY_MATRIX.json"
STORY_AUTHORITY = ROOT / "memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json"

def load(path):
    return json.loads(Path(path).read_text())

def unresolved_character_production_blockers():
    reg = load(RELEASE)
    rows = [r for r in reg.get("receipts", []) if r.get("system_id") == "character-production" and r.get("result") == "BLOCKED"]
    return rows[-1].get("unresolved_blockers", []) if rows else []

def character_matrix():
    doc = load(CHAR_MATRIX)
    return {row["character_id"]: row for row in doc.get("characters", [])}

def story_authority_matrix():
    doc = load(STORY_AUTHORITY)
    return doc, {row["story_unit_id"]: row for row in doc.get("story_units", [])}

def dk_authority_valid():
    doc = load(AUTH)
    row = next((x for x in doc.get("master_lineup", {}).get("stale_for", []) if x.get("character_id") == "CHAR-WILSON-LOOK"), None)
    if not row:
        return False
    text = (str(row.get("canonical_architecture", "")) + "\n" + SPEC.read_text()).upper()
    return all(x in text for x in ["ONE BODY", "GORILLA", "FOUR-LEGGED", "ARSENAL"])

def render_eligibility(packet: dict) -> dict:
    required = [
      "page_id","page_number","page_function","narrative_purpose","story_beat",
      "fact_dependencies","character_ids","character_authority_refs","exact_reference_assets",
      "world_state_ref","venue_ref","geography_ref","composition","foreground","midground","background",
      "text_hierarchy","headline","copy_fields","deterministic_data_fields","visual_objects",
      "negative_constraints","drift_risks","rejection_conditions","mobile_readability_requirements",
      "previous_page","next_page","status",
      "story_authority_id","story_authority_hash","story_authority_receipt","story_authority_state"
    ]
    missing = [k for k in required if k not in packet]
    if missing:
        return {"state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_INVALID","missing":missing}

    story_doc, stories = story_authority_matrix()
    sid = packet.get("story_authority_id")
    current = stories.get(sid)
    if not current:
        return {"state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_STALE","detail":"STORY_AUTHORITY_ID_UNKNOWN"}
    if packet.get("story_authority_state") != "CURRENT":
        return {"state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_STALE","detail":"STORY_AUTHORITY_STATE_NOT_CURRENT"}
    if packet.get("story_authority_hash") != current.get("story_authority_hash"):
        return {
          "state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_STALE",
          "detail":"STORY_AUTHORITY_HASH_MISMATCH",
          "expected":current.get("story_authority_hash"),
          "supplied":packet.get("story_authority_hash")
        }
    expected_receipt = "memo-os/week-4/publication-readiness/WEEK_04_STORY_AUTHORITY_REGISTER.json"
    if packet.get("story_authority_receipt") != expected_receipt:
        return {"state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_STALE","detail":"STORY_AUTHORITY_RECEIPT_INVALID"}
    if current.get("status") != "CURRENT":
        return {"state":"PAGE_RENDER_BLOCKED","reason":"PAGE_PACKET_STALE","detail":"STORY_AUTHORITY_NOT_CURRENT"}

    chars = packet.get("character_ids") or []
    matrix = character_matrix()
    unregistered = [cid for cid in chars if cid not in matrix]
    if unregistered:
        return {"state":"PAGE_RENDER_BLOCKED","reason":"CHARACTER_AUTHORITY_UNREGISTERED","characters":unregistered}

    if "CHAR-WILSON-LOOK" in chars and not dk_authority_valid():
        return {"state":"PAGE_RENDER_BLOCKED","reason":"CHARACTER_AUTHORITY_FAIL","character_id":"CHAR-WILSON-LOOK"}

    if chars:
        assets = packet.get("exact_reference_assets") or []
        by_id = {x.get("character_id"): x for x in assets if isinstance(x, dict)}
        absent = [cid for cid in chars if cid not in by_id]
        if absent:
            return {"state":"PAGE_RENDER_BLOCKED","reason":"CHARACTER_REFERENCE_MISSING","characters":absent}

        mismatched = []
        for cid in chars:
            expected = matrix[cid]["expected_sha256"]
            supplied = by_id[cid].get("expected_sha256")
            if supplied != expected:
                mismatched.append({"character_id":cid,"expected_sha256":expected,"supplied_sha256":supplied})
        if mismatched:
            return {"state":"PAGE_RENDER_BLOCKED","reason":"CHARACTER_REFERENCE_HASH_MISMATCH","mismatches":mismatched}

        if "CHAR-PHILLIP-PITTS" in chars:
            continuity = packet.get("character_continuity", {})
            tds = continuity.get("CHAR-PHILLIP-PITTS") if isinstance(continuity, dict) else None
            if not tds:
                return {"state":"PAGE_RENDER_BLOCKED","reason":"CHARACTER_CONTINUITY_UNRESOLVED","character_id":"CHAR-PHILLIP-PITTS"}

        blockers = unresolved_character_production_blockers()
        if blockers:
            return {
              "state":"PAGE_RENDER_BLOCKED",
              "reason":"GENERATION_BLOCKED_PROVIDER_CAPABILITY_UNPROVEN",
              "external_blockers":blockers
            }

    if packet.get("status") not in {"PAGE_RENDER_ELIGIBLE","RENDERED","PAGE_LOCKED"}:
        return {"state":"PAGE_RENDER_BLOCKED","reason":"UPSTREAM_PACKET_NOT_ELIGIBLE"}

    if story_doc.get("generation_state") != "PASS_TO_PRODUCTION":
        return {
          "state":"PAGE_RENDER_BLOCKED",
          "reason":"STORY_AUTHORITY_GENERATION_HOLD",
          "generation_state":story_doc.get("generation_state")
        }

    return {"state":"PAGE_RENDER_ELIGIBLE","page_id":packet["page_id"]}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("packet")
    args = p.parse_args()
    result = render_eligibility(load(Path(args.packet)))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["state"] == "PAGE_RENDER_ELIGIBLE" else 2)
