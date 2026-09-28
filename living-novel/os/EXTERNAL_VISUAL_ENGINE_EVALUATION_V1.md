# EXTERNAL VISUAL ENGINE EVALUATION V1
**Decision:** SELECT COMFYUI AS PRIMARY RENDER-ORCHESTRATION ADAPTER TARGET
**Date:** 2026-09-27
**Scope:** Novel OS renderer-neutral external pixel production
## Requirements
Reference-image conditioning; img2img; structural composition control; ControlNet/depth/edge; masks/inpainting; IP-Adapter/equivalent; multi-reference; deterministic seeds; persistent/serializable workflows; model interchangeability; high-resolution path; local/cloud portability; API automation; reproducibility; provenance.
## Candidates
### ComfyUI — SELECTED
Mature graph/workflow architecture designed to serialize generation pipelines and compose model/control nodes. It is the best boundary for Novel OS because a NovelVisualJob can compile into a workflow graph rather than a monolithic prompt. Model/control capability can be supplied by the broad ComfyUI ecosystem and underlying diffusion implementations. Renderer hardware remains replaceable.
### Hugging Face Diffusers — CAPABILITY LAYER / FALLBACK
Excellent programmable primitives. Current upstream documentation supports IP-Adapter reference images, multiple IP-Adapters and masks, ControlNet structural conditioning including depth/edges, img2img/inpainting, and seeded torch generators. Strong lower-level backend but requires Novel OS to own more orchestration code than ComfyUI.
### SwarmUI — NOT PRIMARY
Useful higher-level UI/orchestration surface, but its documented ControlNet support is provided through the ComfyUI backend. This adds an extra layer without improving the Novel OS adapter boundary.
### InvokeAI — NOT SELECTED FOR V1
Capable production application, but Novel OS benefits more from a renderer graph as the direct contract boundary. Keep as future adapter candidate; do not bind V1 to it.
## Selection rationale
Novel OS needs control graphs, not another creative authority. ComfyUI maps composition/reference/object/control requirements into inspectable nodes and preserves workflow provenance. Diffusers provides independently documented primitives underneath/alongside that strategy.
## Architecture
Novel OS → NovelVisualJob → ComfyUIAdapter → serialized workflow → external compute/backend → RenderResult → Novel OS QA.
## Compute
No dedicated GPU infrastructure is required by contract. Adapter transport may target local, hosted, or externally managed ComfyUI execution.
## Governance
External renderer has zero canon authority. A successful HTTP/render job is not an approved illustration. Only Novel OS QA + Closer can promote an output.
## S03 acceptance test
Compile S03 composition map + OBJ-2026-CLEAN-LEDGER lock + S01/S02 reference provenance + negatives into one NovelVisualJob. Use structural/reference nodes rather than prompt-only generation.
