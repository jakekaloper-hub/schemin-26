# All Current Atlas Sites Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; no independent agents available in this session.

**Goal:** Give all 23 current Atlas locations an explicit site-specific visualization candidate, retain the three existing Wetlands models and all recent fixes, and independently enumerate 48 editorial expansion proposals without activating them.
**Architecture:** Add an additive 20-site asset factory and source-derived coverage report inside the existing observer preview. Compose it with the existing regional factory; retain source IDs, positions, statuses, source dates, viewer-only controls, publication rules and source-built host.
**Tech Stack:** Pinned Three.js 0.187.0, native JavaScript modules, Node tests, Python builder, existing browser verification.
**Spec:** Existing observer foundation spec and Founder interview #309/6900676650; new scope from “handle all sites planned rightnow”, recorded in #314/6954429823.

## Global Constraints
- No new OS, canonical writes, public private-edition assets, paid services, dependency upgrades, merge or deployment.
- Existing source geometry is abstract/non-metric. All new local shapes/materials remain CANDIDATE_NOT_APPROVED; no historical repairs or new sites implied.
- All 23 current locations have deterministic scene support. 48 CAND-* proposals remain non-rendered and preserve lifecycle status.
- No actor generation, named species or visitor interaction with inhabitants. No claim of final art acceptance.
- Existing Wetlands water/canopy tests remain intact. Water motion is independent of global calm; pause holds motion.

## Review Focus
- Dense central locations: prevent local model footprints from overlapping by limiting visual footprint to nearest source anchor, never move source anchors.
- Missing/duplicate/unknown IDs: fail or omit unknown models, never invent source truth.
- Geometry/memory: finite bounds, bounded object counts, shared materials, deterministic output, idempotent disposal.
- Runtime/fallback/reader: no camera control while reading; source history return works for every linked location.
- Privacy and scope: no private original image assets in repository build; proposals are tracked in internal coverage only.

### Task 1: All-sites model coverage
- [ ] Add failing tests `preview/tests/atlas-site-assets.test.mjs` against actual source-derived bindings.
- [ ] Implement `preview/atlas-site-assets.mjs`: `supportedAtlasSiteIds()` and `buildAtlasSiteAssets(THREE, bindings, height)` returning root, locations, water, tick, dispose and read-only authority metadata.
- [ ] Test exact complement to existing three models, source landmark bindings, deterministic bounded geometry, dense-anchor fitting, no mutations, motion/pause/disposal.

### Task 2: Existing host integration
- [ ] Add regressions for combined renderer coverage and builder bundle inclusion.
- [ ] Extend injectable renderer with optional extra asset factory, suppress generic markers only for genuinely handled IDs; append extra assets before static batching, include tick/disposal, expose coverage in renderer stats.
- [ ] Include new module through current offline builder/app binding. Preserve existing entry and source-state policy.
- [ ] Run all inherited Node and Python suites and repeat build checks.

### Task 3: Coverage and visual/browser verification
- [ ] Add source-derived report script enumerating active sites and proposal lifecycle; no source-authority writes.
- [ ] Build existing HTML from exact source catalog; inspect desktop and mobile routes for all 23 current sites; capture representative actual rendered screenshots.
- [ ] Preserve private-edition option separately; verify history → exact-camera return, global calm, pause, graphics fallback.
- [ ] Record actual results, outstanding visual/hardware/live gates and per-site evidence.

### Task 4: Persist and handoff
- [ ] Recheck shared branch for concurrent work; append only scoped source changes under expected-HEAD fast-forward semantics.
- [ ] Inspect new CI evidence. Record bounded completion, not universal/final environment approval.
- [ ] Deliver an inspectable build, coverage matrix and source/test receipts.
