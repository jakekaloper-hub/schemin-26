# Schemin Story Production Graph V1

**Status:** IMPLEMENTATION CANDIDATE — Issue #306  
**Authority:** subordinate to `SCHEMIN_26_PROJECT_MISSION.md`, `PROJECT_CONTROL_REGISTRY.md`, active source/data authority, Character Canon, World Engine/Atlas, Memo OS, Novel/Chronicle systems, Render Adapter and publication gates.

## North Star
One verified event should be able to drive multiple Schemin products without copying or mutating upstream truth.

```
verified evidence
  -> event envelope
  -> character/world hydration
  -> encounter + scene graph
  -> chronicle projections
  -> compiler build graph
  -> existing render adapters
  -> artifact evidence
  -> existing QA/publication gates
  -> governed world-memory writeback
```

This directory owns **integration contracts only**. It is not a new canon database, story OS, world model, character authority, publication authority or renderer.

## Contracts
- `event_v1.schema.json` — canonical event envelope that references upstream authority.
- `encounter_v1.schema.json` — shared encounter state inherited by related scenes; prevents repeating or drifting venue/participant anchors.
- `scene_v1.schema.json` — reusable scene object with encounter inheritance, continuity and state deltas.
- `chronicle_projection_v1.schema.json` — derived read model for character/relationship/place/artifact history.
- `compiler_manifest_v1.schema.json` — build lineage and dependency/invalidation manifest.
- `fixtures/week9_minimal.json` — narrow Week 9 conformance fixture, not a rewrite of Week 9 canon.
- `validate_story_graph.py` — dependency-free structural validator.
- `dependency_invalidation.py` — transitive impact calculation and minimal rebuild-job selection.
- `build_chronicle_projection.py` — rebuildable character/relationship Chronicle read-model helpers.
- `tests/test_story_production_graph.py` — conformance tests for structural validation, invalidation and Chronicle derivation.

## Board ownership
- Closer: mission scope and convergence
- Setup Man: build graph, resumability, invalidation
- Scout: source/evidence boundary
- Umpire: fail-closed acceptance
- Beat Writer: scene causality/POV/transitions
- Groundskeeper: weekly operational throughput
- GM: reader/product value
- Pitching Coach: generation packet boundaries
- Warden: security/dependency boundaries
- Commissioner: league recognition/personalization
- Analyst: reuse/divergence/correction metrics
- Librarian: provenance/supersession
- Agent: cross-surface identity
- Bookkeeper: reuse/cost discipline
- Commissioner General: rights/publication review
- Clubhouse Manager: owner/character/role boundaries
- Scout Master: distribution value
- Architect: schemas/contracts/validators

## Invariants
1. Event objects reference evidence; they do not become evidence.
2. Scene objects reference Character/World authority; they do not replace it.
3. Chronicle objects are projections; deleting/rebuilding them cannot alter canon.
4. Compiler outputs are artifacts; renderers cannot promote facts or world state.
5. Unknown history remains unknown.
6. Mercer-private intelligence cannot enter public story artifacts.
7. Outcome branches remain provisional until upstream Fact Lock selects the result.
8. Project Control promotion requires independent Umpire acceptance on exact HEAD.

## First conformance target
Week 9 is the first fixture because its existing previs already proves matchup cards, page contracts, written beats, branch endings, character references, composition fields, adjacency and QA structure. The fixture here demonstrates translation only; it does not supersede any Week 9 file.

## Execution state — 2026-11-12

- Issue #306 is the authoritative implementation mission.
- PR #307 is the draft implementation surface.
- Repository Merge Gate and Bullpen Runtime CI passed on the initial seven-file contract tranche.
- Encounter inheritance, invalidation, Chronicle projection helpers and tests are now implemented on the same branch and require fresh exact-HEAD CI.
- External Netlify deploy-preview reported failure on the earlier HEAD; no site/runtime code was changed in that tranche, so it remains an explicit independent hold rather than a Story Graph acceptance signal.
- Project Control remains unpromoted pending exact-HEAD CI, multi-matchup conformance and independent Umpire acceptance.
