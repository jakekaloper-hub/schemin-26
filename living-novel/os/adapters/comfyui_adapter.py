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
    return {
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

def main(path: str) -> None:
    job = json.loads(Path(path).read_text())
    print(json.dumps(compile_job(job), indent=2))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
