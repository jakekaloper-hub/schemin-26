"""Novel OS ComfyUI renderer adapter v1.
Compiles a renderer-neutral NovelVisualJob into a ComfyUI API workflow envelope.
This module does not own canon or approve outputs.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

REQUIRED = {
    "schema","job_id","beat_id","manuscript_anchor","composition_map",
    "reference_assets","object_locks","character_locks","environment_packet",
    "camera_spec","lighting_spec","negative_constraints",
    "continuity_predecessors","output","seed_policy","qa_contract"
}

def validate_job(job: dict[str, Any]) -> None:
    missing = sorted(REQUIRED - set(job))
    if missing:
        raise ValueError(f"NovelVisualJob missing required fields: {missing}")
    if job["schema"] != "NovelVisualJob/v1":
        raise ValueError("Unsupported NovelVisualJob schema")
    out = job["output"]
    if not all(k in out for k in ("width","height","format")):
        raise ValueError("output requires width, height, format")

def compile_job(job: dict[str, Any]) -> dict[str, Any]:
    """Create a portable workflow specification.

    Node IDs/model bindings remain deployment configuration. This deliberately
    avoids hard-coding a checkpoint or GPU provider into Novel OS.
    """
    validate_job(job)
    character_visual = None
    character_locks = job["character_locks"]
    if character_locks:
        # Existing renderer adapter is the final canonical scene-compilation
        # boundary. Fail before generating a provider graph if visual subjects
        # or geography cannot be proven from current owner IDs / world canon.
        if not isinstance(character_locks, list) or any(
            not isinstance(lock, dict) or not lock.get("character_id")
            for lock in character_locks
        ):
            raise ValueError("Character-bearing NovelVisualJob must declare immutable character_id locks")
        ids=[lock["character_id"] for lock in character_locks]
        if len(ids)!=len(set(ids)):
            raise ValueError("Character-bearing NovelVisualJob duplicates a character_id")
        environment = job["environment_packet"]
        if not isinstance(environment, dict) or not environment.get("location_id"):
            raise ValueError("Character-bearing NovelVisualJob requires active location_id")
        import sys
        root=Path(__file__).resolve().parents[3]
        adapter_path=root/"world/location-control-plane/adapters"
        if str(root) not in sys.path:sys.path.insert(0,str(root))
        if str(adapter_path) not in sys.path:sys.path.insert(0,str(adapter_path))
        from novel_adapter import compile_novel_location_packet
        packet=compile_novel_location_packet(environment["location_id"],ids)
        visual=packet.get("character_visual_authority",{})
        if (packet.get("status")!="READY_FOR_SEMANTIC_QA"
            or visual.get("state")!="COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE"):
            raise ValueError("Character-bearing NovelVisualJob has unresolved character, physical or spatial canon")
        character_visual = {
            "state":"COMMISSIONER_APPROVED_APPEARANCE_CONTEXT__PROVIDER_HOLD",
            "current_visual_authority": visual,
            "physical_constraints":packet["character_physical_constraints"],
            "spatial_anchors":packet["character_spatial_anchors"],
            "source_and_subject_binding_verified":False,
            "image_generation_eligible":False,
            "t15":"HOLD","t16":"HOLD",
        }
    result = {
        "adapter": "novel-os-comfyui/v1",
        "job_id": job["job_id"],
        "engine": "ComfyUI",
        "state": "COMPILED_UNRENDERED",
        "controls": {
            "composition_map": job["composition_map"],
            "references": job["reference_assets"],
            "object_locks": job["object_locks"],
            "character_locks": job["character_locks"],
            "environment_packet": job["environment_packet"],
            "camera": job["camera_spec"],
            "lighting": job["lighting_spec"],
            "negative_constraints": job["negative_constraints"],
        },
        "output": job["output"],
        "seed_policy": job["seed_policy"],
        "qa_contract": job["qa_contract"],
        "comfyui_graph_requirements": [
            "load approved reference image(s)",
            "derive or load structural composition control",
            "bind reference/style conditioning",
            "bind depth/edge/layout control where available",
            "apply object/region constraints",
            "sample with recorded seed",
            "decode/save image with workflow metadata",
        ],
    }
    if character_visual is not None:
        result["controls"]["approved_character_visual_context"] = character_visual
        result["state"] = "COMPILED_UNRENDERED_CHARACTER_PROVIDER_QA_HOLD"
    return result

def main(path: str) -> None:
    job = json.loads(Path(path).read_text())
    print(json.dumps(compile_job(job), indent=2))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
