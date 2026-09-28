# VISUAL RENDERER ADAPTER CONTRACT V1
**Status:** BINDING / RENDERER-NEUTRAL
## NovelVisualJob
Required fields:
- job_id
- beat_id
- manuscript_anchor
- composition_map
- reference_assets[] {id, role, provenance, approval_state, weight?}
- object_locks[]
- character_locks[]
- environment_packet
- camera_spec
- lighting_spec
- negative_constraints[]
- continuity_predecessors[]
- text_safe_regions[]
- output {width,height,format}
- seed_policy {mode,fixed_seed?}
- qa_contract
## RendererAdapter
`compile(job) -> RendererWorkflow`
`render(workflow) -> RenderResult`
The adapter may translate controls/models but may not change beat truth, canon locks, or QA criteria.
## RendererWorkflow
Must record adapter version, engine, model/checkpoint identifiers, control modules, reference bindings, masks/depth/edge inputs, generation parameters, seed and serialized native workflow payload.
## RenderResult
- image artifact/URI
- job_id
- engine/model/workflow identifiers
- seed
- reference provenance
- generation metadata
- execution timestamp/status
## Authority
RenderResult state begins RENDERED_UNAPPROVED. Novel OS Visual QA + Continuity QA + Closer may promote to APPROVED.
## Failure semantics
Transport/model failure = IMPLEMENTATION FAILURE.
Canon/reference deficiency = CREATIVE BLOCKER.
QA rejection = RENDER FAILURE requiring diagnosis.
Two materially similar QA failures trigger the Novel OS repeated-generation escape rule.
