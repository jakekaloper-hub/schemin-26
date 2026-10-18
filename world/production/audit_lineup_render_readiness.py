#!/usr/bin/env python3
"""G4 semantic canary audit on *actual* existing Memo/Novel world adapters.

This does not submit any image request: renderer_capabilities_v1 explicitly
does not expose a verified native reference/subject binding route. Any audit
that claims rendered raster QA from these packet checks is invalid.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
ADAPTERS=ROOT/"world/location-control-plane/adapters"
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
if str(ADAPTERS) not in sys.path:sys.path.insert(0,str(ADAPTERS))
from memo_adapter import compile_memo_location_packet
from novel_adapter import compile_novel_location_packet
from world.production.build_visual_world_packet import build_packet

def audit():
    registry=json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]
    owners={x["character_id"]:x for x in registry}
    lineup=json.loads((ROOT/"canon/characters/APPROVED_LINEUP_2026_10_18.json").read_text())
    capability=json.loads((ROOT/"canon/characters/renderer_capabilities_v1.json").read_text())
    route=capability["routes"]["CURRENT_CHATGPT_IMAGE_RENDERER"]
    assert route["production_state"]=="PROVIDER_CAPABILITY_BLOCKED", "Re-assess route; do not use stale block claim"
    assert not route["returns_mounted_byte_hash_receipt"]
    assert not route["returns_subject_binding_receipt"]
    assert len(owners)==12
    mapping={
        "A_DK_SINGLE":["CHAR-WILSON-LOOK"],
        "B_HMB_SINGLE":["CHAR-AUSTIN-BYARS"],
        "C_OBIWAN_COMPANION":["CHAR-JAKE-KALOPER"],
        "D_TDS_THREE_HEAD":["CHAR-PHILLIP-PITTS"],
    }
    canaries=[]
    for name,ids in mapping.items():
        primary=owners[ids[0]]["primary_location_id"]
        memo=compile_memo_location_packet(primary,ids)
        novel=compile_novel_location_packet(primary,ids)
        canaries.append({
            "id":name,"character_ids":ids,"location_id":primary,
            "memo_status":memo["status"],"novel_status":novel["status"],
            "visual_lineup_sha256":memo["character_visual_authority"]["master_lineup_sha256"],
            "physics_present":bool(memo["character_physical_constraints"][ids[0]]["anatomy_constraints"]),
            "spatial_present":bool(novel["character_spatial_anchors"][ids[0]]["home_location_id"]),
            "reference_provider_mount_verified":False,
            "generated_artwork":"NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN",
            "output_instance_visual_QA":"NOT_PERFORMED",
        })
    roster=[]
    for cid,o in owners.items():
        pkt=compile_memo_location_packet(o["primary_location_id"],[cid])
        assert pkt["status"]=="READY_FOR_SEMANTIC_QA"
        assert pkt["character_rendering_eligible"] is False
        roster.append(cid)
    canaries.append({
        "id":"E_TWELVE_SEPARATE_CHARACTER_PACKETS",
        "characters_resolved":len(roster),"character_ids":sorted(roster),
        "source_binding":"UNPROVEN",
        "generated_artwork":"NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN",
    })
    all_ids=sorted(owners)
    multi=compile_novel_location_packet("LOC-LEAGUE-CHAMBER",all_ids)
    canaries.append({
        "id":"F_MULTI_CHARACTER_SCENE",
        "character_ids":all_ids,"location_id":"LOC-LEAGUE-CHAMBER",
        "semantic_status":multi["status"],
        "visual_subject_count":len(multi.get("character_visual_authority",{}).get("subjects",[])),
        "image_generation_eligible":multi.get("character_rendering_eligible",False),
        "generated_artwork":"NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN",
    })
    matchup=["CHAR-KEVIN-ZEEK","CHAR-WILSON-LOOK"]
    memo=compile_memo_location_packet("LOC-RED-RUINS",matchup)
    world=build_packet("LOC-RED-RUINS")
    canaries.append({
        "id":"G_RED_LEOPARDS_HOST_DK_MATCHUP",
        "character_ids":matchup,
        "existing_venue_id":"LOC-RED-RUINS",
        "memo_semantic_status":memo["status"],
        "memo_visual_subjects":len(memo.get("character_visual_authority",{}).get("subjects",[])),
        "world_packet_home_character_ids":world["character"]["principal_character_ids"],
        "geography_new_or_invented":False,
        "generated_artwork":"NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN",
        "output_identity_QA":"NOT_PERFORMED",
    })
    assert len(canaries)==7
    assert all(x.get("generated_artwork")=="NOT_SUBMITTED__PROVIDER_SUBJECT_BINDING_UNPROVEN" for x in canaries)
    return {
        "schema_version":"1.0",
        "date":"2026-10-18",
        "approved_master_sha256":lineup["sha256"],
        "run_type":"REAL_MEMO_NOVEL_ADAPTER_INVOCATION_AND_SOURCE_CAPABILITY_PREFLIGHT",
        "live_image_generation_calls":0,
        "actual_generated_output_count":0,
        "provider_route":"CURRENT_CHATGPT_IMAGE_RENDERER",
        "provider_status":route["production_state"],
        "mounted_byte_hash_receipts_available":False,
        "subject_binding_receipts_available":False,
        "semantic_canary_count":len(canaries),
        "production_character_image_eligible":False,
        "independent_umpire_C1":"HOLD",
        "t15":"HOLD","t16":"HOLD",
        "canaries":canaries,
    }

if __name__=="__main__":
    print(json.dumps(audit(),indent=2))
