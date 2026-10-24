# Schemin ’26 — Unreal Commonwealth Production Blueprint v1

**Status:** ACTIVE DEVELOPMENT PLAN / NOT A RELEASE RECEIPT
**Executive owner:** Closer. **Technical:** Architect/Groundskeeper. **World truth:** World Engine and Atlas. **Creative:** Visual Direction and Novel OS. **Safety:** Librarian/Warden. **Acceptance:** Independent Umpire.
**Source of truth:** Existing schemin-26 canon, World Engine, location control, history, event and visual reference registries. This plan does not create a second OS.
**Local UE workspace:** `~/Developer/ai/Schemin_UE_Prototype` (Unreal Engine 5.8, Mac M3 Pro 18 GB). GitHub main does not store UE caches/binary outputs.

## North Star

Build an explorable, cinematic and evolving Commonwealth by *deriving* spatial and narrative experiences from authoritative Schemin world records. New scenes are previews until separately promoted. Never invent absolute metric position from abstract Atlas coordinates, alter character morphology, imply fresh ESPN data, or mutate canon from Unreal.

## Immutable lifecycle

Resolve authority -> pin commit and hashes -> validate source data -> compile location and encounter specs -> build reusable kit -> generate UE preview levels -> load/inspect -> test collision/Play mode -> light and compose -> record cinematics -> capture rendered previews -> validate source receipts and performance -> review -> publish only approved derivatives -> archive evidence -> advance to next work package.

## Work breakdown and execution order

### W0 — Runtime, provenance, repository layout
1. Keep UE project separate, inspect its exact state and source-control strategy; use .gitignore and LFS assessment before committing UE binaries.
2. Produce reproducible Mac CLI entrypoint, safe reruns, logging, run IDs and resumable status ledger.
3. Verify exact byte hashes of source records per pinned Git SHA. Fail closed on missing or drifted authority.
**Exit:** rebuild twice gives identical manifests; smoke logs/metadata persisted.

### W1 — Canonical spatial data compilation
1. Consume World Engine V1.1, Atlas V2, location-control-plane source hierarchy.
2. Compile 23 existing locations (count is snapshot-specific), 7 regions, routes, settlements, institutions, traversal edges, encounter venue rules, history and evolving world state.
3. Distinguish permanent, provisional and interpretive records, unresolved scale and source provenance. Never convert abstract coordinates to meters without approved scale.
4. Emit per-location design packets and machine-checkable spatial manifests.
**Exit:** every record has stable ID and traceable evidence; unsupported spatial claims become blockers.

### W2 — Reusable environment component system
1. Develop modular, parameterized prototype components: terrain/landforms, roads, water, structures, vegetation, weather, landmarks and signage.
2. Use source-backed descriptors; placeholder geometry is labeled, not promoted.
3. Enforce M3 Pro 18 GB performance budgets, scalability, reproducible construction, deterministic names and idempotent updates.
**Exit:** one location and two contrasted biomes have distinguishable, inspectable scenes with no invented canon.

### W3 — World navigation and playable preview
1. Build separate Atlas overview with regional transitions/links; not assumed continuous geographically scaled world.
2. Implement player starts, ground collision, lighting, camera, GameMode and Play-in-Editor test.
3. Conduct measured editor / standalone test (frame time, memory, errors) and save evidence.
**Exit:** character can walk in a source-backed preview without falling through ground or crashing.

### W4 — Character and inhabitants
1. Read twelve-character registry and latest Commissioner-approved image authority.
2. No canonical character meshes, actor placements, animations, appearances or video until exact-reference and subject-binding gates pass.
3. Use clearly anonymous geometry for navigation testing where allowed.
**Exit:** independent character continuity validation or explicit HOLD.

### W5 — Cinematic studio and weekly Memo
1. Add Sequencer camera tracks, lighting presets, shot manifests, staging rules and an output preset.
2. Render one source-safe non-character scene, inspect actual frames, record resolution and timing.
3. Prepare reusable shot pipeline for six matchup features and novel episodes, with publication QA.
**Exit:** verified rendered artifact, not a blank Level Sequence.

### W6 — Living events and ESPN truth
1. Read frozen verified sports facts, venue resolver, event chronology, entering state and world consequences.
2. Shadow replay historical scenarios; do not mutate world state or simulate unverified live results as real.
3. Translate event-state changes to versioned scene overlays only after event/canon QA.
**Exit:** one event produces reproducible, source-cited preview and no canon writeback.

### W7 — Web/Atlas publication surfaces
1. Compare downloadable cinematic renders, lightweight web 3D, UE Pixel Streaming, still imagery and interactive map with actual deployment costs.
2. Prioritize lightweight browser delivery; no assumption that native UE content runs directly in browsers.
3. Publish only signed accepted derivatives; optional higher-cost hosting requires Commissioner budget authorization.
**Exit:** one reviewable safe preview with clear publication permissions.

### W8 — Scale-out, QA, release
1. Generate full coverage/quality matrices for regions, locations, routes, characters, encounters, cinematics and continuity.
2. Run regression on repeated builds, negative provenance, stale events, scene drift, hardware, and packaging.
3. Librarian validates placement; Umpire independently verifies evidence; Closer may merge only when all gates pass.
**Exit:** independent PASS; otherwise HOLD with exact remedial action.

## Automation protocol (human-independent implementation decisions, not unsupervised promises)
- The runner proceeds to the next queued *safe local task* after a passing gate without asking the Commissioner to choose routine implementation details.
- Failed validation becomes BLOCKED with logs; non-blocked tasks may proceed.
- Do not force automatic canonical merges or payments.
- A CLI job can run while the Mac is awake and its process remains active. ChatGPT does not continue reasoning or invoke tools after the conversation response without a separate configured agent/task.
- Daily or on-demand scheduled invocations must use an explicitly installed/configured local scheduler or supported automation, with clear execution evidence; never assume a local file write starts an always-on agent.

## Required evidence for every work package
`task_id, source_commit, source_hashes, inputs, commands, output_paths, negative_tests, engine_exit_code, warnings, scene_validation, image/video_preview_paths, hardware_measurements, Umpire_disposition`. Reports must use IMPLEMENTED / TESTED / AUDITED / PROMOTED / BLOCKED / REMAINING.

## Current baseline, verified October 22, 2026
- Local project created, UE 5.8 commandlet runs.
- Canonical source snapshot 23 locations / 7 zones; distinct status maintained.
- 23 per-location proxy maps, 1 Atlas overview, 1 Trade Jedi walkable-test map, blank cinematic sequence.
- 16/16 local Python test methods passed most recently; editor commandlet asset-generation tests have passed.
- Play-in-Editor usability, meaningful environment art, actual cinematic renders, canonical character integration, website delivery and independent merge acceptance: NOT COMPLETE.

## Immediate uninterrupted batch
(1) establish structured status/coverage ledger -> (2) create resumable local runner -> (3) build source-backed region/environment descriptors -> (4) implement one repeatable visually distinctive sample without canon promotion -> (5) run build + verification and collect evidence -> (6) continue to additional environments that pass prerequisites; report actual completed output only.
