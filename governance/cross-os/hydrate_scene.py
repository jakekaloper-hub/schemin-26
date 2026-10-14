"""Read-only cross-OS scene hydration using EXISTING location adapters.

Produces an evidence packet for editors and renderers, never publication approval.
No fabricated source references: caller must supply authenticated evidence refs.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
LCP=ROOT/"world/location-control-plane"

def _load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

MEMO=_load("memo_adapter_xos",LCP/"adapters/memo_adapter.py")
NOVEL=_load("novel_adapter_xos",LCP/"adapters/novel_adapter.py")
CORE=_load("location_compiler_xos",LCP/"compiler/location_control_plane.py")


def hydrate_scene(scene):
    required=("scene_id","verified_event_ref","source_timestamp","character_id",
              "character_source_ref","location_id","world_state_ref")
    if not isinstance(scene,dict) or any(not isinstance(scene.get(k),str) or not scene[k].strip() for k in required):
        return {"status":"BLOCKED","reason":"MISSING_SCENE_SOURCE_EVIDENCE"}
    if scene.get("private_mercer_data") or scene.get("world_mutation") or scene.get("art_claims_canon"):
        return {"status":"BLOCKED","reason":"UNAUTHORIZED_CROSS_OS_WRITE"}
    character=scene["character_id"]
    lid=scene["location_id"]
    memo=MEMO.compile_memo_location_packet(lid,[character],event_class=scene.get("event_class","REGULAR"))
    novel=NOVEL.compile_novel_location_packet(lid,[character],event_class=scene.get("event_class","NON_MATCHUP"))
    visual=CORE.compile_world_packet(lid,[character],"VISUAL",
             event_class=scene.get("event_class","REGULAR"),
             reference_requirement=scene.get("reference_requirement","SEMANTIC"))
    packets={"memo_os":memo,"novel_os":novel,"visual_grounding":visual}
    statuses={name:pack.get("status") for name,pack in packets.items()}
    acceptable={"memo_os":{"READY_FOR_SEMANTIC_QA"},"novel_os":{"READY_FOR_SEMANTIC_QA"},
                "visual_grounding":{"READY_FOR_RENDER"}}
    if any(statuses[key] not in acceptable[key] for key in packets):
        return {"status":"BLOCKED","reason":"AUTHORITATIVE_LOCATION_HYDRATION_NOT_READY",
                "consumer_statuses":statuses,"packets":packets}
    shared={k:scene[k] for k in required}
    # Interactive Atlas is a derived read-only lookup, not a fabricated write adapter.
    atlas_location=CORE.resolve_location(lid)
    if atlas_location.get("status")!="CURRENT_LOCATION_RESOLVED":
        return {"status":"BLOCKED","reason":"ATLAS_LOCATION_UNRESOLVED"}
    views={}
    for consumer in ("memo_os","novel_os","visual_grounding","interactive_atlas"):
        views[consumer]={
            **{k:scene[k] for k in ("character_id","location_id","world_state_ref","verified_event_ref")},
            "narrative_purpose":(scene.get("narrative_purpose_by_consumer") or {}).get(consumer,
                "Consumer-specific creative treatment required before production")
        }
    return {
        "status":"HYDRATED_FOR_EDITORIAL_REVIEW_NOT_RENDER_APPROVED",
        "scene_id":scene["scene_id"],"shared":shared,"views":views,
        "consumer_statuses":statuses,"packets":packets,
        "atlas_location":atlas_location["location"],"read_only":True,
        "render_release_authorized":False,
        "unverified_claims":["character_source_ref must be separately hash/mount verified",
             "source event freshness is caller assertion until Scout evidence checked",
             "world_state_ref requires temporal/version proof",
             "Umpire visual review pending"]
    }


if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path)
    args=ap.parse_args()
    result=hydrate_scene(json.loads(args.source.read_text()))
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["status"].startswith("HYDRATED_") else 1)
