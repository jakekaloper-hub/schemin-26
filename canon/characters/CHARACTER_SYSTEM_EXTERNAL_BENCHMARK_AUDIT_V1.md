# BULLPEN CHARACTER SYSTEM — EXTERNAL ARCHITECTURE BENCHMARK AUDIT
Date: 2026-09-29
Status: SENIOR-GRADE ARCHITECTURE REVIEW / REBUILD REQUIRED BEFORE ACTIVE

## External benchmark set
Reviewed mature public patterns rather than cloning a fantasy-character repository:
1. Pixar OpenUSD — composed scene/asset architecture, layered overrides, explicit references/payloads, variants and asset resolution.
2. Academy Software Foundation OpenTimelineIO — typed serialized schemas, external/missing media references, adapters/plugins, media linking, versioned schemas and media bundles.
3. Pydantic — canonical typed models, validation boundaries, serialization and generated JSON Schema.
4. python-jsonschema / JSON Schema — machine-verifiable schema contracts and explicit validation failures.
These are architecture analogues, not character-canon sources.

## What the rebuild gets right
Stable Character IDs separate from mutable team names; active vs superseded identity; owner-scoped packages/negative locks; references separated from semantic canon; deterministic resolver concept; render-contract stage; fail-closed QA vocabulary; subordinate consumers; POV separated from anatomy and evidence-classified.

## Senior-grade gaps
P0 — Runtime model is duplicated. CHARACTER_REGISTRY.yaml, package YAMLs, T04 specs, Master Canon prose and Python hard-coded REGISTRY repeat truth. Need one canonical typed data model; documents become generated/supplementary views.
P0 — Resolver embeds data instead of loading validated records. Alias collisions must fail at build/CI.
P0 — No formal schema/version migration layer. Add schema_version, typed models, strict unknown-field handling, migrations and compatibility tests.
P0 — Reference resolver incomplete. Introduce first-class AssetReference: logical ID, role, status, URI/path, SHA-256, media type, dimensions, provenance, approval event, supersession and availability. Missing media is explicit.
P1 — Need explicit composition semantics: base identity + approved version + continuity overlay + weekly-story overlay + scene overlay. Stronger layers change only whitelisted fields.
P1 — POV needs typed provenance and must not mix with anatomy truth.
P1 — QA needs executable policy objects with check/severity/evidence/observed/expected/evaluator version/decision trace.
P1 — Need immutable build/publication manifest containing package versions, asset hashes, resolver version, render-contract hash, scene-state hash, QA and output hash.
P1 — Tests are too report-heavy. Critical invariants must become executable CI.
P2 — Ten authored files per character create synchronization risk. Prefer compact canonical source and generated views.

## Target architecture
Authoritative typed CharacterRecord → Schema validation → Registry/index compiler → Asset resolver → Layer composer → Narrative POV/state composer → Render-contract compiler → Generator adapter → Character QA policy engine → Publication receipt → consumers.

## Composition layers, weakest to strongest
1. IDENTITY_BASE — species/body/head/silhouette/material language.
2. APPROVED_CHARACTER_VERSION — explicit Commissioner-approved redesign.
3. CONTINUITY_STATE — permitted haircut/wear/scars/equipment state.
4. WEEKLY_STORY_STATE — verified result/reputation/pressure/POV consequence.
5. SCENE_STATE — pose/action/camera/weather/lighting.
6. EXPLICIT_COMMISSIONER_OVERRIDE — logged approval only.
Each field declares which layer may author it.

## Bullpen decision
CCCP concept is sound, but current implementation is a release-candidate prototype, not yet a senior-grade production control plane. Preserve canon content; refactor operations into typed, schema-validated, registry-driven infrastructure before ACTIVE.

ARCHITECT: REBUILD_APPROVED.
LIBRARIAN: PASS concept / provenance-native asset model required.
CHARACTER DIRECTOR: PASS semantics / single-source compilation required.
NARRATIVE DIRECTOR: PASS POV direction / typed evidence-bound POV required.
VISUAL DIRECTOR: PASS direction / asset resolver + render receipts required.
RED TEAM: HOLD ACTIVE — duplicate truth remains exploitable.
UMPIRE: HOLD ACTIVE — reports must become executable tests.
CLOSER: preserve content; rebuild operations around typed source-of-truth.
